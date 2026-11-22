"""Run the eye over the labeled film and score the filed predictions F1 to F5 (see PREDICTIONS.md and film/LABELS.md)."""
import json, sys
import numpy as np
from PIL import Image
import eye

E = eye.Eye(64); CL = ["C", "P", "F"]
labels = json.load(open("film/labels.json"))
rows = []
for eid, labs in sorted(labels.items()):
    im = np.asarray(Image.open("film/browse/%s.jpg" % eid).convert("L"), dtype=np.int64)
    for p, lab in enumerate(labs):
        patch = im[25:89, 4 + 64 * p: 4 + 64 * p + 64]
        rows.append({"frame": eid, "patch": p, "label": lab, "train": int(eid[-3:]) % 2 == 0, "r": E.look(patch)})
json.dump(rows, open("results/film_readings.json", "w"))
R = np.array([r["r"] for r in rows], dtype=np.float64); lab = np.array([r["label"] for r in rows]); tr = np.array([r["train"] for r in rows])
X = np.log10(1 + R)
def scale(cols):
    m = X[tr][:, cols].mean(0); s = X[tr][:, cols].std(0) + 1e-9
    return np.hstack([(X[:, cols] - m) / s, np.ones((len(X), 1))])
def perceptron(Z, y, classes, epochs=100):          # multiclass perceptron, fixed order, averaged weights
    W = np.zeros((len(classes), Z.shape[1])); A = np.zeros_like(W); idx = [i for i in range(len(y))]
    for _ in range(epochs):
        for i in idx:
            k = classes.index(y[i]); g = int(np.argmax(W @ Z[i]))
            if g != k: W[k] += Z[i]; W[g] -= Z[i]
            A += W
    return A
def score(pred, truth):
    return float(np.mean(pred == truth))
def best_threshold(v, y, a, b):                      # one threshold, either direction, best training accuracy
    best = (-1, None, None); vs = np.sort(np.unique(v))
    for t in (vs[:-1] + vs[1:]) / 2:
        for lo, hi in ((a, b), (b, a)):
            acc = np.mean(np.where(v <= t, lo, hi) == y)
            if acc > best[0]: best = (acc, t, (lo, hi))
    return best
out = {"n_patches": len(rows), "counts": {c: int((lab == c).sum()) for c in CL + ["?"]}}
rings = R[:, 1:9]; inner = rings[:, :2].sum(1) / np.maximum(rings.sum(1), 1)
two = np.isin(lab, ["C", "F"]); trn2 = two & tr; tst2 = two & ~tr
acc, t, (lo, hi) = best_threshold(inner[trn2], lab[trn2], "C", "F")
out["F1_fixed_rule_heldout"] = score(np.where(inner[tst2] <= t, lo, hi), lab[tst2])
three = np.isin(lab, CL); trn3 = three & tr; tst3 = three & ~tr
allc = list(range(43)); norw = list(range(9))
Z = scale(allc); W2 = perceptron(Z[trn2], lab[trn2], ["C", "F"])
out["F2_trained_two_class_heldout"] = score(np.array(["C", "F"])[np.argmax(Z[tst2] @ W2.T, 1)], lab[tst2])
W3 = perceptron(Z[trn3], lab[trn3], CL)
p3 = np.array(CL)[np.argmax(Z[tst3] @ W3.T, 1)]; out["F3_trained_three_class_heldout"] = score(p3, lab[tst3])
out["F3_confusion_rows_truth_cols_pred"] = {c: {d: int(((lab[tst3] == c) & (p3 == d)).sum()) for d in CL} for c in CL}
Zn = scale(norw); W3n = perceptron(Zn[trn3], lab[trn3], CL)
out["F4_three_class_without_wedges_heldout"] = score(np.array(CL)[np.argmax(Zn[tst3] @ W3n.T, 1)], lab[tst3])
b = X[:, 0]; best = (-1, None)                       # brightness: the center spot alone, two thresholds, C < P < F
qs = np.unique(np.quantile(b[trn3], np.linspace(0, 1, 101)))
for i, t1 in enumerate(qs):
    for t2 in qs[i:]:
        acc = np.mean(np.where(b[trn3] <= t1, "C", np.where(b[trn3] <= t2, "P", "F")) == lab[trn3])
        if acc > best[0]: best = (acc, (t1, t2))
t1, t2 = best[1]; out["F5_brightness_three_class_heldout"] = score(np.where(b[tst3] <= t1, "C", np.where(b[tst3] <= t2, "P", "F")), lab[tst3])
bacc, bt, (blo, bhi) = best_threshold(b[trn2], lab[trn2], "C", "F")
out["brightness_two_class_heldout"] = score(np.where(b[tst2] <= bt, blo, bhi), lab[tst2])
json.dump(out, open("results/film_results.json", "w"), indent=1)
print(json.dumps(out, indent=1))
