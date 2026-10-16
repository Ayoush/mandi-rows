# Agmarknet Commodities and Data Source

## Data source

Agmarknet (Agricultural Marketing Information Network) publishes agricultural
market information, including daily commodity prices across markets in India.

The public dataset is available through the Government of India's Open
Government Data Platform:

[Current Daily Price of Various Commodities from Various Markets (Mandi)](https://data.gov.in/catalog/current-daily-price-various-commodities-various-markets-mandi)

The full historical dump is an external dataset. It is listed in
`registry/files.json` as `agmarknet-bulk` with status `not-downloaded`.
This repository instead uses frozen CSV snapshots for reproducible,
offline validation and testing.

## CSV structure

Agmarknet CSV exports contain market-level observations of commodities and
their prices. Depending on the export, fields can describe the reporting date,
state, district, market, commodity, variety, grade, arrivals, and minimum,
maximum, or modal price.

Column names and availability can vary between exports. Check the actual
header row before processing a downloaded file, and consult
[Agmarknet CSV Columns](columns.md) for this repository's expected column
schema.

Real-world files may contain data-quality issues such as missing prices,
prices formatted with thousands separators (for example, `1,250`), UTF-8 BOM
headers, or duplicate market-day rows. The project includes loading,
normalization, and validation logic to help identify these issues.

## Check a CSV file

Run the checker from the repository root:

```bash
python -m mandi_rows.cli check path/to/your-file.csv
```

For example, to check a bundled market snapshot:

```bash
python -m mandi_rows.cli check spec/markets/indore-wheat.csv
```

The checker reports the file, row count, and any detected flags. Use a path
to a CSV file that exists locally; the command does not download the external
dataset automatically.

## Common commodity categories

Examples of common categories represented in agricultural market data include:

- **Cereals:** wheat, rice, maize
- **Pulses:** gram, lentil, pigeon pea
- **Vegetables:** potato, onion, tomato
- **Oilseeds:** mustard seed, soybean, groundnut
- **Spices:** turmeric, chilli, cumin

These are illustrative examples, not a complete or authoritative classification
of every commodity in the Agmarknet catalogue.
