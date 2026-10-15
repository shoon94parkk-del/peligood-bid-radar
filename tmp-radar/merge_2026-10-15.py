#!/usr/bin/env python3
"""2026-10-15 Peligood Bid Radar merge script.
- index.html const D: remove 4 expired, set all n=0, update R26BK01759430-000, add new R26BK01758442-000
- write data/2026-10-15.json snapshot
"""
import json, re, datetime

REPO = "/home/hatch/workspace/peli"
HTML = REPO + "/index.html"

html = open(HTML, encoding="utf-8").read()
start = html.find("const D=") + len("const D=")
end_anchor = html.find("for(const x of D)")
assert start > 0 and end_anchor > start, "D array not found"
arr_text = html[start:end_anchor].strip()
assert arr_text.endswith("];"), f"unexpected array end: {arr_text[-10:]!r}"
D = json.loads(arr_text[:-1])  # drop trailing ';'
print("loaded records:", len(D))

EXPIRED = {"R26BK01740633-000", "R26BK01752627-000", "JJU-2026-112", "R26BK01755549-000"}
removed = [r for r in D if r.get("noticeNo") in EXPIRED]
kept = [r for r in D if r.get("noticeNo") not in EXPIRED]
print("removed:", [r["noticeNo"] for r in removed])
assert len(removed) == 4, f"expected 4 expired, got {len(removed)}"

for r in kept:
    r["n"] = 0

# --- update R26BK01759430-000 ---
for r in kept:
    if r.get("noticeNo") == "R26BK01759430-000":
        r["why"] = ("10/6 구공고 R26BK01740811(2.2억원) 취소 후 10/7 유효 공고 R26BK01759430(2.4억원)으로 게시. "
                    "[10/15 확인] R26BK01758442-000(2,182만원, 10/19 마감)은 kimkj 2차 정보상 유효한 별도 소규모 공고로 별도 등록 — 원문 대조 미완. "
                    "EV 정비 교육용 디지털트윈 콘텐츠 과업으로 인접적합.")
        r["previousNoticeNo"] = "R26BK01740811-001 (취소)"
        r["bidMethodEvidence"] = (r.get("bidMethodEvidence", "") +
            " [10/15] 제안요청서(bmap 호스팅) 추가 확인: 사업명 'AI 기반 디지털트윈 EV 정비 교육용 콘텐츠 개발'(첨단분야 혁신융합대학사업·국민대 미래자동차사업단), "
            "용역예산 240,000,000원(부가세 포함), 기술평가 90%+가격평가 10% — '제안서 필수' 확정.")

# --- new record: R26BK01758442-000 ---
new_rec = {
    "source": "나라장터(G2B) / kimkj.com AI 게시판 2026-10-07 회차",
    "amount": "2,181만 8,182원",
    "url": "https://kimkj.com/ai-board/?mod=document&uid=18106",
    "urlType": "discovery",
    "lifecycle": "bid",
    "noticeNo": "R26BK01758442-000",
    "d": "2026.10.19 10:00",
    "deadlineType": "입찰마감",
    "noticeType": "입찰공고",
    "title": "AI기반 디지털트윈 EV 정비 교육용 콘텐츠 제작(수정)",
    "a": "국민대학교 산학협력단",
    "task": "AI-디지털트윈 기반 EV 정비 교육 콘텐츠 제작",
    "why": "10/6 게시 별도 소규모 공고(2,182만원)로 10/15 2차 정보(kimkj) 확인 시 유효. 동일 사업 대규모 공고 R26BK01759430-000(2.4억원)과 별도 건. EV 정비 교육용 디지털트윈 콘텐츠 과업으로 인접적합.",
    "f": "보통",
    "q": "확인 필요 — 2차 정보(kimkj)만 확인, 공고문 원문 미확인",
    "j": "확인 필요 — 원문 미확인",
    "n": 1, "h": 0, "t": "active",
    "bidMethod": "확인 필요",
    "bidMethodEvidence": "kimkj 10-07 회차 2차 정보만 확인(공고일 10/06 17:53, 마감 10/19 10:00). 나라장터 원문 직접 조회 불가(HTML5/JS 장벽) — 입찰방식 판정 근거 없음. 제목만으로 추정 금지.",
    "peligoodFit": "인접적합",
    "fitEvidence": "AI-디지털트윈 기반 EV 정비 교육 콘텐츠 제작이 과업 중심. 페리굿의 3D 모델링·인터랙션 프로그래밍·교육콘텐츠 기획 역량으로 자연 수행 가능. VR/실감형 과업 명시는 확인되지 않아 핵심적합 아님.",
    "relatedNoticeNo": "R26BK01759430-000 (동일 사업 대규모 공고, 별도 건)"
}
kept.append(new_rec)

