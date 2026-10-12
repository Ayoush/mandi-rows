"""Tests for commodity alias resolution."""
from mandi_rows.alias import resolve_commodity


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
