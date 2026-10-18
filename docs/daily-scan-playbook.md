# Peligood Daily Bid Radar — Cross-source scan playbook
Updated: 2026-10-15 (Asia/Seoul)

## Scope and operating rules
Goal: minimize missed **actionable** opportunities, not maximize irrelevant keyword results. No public index or accessible API can guarantee discovery of all public, university, S2B, SRM and private tenders. Never state absolute coverage.

Before a scan read AGENTS.md, project-memory.md, regression-guardrails.md, decision-log.md, current data and dashboard. Record run time in KST and compare previous snapshot. Preserve previous research history rather than overwrite source evidence. Concurrent updates require re-fetching SHA and merging safely.

## Search matrix — complete all four channels independently
| Channel | Original channels | Complementary discovery | Required query groups |
| --- | --- | --- | --- |
| Public procurement | G2B full tender/corrections/cancellations, pre-spec/plan, **KEPCO SRM**, LH, D2B, rail, provincial portals, cultural and education agencies | Bidpro, SeenThis, Jodaln, auction/index mirrors | VR/XR + simulator/training + exhibition + 3D/digital twin + e-learning/video |
| Universities | Institution purchasing bulletins, industry academic units, RISE/LINC, hospitals, K-MOOC | G2B and open bid mirrors | 3D, animation, AI learning, VR lab, e-learning, simulation |
| School and education | S2B, education offices, elementary/secondary/vocational school bidding | Search indexed institution titles and dated notices | VR safety, training hardware, virtual sports, interactive exhibitions |
| Private / consortium | Publicly accessible G2B private buyers, corporations, hospitals, foundations, production studios, open corporate RFP | Bid mirrors, association bulletins | 3D modeling, voxel animation, museum video, motion graphics, training videos, content production |

Every track also searches literal terms, alternate spellings, task-oriented terms without XR, and issuer-name + task combinations. Never stop after one high-yield source. If an inaccessible channel is relevant, mark partial/blocked and record a concrete follow-up; do not represent it as checked exhaustively.

## Five independent keyword families
1. VR/AR/MR/XR, mixed/augmented reality, immersive, HMD, VR SPACE, 4D motion, metaverse, interactive experience
2. Safety, CPR, firefighting, industrial training, technical education, welding, painting, maintenance, simulator, equipment integration
3. 3D / voxel modeling, animation, keyframe, CGI, digital twin, virtual factory, spatial computing
4. Online education, e-learning, K-MOOC, AI/Science simulation, educational digital content
5. Museum/video/promo, exhibit/experience installation, motion graphics, virtual production, educational and corporate film

Filter bare GPUs, printers, stock software purchases and hardware without content-development/service work. Do not dismiss adjacent work merely for omitting the letters VR.

## P0: Every watch follows its issuer's original procurement system
For every active watch/pre-spec/plan and recently expired bid, search using BOTH the original ID and (issuer + exact/alternate/short task title), on the original procurement platform and independent discovery sources. Search at least the last 7 days; broaden corrections and re-bids to 30 days. Look for new IDs, cancellation/extension/failed award and revised deadlines. Promotion creates one new valid bid, removes the old watch from visible D, and preserves the lineage in data.lifecycleChanges. A missed item discovered retrospectively belongs in the missed-opportunities log for later evaluation. A negative query is 'not found via these channels at this time', never proof of nonexistence.

Prior failures that must not recur:
- KEPCO SRM G142600027 Watch failed to discover G142600030 new VR SPACE tender.
- Private G2B 3D animation, K-MOOC/video education and police museum filming missed when only XR words were searched.
- G2B R26BK01758442-000 was resurrected from stale indexed snippets despite its -001 cancelled amendment.
- A specification-and-price tender was incorrectly labelled price-only.
- Template tender files with conflicting dates/issuer were mistaken for definitive current bidding conditions.

## Verification gates
Record: actual noticeNo + amendment/sequence + issuer; publication, cancellation/amendment date; total funding and VAT versus estimate; bid deadline; registration, consortium, in-person proposal and presentation dates separately; scope, deliverables and fit; license/registration codes, geographic limits, direct-production certificate and subcontract/consortium rules; bidMethod and explicit award/evaluation mechanic; source URLs and evidence confidence. Require issuer original/RFP when accessible or independent corroboration; mark conflicts as conditional rather than active. Never infer a canonical G2B URL by a string pattern. Preserve an actually opened individual discovery URL if original is blocked.

Do not label '가격입찰만' when any mandatory scored technical/proposal stage exists. Specify pass/fail specification plus lowest price distinctly. Do not infer mandatory attendance from a file named 'presentation'. Record supplier eligibility as 'confirmed/needs verification/unlikely', not assumptions.

## Commit + Render acceptance
Write data/YYYY-MM-DD.json and index.html with the SAME active/watch set and status, keeping URL provenance, original UI and deadline-first mobile functionality. Run `node scripts/validate-project.mjs` and `node --test scripts/test-validator.mjs`; both must pass. GitHub Actions project-contract.yml must pass for the exact main SHA. With autoDeploy enabled do not trigger a redundant Render deploy; independently verify Render live SHA equals latest GitHub main SHA and fetch the public rendered HTML to confirm headline date, new cards, removed cards and filters. If delayed or failing, report saved/tested but not deployed. A successful GitHub test is not equivalent to a live deploy.

## Daily concise report
- Confirmed newly actionable tenders; missed and recovered compared with previous run, especially Watch -> new bid
- Deadlines within 3 days, including PRE-deadlines for registration and in-person proposals
- Removed canceled/expired/duplicate items, and conditional/not eligible candidates
- Four-channel coverage table (search path / candidates / new actionable / blocked)
- Active bids + watches, provenance source coverage and unresolved original-document conflicts
- GitHub SHA, CI conclusion, Render live SHA, observed site marker and one-click URLs

### 2026-10-19 supplementary missed 3D asset tender rule
Search private G2B buyers for `3D asset library`, `에셋 라이브러리`, `방송 3D`, `OBJ`, `FBX`, `GLB`, `PBR 텍스처`, `retopology`, `UV`, `3D 스캔 데이터`, and `CG 콘텐츠`, in addition to conventional VR/AR/모델링. On 2026-10-19 manual recheck uncovered S팩스페이스/스팩스페이스 R26BK01764536-000 (10/12 posted, 10/26 close, 205.7m KRW) missing from the earlier 4-channel scan. Verify issuer, per-item deliverables, restrictions, and technical vs price scoring; avoid promoting equipment-only matches (e.g. KISTI R26BK01775449).
