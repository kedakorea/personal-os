"""브랜디움 사이트 페이지 나누기 (2026-10-23)
원본은 _src/onepage.html (한 장짜리). 고칠 때는 원본을 고치고 이걸 다시 돌린다:  python3 _src/build.py
→ index.html(메인) · os/ · how/ · shop/ · about/ 를 만든다. 각 페이지는 같은 원본에서 자기 칸만 보이게 한다."""
import re, os
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
src = open(os.path.join(R, "_src/onepage.html")).read()

# 원본 칸 순서대로 어느 페이지에 보일지
PG = ["home", "home", "home", "home", "home", "os", "os", "home", "home", "os", "os", "os", "os", "os", "os", "os", "os",
      "home shop", "how", "how", "home", "home os how shop chips", "home", "how shop chips"]
secs = list(re.finditer(r"<section\b", src))
assert len(secs) == len(PG), (len(secs), len(PG))
out, last = [], 0
for m, pg in zip(secs, PG):
    out.append(src[last:m.end()]); out.append(' data-pg="%s"' % pg); last = m.end()
out.append(src[last:]); s = "".join(out)

PAGES = {
    "home": ("", "브랜디움 BRAND!UM — 퍼스널 OS, 나 대신 일하는 AI 시스템", None),
    "os": ("os/", "퍼스널 OS란? — 브랜디움 BRAND!UM", ("WHAT IS PERSONAL OS", "퍼스널 OS는<br>이렇게 일합니다", "도구가 아니라 조직. 대표님 업무에 맞춘 부서·매니저·업무 앱이 휴대폰 한 대로 움직입니다.")),
    "how": ("how/", "진행 방식 · 자주 묻는 질문 — 브랜디움 BRAND!UM", ("HOW IT WORKS · FAQ", "어떻게<br>진행되나요?", "상담부터 세팅, 30일 적응 지원까지. 미리 알아 두실 것도 모았습니다.")),
    "shop": ("shop/", "세팅 상품 — 퍼스널 OS 방문형·원격형 | 브랜디움 BRAND!UM", ("SHOP", "퍼스널 OS<br>세팅 상품", "대표님 업무에 맞춘 AI 비서 조직을 통째로 세팅해 드립니다. 방문형과 원격형 중에 고르세요.")),
    "chips": ("chips/", "칩 상점 — 내 OS에 업무를 하나씩 더하기 | 브랜디움 BRAND!UM", ("CHIP SHOP", "칩<br>상점", "칩 3개 1,000원부터. 업무 지시서·템플릿·자동 업무를 받아 채팅창에 붙여넣으면 바로 설치돼요.")),
}

