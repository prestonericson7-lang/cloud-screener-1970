# Predictions, filed before the first run

Filed at 8:46 AM on November 22, 2026, before a line of the eye's code was written or run. Each has a confidence (ESTIMATE). Graded below each one after the runs;
nothing above a grade is changed after it is filed.

## The eye (Litton's ring-and-wedge detector, in software)

The eye takes a 128 by 128 patch of film, forms its two-dimensional Fourier power spectrum (what Litton's lens did with light), and sums the power over
8 half-rings, 34 wedges and a center spot: 43 numbers. Test cards are synthetic, so the right answers are known from geometry alone.

**E1 (99%).** Two runs of the eye on the same patch give the same 43 integers, bit for bit (the same SHA-256 over the outputs).

**E2 (85%).** The integer eye agrees with a 64-bit floating-point FFT of the same patch: every one of the 43 sums that holds at least 0.1% of the
patch's off-center power is within 0.5% of the reference, on all three test cards.

**E3 (85%).** A sinusoidal grating at 20 cycles across and 12 down (radius 23.3 cycles per patch, direction 31 degrees): at least 95% of the ring
half's off-center power lands in the one ring that contains radius 23.3, and at least 95% of the wedge half's power in the one wedge that contains
211 degrees (the grating's mirror image, by the spectrum's symmetry).

**E4 (80%).** A centered bright disk, 20 pixels in radius: the 34 wedges hold nearly equal power, the largest within 1.3 times the smallest, because
a disk looks the same from every angle.

**E5 (75%).** A thin bright bar along the patch's diagonal: at least 80% of the wedge half's power lands in the one wedge that contains the bar's
normal, 315 degrees.

**E6 (70%).** One patch takes under 0.2 seconds on the CPU (the eye is small; the GPUs stay with other work).

## Grades, 8:48 AM (MEASURED; results/testcards_run1.json and run2.json)

- **E1: HELD.** Two runs, the same 43 integers on all three cards (fingerprints f3826e214a75, 3fe2c75d7bf1, 3dd76ffc5c79).
- **E2: HELD.** The worst relative difference from the 64-bit floating-point FFT is 0.04182%, against the 0.5% allowed.
- **E3: HELD.** The grating puts 99.999% of the ring half's power in ring 2 and 99.999% of the wedge half's in wedge 5.
- **E4: FAILED.** The disk's wedges differ by a factor of 34.4, not 1.3. The cause is mine: nearly all of a 20-pixel disk's light lies within
  about 4 frequency bins of the center, and on a 128-point grid those few bins cannot be shared evenly among 34 wedges, so the wedges that own them
  take almost everything. Litton's wedges were continuous; these are pixels. The prediction misjudged the grid, not the optics.
- **E5: HELD.** The diagonal bar puts 100.000% of the wedge half's power in wedge 25, which holds 315 degrees.
- **E6: HELD.** 9.9 milliseconds a patch on the CPU.

## A change, with its prediction filed first (8:48 AM)

**W1 (60%).** One change only: the wedges begin outside ring 1 (beyond 17.5 frequency bins), where every wedge owns enough bins, and the bins
inside go to no wedge (the rings still read them). With that change the disk's wedges differ by no more than a factor of 1.3, and E1, E2, E3 and
E5 still hold.

### Grade of W1, 8:49 AM (MEASURED; results/testcards_w1_run1.json and run2.json)

- **W1: FAILED, and kept.** The disk's wedges now differ by a factor of 1.70, down from 34.4 but not within 1.3. E1, E2 (worst 0.0577%), E3 and E5 still
  hold, so the change stays: it is a twentyfold improvement that breaks nothing. What is left is the grid itself: wedges near the axes own different
  numbers of pixels from wedges on the diagonals (149 to 196 here), and the light near the inner edge is strong.

## Open, filed but not run: W2

**W2 (65%).** Split each frequency bin's power among the wedges by the area of the bin each wedge covers (16 by 16 sub-points a bin, counted in
integers), the way Litton's continuous wedges collected light. The disk's wedges then differ by no more than 1.3. Expected cost: the grating's single
bright bin can straddle two wedges, so E3's wedge share may fall below 95% (a real detector's spot has width too). Not run yet; anyone may.

