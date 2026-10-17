"""Tests for commodity alias resolution."""
from mandi_rows.alias import resolve_commodity, normalise_unit


def test_pyaz_resolves_to_onion():
    assert resolve_commodity("pyaz") == "Onion"


def test_aloo_resolves_to_potato():
    assert resolve_commodity("aloo") == "Potato"


def test_canonical_name_unchanged():
    assert resolve_commodity("Onion") == "Onion"


def test_unknown_name_unchanged():
    assert resolve_commodity("BlueberryXYZ") == "BlueberryXYZ"


def test_case_insensitive():
    assert resolve_commodity("Wheat") == "Wheat"
    assert resolve_commodity("WHEAT") == "Wheat"


def test_gehun_resolves_to_wheat():
    assert resolve_commodity("gehun") == "Wheat"


def test_normalize_quintal():
    assert normalise_unit("Quintal") == "Qtl"


def test_lower_case_quintal():
    assert normalise_unit("quintal") == "Qtl"


def test_normalize_Kg_unchanged():
    assert normalise_unit("Kg") == "Kg"


def test_normalize_qtls():
    assert normalise_unit("QTLS") == "Qtl"


def test_canonical_unit_unchanged():
    assert normalise_unit("Qtl") == "Qtl"


def test_unknown_unit_unchanged():
    assert normalise_unit("BlueberryXYZ") == "BlueberryXYZ"
