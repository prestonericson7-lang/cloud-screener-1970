# Labels, by eye, before any machine reads the film

Each preview strip (1,480 by 115 pixels) gives 23 patches of 64 by 64 pixels: rows 25 to 88, columns starting at 4 and stepping by 64. Patch 0 is
at the left end of the strip as USGS serves it. Every patch is labeled by Claude looking at the enlarged patch, before the eye reads any of them.

- **C, clear:** no cloud visible in the patch.
- **F, cloudy:** cloud covers nearly all of the patch (about 90% or more); the ground is hidden.
- **P, partly cloudy:** visible cloud anywhere between those, scattered small cumulus included.
- **?, uncertain:** cannot tell at this resolution (bright fields, haze, or a blur that may or may not be cloud). Left out of every score.

Training frames: even numbers. Held-out frames: odd numbers (fixed in the amendment of PREDICTIONS.md before any labeling).

| frame | patches 0 to 22 |
|---|---|
| DS1007-1056DA100 | C C C ? C C C C C C ? ? ? C C C C ? ? ? ? ? ? |
| DS1007-1056DA106 | C C C ? ? C C ? C C C C C ? ? C ? C C ? ? ? ? |
| DS1007-1056DA112 | C C C C C C C C C C C C C C C C C ? ? ? ? ? ? |
| DS1007-1056DA118 | ? ? C C C C C C C C C C C C C C C C C C ? ? ? |
| DS1007-1056DA124 | P P ? P C C C C C C C C C C C C C C C C C C ? |
| DS1007-1056DA129 | P P C C P P P P P P C C C C C C C P C C C C C |
| DS1007-1056DA130 | P ? P P C C P P P P P C C C C C C C C C C C C |
| DS1007-1056DA131 | P P P P P ? C P P P P P C C C C C C C C C C C |
| DS1007-1056DA132 | F ? F F F F ? P P P P P P C C C C C C C C C C |
| DS1007-1056DA133 | F F F P P F F F P P P P P P P C C C C C C C C |
| DS1007-1056DA134 | F F F F P P F F F F ? P P P P P P C C C C C ? |
| DS1007-1056DA135 | F F F F F P P P ? F F P P ? P P P P P C C C P |
| DS1007-1056DA136 | F F F F F F P P P ? F F F F F P P P C C C C C |
| DS1007-1056DA137 | F F F F F F F F F F F F F F F P P P P C P P C |
| DS1007-1056DA138 | F F F F F F F F F F F F F F F F F P P P P P C |
| DS1007-1056DA139 | F F F F F F F F F F F F F F F F F ? P P P P C |
| DS1007-1056DA140 | F F F F F F F F F F F P ? F P F P P P P P P P |
| DS1007-1056DA141 | F F F F F F F F P P P F F P P P P P P P P P P |
| DS1007-1056DA142 | F F F F F F F F P P P P P P F F P P C C C C P |
| DS1007-1056DA143 | F F F P P P ? P P P P P P P P P P P P P C C C |
| DS1007-1056DA144 | P ? P P P P P P P P P P P P P P P P P P C C C |
| DS1007-1056DA145 | P P P P P P P P P P P ? P ? P ? P ? F ? P C C |

Counts: C 166, P 166, F 123, ? 51. Training (even frames): C 121, P 73, F 64, ? 41. Held out (odd frames): C 45, P 93, F 59, ? 10.