## The film: predictions filed 8:59 AM, before any film was downloaded

The film: CORONA mission 1007-1, pass 56-D, aft camera, June 23, 1964, over central Russia (about 52.6 to 50.5 degrees north, 38 east), frames
DS1007-1056DA130 (mostly clear), DA135 (partly covered) and DA138 (a solid deck over two-thirds of the frame), chosen from USGS browse images; more
frames of the same pass may follow. Each frame is cut into 128 by 128 patches, and every patch is labeled clear, partly cloudy or cloudy by eye, before
any machine reads it. Patches are split into training and held-out sets by frame position, fixed before any score is computed. Two decision rules,
neither claimed to be the 1970 original: the fixed rule (the share of off-center power in the inner rings against the outer, with a threshold set on
the training patches), and the trained rule (a linear threshold unit on the logarithms of the 43 readings, taught by the perceptron rule).

**F1 (80%).** Clear against cloudy (partly cloudy left out), held-out patches: the fixed rule gets at least 90% right.

**F2 (70%).** The trained rule gets at least 90% on the same patches, and at least as many as the fixed rule.

**F3 (55%).** All three classes, held-out patches: the trained rule gets at least 70% right.

**F4 (70%).** The wedges add little to cloud screening: dropping the 34 wedges changes the trained rule's three-class score by less than 5 points.

**F5 (50%).** The honest baseline: brightness alone (the center spot) with a threshold set the same way. The eye's trained rule beats it by at least
5 points on three classes. If it does not, the diffraction eye bought the 1970 machine nothing that a light meter could not.

### Amendment, 9:19 AM, before the eye has read any film

The full scans cannot be had from this machine today: EarthExplorer's sign-in runs Google's reCAPTCHA and its search page loads its controls from
Google's servers, and this network does not reach Google. So F1 to F5 run first on the film USGS serves without sign-in: its browse previews of the
same pass (1,480 by 115 pixels a frame, about 135 m of ground a pixel), with the eye built at 64 by 64 instead of 128 by 128 because the strips are
115 pixels tall. The eye at 64 keeps Litton's layout (8 equal rings from 2 bins to the Nyquist radius of 32, 34 wedges beyond ring 1, the center
spot, the gap along the film's travel) and gets its own pinned fingerprints. Frames DS1007-1056DA129 to DA145 (all 17), plus DA100, DA106, DA112,
DA118 and DA124 for more clear ground. Each strip's middle 64 rows are cut into 23 patches. Training and held-out sets: even frame numbers train,
odd frame numbers are held out, fixed now. A patch whose label is uncertain by eye is marked so and left out of every score. The predictions above are
not changed. The full-scan run stays open for a machine that can sign in.

### Grades of F1 to F5, 9:24 AM (MEASURED; results/film_results.json; held-out frames only, the split fixed in the amendment)

- **F1: FAILED.** The fixed ring rule tells clear from cloudy on 66.3% of held-out patches, not 90%. The inner rings' share of the spectrum does not
  separate a cloud deck from farmland by itself.
- **F2: HELD.** The trained rule: 99.0%, and well above the fixed rule.
- **F3: HELD.** All three classes: 85.8%. Clear 40 of 45 right; partly cloudy 76 of 93 (11 called clear, 6 cloudy); cloudy 53 of 59.
- **F4: HELD.** Without the 34 wedges: 87.3%, a change of +1.5 points. Clouds have no direction; the rings carry the signal.
- **F5: HELD.** Brightness alone, three classes: 69.0%; the eye's trained rule beats it by 16.8 points.

**What the grades leave out, said plainly.** On clear against cloudy, brightness alone gets 100% of held-out patches right: a light meter can tell
clear ground from a cloud deck. The diffraction eye earns its keep on the hard case, partial cloud, which is where a screener for target locations
lives. Exploratory, not predicted (results/film_explore.json): the rings alone, without brightness, get 85.3%, so the shape of the diffraction
pattern carries the signal by itself; and with the training and held-out frames swapped, the eye gets 73.6% (rings alone 68.2%), because the
even frames hold the northern farmland strips that look unlike the cloudy south. The honest range is about 74 to 86%, depending on which frames teach.
