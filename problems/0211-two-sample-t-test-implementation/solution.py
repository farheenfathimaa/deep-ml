import numpy as np
import math

# scipy is not available in this environment. The two helpers below compute
# the regularized incomplete beta function via the Numerical Recipes
# continued-fraction algorithm — you'll need them to compute the p-value
# from the t-distribution.
def _betacf(a, b, x):
    """Continued fraction for the incomplete beta function."""
    max_iter, eps = 200, 3e-12
    qab, qap, qam = a + b, a + 1.0, a - 1.0
    c = 1.0
    d = 1.0 - qab * x / qap
    if abs(d) < 1e-30: d = 1e-30
    d = 1.0 / d
    h = d
    for m in range(1, max_iter + 1):
        m2 = 2 * m
        aa = m * (b - m) * x / ((qam + m2) * (a + m2))
        d = 1.0 + aa * d
        if abs(d) < 1e-30: d = 1e-30
        c = 1.0 + aa / c
        if abs(c) < 1e-30: c = 1e-30
        d = 1.0 / d
        h *= d * c
        aa = -(a + m) * (qab + m) * x / ((a + m2) * (qap + m2))
        d = 1.0 + aa * d
        if abs(d) < 1e-30: d = 1e-30
        c = 1.0 + aa / c
        if abs(c) < 1e-30: c = 1e-30
        d = 1.0 / d
        delta = d * c
        h *= delta
        if abs(delta - 1.0) < eps: break
    return h

def _betainc(a, b, x):
    """Regularized incomplete beta function I_x(a, b)."""
    if x <= 0.0: return 0.0
    if x >= 1.0: return 1.0
    lbeta = math.lgamma(a) + math.lgamma(b) - math.lgamma(a + b)
    front = math.exp(math.log(x) * a + math.log(1.0 - x) * b - lbeta)
    if x < (a + 1.0) / (a + b + 2.0):
        return front * _betacf(a, b, x) / a
    return 1.0 - front * _betacf(b, a, 1.0 - x) / b

def t_cdf(t, df):
    """Cumulative distribution function (CDF) of Student's t-distribution."""
    x = df/(df + t**2)
    return 1.0 - 0.5 * _betainc(df / 2.0, 0.5, x) if t>=0 else 0.5 * _betainc(df / 2.0, 0.5, x)

def two_sample_t_test(sample1: list[float], sample2: list[float],
                      alpha: float = 0.05) -> dict:
    """
    Perform a two-sample independent t-test (Welch's t-test).

    Args:
        sample1: First sample data
        sample2: Second sample data
        alpha: Significance level (default 0.05)

    Returns:
        Dictionary containing:
        - t_statistic: The calculated t-statistic
        - p_value: Two-tailed p-value
        - degrees_of_freedom: Degrees of freedom (Welch-Satterthwaite)
        - reject_null: Boolean, whether to reject null hypothesis
        - cohens_d: Effect size (Cohen's d)
    """
    # Your code here
    n1, n2 = len(sample1), len(sample2)
    
    # Step 1: Means and Variances (using Bessel's correction ddof=1)
    mean1, mean2 = np.mean(sample1), np.mean(sample2)
    var1 = np.var(sample1, ddof=1)
    var2 = np.var(sample2, ddof=1)

    # Step 2: Standard Error
    se = np.sqrt((var1/n1) + (var2/n2))

    # Step 3: T-Statistic
    t_stat = (mean1 - mean2) / se

    # Step 4: Degrees of Freedom (Welch-Satterthwaite)
    num = ((var1 / n1) + (var2 / n2)) ** 2
    den = (((var1 / n1) ** 2)/ (n1-1)) + (((var2 / n2) ** 2)/ (n2-1))
    df = num/den

    # Step 5: Two-tailed P-value
    # Two-tailed p-value = 2 * (1 - CDF(|t|))
    p_val = 2.0 * (1.0 - t_cdf(abs(t_stat), df))

    # Step 6: Reject Null Hypothesis decision
    reject_null = bool(p_val < alpha)

    # Step 7: Cohen's d (Effect Size)
    s_pooled = np.sqrt(((n1 - 1) * var1 + (n2 - 1) * var2) / (n1 + n2 - 2))
    cohens_d = (mean1 - mean2) / s_pooled

    return {
        't_statistic': float(t_stat),
        'p_value': float(p_val),
        'degrees_of_freedom': float(df),
        'reject_null': reject_null,
        'cohens_d': float(cohens_d)
    }