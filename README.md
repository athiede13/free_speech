# free_speech

Code used for **Thiede, A. et al. Atypical MEG inter-subject correlation during listening to continuous natural speech in dyslexia, Neuroimage. 216 (2020) 116799. https://doi.org/10.1016/j.neuroimage.2020.116799.** Most of the code makes use of the [MNE Python](https://github.com/mne-tools/mne-python) software package.

DOI for the code: [![DOI](https://zenodo.org/badge/176300570.svg)](https://zenodo.org/badge/latestdoi/176300570)

## Preprocessing

Removal of noisy channels, maxfilter and physiological artifacts from MEG data.

## Source modeling

Setup of source space, forward and inverse operators in individual cortically-constrained source space.

## Inter-subject correlation (ISC)

Pair-wise correlation of MEG amplitude envelopes for different frequency bands, group averages. Code originally used in [Suppanen, E., 2014. Inter-subject correlation of MEG data during movie viewing. Master’s thesis, Aalto University School of Electrical Engineering.](http://urn.fi/URN:NBN:fi:aalto-201412303344)

## Statistics

- One-sample permutation *t*-test to check for significance of ISCs.
- Group contrast with independent-samples permutation *t*-test.
- Correlation of ISCs with reading-related measures with Mantel test. Also refer to https://version.aalto.fi/gitlab/BML/bramila/tree/master

All cluster-corrected.