CSS = """
/* 페이지 나누기 (2026-10-23) */
section[data-pg]{display:none}
body[data-pg=home] section[data-pg~=home],body[data-pg=os] section[data-pg~=os],body[data-pg=how] section[data-pg~=how],body[data-pg=shop] section[data-pg~=shop],body[data-pg=chips] section[data-pg~=chips]{display:block}
body[data-pg=home] section[data-pg~=home][hidden],body[data-pg=os] section[data-pg~=os][hidden]{display:none}
.pghead{background:var(--cream);padding:70px calc(var(--frame) + 14px) 54px;border-radius:0 0 28px 28px}
.pghead .label{display:inline-block;margin-bottom:14px}
.pghead h1{font-size:clamp(34px,6vw,64px);line-height:1.15;letter-spacing:-.02em}
.pghead p{margin-top:16px;font-size:17px;opacity:.75;max-width:640px}
.more{display:grid;grid-template-columns:repeat(4,1fr);gap:14px;margin-top:26px}
.more a{display:block;background:#fff;border:2px solid var(--ink);border-radius:20px;padding:22px 20px;text-decoration:none;transition:transform .2s}
.more a:hover{transform:translateY(-3px)}
.more b{display:block;font-size:19px;margin:8px 0 6px}.more span{font-size:14px;opacity:.7;line-height:1.6}.more i{font-style:normal;font-size:26px}
@media(max-width:860px){.more{grid-template-columns:1fr 1fr}}
.chips-why{font-size:16px;opacity:.8;margin-top:12px;max-width:680px;line-height:1.75}
.packs{display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin:28px 0 10px}
.pack{background:#fff;border:2px solid var(--ink);border-radius:20px;padding:20px 18px;text-align:center;position:relative}
.pack .n{font-family:'Josefin Sans',Pretendard;font-weight:800;font-size:34px;line-height:1}.pack .n small{font-size:15px;margin-left:3px}
.pack .w{font-size:20px;font-weight:800;margin:10px 0 2px}.pack .per{font-size:12.5px;opacity:.6}
.pack a{display:block;margin-top:14px;padding:11px;border-radius:12px;background:var(--ink);color:#fffaf0;text-decoration:none;font-weight:800;font-size:15px}
.pack.best{background:var(--butter2)}.pack .rib{position:absolute;top:-11px;left:50%;transform:translateX(-50%);background:var(--ink);color:#fffaf0;font-size:11px;font-weight:800;padding:3px 10px;border-radius:99px;white-space:nowrap}
@media(max-width:860px){.packs{grid-template-columns:1fr 1fr}}
.wallet{display:flex;justify-content:space-between;align-items:center;gap:10px;background:var(--ink);color:#fffaf0;border-radius:16px;padding:14px 18px;margin:18px 0 6px;font-size:15px}
.wallet b{font-size:20px}.wallet a{color:var(--cream)}
.ftabs{display:flex;gap:8px;flex-wrap:wrap;margin:34px 0 18px}
.ftabs button{font:800 14px Pretendard;padding:9px 16px;border-radius:99px;border:2px solid var(--ink);background:#fff;color:var(--ink);cursor:pointer}
.ftabs button.on{background:var(--ink);color:#fffaf0}
@media(max-width:700px){.ftabs{flex-wrap:nowrap;overflow-x:auto;padding-bottom:4px;margin-right:calc(-1 * var(--frame) - 14px)}.ftabs button{flex:none}}
.grid{display:grid;grid-template-columns:repeat(4,1fr);gap:18px}
@media(max-width:1000px){.grid{grid-template-columns:repeat(3,1fr)}}@media(max-width:700px){.grid{grid-template-columns:1fr 1fr;gap:12px}}
.prd{background:#fff;border:2px solid var(--ink);border-radius:20px;overflow:hidden;cursor:pointer;display:flex;flex-direction:column;transition:transform .18s,box-shadow .18s}
.prd:hover{transform:translateY(-4px);box-shadow:0 10px 0 var(--ink)}
.prd .th{aspect-ratio:4/3;display:flex;align-items:center;justify-content:center;position:relative;border-bottom:2px solid var(--ink)}
.prd .th i{font-style:normal;font-size:clamp(46px,7vw,72px);filter:drop-shadow(0 4px 0 rgba(67,47,46,.18))}
.prd .th em{position:absolute;left:10px;bottom:10px;font-style:normal;font-size:11px;font-weight:800;background:#fffaf0;border:1.5px solid var(--ink);border-radius:99px;padding:3px 9px}
.prd .bd{position:absolute;right:10px;top:10px;font-size:11px;font-weight:900;letter-spacing:.04em;padding:4px 9px;border-radius:99px;background:var(--ink);color:#fffaf0}
.prd .bd.NEW{background:#e8573f}.prd .bd.무료{background:#2f9e6b}.prd .bd.출시{background:#999}
.prd .tx{padding:14px 14px 16px;display:flex;flex-direction:column;gap:6px;flex:1}
.prd .nm{font-weight:800;font-size:15.5px;line-height:1.35}
.prd .sm{font-size:12.5px;opacity:.65;line-height:1.55;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden}
.prd .pr{margin-top:auto;display:flex;align-items:baseline;gap:6px;padding-top:6px}
.prd .pr b{font-family:'Josefin Sans',Pretendard;font-size:21px}.prd .pr small{font-size:11.5px;opacity:.55}
.prd .go{margin-top:8px;font:800 14px Pretendard;padding:10px;border-radius:12px;border:0;background:var(--ink);color:#fffaf0;cursor:pointer}
.prd .go[disabled]{background:#ddd;color:#777;cursor:default}.prd.mine .go{background:var(--cream);color:var(--ink)}
.prd.soon{opacity:.6}
.t-지시서{background:#c4dae8}.t-업무{background:#feefb8}.t-디자인{background:#f6c9c0}.t-자동{background:#cfe3c4}.t-서비스{background:#d9cdea}.t-맛보기{background:#fffaf0}.t-캐다{background:#ead9c6}
.pm{position:fixed;inset:0;background:rgba(30,20,20,.55);z-index:80;display:flex;align-items:center;justify-content:center;padding:18px}
.pm[hidden]{display:none}
.pm .box{background:#fffaf0;border:2px solid var(--ink);border-radius:24px;max-width:760px;width:100%;max-height:90vh;overflow:auto;display:grid;grid-template-columns:280px 1fr}
@media(max-width:700px){.pm .box{grid-template-columns:1fr}.pm .th{aspect-ratio:2/1!important}}
.pm .th{aspect-ratio:1/1;display:flex;align-items:center;justify-content:center;border-right:2px solid var(--ink);position:relative}
.pm .th i{font-style:normal;font-size:96px}
.pm .in{padding:24px 24px 22px;position:relative}
.pm .x{position:absolute;right:14px;top:12px;border:0;background:none;font-size:24px;cursor:pointer;color:var(--ink)}
.pm .tg{font-size:12px;font-weight:800;opacity:.6}.pm h3{font-size:24px;margin:4px 0 6px;line-height:1.3}
.pm .pp{font-family:'Josefin Sans',Pretendard;font-weight:800;font-size:26px}.pm .pp small{font-family:Pretendard;font-size:13px;opacity:.55;margin-left:6px;font-weight:600}
.pm h4{font-size:14px;margin:18px 0 8px}.pm p.w{font-size:14.5px;line-height:1.7}
.pm .say span{display:inline-block;background:var(--ink);color:#fffaf0;border-radius:16px 16px 4px 16px;padding:7px 12px;font-size:13.5px;margin:0 6px 6px 0}
.pm ul{list-style:none;font-size:14px;line-height:1.9}.pm li:before{content:"✓ ";font-weight:800}
.pm .buy{width:100%;margin-top:18px;font:800 16px Pretendard;padding:15px;border-radius:14px;border:0;background:var(--ink);color:#fffaf0;cursor:pointer}
.pm .buy[disabled]{background:#ddd;color:#777}
.pm .nt{font-size:12px;opacity:.6;margin-top:10px;line-height:1.6}
.pm .steps3{padding-left:20px;font-size:14px;line-height:1.9}.pm .ptxt{width:100%;height:150px;margin-top:12px;border:1.5px solid var(--sand);border-radius:12px;padding:10px;font:12.5px/1.6 ui-monospace,Menlo,monospace;background:#fff;color:var(--ink);resize:vertical}
.chiprule{margin-top:22px;font-size:13.5px;line-height:1.8;opacity:.75}
.svc{display:grid;grid-template-columns:1fr 1fr;gap:20px;margin-top:22px}@media(max-width:760px){.svc{grid-template-columns:1fr}}
.sv{display:block;background:#fff;border:2px solid var(--ink);border-radius:24px;overflow:hidden;text-decoration:none;transition:transform .2s,box-shadow .2s}.sv:hover{transform:translateY(-4px);box-shadow:0 10px 0 var(--ink)}
.sv .im{aspect-ratio:16/9;background:#eee center/cover;border-bottom:2px solid var(--ink);position:relative}.sv .im span{position:absolute;left:14px;top:14px;background:var(--ink);color:#fffaf0;font-size:11.5px;font-weight:800;padding:4px 10px;border-radius:99px}
.sv .tx{padding:20px 22px 22px}.sv em{font-style:normal;font-size:12.5px;font-weight:800;opacity:.6}.sv b{display:block;font-size:22px;margin:4px 0 8px}.sv p{font-size:14.5px;opacity:.75;line-height:1.7}
.sv .pr{margin-top:14px;display:flex;align-items:baseline;gap:8px;flex-wrap:wrap}.sv .pr s{opacity:.45;font-size:14px}.sv .pr strong{font-size:26px}.sv .pr small{font-size:12px;opacity:.55}
.sv .go{display:block;margin-top:14px;text-align:center;background:var(--ink);color:#fffaf0;font-weight:800;padding:13px;border-radius:14px}
.teaser-chip{display:flex;gap:20px;align-items:center;justify-content:space-between;flex-wrap:wrap;background:#fff;border:2px solid var(--ink);border-radius:24px;padding:26px 28px;margin-top:26px}
.teaser-chip b{font-size:22px}.teaser-chip p{opacity:.75;margin-top:6px}
.teaser-chip a{background:var(--ink);color:#fffaf0;text-decoration:none;font-weight:800;padding:14px 22px;border-radius:14px}
"""

