# Theory and prior work

AuctionLab implements known mechanism theory for inspection. It does not invent VCG, the core deficit example, the menu characterization, independent verification, or winner determination.

- [Avrim Blum, lecture14, scribe Hsu-Chun Hsiao, February28,2013](https://www.cs.cmu.edu/~arielpro/15896/docs/notes14.pdf): externality/pivot-price formula and truthful utility derivation.
- [Tim Roughgarden, Lectures on Combinatorial Auctions,2005](https://theory.stanford.edu/~tim/f05/ca.pdf): complete bundle valuations, quasilinear utility, efficient allocation, VCG truthfulness and computational limits.
- [Combinatorial Auctions and the VCG Mechanism, university lecture handout](https://pages.cs.wisc.edu/~shuchi/courses/880-S11/handouts/2.pdf): corroborating definitions and mechanism exposition.
- [Lawrence M. Ausubel and Paul Milgrom, The Lovely but Lonely Vickrey Auction](https://milgrom.people.stanford.edu/wp-content/uploads/2005/12/Lovely-but-Lonely-Vickrey-Auction-072404a.pdf): classical bundle-versus-singletons examples, VCG weaknesses, seller-inclusive coalitional values and core definitions. The default10/6/6 numbers are a developed numerical variation of that established pattern. We do not claim a new counterexample.
- [Vincent Conitzer and Tuomas Sandholm, Failures of the VCG Mechanism in Combinatorial Auctions and Exchanges, AAMAS2006](https://www.cs.cmu.edu/~conitzer/vcgfailuresAAMAS06.pdf): individual truthfulness is distinct from revenue guarantees and collusion immunity. No collusion search is implemented here.
- [Robert Day and Paul Milgrom, Core-selecting package auctions, accepted2007](https://milgrom.people.stanford.edu/wp-content/uploads/2008/06/Core-Selecting-Package-Auctions.pdf): coalitional formulation and boundary with core-selecting mechanisms. AuctionLab audits VCG; it does not implement a core-selecting mechanism.
- [Caminati, Kerber, Lange and Rowat, VCG - Combinatorial Vickrey-Clarke-Groves Auctions, Archive of Formal Proofs, April30,2015](https://isa-afp.org/entries/Vickrey_Clarke_Groves.html): existing formalization includes tie-breaking, well-defined allocation/prices and nonnegative-price results. AuctionLab is finite replay, not formal verification.
- [Existing Rust vcg-auction source](https://docs.rs/vcg-auction/latest/src/vcg_auction/vcg.rs.html): prior implementation, not a dependency or benchmark.

Sources reviewed November10,2026. Mathematical results are credited to their authors; all code, synthetic controls and UI in this project are developed implementation work. No empirical market evidence, commercial recommendation or scalability comparison is claimed.
