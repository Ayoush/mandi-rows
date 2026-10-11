**# Column dictionary

Mandi price CSV files follow the Agmarknet export format. This document describes the columns supported by mandi-rows, including their data types, meanings and example values:

## Required columns

| Column | Type | Description | Example |
|--------|------|-------------|-------------|
| `State` | string | Indian state name | Maharashtra |
| `District` | string | District name | Pune |
| `Market` | string | Mandi/market name | Pune |
| `Commodity` | string | Crop or product name | Onion |
| `Variety` | string | Crop variety | Other |
| `Arrival_Date` | date | Date of price record (DD/MM/YYYY) | 15/04/2024 |
| `Min_Price` | number | Minimum price in ₹/quintal | 800 |
| `Max_Price` | number | Maximum price in ₹/quintal | 1200 |
| `Modal_Price` | number | Modal (most common) price in ₹/quintal | 1000 |

## Optional Column

| Column | Type | Description | Example |
| `Grade` | string | Grade Quality of commodity | FAQ |
| `Unit` | string | Unit of measurement | Quintal |
| `Arrival_in_Qtl` | float | Quantity of commodity that arrived, measured in quintals | 125.5 |

**Sample row:**

```
Maharashtra,Pune,Pune,Onion,Other,FAQ,15/04/2024,800,1200,1000
```
**Note:** `Modal_Price` is the most common price at which transactions occurred. It is not necessarily the average of the minimum and maximum prices.