MORE = """<section class="pad light" data-pg="home" id="more">
 <div class="reveal"><span class="label">MORE</span><h2>더 알아보기</h2>
 <div class="more">
  <a href="os/"><i>🧠</i><b>퍼스널 OS란?</b><span>부서·매니저·업무 앱, 휴대폰으로 일하는 법, 실제 화면</span></a>
  <a href="how/"><i>🛠</i><b>진행 방식 · FAQ</b><span>설문 → 인터뷰 → 세팅 → 교육 → 30일 지원, 자주 묻는 질문</span></a>
  <a href="shop/"><i>🛍️</i><b>세팅 상품</b><span>방문형·원격형 상세보기와 일정 예약</span></a>
  <a href="chips/"><i>🪙</i><b>칩 상점</b><span>칩으로 하나씩 더하는 업무·디자인 상품</span></a>
 </div></div>
</section>
"""

TEASER = """<section class="pad cream" data-pg="home" id="chipteaser">
 <div class="reveal"><span class="label">CHIP SHOP</span><h2>작게 더하고 싶을 땐,<br>칩 3개 1,000원부터</h2>
 <div class="teaser-chip"><div><b>🪙 칩 상점</b><p>회의록 정리 규칙, 견적서 양식, 카드뉴스 템플릿처럼 필요한 업무를 하나씩 내 OS에 더하세요. 칩 1개부터 받을 수 있어요.</p></div><a href="chips/">칩 상점 보기 →</a></div></div>
</section>
"""

