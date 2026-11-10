// Robot UR dalle mesh ufficiali (convertite da ~/cella_main/assets, URDF) + cinematica diretta e inversa.
// Coordinate di cella: metri, Z in alto (la radice della scena è ruotata per Three).
import * as THREE from "three";

const PI = Math.PI;
// origini dei giunti dall'URDF: [base_link_inertia, pan, lift, elbow, w1, w2, w3, flange, tool0]
const KIN = {
  ur10e: [[[0, 0, 0], [0, 0, PI]], [[0, 0, 0.1807], [0, 0, 0]], [[0, 0, 0], [PI / 2, 0, 0]], [[-0.6127, 0, 0], [0, 0, 0]],
    [[-0.57155, 0, 0.17415], [0, 0, 0]], [[0, -0.11985, 0], [PI / 2, 0, 0]], [[0, 0.11655, 0], [PI / 2, PI, PI]],
    [[0, 0, 0], [0, -PI / 2, -PI / 2]], [[0, 0, 0], [PI / 2, 0, PI / 2]]],
  ur30: [[[0, 0, 0], [0, 0, PI]], [[0, 0, 0.2363], [0, 0, 0]], [[0, 0, 0], [PI / 2, 0, 0]], [[-0.637, 0, 0], [0, 0, 0]],
    [[-0.5037, 0, 0.201], [0, 0, 0]], [[0, -0.1593, 0], [PI / 2, 0, 0]], [[0, 0.1543, 0], [PI / 2, PI, PI]],
    [[0, 0, 0], [0, -PI / 2, -PI / 2]], [[0, 0, 0], [PI / 2, 0, PI / 2]]],
};
const LINKS = ["shoulder_link", "upper_arm_link", "forearm_link", "wrist_1_link", "wrist_2_link", "wrist_3_link"];

const originMat = ([xyz, rpy]) => new THREE.Matrix4().makeRotationFromEuler(new THREE.Euler(rpy[0], rpy[1], rpy[2], "ZYX")).setPosition(xyz[0], xyz[1], xyz[2]);
const _rz = new THREE.Matrix4();

export class Cinematica {
  constructor(model, base, tcp) {
    this.O = KIN[model].map(originMat);
    this.base = base.clone();
    this.tcp = new THREE.Matrix4().makeTranslation(0, 0, tcp);
    this.tail = this.O[7].clone().multiply(this.O[8]).multiply(this.tcp);
  }
  fk(q, out = new THREE.Matrix4()) {
    out.copy(this.base).multiply(this.O[0]);
    for (let i = 0; i < 6; i++) out.multiply(this.O[i + 1]).multiply(_rz.makeRotationZ(q[i]));
    return out.multiply(this.tail);
  }
  // errore 6D: posizione + orientamento (somma dei prodotti vettoriali degli assi)
  _err(q, T, e) {
    const M = this.fk(q, this._M || (this._M = new THREE.Matrix4()));
    const m = M.elements, t = T.elements;
    e[0] = t[12] - m[12]; e[1] = t[13] - m[13]; e[2] = t[14] - m[14];
    e[3] = e[4] = e[5] = 0;
    for (let c = 0; c < 3; c++) {
      const a = [m[c * 4], m[c * 4 + 1], m[c * 4 + 2]], b = [t[c * 4], t[c * 4 + 1], t[c * 4 + 2]];
      e[3] += 0.5 * (a[1] * b[2] - a[2] * b[1]); e[4] += 0.5 * (a[2] * b[0] - a[0] * b[2]); e[5] += 0.5 * (a[0] * b[1] - a[1] * b[0]);
    }
    return Math.hypot(e[0], e[1], e[2]) + 0.3 * Math.hypot(e[3], e[4], e[5]);
  }
  ik(T, seed, iters = 160) {
    const q = seed.slice(), e = new Float64Array(6), e2 = new Float64Array(6), J = [...Array(6)].map(() => new Float64Array(6));
    let err = this._err(q, T, e);
    for (let it = 0; it < iters && err > 2e-5; it++) {
      for (let j = 0; j < 6; j++) {
        const h = 1e-5; q[j] += h; this._err(q, T, e2); q[j] -= h;
        for (let i = 0; i < 6; i++) J[i][j] = (e[i] - e2[i]) / h; // d(pos)/dq = -d(e)/dq
      }
      // dq = J^T (J J^T + l^2 I)^-1 e
      const lam = 0.02, A = [...Array(6)].map(() => new Float64Array(7));
      for (let i = 0; i < 6; i++) {
        for (let k = 0; k < 6; k++) { let s = 0; for (let j = 0; j < 6; j++) s += J[i][j] * J[k][j]; A[i][k] = s + (i === k ? lam * lam : 0); }
        A[i][6] = e[i];
      }
      for (let c = 0; c < 6; c++) {
        let p = c; for (let r = c + 1; r < 6; r++) if (Math.abs(A[r][c]) > Math.abs(A[p][c])) p = r;
        [A[c], A[p]] = [A[p], A[c]];
        for (let r = 0; r < 6; r++) if (r !== c) { const f = A[r][c] / A[c][c]; for (let k = c; k < 7; k++) A[r][k] -= f * A[c][k]; }
      }
      const y = A.map((r, i) => r[6] / r[i]);
      let mx = 0;
      const dq = new Float64Array(6);
      for (let j = 0; j < 6; j++) { let s = 0; for (let i = 0; i < 6; i++) s += J[i][j] * y[i]; dq[j] = s; mx = Math.max(mx, Math.abs(s)); }
      const k = mx > 0.25 ? 0.25 / mx : 1;
      for (let j = 0; j < 6; j++) q[j] += dq[j] * k;
      err = this._err(q, T, e);
    }
    return { q, err };
  }
}

