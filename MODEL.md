# Model and certificate semantics

Let N be bidders and G be items. A feasible allocation assigns each item to a bidder or leaves it with the seller. Bundles T_i are disjoint. The input provides every v_i(T), normalized at v_i(empty)=0, monotone, nonnegative and integral. Utility is v_i(T_i)-p_i. Seller value/reserve is zero.

## Allocation and pivot prices

W(S) is maximum sum of reported values over allocations using only bidders S. The complete certificate includes every maximizing ownership ID for every subset S, not just the first optimum. IDs are lexicographic base-(n+1) owner vectors, with owner 0 for the seller and owner (i+1) for bidder i.

For every efficient allocation x, bidder i pays:

`p_i = W(N\{i}) - sum_{j != i} v_j(T_j)`.

Truthful utility is therefore `u_i = W(N)-W(N\{i})`. It is nonnegative because removing i cannot improve the optimum. Price is nonnegative because the chosen others' allocation is feasible without i; it is at most i's assigned value by optimality of W(N). Utilities and revenue `R=W(N)-sum_i u_i` are tie-invariant, even when the per-bidder price vectors are not. No price is applied to non-efficient allocation witnesses.

## Report-independent bundle menus

For each i and each bundle T, let H_i(G\T) be maximum welfare of other bidders on the unreserved items. The menu price is `q_i(T)=W(N\{i})-H_i(G\T)`. Both terms use others' reports only. Every remaining-goods optimum witness is retained.

For every T, `v_i(T)+H_i(G\T)<=W(N)`. Thus `v_i(T)-q_i(T)<=u_i`. Equality holds for every bundle assigned to i in an efficient allocation, and each maximizing menu bundle can occur in an efficient allocation. The certificate checks this entire finite bundle menu.

## Seller-inclusive cooperative core

A coalition with the seller and bidders S has value W(S). Its current total payoff is `R+sum_{i in S}u_i`. Slack is payoff minus value. Deficit is max(0,-slack). The certificate reports every S, every deficit and every blocking subset. The full coalition has slack 0 by conservation. Coalitions without the seller own no goods, have value 0 and cannot block the nonnegative truthful bidder utilities. This statement relies on the zero-reserve seller-ownership model.

A positive deficit is a cooperative transferable-utility blocking witness. It does not supply an actual bidding strategy, equilibrium, self-enforcing coalition, budget-feasible deviation or collusion plan. Core auditing is not core-selecting payment design.

## Explicit unilateral reports

For each supplied report by i, keep all other values fixed. Enumerate every allocation maximizing the modified reported welfare. Compute the same externality price, then true utility using original v_i. Compare every resulting tie with truthful u_i, recording the worst/best utility gain. Under these assumptions, the general VCG truthfulness theorem predicts no positive gain. The implementation only checks supplied reports. An empty report list means no reports were tested, not proof of immunity.

## Verification architecture

Python generation enumerates ownership vectors. The independently implemented verifier imports only the input model and instead enumerates disjoint bundle products, derives ownership IDs and recomputes every field recursively with exact non-boolean integer types. Missing, reordered, duplicated or extra evidence is rejected. Input is carried inside each certificate; verification establishes consistency with that input, not authenticity of the input's economic truth.

JavaScript generation/replay changes census representation but shares evidence construction. Cross-language complete-report equality supplements the independent Python replay. Optional HiGHS binary bundle solves cross-check every coalition and menu welfare subproblem, with explicit integer and item-feasibility checks, not just solver success.

Certificates are not cryptographic signatures or formal proofs. Exhaustive enumeration is bounded at 256 ownership allocations; independently replaying small finite evidence is not a claim to solve large winner-determination problems.
