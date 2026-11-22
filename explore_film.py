"""Exploratory, not predicted: the spectrum without brightness, and the training and held-out frames swapped."""
import json, numpy as np
rows = json.load(open("results/film_readings.json")); CL = ["C", "P", "F"]
R = np.array([r["r"] for r in rows], float); lab = np.array([r["label"] for r in rows]); X = np.log10(1 + R)
def run(cols, tr):
    m = X[tr][:, cols].mean(0); s = X[tr][:, cols].std(0) + 1e-9; Z = np.hstack([(X[:, cols] - m) / s, np.ones((len(X), 1))])
    three = np.isin(lab, CL); a, b = three & tr, three & ~tr
    W = np.zeros((3, Z.shape[1])); A = np.zeros_like(W)
    for _ in range(100):
        for i in np.where(a)[0]:
            k = CL.index(lab[i]); g = int(np.argmax(W @ Z[i]))
            if g != k: W[k] += Z[i]; W[g] -= Z[i]
            A += W
    return round(float(np.mean(np.array(CL)[np.argmax(Z[b] @ A.T, 1)] == lab[b])), 4)
even = np.array([int(r["frame"][-3:]) % 2 == 0 for r in rows])
out = {"rings_only_no_brightness": run(list(range(1, 9)), even), "all_43": run(list(range(43)), even),
       "swapped_split_all_43": run(list(range(43)), ~even), "swapped_split_rings_only": run(list(range(1, 9)), ~even),
       "swapped_split_center_plus_rings": run(list(range(9)), ~even)}
json.dump(out, open("results/film_explore.json", "w"), indent=1); print(out)
