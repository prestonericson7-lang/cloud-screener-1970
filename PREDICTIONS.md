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
