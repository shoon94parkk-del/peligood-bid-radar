import fs from 'node:fs';
import path from 'node:path';

const mustExist=[
  'AGENTS.md',
  'docs/project-memory.md',
  'docs/regression-guardrails.md',
  'docs/decision-log.md',
  'index.html',
];
for(const file of mustExist){
  if(!fs.existsSync(file)) throw new Error('missing required file: '+file);
}

const memory=fs.readFileSync('docs/project-memory.md','utf8');
const guard=fs.readFileSync('docs/regression-guardrails.md','utf8');
for(const token of ['VR/AR/metaverse','urlType=official','urlType=discovery','bid','pre-spec','watch']){
  if(!memory.includes(token)) throw new Error('project memory missing contract: '+token);
}
for(const token of ['Every actionable','Never fabricate an official URL','Pre-spec opinion deadline']){
  if(!guard.includes(token)) throw new Error('guardrails missing contract: '+token);
}

const dataDir='data';
const files=fs.existsSync(dataDir)?fs.readdirSync(dataDir).filter(x=>/^\d{4}-\d{2}-\d{2}\.json$/.test(x)).sort():[];
if(!files.length) throw new Error('no daily research JSON');
const latest=files.at(-1);
const payload=JSON.parse(fs.readFileSync(path.join(dataDir,latest),'utf8'));
const rows=[...(payload.new||[]),...(payload.updates||[])];
const required=['source','amount','url','urlType','lifecycle','noticeNo','d','deadlineType','noticeType','title','a','task','why','f','q','j','n','h','t','bidMethod','bidMethodEvidence','peligoodFit','fitEvidence'];
for(const row of rows){
  for(const key of required){
    if(row[key]===undefined||row[key]===null||(typeof row[key]==='string'&&!row[key].trim())){
      throw new Error(latest+': missing '+key+' for '+(row.title||'row'));
    }
  }
  if(['bid','pre-spec'].includes(row.lifecycle)){
    if(!/^https:\/\//i.test(String(row.url||''))) throw new Error(latest+': actionable item missing https URL: '+row.title);
    if(!['official','discovery','external'].includes(row.urlType)) throw new Error(latest+': invalid urlType: '+row.title);
  }
  if(row.bidMethod==='가격입찰'&&(!row.participationStatus||!row.participationReason)){
    throw new Error(latest+': price bid missing participation evidence: '+row.title);
  }
}
const noticeNos=rows.map(row=>row.noticeNo);
if(new Set(noticeNos).size!==noticeNos.length) throw new Error(latest+': duplicate noticeNo in daily changes');
console.log('Peligood project contract OK:',latest,(payload.new||[]).length,'new rows,',(payload.updates||[]).length,'updates');