// posa utensile: posizione + asse Z dell'utensile + direzione X (ortogonalizzata)
export function posa(p, z = [0, 0, -1], x = [1, 0, 0]) {
  const Z = new THREE.Vector3(...z).normalize();
  const X = new THREE.Vector3(...x); X.addScaledVector(Z, -X.dot(Z)).normalize();
  const Y = new THREE.Vector3().crossVectors(Z, X);
  return new THREE.Matrix4().makeBasis(X, Y, Z).setPosition(p[0], p[1], p[2]);
}

const MAT = {
  "7dadcc": () => new THREE.MeshStandardMaterial({ color: 0x86a9c4, roughness: 0.45, metalness: 0.1, polygonOffset: true, polygonOffsetFactor: -2, polygonOffsetUnits: -4 }),
  d1d1d1: () => new THREE.MeshStandardMaterial({ color: 0xd9dad6, roughness: 0.42, metalness: 0.15 }),
  ffffff: () => new THREE.MeshStandardMaterial({ color: 0xd9dad6, roughness: 0.42, metalness: 0.15 }),
  "474747": () => new THREE.MeshStandardMaterial({ color: 0x3c4046, roughness: 0.6, metalness: 0.2 }),
  cccccc: () => new THREE.MeshStandardMaterial({ color: 0xb8bcc0, roughness: 0.35, metalness: 0.75 }),
  "4c4c4c": () => new THREE.MeshStandardMaterial({ color: 0x4a4e54, roughness: 0.5, metalness: 0.4 }),
};
const matFor = (c) => (MAT[c] || (() => new THREE.MeshStandardMaterial({ color: 0x17191c, roughness: 0.55, metalness: 0.2 })))();

// Costruisce il robot animabile da un glTF caricato (nodi "<link>[#L|#R]__c<colore>__…")
export class Robot {
  constructor(gltfScene, model, tcp) {
    this.model = model;
    this.root = new THREE.Group();
    const O = KIN[model].map(originMat);
    const frame = (m) => { const g = new THREE.Group(); g.matrixAutoUpdate = false; g.matrix.copy(m); return g; };
    const inertia = frame(O[0]); this.root.add(inertia);
    this.links = { base_link_inertia: inertia };
    this.joints = [];
    let parent = inertia;
    for (let i = 0; i < 6; i++) {
      const o = frame(O[i + 1]); parent.add(o);
      const j = new THREE.Group(); o.add(j); this.joints.push(j); this.links[LINKS[i]] = j; parent = j;
    }
    this.tool0 = frame(O[7].clone().multiply(O[8])); parent.add(this.tool0);
    this.tcpObj = new THREE.Group(); this.tcpObj.position.z = tcp; this.tool0.add(this.tcpObj);
    this.fingerL = new THREE.Group(); this.fingerR = new THREE.Group();
    this.links.wrist_3_link.add(this.fingerL, this.fingerR);
    // direzione di chiusura della pinza (asse Y di tool0) nel riferimento di wrist_3
    this.closeDir = new THREE.Vector3(0, 1, 0).applyMatrix3(new THREE.Matrix3().setFromMatrix4(this.tool0.matrix));
    this.parts = []; // [{name, mesh}] per la costruzione pezzo per pezzo
    const meshes = [];
    gltfScene.traverse((o) => { if (o.isMesh) meshes.push(o); });
    for (const m of meshes) {
      const [lk, col, orig = ""] = m.name.split("__");
      const [link, side] = lk.split("#");
      const tgt = side === "L" ? this.fingerL : side === "R" ? this.fingerR : this.links[link];
      if (!tgt) continue;
      m.updateWorldMatrix(true, false);
      const geo = m.geometry.clone().applyMatrix4(m.matrixWorld);
      const mesh = new THREE.Mesh(geo, matFor(col.slice(1)));
      mesh.castShadow = true; mesh.receiveShadow = true;
      tgt.add(mesh);
      this.parts.push({ link: /robotiq|coupler/.test(orig) ? "gripper" : link, mesh });
    }
    this.q = [0, 0, 0, 0, 0, 0];
  }
  set(q, grip = 0) {
    for (let i = 0; i < 6; i++) this.joints[i].rotation.z = q[i];
    const d = 0.018 * grip; // corsa visiva delle dita
    this.fingerL.position.copy(this.closeDir).multiplyScalar(-d);
    this.fingerR.position.copy(this.closeDir).multiplyScalar(d);
  }
}
