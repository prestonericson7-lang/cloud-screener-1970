"""The eye of NPIC's 1970 Target Indexing Device, rebuilt from Litton's patent (US 3,689,772).

A 128 x 128 film patch -> its two-dimensional Fourier power spectrum (what Litton's lens did with light) -> the power summed over
8 half-rings (one half of the spectrum), 34 wedges (the other half) and a small center spot: 43 numbers, in that order
(center, rings 0..7, wedges 0..33). Everything after the two small cosine tables is integer arithmetic, so every run on every
machine gives the same bits; the tables are checked against their SHA-256 at import.
"""
import hashlib, math
import numpy as np

N = 128            # patch size in pixels (the integer bounds below are worked out for this size)
Q = 14             # fixed-point bits of the cosine and sine table
RINGS, WEDGES = 8, 34   # Litton's counts: "eight concentric annular hemi-ring or zone detectors", "34 radial sector detectors"
R_CENTER4 = 8      # center spot radius, in quarter frequency bins (2 bins). ASSUMPTION: the patent gives no size.
R_MAX4 = 4 * (N // 2)   # outer edge of the detector: the Nyquist radius, 64 bins
RING_W4 = (R_MAX4 - R_CENTER4) // RINGS   # 31 quarter bins (7.75 bins). ASSUMPTION: equal-width rings.
WEDGE_R_MIN4 = R_CENTER4 + 2 * RING_W4   # wedges begin beyond ring 1 (17.5 bins): change W1, see PREDICTIONS.md
assert R_CENTER4 + RINGS * RING_W4 == R_MAX4

def _round_half_up(x):
    return int(math.floor(x + 0.5))

# cos and sin of 2*pi*m/N, scaled by 2**Q; and the wedge boundary directions, scaled by 2**30
_COS = np.array([_round_half_up((1 << Q) * math.cos(2 * math.pi * m / N)) for m in range(N)], dtype=np.int64)
_SIN = np.array([_round_half_up((1 << Q) * math.sin(2 * math.pi * m / N)) for m in range(N)], dtype=np.int64)
_PHI = [math.pi + math.pi * j / WEDGES for j in range(WEDGES + 1)]          # 180 to 360 degrees
_BC = [_round_half_up((1 << 30) * math.cos(p)) for p in _PHI]
_BS = [_round_half_up((1 << 30) * math.sin(p)) for p in _PHI]

def table_sha():
    h = hashlib.sha256()
    for a in (_COS.tolist(), _SIN.tolist(), _BC, _BS):
        h.update((",".join(map(str, a)) + ";").encode())
    return h.hexdigest()

TABLE_SHA = "0f01140bf9f8b057b707beef007566450be92f6bd39ea432fc1350550fe31789"
LAYOUT_SHA = "e3548f165b14681596c7e0eb64020c86f62b7d0a10452c72c0c3b58192affdd1"
if table_sha() != TABLE_SHA:
    raise RuntimeError("this machine rounds the cosine table differently; the outputs would not match the published ones")

_k = np.arange(N)
_IDX = (np.outer(_k, _k) % N)
C = _COS[_IDX]      # C[k, n] = cos(2 pi k n / N) * 2**Q, symmetric
S = _SIN[_IDX]

def _shift(a, q=Q):
    return (a + (1 << (q - 1))) >> q        # round half up, exact on integers

def power_spectrum(patch):
    """|F|^2 of an N x N patch of integers 0..255, as int64. F[v, u]: v is the frequency down the rows, u across the columns."""
    x = np.asarray(patch, dtype=np.int64)
    assert x.shape == (N, N) and x.min() >= 0 and x.max() <= 255
    a_re = _shift(x @ C)                     # along each row (u)
    a_im = -_shift(x @ S)
    f_re = _shift(C @ a_re + S @ a_im)       # then down each column (v)
    f_im = _shift(C @ a_im - S @ a_re)
    return f_re * f_re + f_im * f_im

def _freq(i):
    return i if i < N // 2 else i - N

def _layout():
    """Which detector each frequency bin falls on: -1 for none (the dividing gap, the corners beyond the circle)."""
    center = np.zeros((N, N), bool); ring = -np.ones((N, N), np.int64); wedge = -np.ones((N, N), np.int64)
    for v in range(N):
        fv = _freq(v)
        for u in range(N):
            fu = _freq(u); r2_16 = 16 * (fu * fu + fv * fv)
            if r2_16 <= R_CENTER4 * R_CENTER4:
                center[v, u] = True; continue
            if r2_16 > R_MAX4 * R_MAX4 or fv == 0:          # outside the detector, or on the gap along the film's travel
                continue
            if fv > 0:                                       # the ring half
                j = 0
                while r2_16 > (R_CENTER4 + (j + 1) * RING_W4) ** 2:
                    j += 1
                ring[v, u] = j
            elif r2_16 > WEDGE_R_MIN4 * WEDGE_R_MIN4:       # the wedge half, beyond ring 1: count boundaries at or behind this bin
                wedge[v, u] = sum(1 for j in range(1, WEDGES) if _BC[j] * fv - _BS[j] * fu >= 0)
    return center, ring, wedge

CENTER, RING, WEDGE = _layout()

def layout_sha():
    return hashlib.sha256(CENTER.tobytes() + RING.tobytes() + WEDGE.tobytes()).hexdigest()

if LAYOUT_SHA and layout_sha() != LAYOUT_SHA:
    raise RuntimeError("the detector layout differs from the published one")

def read(power):
    """The 43 detector readings from a power spectrum (integers, or floats for a reference)."""
    out = [power[CENTER].sum()]
    out += [power[RING == j].sum() for j in range(RINGS)]
    out += [power[WEDGE == j].sum() for j in range(WEDGES)]
    return out

def look(patch):
    return [int(v) for v in read(power_spectrum(patch))]

def sha(readings):
    return hashlib.sha256(",".join(str(int(v)) for v in readings).encode()).hexdigest()
