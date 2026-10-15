import test from 'node:test';
import assert from 'node:assert/strict';
import {validateRadarSnapshot,extractDashboardRecords} from './validate-project.mjs';
const source={
 source:'G2B',amount:'10,000,000원',url:'https://example.org/notice/77',
 urlType:'discovery',lifecycle:'bid',noticeNo:'R26BK01758442-000',
 d:'2026.10.20 10:00',deadlineType:'입찰마감',noticeType:'입찰공고',title:'Sample VR project',
 a:'Demo institution',task:'VR education',why:'Direct fit',f:'높음',q:'licence check',
 j:'joint bid check',n:1,h:0,t:'active',bidMethod:'제안서 필수',
 bidMethodEvidence:'기술제안서 필수',peligoodFit:'핵심적합',fitEvidence:'VR development'
};
const snapshot=(items=[source])=>({
 updated:'2026-10-15',executedAt:'2026-10-15T10:03:00+09:00',
 counts:{newOrPromoted:1,totalValid:items.length,bid:items.length,watch:0,preSpec:0,plan:0},
 new:[items[0]],updates:[],currentNotices:items,
 removedOrExcluded:[],lifecycleChanges:[]
});
test('baseline valid active bid',()=>{
 assert.equal(validateRadarSnapshot(snapshot(),[source],{asOfMs:Date.parse('2026-10-15T10:03:00+09:00')}).bids,1);
});
test('duplicate card is rejected',()=>{
 const rows=[source,{...source,title:'different title'}],payload=snapshot(rows);payload.counts.newOrPromoted=1;
 assert.throws(()=>validateRadarSnapshot(payload,rows),/duplicate noticeNo/);
});
test('expired card rejected',()=>{
 assert.throws(()=>validateRadarSnapshot(snapshot(),[source],{asOfMs:Date.parse('2026-10-21T10:03:00+09:00')}),/expired before/);
});
test('canceled later sequence cannot be resurrected from old listing',()=>{
 const p=snapshot();
 p.removedOrExcluded=[{noticeNo:'R26BK01758442-000',status:'cancelled',reason:'-001 차수 취소공고'}];
 assert.throws(()=>validateRadarSnapshot(p,[source]),/known cancellation/);
});
test('mismatch between snapshot and dashboard is rejected',()=>{
 const p=snapshot(),bad={...source,d:'2026.10.21 10:00'};
 assert.throws(()=>validateRadarSnapshot(p,[bad]),/mismatch/);
});
test('invalid dashboard JS is rejected',()=>{
 const html='<html><script>const D='+JSON.stringify([source])+'; let = ;</script></html>';
 assert.throws(()=>extractDashboardRecords(html),/syntax error/);
});
test('spec-and-price with technical proposal cannot be called price-only',()=>{
 const bad={...source,bidMethod:'가격입찰',bidMethodEvidence:'기술제안서 평가 후 최저가',participationStatus:'확인 필요',participationReason:'조건'};
 const p=snapshot([bad]);assert.throws(()=>validateRadarSnapshot(p,[bad]),/price-only/);
});
