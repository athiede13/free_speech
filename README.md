# free_speech

Code used for **Thiede et al. Atypical brain-to-brain synchronization during listening to continuous natural speech in dyslexia, submitted.**

## Preprocessing

Removal of noisy channels, maxfilter and physiological artifacts from MEG data.

## Source modeling

Setup of source space, forward and inverse operators in individual cortically-constrained source space.

## Inter-subject correlation (ISC)

Pair-wise correlation of MEG amplitude envelopes for different frequency bands, group averages. Code originally used in Suppanen, E., 2014. Inter-subject correlation of MEG data during movie viewing. Master’s thesis, Aalto University School of Electrical Engineering.

## Statistics

- One-sample permutation *t*-test to check for significance of ISCs.
- Group contrast with independent-samples permutation *t*-test.
- Correlation of ISCs with reading-related measures with Mantel test. Also refer to https://version.aalto.fi/gitlab/BML/bramila/tree/master

All cluster-corrected.
