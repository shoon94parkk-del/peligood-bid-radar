import fs from 'node:fs';
import path from 'node:path';
import vm from 'node:vm';
import { pathToFileURL } from 'node:url';

const requiredDocuments=[
  'AGENTS.md','docs/project-memory.md','docs/regression-guardrails.md',
  'docs/decision-log.md','docs/daily-scan-playbook.md','index.html'
];
export const requiredRecordFields=[
  'source','amount','url','urlType','lifecycle','noticeNo','d','deadlineType',
  'noticeType','title','a','task','why','f','q','j','n','h','t',
  'bidMethod','bidMethodEvidence','peligoodFit','fitEvidence'
];

export function extractDashboardRecords(html){
  if(typeof html!=='string') throw new Error('dashboard HTML not a string');
  const mark=html.search(/\bconst\s+D\s*=/);
  if(mark<0) throw new Error('missing const D dashboard data');
  const equal=html.indexOf('=',mark);
  const start=html.indexOf('[',equal);
  if(start<0) throw new Error('missing D array opening bracket');
  const finish=html.indexOf('];',start);
  if(finish<0) throw new Error('missing D array closing delimiter');
  let records;
  try { records=JSON.parse(html.slice(start,finish+1)); }
  catch(err){ throw new Error('invalid dashboard D JSON: '+err.message); }
  if(!Array.isArray(records)) throw new Error('dashboard D must be array');
  const scripts=[...html.matchAll(/<script\b[^>]*>([\s\S]*?)<\/script>/gi)];
  if(scripts.length===0) throw new Error('no dashboard JavaScript found');
  for(const [index,script] of scripts.entries()){
    try { new vm.Script(script[1],{filename:'dashboard-script-'+index+'.js'}); }
    catch(err){ throw new Error('dashboard JavaScript syntax error: '+err.message); }
  }
  return records;
}

const normalizeNoticeBase=id=>{
  const m=String(id||'').match(/^(R\d{2}BK\d{8})(?:-\d{3})?$/i);
  return m?m[1].toUpperCase():String(id||'').trim();
};
const toMsKst=deadline=>{
  const m=String(deadline||'').match(/^(\d{4})\.(\d{2})\.(\d{2})\s+(\d{2}):(\d{2})/);
  return m?Date.parse(`${m[1]}-${m[2]}-${m[3]}T${m[4]}:${m[5]}:00+09:00`):NaN;
};
const populated=x=>x!==null&&x!==undefined&&(typeof x!=='string'||x.trim().length>0);
const own=(o,k)=>Object.prototype.hasOwnProperty.call(o,k);

