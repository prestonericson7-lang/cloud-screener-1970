# The 1970 cloud screener, rebuilt

In 1969 and 1970 the CIA's National Photographic Interpretation Center (NPIC) had Litton Systems of Van Nuys, California build a Target Indexing
Device: a machine of about 2,750 pounds that read reconnaissance film at 100 feet a minute and told, for each target, whether cloud hid it. It saw
the film through a lens, which turns a picture into its diffraction pattern, and read that pattern with a detector of rings and wedges. Litton's
engineers patented the detector in 1971. This repository rebuilds that eye from the patent, exactly, so anyone can run it and get the same numbers,
and then puts it to the machine's own job on declassified film of the same years.

Done by Claude with Preston Ericson, November 2026. How the records were found, and the history around them, is in the companion repository
[the-winter-that-wasnt](https://github.com/prestonericson7-lang/the-winter-that-wasnt).

## What the record gives (each read in its source)

- **The job.** "an automatic cloud screening technique for use in the target indexing operation normally performed (manually) during initial
  handling of newly acquired imagery prior to interpretation," in two modes: whether "specific target locations are cloud free, partially covered
  or fully cloud covered (look thru mode), or ... the amount of cloud cover for each frame" (NPIC's test plan, November 12, 1970, CIA record
  [CIA-RDP78B05703A000100030009-3](https://www.cia.gov/readingroom/document/cia-rdp78b05703a000100030009-3)).
- **The technique.** Diffraction pattern sampling, chosen by NPIC on September 2, 1969.
- **The eye.** US patent [3,689,772](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/3689772) (filed August 18, 1971; Nicholas
  George, James T. Thomasson, Abraham Spindel; assigned to Litton Systems): "eight concentric annular hemi-ring or zone detectors" reading energy
  "as a function of radius," "34 radial sector detectors" reading it "as a function of angle," a small center detector for the undiffracted
  light, and a gap between the two halves turned to hide the streaks that film scratches make.
- **The maker.** Litton, named in three released records though sanitized everywhere else (see the companion repository's docs/02).
- **The machine.** "the main chassis, two magnetic tape units, a tape controller, a DDP.516 computer and a teletype."
- **Not in the record:** how the device turned its readings into clear, partly cloudy or cloudy. Nothing here claims to be the original rule.

## The eye ([eye.py](eye.py))

A 128 by 128 patch of film goes to its two-dimensional Fourier power spectrum, computed in 14-bit fixed-point integers (the kind of arithmetic a
16-bit machine of the day used), and the power is summed over the detector's regions: 43 readings, the center spot, 8 rings, 34 wedges. Choices the
patent leaves open, made here and marked as ours: equal-width rings from 2 to 64 frequency bins; a center spot 2 bins wide; the dividing gap is
the row of frequencies along the film's travel; the wedges begin beyond ring 1 (change W1, below).

Every step after two small cosine tables is integer arithmetic, and the tables and the detector layout are checked against their SHA-256 when
[eye.py](eye.py) loads, so the same patch gives the same 43 integers on any machine.

## The test cards ([testcards.py](testcards.py)) and the predictions ([PREDICTIONS.md](PREDICTIONS.md))

Three synthetic cards whose right answers follow from geometry: a grating, a disk and a diagonal bar. Six predictions were filed and committed
before any code existed, then graded:

| | Prediction | Result |
|---|---|---|
| E1 | the same bits on every run | held |
| E2 | within 0.5% of a 64-bit floating-point FFT | held (worst 0.058%) |
| E3 | a grating lands in one ring and one wedge | held (99.999%) |
| E4 | a disk spreads evenly over the 34 wedges | failed (34 times, then 1.7 times after W1) |
| E5 | a diagonal bar lands in the wedge of its normal | held (100%) |
| E6 | under 0.2 s a patch on a CPU | held (0.01 s) |

E4 failed because a disk's light sits within a few frequency bins of the center, where a pixel grid cannot share it evenly among 34 wedges.
Litton's wedges were continuous. W1 (wedges begin beyond ring 1) cut the spread twentyfold; W2 (split each bin among wedges by area) is filed and
open.

## Run it

Python 3 and NumPy. `python testcards.py` writes `results/testcards.json`. Your fingerprints should match these exactly:

- grating `21fca8ee051461c033868b4054b496d75a2d03f0570cc6c2ae0969bbe4354aee`
- disk `646b925b1702e767420cd50e057e2756eda47195338a9d320517f9c0b84b025d`
- bar `b702b31a0b5382cd6e27cfcc0817669e73d8e10702f591282073dfe35d5bae32`

## Next: the film (not done yet)

Declassified CORONA reconnaissance frames from 1960 to 1972 (USGS EarthExplorer). Frames with cloud and without, cut into patches, every patch
labeled clear, partly cloudy or cloudy by eye before any machine sees it; predictions filed first; then a fixed rule (power in the inner rings
against the outer: cloud is bright and smooth, ground is textured) and a trained rule (a linear threshold unit taught on examples, the kind its
era's learning machines used), scored only on patches held out from training. After that, on the same footing: Scope Incorporated's prenormalizer
(US patent 3,566,080), the front end of the CONFLEX I learning machine the CIA tested on rotated railyards in 1965.

## What this is and is not

A faithful reconstruction of what the record describes, not a recovery of the original: its settings and its film are classified or gone. It can
show what a 1970 machine could do on the same kind of film and test what the records claim. It will not uncover a hidden modern capability; by
everything the released record shows, there was none ahead of the open world.

## License

Text and code: [Creative Commons Attribution 4.0](https://creativecommons.org/licenses/by/4.0/) ([LICENSE](LICENSE)). The CIA records and US patents
quoted are US government works or public records.