SVC = """<section class="pad light" data-pg="shop" id="svc">
 <div class="reveal"><span class="label">PRODUCTS</span><h2>두 가지 중에 고르세요</h2>
 <div class="svc">
  <a class="sv" href="product/?p=visit"><div class="im" style="background-image:url(dash/07.jpg)"><span>LAUNCHING EVENT</span></div><div class="tx"><em>☕ VISIT · 방문형</em><b>퍼스널 OS 방문형 세팅</b><p>노트북 들고 브랜디움 라운지로. 마주 앉아 처음부터 끝까지 옆에서 세팅해 드려요. 컴퓨터가 낯선 분께 추천.</p><div class="pr"><s>2,500,000원</s><strong>990,000원</strong><small>VAT 포함</small></div><span class="go">자세히 보고 예약하기 →</span></div></a>
  <a class="sv" href="product/?p=remote"><div class="im" style="background-image:url(dash/04.jpg)"><span>LAUNCHING EVENT</span></div><div class="tx"><em>💻 REMOTE · 원격형</em><b>퍼스널 OS 원격형 세팅</b><p>화상 인터뷰와 원격 접속으로 전국 어디서나. 늘 켜 두는 데스크톱에 세팅하면 가장 좋아요.</p><div class="pr"><s>2,200,000원</s><strong>880,000원</strong><small>VAT 포함</small></div><span class="go">자세히 보고 예약하기 →</span></div></a>
 </div>
 <p class="chiprule">두 상품 모두 사전 설문 · 업무 인터뷰 · 설계서 · 세팅 · 사용 교육 · 30일 적응 지원 포함 · Claude 구독료(월 $100)는 별도</p>
 <div class="teaser-chip" style="margin-top:30px"><div><b>🪙 이미 세팅을 받으셨나요?</b><p>칩 상점에서 회의록 규칙·견적서 양식·카드뉴스 템플릿 같은 업무를 하나씩 더할 수 있어요.</p></div><a href="chips/">칩 상점 가기 →</a></div>
 </div>
</section>
"""

