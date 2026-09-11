import numpy as np

from ftm_kpe.legacy.owa import generate_owa_weights, owa_aggregation, std_quantifier_feng


def test_feng_weights_form_a_partition() -> None:
    weights = generate_owa_weights(5, std_quantifier_feng)

    assert np.all(weights >= 0)
    assert np.isclose(weights.sum(), 1.0)


def test_owa_preserves_constant_values() -> None:
    result = owa_aggregation([0.4, 0.4, 0.4, 0.4], quantifier="feng")

    assert np.isclose(result[0], 0.4)
