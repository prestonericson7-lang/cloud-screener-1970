"""Three synthetic test cards whose right answers follow from geometry, and the checks for predictions E1 to E6."""
import json, math, sys, time
import numpy as np
import eye

N = eye.N
y, x = np.mgrid[0:N, 0:N]
CARDS = {
    "grating": np.rint(128 + 100 * np.cos(2 * np.pi * (20 * x + 12 * y) / N)).astype(np.int64),   # 20 across, 12 down
    "disk": np.where((x - 63.5) ** 2 + (y - 63.5) ** 2 <= 20 ** 2, 255, 0).astype(np.int64),
    "bar": np.where(np.abs(((x - y + N // 2) % N) - N // 2) <= 1, 255, 0).astype(np.int64),     # along x = y, wraps cleanly
}

def ring_of(r):      # which ring holds radius r (in bins)
    return int((4 * r - eye.R_CENTER4) // eye.RING_W4)

def wedge_of(deg):   # which wedge holds a direction between 180 and 360 degrees
    return int((deg - 180) // (180 / eye.WEDGES))

def run(E=None):
    E = E or eye._E
    out = {"mode": E.mode, "table_sha": E.table_sha(), "layout_sha": E.layout_sha(), "cards": {}}
    grades = {}
    e2_ok = True; worst = 0.0; times = []
    for name, card in CARDS.items():
        t = time.perf_counter(); a = E.look(card); times.append(time.perf_counter() - t)
        b = E.look(card)
        ref = E.read(np.abs(np.fft.fft2(card.astype(np.float64))) ** 2)
        off = sum(a[1:])
        for i, (ai, ri) in enumerate(zip(a, ref)):
            if i > 0 and ri >= 0.001 * off:
                err = abs(ai - ri) / ri; worst = max(worst, err); e2_ok &= err <= 0.005
        rings, wedges = a[1:1 + eye.RINGS], a[1 + eye.RINGS:]
        out["cards"][name] = {"readings": a, "sha": eye.sha(a), "same_twice": a == b,
                              "ring_share": [round(v / sum(rings), 5) for v in rings], "wedge_share": [round(v / sum(wedges), 5) for v in wedges]}
    c = out["cards"]
    grades["E1"] = all(v["same_twice"] for v in c.values())
    grades["E2"] = e2_ok; out["E2_worst_relative_error"] = worst
    gr = ring_of(math.hypot(20, 12)); gw = wedge_of(180 + math.degrees(math.atan2(12, 20)))
    out["E3"] = {"ring": gr, "ring_share": c["grating"]["ring_share"][gr], "wedge": gw, "wedge_share": c["grating"]["wedge_share"][gw]}
    grades["E3"] = out["E3"]["ring_share"] >= 0.95 and out["E3"]["wedge_share"] >= 0.95
    ws = c["disk"]["wedge_share"]; out["E4"] = {"max_over_min": round(max(ws) / min(ws), 4)}
    grades["E4"] = out["E4"]["max_over_min"] <= 1.3
    bw = wedge_of(315); out["E5"] = {"wedge": bw, "wedge_share": c["bar"]["wedge_share"][bw]}
    grades["E5"] = out["E5"]["wedge_share"] >= 0.80
    out["E6_seconds_per_patch"] = round(max(times), 4); grades["E6"] = max(times) < 0.2
    out["grades"] = {k: bool(v) for k, v in grades.items()}
    out["E2_worst_relative_error"] = float(worst)
    return out

if __name__ == "__main__":
    area = "--area" in sys.argv; args = [a for a in sys.argv[1:] if a != "--area"]
    r = run(eye.Eye(128, wedges="area") if area else None)
    json.dump(r, open(args[0] if args else ("results/testcards_area.json" if area else "results/testcards.json"), "w"), indent=1)
    print(json.dumps({k: r[k] for k in ("grades", "E2_worst_relative_error", "E3", "E4", "E5", "E6_seconds_per_patch")}, indent=1))
    print({k: v["sha"][:16] for k, v in r["cards"].items()})
