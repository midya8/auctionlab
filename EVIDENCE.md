# Reproduction evidence

Measured locally November 10, 2026. These are bounded developed controls and seeded synthetic checks, not held-out evaluation or production performance claims.

| Check | Measured result |
|---|---|
| Python tests | 24 tests |
| Developed controls | 16 |
| Complete report replay corpus | 52 profiles, 1,997 allocations, 163 efficient outcomes, 272 coalition rows, 752 menu entries |
| Explicit-report corpus | 349 reports, 1,394 reported-optimal outcomes |
| Primitive report tampering | 1,204 forgeries rejected |
| Two-good finite type exhaustion | 196 two-bidder profiles; all14 monotone valuation rows over0..2 as each unilateral report; 5,488 reports,12,348 reported-optimal outcomes checked |
| JavaScript tests | 3 tests; complete equality with all52 Python reports, 1,204 primitive forgeries rejected |
| Independent HiGHS bundle reference | 1,024 integer solves, 5,530 constraint rows, zero objective discrepancy at1e-8 tolerance; SciPy1.15.3 |
| Clean wheel reproduction | Six installed module origins, 16 controls, two entrypoints, 32 CLI tamper rejections |
| Actual Chrome | 48 responsive views across1440/768/390px;1,581 selected allocation states;636 menu entries;312 coalition rows;3,441 deviation outcome rows |
| Native Chrome downloads | All16 inputs and16 certificates; actual downloaded certificates independently replayed by Python |
| Visual evidence | 30 captures; desktop hero/core and mobile allocation/menu/deviation pixels inspected |

The report corpus uses three seeded profiles for each combination of1..4 items and1..3 bidders, plus16 developed controls. No fixtures were held out. The browser corpus is the16 controls at3 widths and compares rendered cells against Python results, not its own browser report. Input edits and invalid analysis clear stale evidence and disable downloads. Empty supplied-report lists display an explicit no-audit state.

The Python and browser tests also cover ties, zero values, single-good second price, one-bidder zero externality, menu independence from own report, utility/revenue conservation, scaled values, bidder/item relabeling, strict schema, malformed JSON, booleans/floats, duplicate keys, CLI input bounds and independent verifier imports. Browser download checks include a transport-completion wait and a1.1s inter-download pause; no inference assertion is retried.

Run the commands in README to reproduce. Public native source, CI, Pages and all portfolio showcase checks remain pending in this local snapshot.
