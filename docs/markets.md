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
