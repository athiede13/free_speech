"""
Scipy function for independent t-test modified to not return p-value.

Modified on Thu May 16 18:09:40 2019
@author: Anja Thiede <anja.thiede@helsinki.fi>
"""

from __future__ import division, print_function, absolute_import
from collections import namedtuple
import numpy as np
from numpy import ma
from scipy.stats.stats import (mstats_basic, _chk2_asarray, _contains_nan, _equal_var_ttest_denom,
                               _unequal_var_ttest_denom, _ttest_ind_from_stats
                               )

Ttest_indResult = namedtuple('Ttest_indResult', ('statistic', 'pvalue'))

def ttest_ind_no_p(a, b, axis=0, equal_var=True, nan_policy='propagate'):
    """
    Calculate the T-test for the means of *two independent* samples of scores,
    do not return the p.
    This is a two-sided test for the null hypothesis that 2 independent samples
    have identical average (expected) values. This test assumes that the
    populations have identical variances by default.
    Parameters
    ----------
    a, b : array_like
        The arrays must have the same shape, except in the dimension
        corresponding to `axis` (the first, by default).
    axis : int or None, optional
        Axis along which to compute test. If None, compute over the whole
        arrays, `a`, and `b`.
    equal_var : bool, optional
        If True (default), perform a standard independent 2 sample test
        that assumes equal population variances [1]_.
        If False, perform Welch's t-test, which does not assume equal
        population variance [2]_.
        .. versionadded:: 0.11.0
    nan_policy : {'propagate', 'raise', 'omit'}, optional
        Defines how to handle when input contains nan. 'propagate' returns nan,
        'raise' throws an error, 'omit' performs the calculations ignoring nan
        values. Default is 'propagate'.
    Returns
    -------
    statistic : float or array
        The calculated t-statistic.
    Notes
    -----
    We can use this test, if we observe two independent samples from
    the same or different population, e.g. exam scores of boys and
    girls or of two ethnic groups. The test measures whether the
    average (expected) value differs significantly across samples. If
    we observe a large p-value, for example larger than 0.05 or 0.1,
    then we cannot reject the null hypothesis of identical average scores.
    If the p-value is smaller than the threshold, e.g. 1%, 5% or 10%,
    then we reject the null hypothesis of equal averages.
    References
    ----------
    .. [1] https://en.wikipedia.org/wiki/T-test#Independent_two-sample_t-test
    .. [2] https://en.wikipedia.org/wiki/Welch%27s_t-test
    Examples
    --------
    >>> from scipy import stats
    >>> np.random.seed(12345678)
    Test with sample with identical means:
    >>> rvs1 = stats.norm.rvs(loc=5,scale=10,size=500)
    >>> rvs2 = stats.norm.rvs(loc=5,scale=10,size=500)
    >>> stats.ttest_ind(rvs1,rvs2)
    (0.26833823296239279, 0.78849443369564776)
    >>> stats.ttest_ind(rvs1,rvs2, equal_var = False)
    (0.26833823296239279, 0.78849452749500748)
    `ttest_ind` underestimates p for unequal variances:
    >>> rvs3 = stats.norm.rvs(loc=5, scale=20, size=500)
    >>> stats.ttest_ind(rvs1, rvs3)
    (-0.46580283298287162, 0.64145827413436174)
    >>> stats.ttest_ind(rvs1, rvs3, equal_var = False)
    (-0.46580283298287162, 0.64149646246569292)
    When n1 != n2, the equal variance t-statistic is no longer equal to the
    unequal variance t-statistic:
    >>> rvs4 = stats.norm.rvs(loc=5, scale=20, size=100)
    >>> stats.ttest_ind(rvs1, rvs4)
    (-0.99882539442782481, 0.3182832709103896)
    >>> stats.ttest_ind(rvs1, rvs4, equal_var = False)
    (-0.69712570584654099, 0.48716927725402048)
    T-test with different means, variance, and n:
    >>> rvs5 = stats.norm.rvs(loc=8, scale=20, size=100)
    >>> stats.ttest_ind(rvs1, rvs5)
    (-1.4679669854490653, 0.14263895620529152)
    >>> stats.ttest_ind(rvs1, rvs5, equal_var = False)
    (-0.94365973617132992, 0.34744170334794122)
    """
    a, b, axis = _chk2_asarray(a, b, axis)

    # check both a and b
    cna, npa = _contains_nan(a, nan_policy)
    cnb, npb = _contains_nan(b, nan_policy)
    contains_nan = cna or cnb
    if npa == 'omit' or npb == 'omit':
        nan_policy = 'omit'

    if contains_nan and nan_policy == 'omit':
        a = ma.masked_invalid(a)
        b = ma.masked_invalid(b)
        return mstats_basic.ttest_ind(a, b, axis, equal_var)

    if a.size == 0 or b.size == 0:
        return Ttest_indResult(np.nan, np.nan)

    v1 = np.var(a, axis, ddof=1)
    v2 = np.var(b, axis, ddof=1)
    n1 = a.shape[axis]
    n2 = b.shape[axis]

    if equal_var:
        df, denom = _equal_var_ttest_denom(v1, n1, v2, n2)
    else:
        df, denom = _unequal_var_ttest_denom(v1, n1, v2, n2)

    tvals, pvals = _ttest_ind_from_stats(np.mean(a, axis), np.mean(b, axis), denom, df)

    return tvals
