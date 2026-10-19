# Market and state validation

`check_rows()` flags a known market assigned to an unexpected state with
`MARKET_STATE_MISMATCH`. For example, `Azadpur` in `Maharashtra` produces a flag
on `state`; `Azadpur` in `Delhi` does not. This is a non-fatal flag, so `result.ok`
still depends only on errors. The CLI includes it in text and JSON output.

The lookup in `data/known_markets.json` maps market names to expected states.
Matching ignores case and leading/trailing whitespace in both fields. Unknown
markets (including blank names) are skipped. Spelling variants, abbreviations,
and suffixes are not guessed: `Dahod APMC` and `Dahod` are different names.
This is a partial plausibility check, not proof that a row's location is valid.

## Sources and maintenance

The initial mappings were checked on 2026-10-17 against:

- [eNAM's state/district/mandi table](https://enam.gov.in/aspirational-districts),
  selecting markets in Assam, Bihar, Chhattisgarh, Gujarat, Jharkhand, and Odisha.
- [APMC Azadpur's official site](https://www.apmcazadpurdelhi.com/home/index)
  for Azadpur, Delhi.

Names retain the source's spelling and APMC suffix where present. Entries use
title case for display. The list deliberately omits some generic or ambiguous
names, such as Ramgarh and Junagarh. Market names can recur in different states;
only add a single-state mapping after checking for ambiguity. Remove a mapping
if the same name is found in multiple states rather than rejecting valid rows.
District-based disambiguation is outside this validator's scope.

To extend coverage, add a market/state pair to the JSON, cite its official source
here, and test both the expected state and a mismatch. Keep the file a flat
string-to-string mapping without metadata entries. No network access is needed
at runtime. The wheel bundles the lookup; editable installs read the repository
copy. Rebuild/restart after modifying the data because the lookup is cached.

## Key mandis by state

Notable mandis in Maharashtra, Karnataka, Uttar Pradesh, Punjab and Rajasthan, plus Azadpur in Delhi, with the commodities each is known for. These are general descriptions to help readers find their way around. They are not the lookup data used by the validator described above, and the Known For and Notes columns have not been checked against an official source.

| Market | State | Known For | Notes |
|--------|-------|-----------|-------|
| Vashi | Maharashtra | Fruits, vegetables, onion, potato | Mumbai; the largest APMC in the state |
| Lasalgaon | Maharashtra | Onion | Nashik district; major onion market |
| Pune | Maharashtra | Vegetables, fruits, onion, potato | Main market yard serves the Pune region |
| Sangli | Maharashtra | Turmeric, jaggery, grapes | Major turmeric trading centre |
| Latur | Maharashtra | Soybean, pulses (tur) | Key oilseed and pulse market in Marathwada |
| Yeshwanthpur | Karnataka | Vegetables, onion, potato, tomato | Located in Bengaluru |
| Byadgi | Karnataka | Dry red chilli | Haveri district; known for Byadgi chilli |
| Hubballi | Karnataka | Cotton, chilli, onion, pulses | Dharwad district; major trading centre in north Karnataka |
| Davangere | Karnataka | Maize, cotton, areca nut | Central Karnataka trading hub |
| Raichur | Karnataka | Paddy, cotton, pulses | Northeast Karnataka; rice-growing region |
| Agra | Uttar Pradesh | Potato, vegetables | Major potato trading centre |
| Lucknow | Uttar Pradesh | Fruits, vegetables, mango | State capital; mango belt of Malihabad is nearby |
| Kanpur | Uttar Pradesh | Wheat, pulses, grain | Major grain trading centre |
| Muzaffarnagar | Uttar Pradesh | Jaggery (gur), sugarcane products | Known as a major jaggery trading hub |
| Hapur | Uttar Pradesh | Wheat, grain | Important grain market in western UP |
| Khanna | Punjab | Wheat, paddy | Major grain market in Ludhiana district |
| Ludhiana | Punjab | Wheat, paddy, vegetables | Main market yard of the district |
| Amritsar | Punjab | Wheat, paddy, vegetables | Major trading centre in the Majha region |
| Abohar | Punjab | Kinnow, cotton | Known for kinnow (citrus) production |
| Bathinda | Punjab | Cotton, wheat | Important cotton market in the Malwa region |
| Kota | Rajasthan | Coriander, soybean, wheat | Major trading centre in the Hadoti region |
| Jaipur (Muhana) | Rajasthan | Fruits, vegetables | Main fruit and vegetable market of Jaipur |
| Jodhpur | Rajasthan | Bajra, guar, moong, chilli | Trading centre for crops of the Marwar region |
| Alwar | Rajasthan | Mustard, wheat | Known for mustard trading |
| Sri Ganganagar | Rajasthan | Kinnow, cotton, mustard, wheat | Canal-irrigated farming belt in northern Rajasthan |
| Azadpur | Delhi | Fruits, vegetables, onion, potato | Asia's largest vegetable market |
