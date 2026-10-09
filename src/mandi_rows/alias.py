"""Commodity name alias resolution."""

# Maps alternate commodity names to canonical Agmarknet names.
# Keys are lowercase for case-insensitive lookup.
COMMODITY_ALIASES: dict[str, str] = {
    # Cereals
    "wheat": "Wheat",
    "gehun": "Wheat",
    "rice": "Rice",
    "paddy": "Paddy(Common)",
    "paddy common": "Paddy(Common)",
    "paddy(common)": "Paddy(Common)",
    "maize": "Maize",
    "corn": "Maize",
    "jowar": "Jowar(Sorghum)",
    "sorghum": "Jowar(Sorghum)",
    "bajra": "Bajra(Pearl Millet/Cumbu)",
    "pearl millet": "Bajra(Pearl Millet/Cumbu)",
    # Pulses
    "tur": "Tur Dal(Arhar Dal)",
    "arhar": "Tur Dal(Arhar Dal)",
    "toor dal": "Tur Dal(Arhar Dal)",
    "chana": "Gram(Chana)(Whole)",
    "gram": "Gram(Chana)(Whole)",
    "chickpea": "Gram(Chana)(Whole)",
    "moong": "Moong Dal",
    "green gram": "Moong Dal",
    "urad": "Black Gram Dal(Urd Dal)",
    "black gram": "Black Gram Dal(Urd Dal)",
    # Vegetables
    "onion": "Onion",
    "pyaz": "Onion",
    "kanda": "Onion",
    "tomato": "Tomato",
    "tamatar": "Tomato",
    "potato": "Potato",
    "aloo": "Potato",
    "garlic": "Garlic",
    "lahsun": "Garlic",
    # Oilseeds
    "mustard": "Mustard",
    "sarson": "Mustard",
    "groundnut": "Groundnut",
    "peanut": "Groundnut",
    "soybean": "Soya Bean",
    "soya": "Soya Bean",
    "sunflower": "Sunflower Seed",
    # Spices
    "turmeric": "Turmeric",
    "haldi": "Turmeric",
    "chilli": "Dry Chillies",
    "red chilli": "Dry Chillies",
    "coriander": "Coriander(Leaves)",
    "dhania": "Coriander(Leaves)",
}


def resolve_commodity(name: str) -> str:
    """Return the canonical commodity name, or input unchanged if not an alias."""
    return COMMODITY_ALIASES.get(name.strip().lower(), name)