# dup check
nos = [r.get("noticeNo") for r in kept]
assert len(nos) == len(set(nos)), "duplicate noticeNo!"

# --- write back index.html ---
new_D = "const D=" + json.dumps(kept, ensure_ascii=False, separators=(",", ":")) + ";"
html2 = html[:start] + new_D + html[end_anchor:]
html2 = html2.replace("업데이트 · 2026.10.14 · 09:05 수시 심층검증", "업데이트 · 2026.10.15", 1)
assert "업데이트 · 2026.10.15" in html2
open(HTML, "w", encoding="utf-8").write(html2)
print("index.html updated, records:", len(kept))

# --- counts ---
def fitcat(r):
    f = str(r.get("peligoodFit", ""))
    return f
fitCounts = {}
for r in kept:
    fitCounts[r.get("peligoodFit", "미분류")] = fitCounts.get(r.get("peligoodFit", "미분류"), 0) + 1
bmc = {"price": 0, "proposal": 0, "presentation": 0, "unknown": 0}
for r in kept:
    bm = r.get("bidMethod", "확인 필요")
    if bm == "가격입찰": bmc["price"] += 1
    elif bm == "제안서 필수": bmc["proposal"] += 1
    elif bm == "제안서+발표": bmc["presentation"] += 1
    else: bmc["unknown"] += 1
lc = {"bid": 0, "pre-spec": 0, "plan": 0, "watch": 0}
for r in kept:
    lc[r.get("lifecycle", "watch")] = lc.get(r.get("lifecycle", "watch"), 0) + 1

prev = json.load(open(REPO + "/data/2026-10-14.json", encoding="utf-8"))
conditional = list(prev.get("conditionalCandidates", [])) + [
    {"noticeNo": "R26BK01767057-000", "title": "계류장 관제 시뮬레이터 구축 용역", "agency": "한국항공대학교",
     "amount": "6,727만원", "deadline": "10/19 10:00",
     "reason": "관제 직무훈련 시뮬레이터이나 XR/실감형 과업 명시 없음. 구공고(R26BK01751439-000)는 전자입찰·제한경쟁·단일예가였으나 재공고 조건 변경 가능 — 과업지시서·입찰방식·참가자격 원문 확인 필요",
     "url": "https://steemit.com/avle/@ictexpert/g2b-ict-briefing-20261014-pm", "bidMethod": "확인 필요"},
    {"noticeNo": "R26BK01766180", "title": "스마트공장 시뮬레이션 소프트웨어 구입", "agency": "경일대학교 산학협력단",
     "amount": "2,700만원", "deadline": "10/20 11:00",
     "reason": "시뮬레이션 SW '구입' 건으로 단순 상용 SW 구매 가능성 — 명시적 제외(일반 SW 구매) 해당 시 제외. 콘텐츠 개발 과업 포함 시 재검토",
     "url": "https://steemit.com/avle/@ictexpert/g2b-ict-briefing-20261014-pm", "bidMethod": "확인 필요"},
]

