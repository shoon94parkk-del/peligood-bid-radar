# Peligood Bid Radar agent rules

This repository is a research/output radar for bid opportunities relevant to Peligood. The repository must preserve research provenance, not only the visible card list.

## Read before editing
1. `docs/project-memory.md`
2. `docs/regression-guardrails.md`
3. `docs/decision-log.md`
4. Latest `data/YYYY-MM-DD.json`
5. `index.html`

## Required workflow
1. Search broadly by task meaning, not only literal VR/AR/metaverse keywords.
2. For every actionable bid/pre-spec item, preserve the official notice URL when verified.
3. If the official deep link is not independently verified, preserve the actual discovery/detail URL used to find the notice; never invent a URL.
4. Keep lifecycle (`bid`, `pre-spec`, `watch`, `plan`) explicit.
5. Do not present a historical recurring-pattern watch as a currently actionable bid.
6. Preserve notice number/source/deadline type/provenance fields in research JSON.
7. Run `node scripts/validate-project.mjs` before publishing.
8. Append decision history when search scope, lifecycle rules, URL policy, ranking, or UI behavior changes.

## Never regress
- Product is "입찰할 수 있는 공고", not G2B-only.
- Hidden candidates may come from education content, immersive media, digital twin, AI content, exhibition, 3D/virtual training, etc.
- URL/provenance is mandatory for actionable entries.
- Official URL is preferred; real discovery URL is acceptable when official detail cannot be verified.
- Do not fabricate suitability, deadlines, qualifications, or official links.
- Default dashboard remains deadline-oriented and mobile-readable.

## Required missed-bid recovery checks (2026-10-15)
- Every daily scan MUST search exact titles plus new procurement IDs for every `watch` and tracked pre-spec/plan on the original procurement platform; include KEPCO SRM / 한전전자조달 and public discovery mirrors, not just G2B. A Watch with a verified new active notice MUST be promoted to `bid` and the old Watch must not remain as a duplicate.
- Independently search non-XR titles for 3D modeling, animation, digital education and video content on university/institution/private G2B and open company RFP channels. Preserve low-fit records in conditional research instead of omitting them silently.
- Check current notice amendments/cancellation and all meaningful deadline types; do not infer that an earlier notice is active from search snippets alone.
- Technical-specification-plus-price simultaneous bids are NOT price-only bids. Preserve explicit evaluation/selection mechanics and never claim presentation is mandatory based only on an attachment named `presentation`.
- Compare procurement summary metadata with attached tender PDFs/text; if issuer name, submission deadline, or bidder eligibility contradict, flag for issuer verification rather than treating the copied boilerplate as settled truth.
- Explicitly list newly discovered, confirmed no-longer-actionable, and unverifiable candidates, with exact source URLs; do not claim full-market completeness from search results.
