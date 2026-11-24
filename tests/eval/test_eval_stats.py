"""Pure statistics checked against published worked examples (EV-R18)."""

import pytest

from pfc2_eval import stats


def test_wilson_matches_newcombe_1998_table_examples():
    # Newcombe (1998), Table I, method 3: 81/263 -> (0.2553, 0.3662); 0/20 -> (0.0000, 0.1611).
    interval = stats.wilson(81, 263)
    assert (round(interval.low, 4), round(interval.high, 4)) == (0.2553, 0.3662)
    interval = stats.wilson(0, 20)
    assert (round(interval.low, 4), round(interval.high, 4)) == (0.0, 0.1611)


def test_wilson_rejects_invalid_counts():
    with pytest.raises(ValueError):
        stats.wilson(5, 4)
    with pytest.raises(ValueError):
        stats.wilson(0, 0)


def test_exact_binomial_bound_reproduces_the_preregistered_value():
    # experimental-design.md §3: 0 failures in 990 cases -> p <= 0.302 % (one-sided 95 %).
    assert round(100 * stats.binomial_upper_bound(0, 990), 3) == 0.302
    # Closed form for zero failures: 1 - 0.05 ** (1 / 20) = 0.1391.
    assert round(stats.binomial_upper_bound(0, 20), 4) == 0.1391
    # One failure in 20: Clopper-Pearson one-sided 95 % upper bound is 0.2161.
    assert round(stats.binomial_upper_bound(1, 20), 4) == 0.2161
    assert stats.rule_of_three(990) == pytest.approx(3 / 990)


def test_cluster_bootstrap_resamples_clusters_not_units():
    clusters = {"a": [0.0, 0.0], "b": [1.0, 1.0]}
    result = stats.cluster_bootstrap(clusters, stats.mean, replicates=200, seed=7)
    assert result.estimate == 0.5
    assert set(result.replicates) <= {0.0, 0.5, 1.0}
    assert result.interval.low == 0.0 and result.interval.high == 1.0
    again = stats.cluster_bootstrap(clusters, stats.mean, replicates=200, seed=7)
    assert again == result
    other = stats.cluster_bootstrap(clusters, stats.mean, replicates=200, seed=8)
    assert other.replicates != result.replicates


def test_cluster_bootstrap_degenerates_on_identical_clusters():
    result = stats.cluster_bootstrap({"a": [0.5], "b": [0.5], "c": [0.5]}, stats.mean, replicates=50, seed=1)
    assert result.interval == stats.Interval(0.5, 0.5)


def test_sign_test_exact_two_sided():
    # Nine positive differences of eleven non-zero: p = 2 * (C(11,9)+C(11,10)+C(11,11)) / 2^11 = 134/2048.
    result = stats.sign_test([1, 2, 3, 4, 5, 6, 7, 8, 9, -1, -2, 0])
    assert (result.positive, result.negative, result.ties) == (9, 2, 1)
    assert result.p_value == pytest.approx(134 / 2048)
    assert stats.sign_test([0, 0]).p_value == 1.0
    assert stats.sign_test([1, 1, 1, 1]).p_value == pytest.approx(2 / 16)


def test_holm_step_down_adjustment():
    # Holm (1979): sorted p (0.01, 0.03, 0.04) with m = 3 -> 0.03, 0.06, 0.06 after monotone enforcement.
    assert stats.holm([0.01, 0.04, 0.03]) == (0.03, 0.06, 0.06)
    assert stats.holm([0.5, 0.9]) == (1.0, 1.0)
    with pytest.raises(ValueError):
        stats.holm([1.5])


def test_clopper_pearson_closed_forms_at_zero_and_full_success():
    # Two-sided 95 %: each tail 2.5 %. 0/20 -> (0, 1 - 0.025 ** (1/20)) = (0, 0.1684); 20/20 is its mirror image.
    interval = stats.clopper_pearson(0, 20)
    assert (round(interval.low, 4), round(interval.high, 4)) == (0.0, 0.1684)
    interval = stats.clopper_pearson(20, 20)
    assert (round(interval.low, 4), round(interval.high, 4)) == (0.8316, 1.0)
    with pytest.raises(ValueError):
        stats.clopper_pearson(3, 2)


def test_clopper_pearson_two_sided_contains_the_one_sided_bound_and_is_symmetric():
    # Exact interval by bisection on the binomial tails: 81/263 -> (0.2527, 0.3676), wider than Wilson's
    # (0.2553, 0.3662) and containing the one-sided 95 % upper bound on the same count.
    exact = stats.clopper_pearson(81, 263)
    low, high = exact.low, exact.high
    assert (round(low, 4), round(high, 4)) == (0.2527, 0.3676)
    wilson = stats.wilson(81, 263)
    assert low < wilson.low and high > wilson.high
    assert high >= stats.binomial_upper_bound(81, 263)
    mirror = stats.clopper_pearson(263 - 81, 263)
    assert round(mirror.low, 6) == round(1 - high, 6) and round(mirror.high, 6) == round(1 - low, 6)


def test_cluster_bootstrap_rejects_a_confidence_outside_the_open_unit_interval():
    """E26: confidence = -1 returned an inverted interval instead of an error."""
    import pytest

    from pfc2_eval import stats

    for confidence in (-1.0, 0.0, 1.0, 1.5):
        with pytest.raises(ValueError):
            stats.cluster_bootstrap({"a": [0.0], "b": [1.0]}, stats.mean, seed=0, confidence=confidence)
    assert stats.cluster_bootstrap({"a": [0.0], "b": [1.0]}, stats.mean, seed=0, confidence=0.9).interval.low <= 0.5


def test_percentile_interval_uses_the_order_statistics_of_a_small_bootstrap():
    """stats-206/208: with ten replicates at 95 % the limits are the smallest and the largest replicate."""
    from pfc2_eval import stats

    result = stats.cluster_bootstrap({"a": [0.0], "b": [1.0], "c": [0.25]}, stats.mean, seed=7, replicates=10)
    ordered = sorted(result.replicates)
    # tail = 0.025: low index int(0.25) = 0, high index int(9.75) = 9.
    assert (result.interval.low, result.interval.high) == (ordered[0], ordered[9])
    assert len(stats.cluster_bootstrap({"a": [0.0], "b": [1.0]}, stats.mean, seed=0).replicates) == 2000