snapshot = {
    "runType": "daily",
    "updated": "2026-10-15",
    "executedAt": "2026-10-15T09:00:00+09:00",
    "counts": {"newOrPromoted": 1, "totalValid": len(kept), "bid": lc["bid"], "preSpec": lc["pre-spec"], "plan": lc["plan"], "watch": lc["watch"]},
    "trackCounts": {"publicProcurementChanged": 1, "universityIndustryAcademicChanged": 1, "schoolEducationS2BChanged": 0, "privateVerifiedActiveChanged": 0},
    "fitCounts": fitCounts,
    "bidMethodCounts": bmc,
    "priceOnly": [],
    "channelsChecked": [
        "[A] steemit @ictexpert G2B ICT 브리핑 2026-10-14 PM 회차 전문 스캔 + 10-13 PM/10-08 PM/10-07 PM 회차 부분 스캔 (10-15 AM 회차 미발행)",
        "[A] kimkj.com AI 게시판 2026-10-07 회차 — 국민대 R26BK01758442-000 별도 소규모 공고 유효성 2차 확인",
        "[A] browser.search: 나라장터 VR/XR/실감형/체험관/사전규격/재공고 키워드·공고번호 직접 검색 — watch 6건 후속 공고 모두 미발견",
        "[A] seenthis.kr/bid 직접 접속 실패(RECV_TIMEOUT) — 검색엔진 인덱싱으로 대체 조사",
        "[B] steemit @ictexpert 브리핑 10-13 PM·10-14 PM 회차에서 대학·산학협력단 발주 분류",
        "[B] 전주대학교 구매/입찰 게시판 직접 확인 — JJU-2026-112 [종료], 재공고 없음",
        "[B] seenthis 미러 + browser.search: 대학 VR/XR 입찰 신규·LINC/RISE·대학병원 VR 입찰·재공고 여부",
        "[C] seenthis.kr/bid·/bidplan browser.open 전부 타임아웃 — 검색엔진 스니펫 구조로 우회",
        "[C] steemit ICT 브리핑 10-13 PM·10-14 PM 회차 50건 전수 스캔 — 교육 XR 신규 없음",
        "[C] kosac.re.kr 입찰공고 게시판 직접 확인 — 과학창의재단 NO.2890 접수중·정정 없음 (10-12 기준)",
        "[C] S2B(s2b.kr) — 메인만 열람, 공개 입찰 목록 없음(회원 전용)",
        "[D] 대기업 협력사 포털 공개영역·협회/학회/민간재단 공지·기업 RFP 게시판·뉴스 버티컬·AI·XR 얼라이언스 — 검증 가능한 신규 민간 발주 없음",
    ],
    "watchRecheck": [
        {"noticeNo": "LH-2026-VR-SAFETY-WATCH", "title": "LH VR 안전교육 콘텐츠 후속발주", "status": "10/15 재확인: 후속발주 미발견; Watch 유지"},
        {"noticeNo": "R26BD00275676", "title": "강원랜드 스마트(VR·AI) 안전보건교육 동영상", "status": "10/15 재확인: 9/22 사전규격 의견마감 후 R26BK 본공고 전환 미발견; Watch 유지"},
        {"noticeNo": "R26DD20885559", "title": "한국광기술원 마이크로LED 공정장비 VR 콘텐츠", "status": "10/15 재확인: 10월 발주계획이나 본공고 미발견(10-13 브리핑의 광기술원 공고는 LLM 워크스테이션뿐); Watch 유지"},
        {"noticeNo": "R26DD20889311", "title": "한국가스안전공사 안전성평가 VR 시뮬레이션", "status": "10/15 재확인: 10월 발주계획이나 본공고 미발견(10-14 브리핑의 가스안전공사 공고는 금속수소화물 모니터링뿐); Watch 유지"},
        {"noticeNo": "KEPCO-G142600027-WATCH", "title": "한국발전교육원 복합발전 VR SPACE", "status": "10/15 재확인: 9/29 유찰 후 후속 재공고 미발견; Watch 유지"},
        {"noticeNo": "R26BK01751956-000", "title": "강화천문과학관 천체투영관 4D 모션 시스템", "status": "10/15 재확인: 10/12 16:00 마감 후 후속 재공고 미발견; Watch 유지"},
    ],
    "newOrPromoted": [
        {"noticeNo": "R26BK01758442-000", "title": "AI기반 디지털트윈 EV 정비 교육용 콘텐츠 제작(수정)", "agency": "국민대학교 산학협력단",
         "amount": "2,181만 8,182원", "deadline": "2026.10.19 10:00", "fit": "인접적합", "bidMethod": "확인 필요"}
    ],
    "updates": [
        {"noticeNo": "R26BK01759430-000", "change": "bidMethodEvidence 보강: bmap 호스팅 제안요청서(240,000,000원 부가세 포함, 기술90/가격10) 확인 — '제안서 필수' 확정. previousNoticeNo 정정 R26BK01758442-001(취소)→R26BK01740811-001(취소). R26BK01758442-000 별도 소규모 공고 관계 why에 명시."},
        {"noticeNo": "전 19건 중 기존 n=1 표시 4건(과학창의재단·동의대·강화천문과학관·NHIS) n=0으로 초기화"},
    ],
    "lifecycleChanges": [],
    "removedExpired": [
        {"noticeNo": "R26BK01740633-000", "title": "도장 직무교육용 VR 솔루션 교육장비 도입", "reason": "2026.10.14 10:00 마감"},
        {"noticeNo": "R26BK01752627-000", "title": "가상현실 심폐소생술 기기 구매", "reason": "2026.10.14 10:00 마감"},
        {"noticeNo": "JJU-2026-112", "title": "AI-ICVFX 교육 프로그램 운영 및 글로벌 현장 연수 용역", "reason": "2026.10.14 10:30 마감 · 전주대 게시판 [종료] 확인"},
        {"noticeNo": "R26BK01755549-000", "title": "의료기기 RA 심사 대응 STAGE2 VR 콘텐츠 개발 용역", "reason": "2026.10.14 14:00 마감 · 재공고 없음"},
    ],
    "removedOrExcluded": [
        {"noticeNo": "R26BK01740633-000", "title": "도장 직무교육용 VR 솔루션 교육장비 도입", "reason": "2026.10.14 10:00 마감 — 배열에서 제거"},
        {"noticeNo": "R26BK01752627-000", "title": "가상현실 심폐소생술 기기 구매", "reason": "2026.10.14 10:00 마감 — 배열에서 제거"},
        {"noticeNo": "JJU-2026-112", "title": "AI-ICVFX 교육 프로그램 운영 및 글로벌 현장 연수 용역", "reason": "2026.10.14 10:30 마감 · 전주대 게시판 [종료] 확인 — 배열에서 제거"},
        {"noticeNo": "R26BK01755549-000", "title": "의료기기 RA 심사 대응 STAGE2 VR 콘텐츠 개발 용역", "reason": "2026.10.14 14:00 마감 · 재공고 없음 — 배열에서 제거"},
        {"noticeNo": "R26BK01739262", "title": "[디지털] XR/VR/PC 기반 반도체 실습 프로그램", "reason": "부적합 제외 — 2026-10-08 마감 경과"},
        {"noticeNo": "R26BK01766180", "title": "스마트공장 시뮬레이션 소프트웨어 구입", "reason": "조건부 후보로 분리 기록(사이트 미노출) — 단순 SW 구매 가능성"},
        {"noticeNo": "R26BK01767057-000", "title": "계류장 관제 시뮬레이터 구축 용역", "reason": "조건부 후보로 분리 기록(사이트 미노출) — XR/실감형 과업 명시 없음"},
    ],
    "currentNotices": [{"noticeNo": r.get("noticeNo"), "title": r.get("title"), "d": r.get("d"), "lifecycle": r.get("lifecycle"), "fit": r.get("peligoodFit")} for r in kept],
    "conditionalCandidates": conditional,
    "notes": [
        "2026-10-15 09:00 KST 정규 예약 실행(4트랙 병렬 조사). 신규 1건(인접적합) 등록, 10/14 마감 4건 제거 → 16건(입찰 10·Watch 6).",
        "신규: 국민대 산학협력단 'AI기반 디지털트윈 EV 정비 교육용 콘텐츠 제작(수정)' R26BK01758442-000(2,182만원, 10/19 10:00) — kimkj 2차 정보상 유효한 별도 소규모 공고. 기존 인덱스의 'R26BK01758442-001 취소' 표기는 오기재였음(실제 취소는 R26BK01740811-001). 입찰방식 원문 미확인.",
        "국민대 대규모 공고 R26BK01759430-000: bmap 호스팅 제안요청서 확인으로 '제안서 필수' 확정(기술90/가격10, 2.4억원).",
        "조건부 후보 2건 추가(보고에만 기록, 사이트 미노출): ①한국항공대 계류장 관제 시뮬레이터(R26BK01767057-000, 6,727만원, 10/19) — XR/실감형 과업 명시 없음. ②경일대 산학협력단 스마트공장 시뮬레이션 SW 구입(R26BK01766180, 2,700만원, 10/20) — 단순 SW 구매 가능성. 기존 조건부 3건(창원대·부산엑스포·관저동) 유지.",
        "watch 6건 모두 본공고 전환/후속 재공고 미발견 → 유지. seenthis 직접 접속 실패·G2B JS 장벽·S2B 로그인 벽 지속 — 2차 정보(브리핑·kimkj·검색 인덱스) 기반이라 전환 시점 누락 가능성 있음.",
        "트랙 C 발견: G2B 첨부파일 직접 다운로드 URL 패턴 확인(pnza/UntyAtchFile 사전규격·pnp/pnpe/UntyAtchFile 입찰공고) — 향후 원문 확인 경로로 활용 가능.",
        "트랙 D(민간): 검증 가능한 신규 민간 발주 0건. 민간 트랙은 비공개 수의·지명 위주라 공개 RFP 발견율이 구조적으로 낮음 — 조사 범위·채널 정의 의사결정 필요(향후).",
    ],
    "scanLimitations": [
        "seenthis.kr/bid·/bidplan browser.open 전부 타임아웃(트랙 1·3) — 검색엔진 인덱싱으로 대체 조사, 10-13~15 게시분 일부 누락 가능",
        "G2B 원문 HTML5/JS 장벽 지속 — 신규 1건·조건부 2건의 입찰방식은 2차 정보 기준 '확인 필요'",
        "국민대 R26BK01758442-000 vs R26BK01759430-000 정확한 관계 — 원문 대조 없이 2차 정보로 별도 공고로 판정",
        "S2B 학교장터 로그인 벽 지속 — 공개 영역만 확인",
        "steemit 10-15 AM 회차 미발행 — 10-14 PM 회차가 최신",
        "과학창의재단 건 kosac 게시판 최신이 10-12 — 10-13~15 정정 여부 미확인",
    ],
}
json.dump(snapshot, open(REPO + "/data/2026-10-15.json", "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print("snapshot written:", len(kept), "records")
print("counts:", snapshot["counts"])
print("fitCounts:", fitCounts)
print("bidMethodCounts:", bmc)
