# AuctionLab

**Truthful alone. Not protected together.**

An exact finite laboratory for multiagent combinatorial allocation, Vickrey-Clarke-Groves (VCG) prices, report-independent bundle menus and seller-coalition core deficits. Synthetic private values, no actual auctions or money.

## The developed teaching contrast

Two items, three bidders. Values are indexed by bundle bitmask: empty, A, B, AB.

| Bidder | Empty | A | B | AB |
|---|---:|---:|---:|---:|
| B1 | 0 | 0 | 0 | 10 |
| B2 | 0 | 6 | 0 | 6 |
| B3 | 0 | 0 | 6 | 6 |

Give A to B2 and B to B3: welfare **12**. Without either winner, welfare is **10**; the other winner contributes **6**. Each winner therefore pays **4**, giving seller revenue **8** and utilities **[0,2,2]**.

The seller together with B1 can generate **10**, yet their current combined payoff is **8**. The resulting cooperative-core deficit is **2**. This does not contradict individual dominant-strategy truthfulness. The example is a developed numerical variation of the established bundle-versus-singletons pattern, not a new counterexample.

Change B1's row to `[0,5,5,10]`: welfare stays 12, revenue becomes 10 and the deficit disappears in this control. This numerical contrast is not a theorem about all complement/substitute valuation classes.

## Inspectable evidence

- Every feasible ownership vector, with seller-retained goods allowed.
- Every welfare-maximizing tie, without outcome cherry-picking.
- Every bidder's optimum-without-bidder witness and pivot-price arithmetic.
- Every seller-inclusive coalition and its value, current payoff, slack and deficit.
- Every bundle's report-independent price menu and truthful utility.
- Every reported-optimal tie for each explicitly supplied unilateral report, scored using true values.
- Strict JSON inputs, complete certificates, independently implemented Python disjoint-bundle replay, and browser-side downloads.

The browser uses an ownership census for generation and a disjoint-bundle census for replay, but shares evidence construction between them. It is not a second independent mechanism implementation. The Python verifier is implemented separately and does not import the generator.

## Run locally

Python 3.10+ and Node 22+. Runtime is Python standard library and dependency-free browser JavaScript.

```sh
python -m auctionlab demo > /tmp/auctionlab-certificate.json
python -m auctionlab verify /tmp/auctionlab-certificate.json
python -m auctionlab run examples/truthful_not_in_core.json
python -m unittest discover -s tests -v
node --test tests/test_engine.cjs
python -m pip install setuptools wheel
python tools/check_installed.py
python -m http.server 8000 --directory docs
```

Open localhost:8000 for the explorer. Real Chrome tests start their own server and isolated browser profile:

```sh
CHROME_BIN=google-chrome node --test tests/test_browser.cjs
```

Optional independent integer-program reference:

```sh
python -m pip install scipy==1.15.3
python tools/check_milp.py
```

The reference constructs binary bidder/bundle variables and item/bidder constraints from each input. It recomputes all coalition optima and every remaining-goods menu subproblem with HiGHS. No answer-derived coefficients, selected-only optimum, or relaxed integrality.

## Model boundary

At most 4 items and 3 bidders. Complete monotone nonnegative integer valuations in 0..100, empty-bundle value zero, free disposal, zero seller reserve and quasilinear private-value utility. Each bidder supplies at most 6 alternative complete report rows. No learned valuations, budgets, common values, false names, collusion audit, actual bidding, core-selecting payment rule, practical market advice or deployment-scale benchmark.

The 16 controls are developed teaching fixtures, not held-out data. Finite selected reports do not establish universal truthfulness. The test suite separately exhausts all 196 two-bidder profiles over the 14 monotone two-good value rows with entries 0..2, testing all 14 report types per bidder in schema-valid batches. That is an explicitly bounded type universe, not all possible valuations.

All efficient ties are retained. Truthful utilities and seller revenue are tie-invariant; bidder payment vectors may differ. See [MODEL.md](MODEL.md) for definitions and derivations, [EVIDENCE.md](EVIDENCE.md) for measured checks and [SOURCES.md](SOURCES.md) for provenance.

## Publication checks

Reproduction results describe bounded checks, not a claim about the latest deployment. Inspect the current commit and its [native workflow results](https://github.com/midya8/auctionlab/actions) before relying on publication status. The implementation does not interact with actual auctions or payments.

MIT licensed. Established mechanism theory is credited separately; no first-implementation or new-theorem claim.
