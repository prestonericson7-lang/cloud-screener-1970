"""W3: a card with no edge (a smooth radial ripple whose spectrum is a ring of radius 30), read by both wedge modes. See PREDICTIONS.md."""
import json, numpy as np
import eye
n = 128; y, x = np.mgrid[0:n, 0:n]; r = np.hypot(x - 63.5, y - 63.5)
card = np.rint(128 + 100 * np.cos(2 * np.pi * r * 30 / n) * np.exp(-r ** 2 / (2 * 20.0 ** 2))).astype(np.int64)
out = {}
for mode in ("bins", "area"):
    E = eye.Eye(n, wedges=mode); a = E.look(card); b = E.look(card); w = a[1 + eye.RINGS:]
    inner = w[1:33]; m = sum(inner) / len(inner)
    out[mode] = {"same_twice": a == b, "sha": eye.sha(a), "max_over_min_wedges_1_to_32": round(max(inner) / min(inner), 4),
                 "wedge_0_and_33_vs_mean": [round(w[0] / m, 3), round(w[33] / m, 3)], "ring_share": [round(v / sum(a[1:9]), 4) for v in a[1:9]]}
out["W3_held"] = bool(out["area"]["max_over_min_wedges_1_to_32"] <= 1.1 and out["bins"]["max_over_min_wedges_1_to_32"] > 1.1)
json.dump(out, open("results/w3_ring.json", "w"), indent=1); print(json.dumps(out, indent=1))