SHOP = """<section class="pad light" data-pg="chips" id="chips">
 <div class="reveal">
 <p class="chips-why" style="margin-top:0">칩은 브랜디움 전용 캐시입니다. 한 번 충전해 두면 업무 지시서·템플릿·자동 업무를 필요할 때마다 하나씩 받아 내 퍼스널 OS에 더할 수 있어요. 받으면 바로 <b>설치 문구</b>가 나와요. 내 퍼스널 OS 채팅창에 붙여넣기만 하면 매니저가 알아서 설치합니다. 기다릴 필요 없어요.</p>
 <div class="wallet" id="wallet"><span>🪙 내 칩</span><span id="wbal"><a href="account/">로그인하면 보여요</a></span></div>
 <div class="packs">
  <div class="pack"><div class="n">1<small>칩</small></div><div class="w">400원</div><div class="per">낱개</div><a href="order/?p=chip1">충전하기</a></div>
  <div class="pack best"><span class="rib">가장 많이 사요</span><div class="n">3<small>칩</small></div><div class="w">1,000원</div><div class="per">칩당 333원</div><a href="order/?p=chip3">충전하기</a></div>
  <div class="pack"><div class="n">10<small>칩</small></div><div class="w">3,000원</div><div class="per">칩당 300원</div><a href="order/?p=chip10">충전하기</a></div>
  <div class="pack"><span class="rib">+보너스 3칩</span><div class="n">33<small>칩</small></div><div class="w">8,000원</div><div class="per">칩당 242원</div><a href="order/?p=chip30">충전하기</a></div>
 </div>
 <p class="chiprule" style="margin-top:6px">VAT 포함 · 칩은 퍼스널 OS 세팅을 받으신 분(또는 받으실 분)의 OS에 설치되는 상품용입니다.</p>
 <div class="ftabs" id="ftabs"></div>
 <div class="grid" id="items"><p style="padding:18px 0;opacity:.6">상품을 불러오는 중…</p></div>
 <p class="chiprule">· 칩은 충전 후 7일 안, 하나도 쓰지 않았으면 전액 환불됩니다. 일부를 쓴 뒤에는 쓴 칩을 1개 400원으로 계산해 뺀 나머지를 돌려드려요. 보너스 칩은 환불되지 않습니다.<br>· 칩으로 받은 상품은 받는 즉시 내 OS에 설치되는 디지털 상품이라 취소·환불되지 않습니다. 설명대로 작동하지 않으면 칩으로 돌려드립니다.<br>· 유효기간: 충전한 칩 5년 · 보너스 칩 1년. 자세한 내용은 <a href="refund/">환불 규정</a>을 확인해 주세요.</p>
 </div>
</section>
"""

