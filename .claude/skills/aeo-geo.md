---
name: aeo-geo
description: "Answer Engine Optimization (AEO) and Generative Engine Optimization (GEO). Optimizes content for AI-powered search engines (ChatGPT, Perplexity, Google AI Overviews, Gemini) and featured snippets/voice search. Use when building pages that should be cited by AI engines or appear in featured snippets."
---

# AEO / GEO Optimization Skill

Optimize web content for AI-powered search engines and answer engines.

## GEO — Generative Engine Optimization

GEO optimizes for AI search engines (Perplexity, ChatGPT Search, Google AI Overviews, Gemini) that synthesize answers from multiple sources and cite pages.

### Key Statistics
- AI-referred traffic grew 527% (Jan-May 2025)
- Content optimized for AI citation shows 33-40% higher visibility
- Content under 30 days old receives 3.2x citation boost
- E-E-A-T signals provide +40% AI citation boost
- TL;DR strategy delivers +35% citation boost
- Brand mentions correlate 3x more with AI visibility than backlinks
- 92% of AI Overview citations come from top-10 ranking pages
- AI crawlers do NOT execute JavaScript — server-side rendering is critical

### GEO Signals to Implement

**E-E-A-T (Experience, Expertise, Authoritativeness, Trustworthiness):**
- Named authors with visible credentials
- About page explaining who runs the site, background, qualifications
- Contact information (phone, address, email) accessible
- Trust signals: testimonials, awards, certifications, press mentions
- Organization schema declaring brand entity (name, logo, URL, social profiles)

**Content for AI Synthesis:**
- **Factual density**: Include specific facts, statistics, data that AI could cite
- **Clear claims**: State core argument/value proposition plainly at the top
- **Source citation**: Reference external authoritative sources
- **Comprehensiveness**: Fully address the topic, leave no key questions unanswered
- **Entity clarity**: Name brand/person/place clearly and consistently
- **Originality**: Provide unique perspective, original data, or proprietary insights
- **Citability**: Structure 134-167 word passages with specific facts and clear sourcing

**Technical GEO:**
- Rich schema types (Author, Dataset, ClaimReview, SpeakableSpecification)
- HTTPS security
- Clean crawlability — no robots.txt blocks for AI crawlers
- sameAs / brand entity links to social profiles
- Consider `llms.txt` at domain root for guiding AI crawler indexing
- Allow GPTBot, ClaudeBot, PerplexityBot in robots.txt

### Platform-Specific Optimization

| Platform | Priority Signals |
|----------|-----------------|
| ChatGPT | Depth (1500-2500 words) + author credentials |
| Perplexity | Freshness + recent dateModified |
| Claude | Primary source citations + transparent methodology |
| Gemini | Reviews + local citations |
| Google AI Overviews | Top-10 ranking + clear structured answers |

## AEO — Answer Engine Optimization

AEO optimizes for featured snippets, People Also Ask boxes, and voice search.

### Featured Snippet Eligibility
- **Direct answer paragraphs**: Answer key question in 40-60 words right below a question-phrased heading
- **Definition patterns**: Define core topic in a clear "X is..." sentence
- **List content**: Numbered steps or bulleted lists for list snippets
- **Table content**: Comparison tables for table snippets

### Structured Answer Formats
- **FAQ schema**: Questions and answers with proper FAQPage markup
  - Note: Google restricts FAQ rich results to government/healthcare since Aug 2023
  - Still valuable for AI/LLM citation benefit
- **HowTo schema**: Deprecated for Google (Sept 2023) — avoid
- **Question-phrased headings**: H2/H3 using natural question language ("How does X work?", "What is Y?")
- **Speakable schema**: SpeakableSpecification for voice-friendly sections

### Voice Search Readiness
- Conversational, natural language phrasing
- Long-tail question coverage (who/what/when/where/why/how)
- Local signals if applicable (NAP data, local schema, location mentions)
- Concise answers (29 words average for voice search results)

## Implementation Checklist

When building or reviewing pages, ensure:

1. **Clear answer paragraphs** (40-60 words) under question-phrased H2/H3s
2. **FAQ section** with schema markup and natural question language
3. **Factual density** — specific numbers, stats, dates, not vague claims
4. **Author/company credentials** visible on page
5. **Organization schema** with sameAs links to social profiles
6. **Fresh content signals** — visible dates, regular updates
7. **Speakable markup** on key answer sections
8. **Comprehensive coverage** — address all related questions on the topic
9. **Internal linking** with descriptive anchors
10. **Structured data** appropriate to page type

## Scoring Rubric (1-10)

### GEO Score
- E-E-A-T signals (25%)
- Content citability & factual density (25%)
- Structural readability (20%)
- Technical accessibility for AI crawlers (15%)
- Authority & brand signals (15%)

### AEO Score
- Direct answer paragraphs (25%)
- Question-phrased headings (20%)
- Schema markup (FAQ, Speakable) (20%)
- Conversational language (15%)
- Long-tail question coverage (20%)

## Abra Robotics Context

Key questions to answer on the site (for AEO):
- "Chi è il distributore Unitree in Italia?"
- "Quanto costa il Unitree Go2?"
- "Quali robot Unitree sono disponibili in Italia?"
- "Come funziona il finanziamento per robot industriali?"
- "Unitree Go2 vs Go2 Pro: quali sono le differenze?"
- "Robot per università e ricerca in Italia"
- "Come integrare un robot quadrupede in azienda?"

Entity to establish for GEO:
- Abra Robotics = distributore ufficiale Unitree in Italia
- Sedi, contatti, team, certificazioni
- Partnership con Unitree e altri brand (qbrobotics, Keyence, etc.)
