import re, json, datetime, copy

BASE = '/home/hatch/workspace/peli'
html = open(BASE + '/index.html', encoding='utf-8').read()
m = re.search(r'const D=(\[.*?\]);\n', html, re.S)
D = json.loads(m.group(1))
print('before:', len(D))

# 1) remove expired (deadline passed as of 2026-10-02 19:30 KST)
EXPIRED = {'R26BK01742837-000'}  # VR 교육용 장비 구매, 2026.10.02 13:00 마감
D = [r for r in D if r.get('noticeNo') not in EXPIRED]
for r in D:
    r['n'] = 0

# 2) new records
NEW = [
 {
  "source": "G2B", "amount": "공고문 확인 필요",
  "url": "https://www.g2b.go.kr/link/PNPE027_01/single/?bidPbancNo=R26BK01750015&bidPbancOrd=000",
  "urlType": "official", "lifecycle": "bid", "noticeNo": "R26BK01750015-000",
  "d": "2026.10.13 14:00", "deadlineType": "입찰서 제출 마감", "noticeType": "입찰공고",
  "title": "수정유스센터 AI체험관 체험시설 제작 설치(협상에의한계약)",
  "a": "재단법인성남시청소년청년재단",
  "task": "AI체험관 체험시설 제작·설치",
  "why": "체험관 체험시설 제작·설치가 과업 중심. 페리굿의 체험관 구축·실감형 체험콘텐츠 제작 역량과 연결. XR/인터랙티브 콘텐츠 포함 여부는 원문 확인 필요.",
  "f": "높음", "q": "확인 필요 — 공고문 원문 미확인", "j": "원문 확인 필요",
  "n": 1, "h": 0, "t": "active",
  "bidMethod": "제안서 필수",
  "bidMethodEvidence": "공고명에 '(협상에의한계약)' 명시 — 제안서 평가 후 협상대상자 선정 방식",
  "peligoodFit": "인접적합",
  "fitEvidence": "체험관 체험시설 제작·설치가 과업 중심. XR/실감형 과업 포함 여부는 원문 확인 필요(확실하지 않음)."
 },
 {
  "source": "G2B", "amount": "5억 1,600만원",
  "url": "https://www.g2b.go.kr/link/PNPE027_01/single/?bidPbancNo=R26BK01737321&bidPbancOrd=000",
  "urlType": "official", "lifecycle": "bid", "noticeNo": "R26BK01737321-000",
  "d": "2026.10.12 10:00", "deadlineType": "입찰서 제출 마감", "noticeType": "입찰공고",
  "title": "경상남도교육청 학생안전체험원 공공형 안전체험교육장 구축 사업 입찰 공고",
  "a": "경상남도교육청(학생안전체험원)",
  "task": "산업안전교육장·조리안전교육장 구축용 안전체험 실물모형 및 전시콘텐츠 15개 체험존 일체 납품(현장설치도)",
  "why": "교육청 직속 학생안전체험원의 체험관 구축 사업. 페리굿의 체험관 구축·체험형 안전교육 콘텐츠 제작 역량을 자연스럽게 적용 가능. 단 원문에 XR/실감형 과업 명시는 없음(확실하지 않음).",
  "f": "보통", "q": "제한경쟁·전자입찰. 세부품명 6010989901(실물모형및전시물) 등록 필요 추정 — 상세 참가자격은 공고문 원문 미확인(확실하지 않음)", "j": "1식 총액 납품·현장설치",
  "n": 1, "h": 0, "t": "active",
  "bidMethod": "확인 필요",
  "bidMethodEvidence": "seenthis 기본정보상 계약방법 제한경쟁·전자입찰이나 낙찰방법·참가자격은 공고문 원문 미확인. 예가방법 비예가(추첨예가)/총예가로 가격경쟁 가능성은 있으나 확정 불가.",
  "peligoodFit": "인접적합",
  "fitEvidence": "발주계획 주요규격: '학생안전체험원 산업안전교육장·조리안전교육장 구축용 안전체험 실물모형 및 전시콘텐츠 — 15개 체험존 실물모형·구조물 및 전시연출물 일체'. XR/실감형 과업은 명시되지 않음."
 },
 {
  "source": "G2B", "amount": "1억 487만 9,540원",
  "url": "https://kimkj.com/guestbook/?vid=69",
  "urlType": "discovery", "lifecycle": "pre-spec", "noticeNo": "R26BD00280028",
  "d": "2026.10.06 23:59", "deadlineType": "의견등록 기한(사전규격)", "noticeType": "사전규격",
  "title": "카자흐스탄 크즐오르다 대학교 인공지능 단과대학 내 VR 실습실 장비 설치사업 구축",
  "a": "서울과학기술대학교 산학협력단",
  "task": "카자흐스탄 크즐오르다 대학교 AI 단과대학 내 VR 실습실 장비 설치사업 구축(용역)",
  "why": "VR 실습실 구축·장비 설치는 페리굿의 HMD·PC·CMS 통합납품, 체험관 구축 역량과 직접 연결.",
  "f": "높음", "q": "사전규격 단계로 참가자격 미공개 — 확인 필요", "j": "확인 필요",
  "n": 1, "h": 0, "t": "active",
  "bidMethod": "확인 필요",
  "bidMethodEvidence": "사전규격 단계로 입찰방식(가격/협상) 미공개",
  "peligoodFit": "핵심적합",
  "fitEvidence": "공고명 'VR 실습실 장비 설치사업 구축' — VR 장비 납품·구축이 과업 중심."
 },
 {
  "source": "충북안전체험관", "amount": "1억 9,855만원",
  "url": "https://jiwonkok.com/12510/download/%EC%B7%A9%EB%B6%81%EC%95%88%EC%A0%84%EC%B2%B4%ED%97%98%EA%B4%80%20XR%EC%B2%B4%ED%97%98%EC%9E%A5%EB%B9%84%20%EB%B0%8F%20%EC%BD%98%ED%85%90%EC%B8%A0%20%EA%B5%AC%EC%B6%95%20%EC%82%AC%EC%97%85%20%EC%A0%9C%EC%95%88%EC%84%9C%20%ED%8F%89%EA%B0%80%EC%9C%84%EC%9B%90(%ED%9B%84%EB%B3%B4%EC%9E%90)%20%EB%AA%A8%EC%A7%91%20%EA%B3%B5%EA%B3%A0%EB%AC%B8.pdf/?inline=1",
  "urlType": "discovery", "lifecycle": "watch", "noticeNo": "충북안전체험관-2026-3호",
  "d": "본공고 미확인 · 평가위원 추첨 9/18 경과 → 본입찰 추적",
  "deadlineType": "본입찰 추적", "noticeType": "평가위원 모집공고(본공고 미확인)",
  "title": "충북안전체험관 XR체험장비 및 콘텐츠 구축 사업 · 본공고 추적",
  "a": "충북안전체험관",
  "task": "XR 체험콘텐츠 제작 및 디바이스 구입 등(계약일로부터 120일 이내)",
  "why": "'XR 체험콘텐츠 제작 및 디바이스 구입'이 과업 중심 — 페리굿 핵심역량(XR 콘텐츠 개발·HMD 디바이스 연동·체험관 구축)과 직접 일치. 본 입찰공고가 아직 미발견이라 watch 유지.",
  "f": "매우 높음", "q": "확인 필요 — 본 입찰공고(참가자격·마감) 미발견", "j": "확인 필요",
  "n": 1, "h": 1, "t": "watch",
  "bidMethod": "제안서 필수",
  "bidMethodEvidence": "공고 제2026-3호(평가위원 모집공고): '협상에 의한 계약방식으로 추진하는 XR체험장비 및 콘텐츠 구축 사업의 제안서 평가' 명시",
  "peligoodFit": "핵심적합",
  "fitEvidence": "사업내용 'XR 체험콘텐츠 제작 및 디바이스 구입 등'. 제한경쟁입찰(협상에 의한 계약)."
 },
 {
  "source": "G2B", "amount": "확인 필요(소액수의)",
  "url": "https://www.g2b.go.kr/link/PNPE027_01/single/?bidPbancNo=R26BK01753843&bidPbancOrd=000",
  "urlType": "official", "lifecycle": "watch", "noticeNo": "R26BK01753843-000",
  "d": "1인 견적 2026.10.02 15:00 마감 · 재공고 추적",
  "deadlineType": "재공고 추적", "noticeType": "1인 견적제출 안내공고(마감)",
  "title": "SW·AI교육거점센터 VR e-스포츠 시스템 구매 · 재공고 추적",
  "a": "부산광역시교육청교육연구정보원",
  "task": "SW·AI교육거점센터 VR e-스포츠 시스템 구매(2인 견적 3회 유찰 → 1인 견적 진행)",
  "why": "VR e-스포츠 시스템 구매 — HMD·PC·CMS 통합납품 역량과 직접 연결. 9월 연속 유찰(2인 견적 3회) 후 1인 견적까지 진행됐고 오늘 마감됐으므로 계약 실패 시 재공고 가능성이 높음.",
  "f": "높음", "q": "소액수의 견적 — 참가자격 등록 확인 필요", "j": "확인 필요",
  "n": 1, "h": 0, "t": "watch",
  "bidMethod": "가격입찰",
  "bidMethodEvidence": "1인 견적제출(소액수의) 방식 — 가격으로 낙찰자 결정. 단 현재 건은 마감됐고 후속 재공고 시 재판정.",
  "peligoodFit": "핵심적합",
  "fitEvidence": "VR e-스포츠 시스템 구매가 과업 — XR 체험장비 통합납품이 과업 중심."
 },
 {
  "source": "G2B", "amount": "3,150만원",
  "url": "https://www.g2b.go.kr/pn/pnz/pnza/UntyAtchFile/downloadFile.do?bfSpecRegNo=R26BD00264156&fileType=BFDTL&fileSeq=1",
  "urlType": "discovery", "lifecycle": "watch", "noticeNo": "R26BD00264156",
  "d": "사전규격 2026.06.22 · 본공고 전환 대기",
  "deadlineType": "본공고 전환 추적", "noticeType": "사전규격(본공고 미확인)",
  "title": "웨어러블 AI·XR 기반 K-아트 실무 교육 첨단 기자재 구축 용역 · 본공고 전환 추적",
  "a": "호원대학교 RISE사업단",
  "task": "웨어러블 AI·XR 기자재 및 구동 소프트웨어·교육 콘텐츠 구축(창업동아리실, 착수일로부터 1개월)",
  "why": "XR 기자재·콘텐츠 통합납품 — 페리굿 핵심역량과 직접 연결. 사전규격에 제한경쟁입찰(최저가격입찰) 예정으로 명시되어 본공고 전환 시 가격입찰 후보.",
  "f": "높음", "q": "사전규격 기준: 최근 3년 실감콘텐츠/XR 분야 10건 이상 납품 + 단일실적 1억원 이상(변동 가능)", "j": "확인 필요",
  "n": 1, "h": 0, "t": "watch",
  "bidMethod": "확인 필요",
  "bidMethodEvidence": "사전규격 과업지시서에 '입찰방법: 제한경쟁입찰(최저가격입찰)' 예정 명시 — 본공고 전환 시 가격입찰 가능성이 높음",
  "peligoodFit": "핵심적합",
  "fitEvidence": "과업 '웨어러블 AI·XR 기자재 및 구동 소프트웨어·교육 콘텐츠 구축' — XR HW+SW+콘텐츠 통합납품이 과업 중심. 기자재: 메타 레이밴 디스플레이 3식, 삼성 갤럭시 XR 2식."
 },
]
D.extend(NEW)

# 3) duplicate noticeNo check
nos = [r.get('noticeNo') for r in D]
assert len(nos) == len(set(nos)), 'duplicate noticeNo!'

# 4) rewrite index.html
newD = json.dumps(D, ensure_ascii=False, separators=(',', ':'))
html2 = html.replace(m.group(0), 'const D=' + newD + ';\n', 1)
html2 = html2.replace('업데이트 · 2026.10.02 · 심층검색', '업데이트 · 2026.10.02 · 심층검색(저녁)', 1)
open(BASE + '/index.html', 'w', encoding='utf-8').write(html2)
print('after:', len(D))
print('expired removed:', EXPIRED)
print('new added:', len(NEW))

# 5) summary counts
from collections import Counter
print('lifecycle:', Counter(r['lifecycle'] for r in D))
print('fit:', Counter(r['peligoodFit'] for r in D))
print('method:', Counter(r['bidMethod'] for r in D))
print('t:', Counter(r['t'] for r in D))
print('n=1:', sum(1 for r in D if r.get('n') == 1))
