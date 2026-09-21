# Peligood Bid Radar project memory

Last updated: 2026-09-22

## Purpose
Find bid opportunities that Peligood could realistically investigate or join. The radar is broader than literal "VR/AR/metaverse" keyword matching and broader than 나라장터-only discovery.

## Search strategy already adopted
Search both direct and hidden/adjacent opportunity language:
- VR / AR / XR / metaverse / immersive content
- digital twin / virtual factory / 3D modeling
- virtual lab / simulation / experiential education
- digital/remote-learning content
- AI content / persona / media production
- exhibition/experience content
- education/training program content
- promotional video/content where production capability overlaps
- software/platform work when Peligood may participate through content/3D/UX or consortium roles

A title that lacks "VR" can still be highly relevant once the detailed task/RFP is read.

## Source/provenance policy
Every actionable item needs research provenance.

Preferred order:
1. verified official notice deep link
2. actual discovery/detail page used to find/verify the notice
3. a watch-only institutional pattern only when no active notice exists, clearly labeled as `watch`

Do not invent a deep link merely because a notice number exists.
When an official G2B bid deep link is verified, use it and keep `urlType=official`.
When an official pre-spec detail link cannot be independently verified, retain the actual discovery page and mark `urlType=discovery`.

## Lifecycle
Current normalized lifecycle values:
- `bid`: current bid notice
- `pre-spec`: pre-specification / advance notice
- `watch`: historical/repeating institution/project pattern, not a current bid
- `plan`: planned procurement where used

Lifecycle and deadline meaning must stay visible. A pre-spec opinion deadline is not the same as a bid-submission deadline.

## Data contract
Research payloads should retain, where applicable:
- title
- agency
- source
- amount/budget
- deadline
- deadlineType
- noticeType
- noticeNo
- lifecycle
- fit
- reason
- task
- qualification notes
- joint/consortium notes
- url
- urlType

These fields are part of the research asset, not expendable UI decoration.

## UI decisions
- Product heading: `입찰할 수 있는 공고`.
- Default orientation is deadline-first.
- Mobile layout remains readable with filter chips and sorting controls.
- Cards open details; the primary link goes to official notice when available.
- If only a discovery link is verified, label it as discovery/research provenance rather than "official".
- Watch items must be visually distinguishable from currently actionable bids.

## History of improvements
- Search expanded beyond VR keyword matches into broad content/digital-twin/AI/education/exhibition opportunities.
- Exact notice identifiers and official G2B deep links were corrected when verified.
- Discovery URLs were retained when official pre-spec deep links were not verified.
- Dashboard wording broadened from a G2B/VR-specific list to bid opportunities.
- Deadline sorting and mobile controls were added.
- P0 lifecycle normalization and URL validation were added.
- Daily research snapshots are stored under `data/`.

## Verification
Run:
`node scripts/validate-project.mjs`

It verifies durable project-memory files and current research JSON provenance fields.
