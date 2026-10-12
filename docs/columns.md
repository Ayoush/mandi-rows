# Column dictionary

Mandi price CSV files follow the Agmarknet export format. The columns mandi-rows works with are:

| Column | Type | Description | Null policy |
|--------|------|-------------|-------------|
| `State` | string | Indian state name | Required |
| `District` | string | District name | Required |
| `Market` | string | Mandi/market name | Required |
| `Commodity` | string | Crop or product name | Required |
| `Variety` | string | Crop variety | Optional |
| `Grade` | string | Quality grade | Optional |
| `Arrival_Date` | date | Date of price record (DD/MM/YYYY) | Required |
| `Min_Price` | number | Minimum price in ₹/quintal | Required if Modal missing |
| `Max_Price` | number | Maximum price in ₹/quintal | Required if Modal missing |
| `Modal_Price` | number | Modal (most common) price in ₹/quintal | Required |

**Sample row:**

```
Maharashtra,Pune,Pune,Onion,Other,FAQ,15/04/2024,800,1200,1000
```
