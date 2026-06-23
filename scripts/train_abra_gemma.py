#!/usr/bin/env python3
"""
Fine-tune Gemma 4 (base Ollama) su feedback Abra → export modello Ollama identico locale/online.

Pipeline:
  1. Esporta finetune-export.jsonl dal Lab
  2. python scripts/train_abra_gemma.py --dataset finetune-export.jsonl
  3. ollama create abra-assistente-ft -f offerte-ai/models/abra-assistente-ft/Modelfile
  4. Online: stesso modello su VPS Ollama + proxy.py (mode=proxy)

Richiede GPU NVIDIA + venv .venv-ai (setup-abra-ai-local.ps1).
"""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "offerte-ai" / "models" / "abra-assistente-ft"
DEFAULT_DATASET = ROOT / "offerte-ai" / "data" / "feedback" / "finetune-dataset.jsonl"

SYSTEM = """Sei l'assistente commerciale di Abra Robotics (distributore Unitree, AMR, cobot in Italia).
Regole:
- Rispondi in italiano, conciso e professionale.
- I PREZZI nel contesto RAG sono ufficiali: non inventare cifre.
- Se mancano dati, invita a contattare info@abrarobotics.com o WhatsApp.
- Non rivelare prezzi Gold o margini interni.
- Per preventivi complessi suggerisci una call con un consulente."""


def load_jsonl(path: Path) -> list[dict]:
    rows = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        rows.append(json.loads(line))
    return rows


def to_chat_rows(entries: list[dict]) -> list[dict]:
    out = []
    for e in entries:
        msgs = e.get("messages") or []
        user = next((m["content"] for m in msgs if m.get("role") == "user"), "")
        asst = next((m["content"] for m in msgs if m.get("role") == "assistant"), "")
        if user and asst:
            out.append({"messages": [{"role": "user", "content": user}, {"role": "assistant", "content": asst}]})
    return out


def write_modelfile(gguf_path: Path | None = None) -> Path:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    mf = OUT_DIR / "Modelfile"
    if gguf_path and gguf_path.exists():
        body = f'FROM ./{gguf_path.name}\n\n'
    else:
        body = "FROM gemma4:e4b\n\n"
    body += "PARAMETER temperature 0.3\nPARAMETER num_predict 512\n\n"
    body += f'SYSTEM """{SYSTEM}"""\n'
    mf.write_text(body, encoding="utf-8")
    return mf


def train_unsloth(dataset_path: Path, epochs: int, max_samples: int) -> Path | None:
    try:
        from unsloth import FastLanguageModel  # noqa: F401
        from trl import SFTTrainer
        from transformers import TrainingArguments
        from datasets import Dataset
    except ImportError:
        print("Unsloth non installato. Esegui: .\\scripts\\train-abra-gemma.ps1 -InstallOnly")
        return None

    entries = to_chat_rows(load_jsonl(dataset_path))
    if not entries:
        print("Dataset vuoto — servono almeno 5-10 esempi con correction o rating=1")
        sys.exit(1)
    if max_samples:
        entries = entries[:max_samples]

    print(f"Training su {len(entries)} esempi...")

    model, tokenizer = FastLanguageModel.from_pretrained(
        model_name="unsloth/gemma-3-4b-it-bnb-4bit",
        max_seq_length=2048,
        load_in_4bit=True,
    )
    model = FastLanguageModel.get_peft_model(
        model,
        r=16,
        target_modules=["q_proj", "k_proj", "v_proj", "o_proj", "gate_proj", "up_proj", "down_proj"],
        lora_alpha=16,
        lora_dropout=0,
        bias="none",
        use_gradient_checkpointing="unsloth",
    )

    def fmt(example):
        text = tokenizer.apply_chat_template(example["messages"], tokenize=False, add_generation_prompt=False)
        return {"text": text}

    ds = Dataset.from_list(entries).map(fmt)

    trainer = SFTTrainer(
        model=model,
        tokenizer=tokenizer,
        train_dataset=ds,
        dataset_text_field="text",
        max_seq_length=2048,
        args=TrainingArguments(
            per_device_train_batch_size=2,
            gradient_accumulation_steps=4,
            warmup_steps=5,
            num_train_epochs=epochs,
            learning_rate=2e-4,
            fp16=not bool(getattr(__import__("torch").cuda, "is_bf16_supported", lambda: False)()),
            bf16=bool(getattr(__import__("torch").cuda, "is_bf16_supported", lambda: False)()),
            logging_steps=1,
            output_dir=str(OUT_DIR / "checkpoints"),
            optim="adamw_8bit",
        ),
    )
    trainer.train()

    merged = OUT_DIR / "merged"
    merged.mkdir(parents=True, exist_ok=True)
    model.save_pretrained_merged(merged, tokenizer, save_method="merged_16bit")

    gguf_dir = OUT_DIR / "gguf"
    gguf_dir.mkdir(parents=True, exist_ok=True)
    model.save_pretrained_gguf(str(gguf_dir), tokenizer, quantization_method="q4_k_m")
    ggufs = list(gguf_dir.glob("*.gguf"))
    if not ggufs:
        print("GGUF non generato — usa Modelfile con FROM gemma4:e4b (prompt-only)")
        return None
    dest = OUT_DIR / ggufs[0].name
    if dest != ggufs[0]:
        shutil.copy2(ggufs[0], dest)
    print(f"GGUF: {dest}")
    return dest


def ollama_create(modelfile: Path, name: str = "abra-assistente-ft") -> None:
    ollama = shutil.which("ollama")
    if not ollama:
        local = Path.home() / "AppData/Local/Programs/Ollama/ollama.exe"
        ollama = str(local) if local.exists() else None
    if not ollama:
        print("ollama non in PATH — crea manualmente: ollama create abra-assistente-ft -f Modelfile")
        return
    subprocess.run([ollama, "create", name, "-f", str(modelfile)], check=True)
    print(f"Modello Ollama '{name}' creato. Usalo in Admin -> Modello: {name}")


def main() -> None:
    ap = argparse.ArgumentParser(description="Fine-tune Abra Gemma → Ollama")
    ap.add_argument("--dataset", type=Path, default=DEFAULT_DATASET)
    ap.add_argument("--epochs", type=int, default=3)
    ap.add_argument("--max-samples", type=int, default=0)
    ap.add_argument("--skip-train", action="store_true", help="Solo crea Modelfile / ollama create")
    args = ap.parse_args()

    if not args.skip_train:
        if not args.dataset.exists():
            print(f"Dataset mancante: {args.dataset}")
            print("Esporta finetune-export.jsonl dal Lab e copialo in offerte-ai/data/feedback/")
            sys.exit(1)
        gguf = train_unsloth(args.dataset, args.epochs, args.max_samples)
        mf = write_modelfile(gguf)
    else:
        mf = write_modelfile()

    ollama_create(mf)
    print("\nOnline: carica lo stesso Modelfile + GGUF sul server Ollama e avvia proxy.py")


if __name__ == "__main__":
    main()
