"""The eye of NPIC's 1970 Target Indexing Device, rebuilt from Litton's patent (US 3,689,772).

An n x n film patch (n = 128, or 64 for the USGS browse previews) -> its two-dimensional Fourier power spectrum (what Litton's lens did with
light) -> the power summed over 8 half-rings (one half of the spectrum), 34 wedges (the other half) and a small center spot: 43 numbers, in that
order (center, rings 0..7, wedges 0..33). Everything after two small cosine tables is integer arithmetic, so every run on every machine gives the
same bits; the tables and the detector layout are checked against their pinned SHA-256 when an eye is built.
"""
import hashlib, math
import numpy as np

Q = 14                   # fixed-point bits of the cosine and sine table
RINGS, WEDGES = 8, 34    # Litton's counts: "eight concentric annular hemi-ring or zone detectors", "34 radial sector detectors"
R_CENTER4 = 8            # center spot radius in quarter bins (2 bins). ASSUMPTION: the patent gives no size.
PINNED = {128: ("0f01140bf9f8b057b707beef007566450be92f6bd39ea432fc1350550fe31789", "e3548f165b14681596c7e0eb64020c86f62b7d0a10452c72c0c3b58192affdd1"),
          64: ("b4b23e0740e7e53a07bf2fbe8b8814f056c493e5cfebf2f92f2b9afa74c5510f", "d3729de0ea8351d3610a0bdeda686694627442a2f4d3acdc8a506159f20b7380")}

def _round_half_up(x):
    return int(math.floor(x + 0.5))

_PHI = [math.pi + math.pi * j / WEDGES for j in range(WEDGES + 1)]          # wedge boundaries, 180 to 360 degrees
_BC = [_round_half_up((1 << 30) * math.cos(p)) for p in _PHI]
_BS = [_round_half_up((1 << 30) * math.sin(p)) for p in _PHI]

def _shift(a, q=Q):
    return (a + (1 << (q - 1))) >> q        # round half up, exact on integers

class Eye:
    def __init__(self, n=128):
        self.n = n
        self.r_max4 = 4 * (n // 2)                               # outer edge: the Nyquist radius
        self.ring_w4 = (self.r_max4 - R_CENTER4) // RINGS         # ASSUMPTION: equal-width rings
        assert R_CENTER4 + RINGS * self.ring_w4 == self.r_max4
        self.wedge_r_min4 = R_CENTER4 + 2 * self.ring_w4          # wedges begin beyond ring 1 (change W1)
        self.cos = np.array([_round_half_up((1 << Q) * math.cos(2 * math.pi * m / n)) for m in range(n)], dtype=np.int64)
        self.sin = np.array([_round_half_up((1 << Q) * math.sin(2 * math.pi * m / n)) for m in range(n)], dtype=np.int64)
        idx = np.outer(np.arange(n), np.arange(n)) % n
        self.C, self.S = self.cos[idx], self.sin[idx]
        self.center, self.ring, self.wedge = self._layout()
        if n in PINNED and (self.table_sha(), self.layout_sha()) != PINNED[n]:
            raise RuntimeError("this machine builds a different eye than the published one (n=%d)" % n)

    def _freq(self, i):
        return i if i < self.n // 2 else i - self.n

    def _layout(self):
        n = self.n; center = np.zeros((n, n), bool); ring = -np.ones((n, n), np.int64); wedge = -np.ones((n, n), np.int64)
        for v in range(n):
            fv = self._freq(v)
            for u in range(n):
                fu = self._freq(u); r2_16 = 16 * (fu * fu + fv * fv)
                if r2_16 <= R_CENTER4 * R_CENTER4:
                    center[v, u] = True; continue
                if r2_16 > self.r_max4 * self.r_max4 or fv == 0:     # outside the detector, or on the gap along the film's travel
                    continue
                if fv > 0:                                            # the ring half
                    j = 0
                    while r2_16 > (R_CENTER4 + (j + 1) * self.ring_w4) ** 2:
                        j += 1
                    ring[v, u] = j
                elif r2_16 > self.wedge_r_min4 * self.wedge_r_min4:  # the wedge half, beyond ring 1
                    wedge[v, u] = sum(1 for j in range(1, WEDGES) if _BC[j] * fv - _BS[j] * fu >= 0)
        return center, ring, wedge

    def table_sha(self):
        h = hashlib.sha256()
        for a in (self.cos.tolist(), self.sin.tolist(), _BC, _BS):
            h.update((",".join(map(str, a)) + ";").encode())
        return h.hexdigest()

    def layout_sha(self):
        return hashlib.sha256(self.center.tobytes() + self.ring.tobytes() + self.wedge.tobytes()).hexdigest()

    def power_spectrum(self, patch):
        """|F|^2 of an n x n patch of integers 0..255, as int64. F[v, u]: v is the frequency down the rows, u across the columns."""
        x = np.asarray(patch, dtype=np.int64)
        assert x.shape == (self.n, self.n) and x.min() >= 0 and x.max() <= 255
        a_re = _shift(x @ self.C); a_im = -_shift(x @ self.S)
        f_re = _shift(self.C @ a_re + self.S @ a_im); f_im = _shift(self.C @ a_im - self.S @ a_re)
        return f_re * f_re + f_im * f_im

    def read(self, power):
        out = [power[self.center].sum()]
        out += [power[self.ring == j].sum() for j in range(RINGS)]
        out += [power[self.wedge == j].sum() for j in range(WEDGES)]
        return out

    def look(self, patch):
        return [int(v) for v in self.read(self.power_spectrum(patch))]

def sha(readings):
    return hashlib.sha256(",".join(str(int(v)) for v in readings).encode()).hexdigest()

# the published 128-pixel eye, under its old names
_E = Eye(128)
N, C, S, CENTER, RING, WEDGE = _E.n, _E.C, _E.S, _E.center, _E.ring, _E.wedge
R_MAX4, RING_W4, WEDGE_R_MIN4 = _E.r_max4, _E.ring_w4, _E.wedge_r_min4
power_spectrum, read, look, table_sha, layout_sha = _E.power_spectrum, _E.read, _E.look, _E.table_sha, _E.layout_sha
