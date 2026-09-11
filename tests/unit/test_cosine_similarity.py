import math

from ftm_kpe.legacy.cosine_similarity import get_cosine


def test_identical_text_has_unit_similarity() -> None:
    assert math.isclose(get_cosine("fuzzy topic model", "fuzzy topic model"), 1.0)


def test_disjoint_text_has_zero_similarity() -> None:
    assert get_cosine("fuzzy", "graph") == 0.0
