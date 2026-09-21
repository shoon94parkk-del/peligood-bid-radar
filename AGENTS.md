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