export function validateRadarSnapshot(payload,dashboardRows,options={}){
  const errors=[];
  const assert=(condition,message)=>{if(!condition)errors.push(message);};
  assert(payload&&typeof payload==='object'&&!Array.isArray(payload),'daily payload missing');
  assert(Array.isArray(dashboardRows),'dashboard rows missing');
  if(!payload||!Array.isArray(dashboardRows))throw Error(errors.join('\n'));
  const rows=dashboardRows;
  const ids=new Set();
  const validLife=new Set(['bid','watch','pre-spec','plan']);
  const bidMethods=new Set(['가격입찰','가격입찰만','제안서 필수','제안서+발표','확인 필요']);
  for(const [i,item] of rows.entries()){
    const prefix='dashboard row '+i+' '+String(item?.noticeNo||'NO-ID');
    assert(item&&typeof item==='object',prefix+' invalid row');
    if(!item||typeof item!=='object')continue;
    const id=String(item.noticeNo||'');
    assert(populated(id),prefix+' missing noticeNo');
    assert(!ids.has(id),prefix+' duplicate noticeNo'); ids.add(id);
    for(const field of requiredRecordFields)assert(own(item,field)&&populated(item[field]),prefix+' missing '+field);
    assert(validLife.has(item.lifecycle),prefix+' unsupported lifecycle');
    assert(bidMethods.has(item.bidMethod),prefix+' unsupported bidMethod');
    assert(['official','discovery','external'].includes(item.urlType),prefix+' invalid urlType');
    assert(/^https:\/\//i.test(String(item.url||'')),prefix+' needs HTTPS individual source');
    assert((item.lifecycle==='watch'&&item.t==='watch')||(item.lifecycle!=='watch'&&item.t==='active'),prefix+' lifecycle/t mismatch');
    if(['bid','pre-spec'].includes(item.lifecycle)){
      const bidDeadline=toMsKst(item.d);
      assert(Number.isFinite(bidDeadline),prefix+' active bid needs a parseable KST deadline');
      if(Number.isFinite(bidDeadline)&&options.asOfMs!==undefined)
        assert(bidDeadline>options.asOfMs,prefix+' expired before snapshot execution');
    }
    if(['가격입찰','가격입찰만'].includes(item.bidMethod)){
      assert(populated(item.participationStatus)&&populated(item.participationReason),prefix+' price-only bid must include eligibility evidence');
      if(/기술제안서|정성평가|협상에\s*의한|발표평가/i.test(String(item.bidMethodEvidence||''))&&!/기술제안서\s*없음/i.test(String(item.bidMethodEvidence||'')))
        errors.push(prefix+' contradicts price-only bid method');
    }
  }
  const count=(life)=>rows.filter(x=>x.lifecycle===life).length;
  assert(payload.counts&&typeof payload.counts==='object','daily counts absent');
  if(payload.counts){
    for(const [field,n] of [['totalValid',rows.length],['bid',count('bid')],['watch',count('watch')],['preSpec',count('pre-spec')],['plan',count('plan')]]){
      assert(payload.counts[field]===n,`daily counts.${field} expected ${n} got ${payload.counts[field]}`);
    }
  }
  const allChanges=[...(payload.new||[]),...(payload.updates||[])];
  const changes=new Set();
  for(const row of allChanges){
    assert(populated(row.noticeNo),'daily change missing noticeNo');
    assert(!changes.has(row.noticeNo),'duplicate daily new/update '+row.noticeNo);
    changes.add(row.noticeNo);
    const dashboard=rows.find(x=>x.noticeNo===row.noticeNo);
    assert(!!dashboard,'daily change absent from dashboard '+row.noticeNo);
    if(dashboard){
      for(const key of ['title','d','lifecycle','bidMethod','url','urlType','amount']){
        assert(String(dashboard[key]??'')===String(row[key]??''),`dashboard/daily change mismatch ${row.noticeNo}.${key}`);
      }
    }
  }
  assert(Array.isArray(payload.new)&&Array.isArray(payload.updates),'daily new/updates must be arrays');
  if(payload.counts)assert(payload.counts.newOrPromoted===(payload.new||[]).length,'newOrPromoted count mismatch');
  if(payload.currentNotices){
    assert(Array.isArray(payload.currentNotices),'currentNotices must be array');
    if(Array.isArray(payload.currentNotices)){
      const activeMap=new Map(payload.currentNotices.map(x=>[x.noticeNo,x]));
      assert(activeMap.size===rows.length,'currentNotices count/IDs mismatch');
      for(const r of rows){
        const stored=activeMap.get(r.noticeNo);
        assert(!!stored,'dashboard notice absent from currentNotices '+r.noticeNo);
        if(stored)for(const field of ['title','d','lifecycle','bidMethod','url','amount']){
          assert(String(r[field]??'')===String(stored[field]??''),`snapshot/dashboard mismatch ${r.noticeNo}.${field}`);
        }
      }
    }
  }
  const canceledIds=new Set();
  for(const canceled of (payload.removedOrExcluded||[])){
    const reason=String(canceled.reason||'');
    if(canceled.status==='cancelled'||(String(canceled.status||'').includes('취소'))||(/취소|cancel/i.test(reason)&&!/(?:취소가 아닌|취소 여부 미확인)/.test(reason)))
      canceledIds.add(normalizeNoticeBase(canceled.noticeNo));
  }
  for(const change of (payload.lifecycleChanges||[])){
    if((change.to==='removed/cancelled'||change.to==='cancelled')&&populated(change.noticeNo))
      canceledIds.add(normalizeNoticeBase(change.noticeNo));
    if(change.from&&change.to&&change.action&&(/watch|pre-spec|plan/i.test(change.action)||/승격/.test(change.action))){
      if(change.from.includes('WATCH')&&rows.some(x=>x.noticeNo===change.from)&&rows.some(x=>x.noticeNo===change.to))
        errors.push('promoted old WATCH and new bid both visible: '+change.from+'->'+change.to);
    }
  }
  for(const row of rows.filter(x=>x.lifecycle==='bid'))
    assert(!canceledIds.has(normalizeNoticeBase(row.noticeNo)),row.noticeNo+' present despite known cancellation');
  if(payload.bidMethodCounts){
    const desired={
      price:rows.filter(x=>x.lifecycle==='bid'&&['가격입찰','가격입찰만'].includes(x.bidMethod)).length,
      proposal:rows.filter(x=>x.lifecycle==='bid'&&x.bidMethod==='제안서 필수').length,
      presentation:rows.filter(x=>x.lifecycle==='bid'&&x.bidMethod==='제안서+발표').length,
      unknown:rows.filter(x=>x.lifecycle==='bid'&&x.bidMethod==='확인 필요').length
    };
    // Prior snapshots sometimes used "check" or "proposalPresentation" field naming.
    for(const [field,n] of Object.entries(desired)){
      const aliases={presentation:['presentation','proposalPresentation'],unknown:['unknown','check']}[field]||[field];
      const found=aliases.find(key=>own(payload.bidMethodCounts,key));
      if(found)assert(payload.bidMethodCounts[found]===n,`bidMethodCounts.${found} expected ${n}`);
    }
  }
  if(errors.length)throw new Error('Peligood contract failed ('+errors.length+'):\n- '+errors.join('\n- '));
  return {count:rows.length,bids:count('bid'),watches:count('watch'),changes:allChanges.length};
}

export function validateRepository(root='.'){
  const read=file=>fs.readFileSync(path.join(root,file),'utf8');
  for(const file of requiredDocuments){
    if(!fs.existsSync(path.join(root,file)))throw Error('missing required file: '+file);
  }
  const memory=read('docs/project-memory.md'),guard=read('docs/regression-guardrails.md');
  for(const token of ['VR/AR/metaverse','urlType=official','urlType=discovery','bid','pre-spec','watch']){
    if(!memory.includes(token))throw Error('project memory missing contract: '+token);
  }
  for(const token of ['Every actionable','Never fabricate an official URL','Pre-spec opinion deadline']){
    if(!guard.includes(token))throw Error('guardrails missing contract: '+token);
  }
  const files=fs.readdirSync(path.join(root,'data')).filter(x=>/^\d{4}-\d{2}-\d{2}\.json$/.test(x)).sort();
  if(!files.length)throw Error('no daily research JSON');
  const newest=files.at(-1),payload=JSON.parse(read('data/'+newest));
  if(payload.updated!==newest.replace('.json',''))throw Error('snapshot date does not match file '+newest);
  const asOfMs=Date.parse(payload.executedAt);
  if(!Number.isFinite(asOfMs))throw Error('daily snapshot executedAt is invalid');
  const rows=extractDashboardRecords(read('index.html'));
  const result=validateRadarSnapshot(payload,rows,{asOfMs});
  console.log('Peligood extended project contract OK:',newest,JSON.stringify(result));
  return result;
}

if(process.argv[1]&&import.meta.url===pathToFileURL(path.resolve(process.argv[1])).href)validateRepository();
