"""Pure-Python statistics for the evaluation (design §7, architecture D7).

No numpy or scipy. Each function cites the worked example its test reproduces.
Intervals are descriptive; an interval containing zero is inconclusive, not evidence of no effect.
"""

from collections.abc import Callable, Mapping, Sequence
from dataclasses import dataclass
from math import comb, sqrt
from random import Random
from statistics import NormalDist


@dataclass(frozen=True)
class Interval:
    low: float
    high: float


@dataclass(frozen=True)
class Bootstrap:
    estimate: float
    interval: Interval
    replicates: tuple[float, ...]
    seed: int


@dataclass(frozen=True)
class SignTest:
    positive: int
    negative: int
    ties: int
    p_value: float


def _z(confidence: float) -> float:
    if not 0.5 < confidence < 1.0:
        raise ValueError("confidence must lie strictly between 0.5 and 1")
    return NormalDist().inv_cdf(0.5 + confidence / 2)


def mean(values: Sequence[float]) -> float:
    if not values:
        raise ValueError("mean of no values")
    return sum(values) / len(values)


def wilson(successes: int, trials: int, *, confidence: float = 0.95) -> Interval:
    """Wilson score interval (Wilson 1927).

    Worked example: Newcombe (1998), Table I, method 3: 81/263 gives (0.2553, 0.3662)
    and 0/20 gives (0.0000, 0.1611).
    """
    if trials <= 0 or not 0 <= successes <= trials:
        raise ValueError("successes must lie in 0..trials with trials > 0")
    z = _z(confidence)
    p = successes / trials
    denominator = 1 + z * z / trials
    center = (p + z * z / (2 * trials)) / denominator
    half = z * sqrt(p * (1 - p) / trials + z * z / (4 * trials * trials)) / denominator
    return Interval(max(0.0, center - half), min(1.0, center + half))


def binomial_upper_bound(failures: int, trials: int, *, confidence: float = 0.95) -> float:
    """One-sided Clopper-Pearson upper bound on the failure probability.

    Zero failures has the closed form 1 - (1 - confidence) ** (1 / trials): 0 failures in the
    990 seeded cases of E1.1 give 0.302 % (experimental-design.md §3). Other counts solve
    P[X <= failures | p] = 1 - confidence for p by bisection on the exact binomial sum.
    """
    if trials <= 0 or not 0 <= failures <= trials or not 0 < confidence < 1:
        raise ValueError("invalid binomial bound arguments")
    if failures == trials:
        return 1.0
    alpha = 1 - confidence
    if failures == 0:
        return 1 - float(alpha ** (1 / trials))

    def lower_tail(p: float) -> float:
        return sum(comb(trials, k) * p**k * (1 - p) ** (trials - k) for k in range(failures + 1))

    low, high = failures / trials, 1.0
    for _ in range(200):
        middle = (low + high) / 2
        if lower_tail(middle) > alpha:
            low = middle
        else:
            high = middle
    return high


def clopper_pearson(successes: int, trials: int, *, confidence: float = 0.95) -> Interval:
    """Two-sided exact (Clopper-Pearson 1934) interval, each tail at (1 - confidence) / 2.

    Both ends reuse the one-sided bisection of `binomial_upper_bound`: the upper end bounds the success
    probability, the lower end is the mirror image of the bound on the failure count. Closed forms at the
    ends: 0/20 gives (0, 1 - 0.025 ** (1/20)) = (0, 0.1684) and 20/20 gives (0.8316, 1). 81/263 gives
    (0.2527, 0.3676), wider than Wilson's (0.2553, 0.3662) as the exact interval must be.
    """
    if trials <= 0 or not 0 <= successes <= trials:
        raise ValueError("successes must lie in 0..trials with trials > 0")
    tail = 1 - (1 - confidence) / 2
    high = 1.0 if successes == trials else binomial_upper_bound(successes, trials, confidence=tail)
    low = 0.0 if successes == 0 else 1 - binomial_upper_bound(trials - successes, trials, confidence=tail)
    return Interval(low, high)


def rule_of_three(trials: int) -> float:
    """Hanley and Lippman-Hand (1983): zero events in n trials suggests a rate below 3/n."""
    if trials <= 0:
        raise ValueError("trials must be positive")
    return 3 / trials


def cluster_bootstrap(
    clusters: Mapping[str, Sequence[float]],
    statistic: Callable[[Sequence[float]], float],
    *,
    replicates: int = 2000,
    seed: int,
    confidence: float = 0.95,
) -> Bootstrap:
    """Seeded percentile bootstrap that resamples whole clusters (kernels), not units.

    With clusters {a: [0, 0], b: [1, 1]} every replicate of the mean lies in {0, 0.5, 1},
    which an iid resample over the four units would not guarantee.
    """
    if not clusters or replicates <= 0 or any(not values for values in clusters.values()):
        raise ValueError("bootstrap needs non-empty clusters and a positive replicate count")
    if not 0 < confidence < 1:
        raise ValueError("bootstrap confidence must lie strictly between 0 and 1")
    names = sorted(clusters)
    pooled = [value for name in names for value in clusters[name]]
    estimate = statistic(pooled)
    random = Random(seed)
    samples = []
    for _ in range(replicates):
        chosen = [random.choice(names) for _ in names]
        samples.append(statistic([value for name in chosen for value in clusters[name]]))
    ordered = sorted(samples)
    tail = (1 - confidence) / 2
    low = ordered[min(len(ordered) - 1, int(tail * len(ordered)))]
    high = ordered[min(len(ordered) - 1, int((1 - tail) * len(ordered)))]
    return Bootstrap(estimate, Interval(low, high), tuple(samples), seed)


def sign_test(differences: Sequence[float]) -> SignTest:
    """Exact two-sided sign test on paired differences; ties are discarded.

    Worked example: 9 positive and 2 negative differences give p = 2 * P[X >= 9 | n = 11, 1/2]
    = 134 / 2048 ~ 0.0654. With no non-zero difference the p-value is 1.
    """
    positive = sum(d > 0 for d in differences)
    negative = sum(d < 0 for d in differences)
    ties = len(differences) - positive - negative
    n = positive + negative
    if n == 0:
        return SignTest(positive, negative, ties, 1.0)
    k = min(positive, negative)
    tail = sum(comb(n, i) for i in range(k + 1)) / 2**n
    return SignTest(positive, negative, ties, min(1.0, 2 * tail))


def holm(p_values: Sequence[float]) -> tuple[float, ...]:
    """Holm (1979) step-down adjustment, returned in the input order.

    Worked example: (0.01, 0.04, 0.03) -> (0.03, 0.06, 0.06): sorted p-values are multiplied by
    m, m - 1, ..., 1 and made monotone non-decreasing, then capped at 1.
    """
    if not p_values or any(not 0 <= p <= 1 for p in p_values):
        raise ValueError("p-values must lie in [0, 1]")
    m = len(p_values)
    order = sorted(range(m), key=lambda i: p_values[i])
    adjusted = [0.0] * m
    running = 0.0
    for rank, index in enumerate(order):
        running = max(running, min(1.0, p_values[index] * (m - rank)))
        adjusted[index] = running
    return tuple(adjusted)
