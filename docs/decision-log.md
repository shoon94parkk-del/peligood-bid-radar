# Peligood Bid Radar decision log

Append-only high-risk decisions.

## 2026-09-22 — Durable project memory
Added project-level research memory, provenance guardrails, and automatic validation so future scans do not fall back to narrow keyword-only or URL-less results.

## 2026-09-20 — Normalize lifecycle and URL validation
Bid, pre-spec and watch states were normalized. URL validation became a P0 because a useful candidate without traceable source/detail URL cannot be acted on or audited.

## 2026-09-20 — Product is broader than 나라장터
The UI was renamed/reframed as `입찰할 수 있는 공고`. G2B remains an important source but the radar is about actionable opportunities, not one portal.

## 2026-09-20 — Preserve discovery provenance
When a verified official pre-spec detail link is not available, keep the real page used during research instead of dropping the item or fabricating an official link.

## 2026-09-19 — Search by task meaning, not title keyword
The scan was expanded to hidden candidates: immersive/education content, AI content, digital twin, 3D/virtual training, exhibitions and adjacent software/content opportunities.

## 2026-09-19 — Deadline-first mobile dashboard
Default sorting prioritizes impending deadlines; mobile layout and sorting controls were aligned so the daily list can be used as an action queue.

## 2026-10-15 — Correct recurring-bid radar misses
Manual independent broad search found four live, absent tender records: SRM G142600030 VR SPACE follow-on (already a Watch but not promoted), private G2B 3D animation R26BK01757095, university e-learning R26BK01764404-001, and police museum video R26BK01759787. Added mandatory daily exact-title Watch lookup including non-G2B portals, broader 3D/video/e-learning searches and a metadata-versus-tender-doc conflict warning. Historical Watch may not be treated as no-current-opportunity without checking the institution's original portal and new bid numbers. Spec/price simultaneous bidding is not a price-only classification.