SHOPJS = """<script src="https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2"></script><script src="os.js"></script>
<div class="pm" id="pm" hidden><div class="box"><div class="th" id="pmth"></div><div class="in" id="pmin"></div></div></div>
<script>
/* 칩 상점 — 쇼핑몰형 (2026-10-23) */
(async function(){
 const sb = supabase.createClient(OS_URL, OS_ANON), box = document.getElementById("items"), E = osEsc, pm = document.getElementById("pm");
 const [{ data: it }, { data: ss }] = await Promise.all([sb.from("shop_items").select("*").order("sort"), sb.auth.getSession()]);
 const u = ss.session && ss.session.user; let bal = null, mine = new Set(), cat = "전체";
 const TC = (t) => "t-" + String(t || "").split(" ")[0];
 const CATS = ["전체", ...[...new Set((it || []).map((x) => x.tier))]];
 async function load() {
  if (!u) return;
  const [{ data: b }, { data: l }] = await Promise.all([sb.rpc("chip_balance"), sb.from("chip_ledger").select("item_key,status").not("item_key", "is", null)]);
  bal = b || 0; mine = new Set((l || []).filter((x) => x.status !== "취소").map((x) => x.item_key));
  document.getElementById("wbal").innerHTML = `<b>${bal}</b> 칩 · <a href="account/">내역 보기</a>`;
 }
 const own = (x) => mine.has(x.key) && x.tier !== "서비스";
 const btn = (x) => !x.active ? ["출시 예정", true] : own(x) ? ["설치 문구 보기", false] : [x.chips ? "받기" : "무료로 받기", false];
 function draw() {
  document.getElementById("ftabs").innerHTML = CATS.map((c) => `<button class="${c === cat ? "on" : ""}" data-c="${E(c)}">${E(c)}</button>`).join("");
  document.querySelectorAll("#ftabs button").forEach((b) => b.onclick = () => { cat = b.dataset.c; draw(); });
  box.innerHTML = (it || []).filter((x) => cat === "전체" || x.tier === cat).map((x) => { const [bt, dis] = btn(x); return `<div class="prd ${x.active ? "" : "soon"} ${own(x) ? "mine" : ""}" data-k="${E(x.key)}">
   <div class="th ${TC(x.tier)}"><i>${x.icon || "📦"}</i><em>${E(x.tier || "")}</em>${x.badge ? `<span class="bd ${E(String(x.badge).split(" ")[0])}">${E(x.badge)}</span>` : ""}</div>
   <div class="tx"><div class="nm">${E(x.name)}</div><div class="sm">${E(x.summary || "")}</div>
   <div class="pr"><b>${x.chips ? "🪙 " + x.chips + "칩" : "무료"}</b>${x.chips ? "" : "<small>가입 선물</small>"}</div>
   <button class="go" data-b="${E(x.key)}" ${dis ? "disabled" : ""}>${bt}</button></div></div>`; }).join("");
  box.querySelectorAll(".prd").forEach((c) => c.onclick = (e) => { if (e.target.closest("button.go")) return; open(c.dataset.k); });
  box.querySelectorAll("button.go").forEach((b) => b.onclick = () => own(it.find((y) => y.key === b.dataset.b)) ? showPrompt(b.dataset.b) : get(b.dataset.b));
 }
 function open(k) {
  const x = it.find((y) => y.key === k), d = x.detail || {}, [bt, dis] = btn(x);
  document.getElementById("pmth").className = "th " + TC(x.tier);
  document.getElementById("pmth").innerHTML = `<i>${x.icon || "📦"}</i>`;
  document.getElementById("pmin").innerHTML = `<button class="x" aria-label="닫기">✕</button><div class="tg">${E(x.tier || "")}${x.badge ? " · " + E(x.badge) : ""}</div><h3>${E(x.name)}</h3>
   <div class="pp">${x.chips ? "🪙 " + x.chips + "칩" : "무료"}</div>
   <h4>무엇을 해 주나요</h4><p class="w">${E(d.what || x.summary || "")}</p>
   ${(d.say || []).length ? `<h4>이렇게 말하면 돼요</h4><div class="say">${d.say.map((s) => `<span>${E(s)}</span>`).join("")}</div>` : ""}
   ${(d.get || []).length ? `<h4>받으면 생기는 것</h4><ul>${d.get.map((s) => `<li>${E(s)}</li>`).join("")}</ul>` : ""}
   <button class="buy" ${dis ? "disabled" : ""}>${bt}</button>
   <p class="nt">${x.tier === "서비스" ? "받으면 담당자가 1영업일 안에 연락드려 일정을 잡습니다." : "받으면 바로 설치 문구가 나와요. 내 퍼스널 OS 채팅창에 붙여넣으면 매니저가 알아서 설치합니다."} 받은 상품은 디지털 상품이라 취소·환불되지 않습니다(작동하지 않으면 칩으로 돌려드림).</p>`;
  pm.hidden = false;
  pm.querySelector(".x").onclick = () => pm.hidden = true;
  pm.querySelector(".buy").onclick = () => own(x) ? showPrompt(k) : get(k);
 }
 pm.addEventListener("click", (e) => { if (e.target === pm) pm.hidden = true; });
 addEventListener("keydown", (e) => { if (e.key === "Escape") pm.hidden = true; });
 async function get(k) {
  const x = it.find((y) => y.key === k);
  if (!u) { sessionStorage.setItem("after_login", location.href); return location.href = "account/"; }
  if (!confirm(`'${x.name}'을(를) ${x.chips ? x.chips + "칩으로 " : ""}받을까요?\\n\\n받은 상품은 바로 내 OS에 설치되는 디지털 상품이라 취소·환불되지 않습니다.`)) return;
  const { data, error } = await sb.rpc("buy_item", { k });
  if (error) { if (error.message.includes("부족") && confirm(error.message + "\\n칩 충전 화면으로 갈까요?")) location.href = "order/?p=chip3"; else if (!error.message.includes("부족")) alert(error.message); return; }
  await load(); draw();
  if (data.prompt) return showPrompt(k, data.prompt, data.balance);
  alert(`받았습니다! 담당자가 1영업일 안에 연락드려 일정을 잡아 드려요.\\n남은 칩: ${data.balance}`); pm.hidden = true;
 }
 async function showPrompt(k, txt, left) {
  const x = it.find((y) => y.key === k);
  if (!txt) { const { data } = await sb.from("shop_contents").select("prompt").eq("key", k).maybeSingle(); txt = data && data.prompt; }
  if (!txt) { alert("이 상품은 담당자가 직접 진행합니다. 곧 연락드려요."); return; }
  document.getElementById("pmth").className = "th " + TC(x.tier);
  document.getElementById("pmth").innerHTML = `<i>${x.icon || "📦"}</i>`;
  document.getElementById("pmin").innerHTML = `<button class="x" aria-label="닫기">✕</button><div class="tg">${left != null ? "받기 완료 · 남은 칩 " + left : "받은 상품"}</div><h3>${E(x.name)}</h3>
   <h4>이렇게 설치하세요 — 1분이면 끝</h4>
   <ol class="steps3"><li><b>[설치 문구 복사]</b>를 누르세요</li><li>내 <b>퍼스널 OS 앱 채팅창</b>에 붙여넣고 보내세요</li><li>매니저가 스스로 설치하고 <b>"✅ 설치 완료"</b>로 알려 드려요</li></ol>
   <textarea class="ptxt" readonly>${E(txt)}</textarea>
   <button class="buy" id="cpy">📋 설치 문구 복사</button>
   <p class="nt">이 문구는 마이페이지·상점에서 언제든 다시 볼 수 있어요. 새 버전이 나오면 같은 문구를 다시 붙여넣으면 업데이트됩니다.</p>`;
  pm.hidden = false;
  pm.querySelector(".x").onclick = () => pm.hidden = true;
  document.getElementById("cpy").onclick = async () => { try { await navigator.clipboard.writeText(txt); } catch (e) { const t = pm.querySelector(".ptxt"); t.select(); document.execCommand("copy"); } document.getElementById("cpy").textContent = "✓ 복사했어요 — 채팅창에 붙여넣으세요"; };
 }
 await load(); draw();
 const q = new URLSearchParams(location.search).get("item"); if (q && it.some((y) => y.key === q)) (own(it.find((y) => y.key === q)) ? showPrompt(q) : open(q));
})();
</script>
"""

