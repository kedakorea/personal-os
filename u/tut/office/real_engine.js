/* 퍼스널 OS 실사 오피스형 3종 (meeting 회의실 · tower 빌딩 층별 · desk 집무실) — 2026-11-11 대표님 지시
   사무실화면.py 가 window.RO={c,company,chief,call,bg,mface,depts:[{name,face}]} 를 넣어 부서/00_비서실/오피스마을.html 로 만든다.
   얼굴: ~/퍼스널OS/회사자료/얼굴/매니저.jpg · <부서이름>.jpg (없으면 이름 첫 글자) */
(function(){
const R=window.RO,C=R.c,$=s=>document.querySelector(s),ESC=s=>String(s==null?'':s).replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
const strip=s=>String(s||'').replace(/^(MY_|\d+[_ ]?)\s*/,'').replace(/^\S*_/,'').trim();
const COL=['#1e31ef','#2f9a6a','#d9822b','#8e44ad','#c0392b','#16a085','#2c3e50','#b8860b'];
const face=(f,n,i,cls)=>f?`<img class="${cls}" src="${f}" alt="">`:`<span class="${cls} mono" style="background:${COL[i%COL.length]}">${ESC((n||'?').slice(0,1))}</span>`;
let BUSY=new Map(),TODO=[],TD=0,LAST='';
async function J(u){try{const r=await fetch(u,{credentials:'same-origin',cache:'no-store'});return r.ok?await r.json():null;}catch(e){return null;}}
function now(){const d=new Date();return {date:`${d.getMonth()+1}월 ${d.getDate()}일 ${'일월화수목금토'[d.getDay()]}요일`,time:d.toTimeString().slice(0,5),night:d.getHours()>=18||d.getHours()<7};}
function st(n){return BUSY.has(n)?['on','작업 중']:['','대기'];}
function said(){if(BUSY.size){const w=[...BUSY.values()][0];return `${R.call}, ${[...BUSY.keys()].join('·')}에서 처리하고 있어요 — ${w.now||w.ask||'작업 중'}`;}return LAST||`${R.call}, 오늘은 무엇부터 할까요?`;}
function cut(s,n){s=String(s||'');return s.length>n?s.slice(0,n)+'…':s;}
function brief(){const t=TODO.slice(0,5).map(i=>`<li><b>${ESC(i.b)}</b>${ESC(cut(i.t,30))}</li>`).join('')||'<li>오늘 할 일이 비어 있어요</li>';return `<ul class="br">${t}</ul>`;}
function render(){
  const T=now(),D=R.depts;let h='';
  if(C==='meeting'){
    const n=D.length,L=Math.ceil(n/2);
    const pos=D.map((d,i)=>{const left=i<L,k=left?i:i-L,m=left?L:n-L,f=m>1?k/(m-1):.5;return [left?33-f*22:67+f*22,40+f*42];});
    h=`<div class="mgr" style="left:50%;top:25%">${`<div class="say1">${ESC(cut(said(),70))}</div>`}${face(R.mface,R.chief,0,'fc big')}<span class="tag on"><i></i>${ESC(R.chief)}</span></div>`+
      D.map((d,i)=>{const [c,s]=st(d.name);return `<div class="seat" data-d="${ESC(d.name)}" style="left:${pos[i][0]}%;top:${pos[i][1]}%">${face(d.face,d.name,i+1,'fc '+c)}<span class="tag ${c}"><i></i>${ESC(d.name)} · ${s}</span></div>`;}).join('');
  }else if(C==='tower'){
    const top=D.length+1;
    h=`<div class="floors"><div class="fl boss"><em>${top+1}F</em>${face(R.mface,R.chief,0,'fc')}<p><b>${ESC(R.chief)} · 집무실</b><small>${ESC(cut(said(),60))}</small></p></div>`+
      D.map((d,i)=>{const [c,s]=st(d.name),w=BUSY.get(d.name);return `<div class="fl ${c}" data-d="${ESC(d.name)}"><em>${top-i}F</em>${face(d.face,d.name,i+1,'fc')}<p><b>${ESC(d.name)}</b><small>${c?ESC(cut(w.now||w.ask||'작업 중',40)):(T.night?'불 끄고 퇴근':'불 켜 두고 대기')}</small></p><span class="tag ${c}"><i></i>${s}</span></div>`;}).join('')+`</div>`;
  }else{
    h=`<div class="board">${face(R.mface,R.chief,0,'fc big')}<div><b>${ESC(R.chief)}</b><small>오늘의 브리핑 · 할 일 ${TD}</small></div>${brief()}<p class="say2">"${ESC(cut(said(),80))}"</p></div>`+
      `<div class="cards">${D.map((d,i)=>{const [c,s]=st(d.name);return `<div class="card ${c}" data-d="${ESC(d.name)}">${face(d.face,d.name,i+1,'fc sq')}<b>${ESC(d.name)}</b><span class="tag ${c}"><i></i>${s}</span></div>`;}).join('')}</div>`;
  }
  $('#scene').innerHTML=h;
  $('#hd').innerHTML=`<b>${ESC(R.company)} ${C==='meeting'?'회의실':C==='tower'?'빌딩':'집무실'}</b><small>${T.date} ${T.time} · 출근 ${D.length+1}명${BUSY.size?' · '+BUSY.size+'개 부서 작업 중':''}</small>`;
}
async function load(){
  const [o,td]=await Promise.all([J('/api/office'),J('/api/todo')]);BUSY=new Map();
  if(o)(o.working||[]).forEach(w=>{const n=strip(w.dept);const d=R.depts.find(x=>x.name===n);BUSY.set(d?d.name:(R.depts[0]||{}).name||'비서실',w);});
  if(td){const B={today:'오늘',tomorrow:'내일',sched:'모레',week:'곧'};const it=(td.items||[]).filter(i=>!i.checked&&B[i.bucket]&&!i.personal);TD=it.filter(i=>i.bucket==='today').length;
    const ord=['today','tomorrow','sched','week'];it.sort((a,b)=>ord.indexOf(a.bucket)-ord.indexOf(b.bucket));TODO=it.map(i=>({b:B[i.bucket],t:i.text}));}
  try{const ts=parent.document.querySelectorAll('#stream .turn.elvin, #stream .turn:not(.me)');const t=ts[ts.length-1];const b=t&&t.querySelector('.bubble');if(b)LAST=(b.innerText||'').replace(/^📋[^\n]*\n/,'').trim();}catch(e){}
  render();
}
document.addEventListener('click',e=>{const d=e.target.closest('[data-d]');if(d&&parent.OSV_ask)parent.OSV_ask(d.dataset.d);const c=e.target.closest('#toChat');if(c&&parent.OSV_close)parent.OSV_close();});
$('#say').onsubmit=e=>{e.preventDefault();const i=$('#say input'),v=i.value.trim();if(!v)return;if(parent.OSV_send&&parent.OSV_send(v)){i.value='';i.placeholder='보냈어요 — 맡은 부서가 작업 중으로 바뀌어요';setTimeout(load,2500);}};
window.OSV_scene=()=>'office';window.OSV_toggle=()=>{};
function split(){let on=false;try{on=parent.document.body.classList.contains('tch-real')&&parent.innerWidth>=1000;}catch(e){}document.body.classList.toggle('split',on);}
split();addEventListener('resize',split);try{parent.addEventListener('resize',split);}catch(e){}
load();setInterval(load,5000);
})();