NAV_OLD = re.search(r'<div class="links">.*?</div>', s).group(0)

def build(pg):
    path, title, head = PAGES[pg]
    t = s
    t = t.replace("</style>", CSS + "</style>", 1)
    t = re.sub(r"<title>.*?</title>", "<title>%s</title>" % title, t, 1)
    t = t.replace('<link rel="canonical" href="https://mybrandium.com/">', '<link rel="canonical" href="https://mybrandium.com/%s">' % path)
    t = t.replace("<head>", '<head>\n<base href="/">', 1)
    t = re.sub(r"<body([^>]*)>", lambda m: '<body%s data-pg="%s">' % (m.group(1), pg), t, 1)
    on = lambda p: ' class="on"' if p == pg else ""
    nav = ('<div class="links"><a href="os/"%s>OS</a><a href="how/"%s>HOW</a><a href="shop/"%s>SHOP</a><a href="chips/"%s>CHIPS</a><a href="how/#faq">FAQ</a><a href="#apply">APPLY</a></div>'
           % (on("os"), on("how"), on("shop"), on("chips")))
    t = t.replace(NAV_OLD, nav, 1)
    # 메인 섹션 링크(#what 등)가 다른 페이지로 옮겨간 것 바로잡기
    for a, b in [('href="#price"', 'href="shop/"' if pg != "home" else 'href="#price"'), ('href="#how"', 'href="how/"'), ('href="#faq"', 'href="how/#faq"'),
                 ('href="#what"', 'href="os/"'), ('href="#mobile"', 'href="os/#mobile"'), ('href="#screens"', 'href="os/#screens"'), ('href="#about"', 'href="/#about"' if pg != "home" else 'href="#about"')]:
        t = t.replace(a, b)
    # 새 칸 넣기
    price_end = t.index("</section>", t.index('id="price"')) + len("</section>")
    t = t[:price_end] + "\n" + TEASER + SHOP + t[price_end:]
    price_start = t.rindex("<section", 0, t.index('id="price"'))
    t = t[:price_start] + SVC + t[price_start:]
    first = t.index("<section", t.index("<body"))
    if head:
        t = t[:first] + '<section class="pghead" data-pg="%s"><span class="label">%s</span><h1>%s</h1><p>%s</p></section>\n' % ((pg,) + head) + t[first:]
    else:
        notedu_end = t.index("</section>", t.index('id="notedu"')) + len("</section>")
        t = t[:notedu_end] + "\n" + MORE + t[notedu_end:]
    # 메뉴 표시: 같은 페이지 안 칸(#…)만 따라가고, 페이지 메뉴는 고정 표시
    t = t.replace("const as=[...document.querySelectorAll('nav .links a')],secs=as.map(a=>document.querySelector(a.getAttribute('href')));",
                  "const as=[...document.querySelectorAll('nav .links a')].filter(a=>a.getAttribute('href').startsWith('#')),secs=as.map(a=>document.querySelector(a.getAttribute('href')));")
    # <base href="/"> 때문에 #칸 링크가 메인으로 가지 않게: 이 페이지에 그 칸이 보이면 그 자리로 스크롤
    t = t.replace("</body>", """<script>document.addEventListener('click',e=>{const a=e.target.closest('a[href^="#"]');if(!a)return;const el=document.querySelector(a.getAttribute('href'));if(el&&el.offsetParent!==null){e.preventDefault();el.scrollIntoView({behavior:'smooth'});history.replaceState(null,'',location.pathname+a.getAttribute('href'))}});</script>\n</body>""")
    if pg == "shop":   # 예전 주소(shop/#chips, shop/?item=) → 칩 상점
        t = t.replace("<head>", "<head>\n<script>if(location.hash=='#chips'||/[?&]item=/.test(location.search))location.replace('/chips/'+location.search)</script>", 1)
    if pg == "chips":
        t = t.replace("</body>", SHOPJS + "</body>")
    d = os.path.join(R, path)
    os.makedirs(d, exist_ok=True)
    open(os.path.join(d, "index.html"), "w").write(t)
    return path or "index.html"

for p in PAGES:
    print("만듦", build(p))
