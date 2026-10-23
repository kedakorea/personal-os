"""브랜디움 사이트 페이지 나누기 (2026-10-23)
원본은 _src/onepage.html (한 장짜리). 고칠 때는 원본을 고치고 이걸 다시 돌린다:  python3 _src/build.py
→ index.html(메인) · os/ · how/ · shop/ · about/ 를 만든다. 각 페이지는 같은 원본에서 자기 칸만 보이게 한다."""
import re, os
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
src = open(os.path.join(R, "_src/onepage.html")).read()

# 원본 칸 순서대로 어느 페이지에 보일지
PG = ["home", "home", "home", "home", "home", "os", "os", "home", "home", "os", "os", "os", "os", "os", "os", "os", "os",
      "home shop", "how", "how", "about", "home os how shop about", "about", "how shop"]
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
    "shop": ("shop/", "상점 — 퍼스널 OS 세팅 · 칩 상점 | 브랜디움 BRAND!UM", ("SHOP", "브랜디움<br>상점", "퍼스널 OS 세팅부터, 칩으로 하나씩 더하는 업무·디자인 상품까지.")),
    "about": ("about/", "브랜디움 소개 — 브랜디움 BRAND!UM", ("ABOUT", "브랜디움과<br>캐다", "바쁜 대표가 만든, 대표를 위한 운영체제.")),
}

CSS = """
/* 페이지 나누기 (2026-10-23) */
section[data-pg]{display:none}
body[data-pg=home] section[data-pg~=home],body[data-pg=os] section[data-pg~=os],body[data-pg=how] section[data-pg~=how],body[data-pg=shop] section[data-pg~=shop],body[data-pg=about] section[data-pg~=about]{display:block}
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
.items{margin-top:26px;border-top:2px solid var(--ink)}
.item{display:grid;grid-template-columns:86px 1fr auto;gap:14px;align-items:center;padding:16px 4px;border-bottom:1px solid rgba(67,47,46,.18)}
.item .tier{font-size:12px;font-weight:800;opacity:.6}
.item b{font-size:16.5px}.item p{font-size:14px;opacity:.72;margin-top:3px;line-height:1.6}
.item .get{display:flex;align-items:center;gap:10px;white-space:nowrap}
.item .c{font-family:'Josefin Sans',Pretendard;font-weight:800;font-size:18px}
.item button{font:800 14px Pretendard;padding:9px 14px;border-radius:10px;border:2px solid var(--ink);background:#fff;color:var(--ink);cursor:pointer}
.item button:hover{background:var(--ink);color:#fffaf0}.item.soon{opacity:.5}.item.soon button{cursor:default}
.item.mine button{background:var(--cream)}
@media(max-width:640px){.item{grid-template-columns:1fr auto}.item .tier{grid-column:1/-1}}
.chiprule{margin-top:22px;font-size:13.5px;line-height:1.8;opacity:.75}
.teaser-chip{display:flex;gap:20px;align-items:center;justify-content:space-between;flex-wrap:wrap;background:#fff;border:2px solid var(--ink);border-radius:24px;padding:26px 28px;margin-top:26px}
.teaser-chip b{font-size:22px}.teaser-chip p{opacity:.75;margin-top:6px}
.teaser-chip a{background:var(--ink);color:#fffaf0;text-decoration:none;font-weight:800;padding:14px 22px;border-radius:14px}
"""

MORE = """<section class="pad light" data-pg="home" id="more">
 <div class="reveal"><span class="label">MORE</span><h2>더 알아보기</h2>
 <div class="more">
  <a href="os/"><i>🧠</i><b>퍼스널 OS란?</b><span>부서·매니저·업무 앱, 휴대폰으로 일하는 법, 실제 화면</span></a>
  <a href="how/"><i>🛠</i><b>진행 방식 · FAQ</b><span>설문 → 인터뷰 → 세팅 → 교육 → 30일 지원, 자주 묻는 질문</span></a>
  <a href="shop/"><i>🪙</i><b>상점</b><span>세팅 상품과 칩으로 사는 업무·디자인 상품</span></a>
  <a href="about/"><i>👋</i><b>브랜디움 소개</b><span>만든 사람과 운영사 캐다</span></a>
 </div></div>
</section>
"""

TEASER = """<section class="pad cream" data-pg="home" id="chipteaser">
 <div class="reveal"><span class="label">CHIP SHOP</span><h2>작게 더하고 싶을 땐,<br>칩 3개 1,000원부터</h2>
 <div class="teaser-chip"><div><b>🪙 칩 상점</b><p>회의록 정리 규칙, 견적서 양식, 카드뉴스 템플릿처럼 필요한 업무를 하나씩 내 OS에 더하세요. 칩 1개부터 받을 수 있어요.</p></div><a href="shop/#chips">칩 상점 보기 →</a></div></div>
</section>
"""

SHOP = """<section class="pad light" data-pg="shop" id="chips">
 <div class="reveal"><span class="label">CHIP SHOP</span><h2>칩 상점</h2>
 <p class="chips-why">칩은 브랜디움 전용 캐시입니다. 한 번 충전해 두면 업무 지시서·템플릿·자동 업무를 필요할 때마다 하나씩 받아 내 퍼스널 OS에 더할 수 있어요. 받은 상품은 담당 매니저가 1영업일 안에 대표님 OS에 설치해 드립니다.</p>
 <div class="wallet" id="wallet"><span>🪙 내 칩</span><span id="wbal"><a href="account/">로그인하면 보여요</a></span></div>
 <div class="packs">
  <div class="pack"><div class="n">1<small>칩</small></div><div class="w">400원</div><div class="per">낱개</div><a href="order/?p=chip1">충전하기</a></div>
  <div class="pack best"><span class="rib">가장 많이 사요</span><div class="n">3<small>칩</small></div><div class="w">1,000원</div><div class="per">칩당 333원</div><a href="order/?p=chip3">충전하기</a></div>
  <div class="pack"><div class="n">10<small>칩</small></div><div class="w">3,000원</div><div class="per">칩당 300원</div><a href="order/?p=chip10">충전하기</a></div>
  <div class="pack"><span class="rib">+보너스 3칩</span><div class="n">33<small>칩</small></div><div class="w">8,000원</div><div class="per">칩당 242원</div><a href="order/?p=chip30">충전하기</a></div>
 </div>
 <p class="chiprule" style="margin-top:6px">VAT 포함 · 칩은 퍼스널 OS 세팅을 받으신 분(또는 받으실 분)의 OS에 설치되는 상품용입니다.</p>
 <div class="items" id="items"><p style="padding:18px 0;opacity:.6">상품을 불러오는 중…</p></div>
 <p class="chiprule">· 칩은 충전 후 7일 안, 하나도 쓰지 않았으면 전액 환불됩니다. 일부를 쓴 뒤에는 쓴 칩을 1개 400원으로 계산해 뺀 나머지를 돌려드려요. 보너스 칩은 환불되지 않습니다.<br>· 칩으로 받은 상품은 받는 즉시 내 OS에 설치되는 디지털 상품이라 취소·환불되지 않습니다. 설명대로 작동하지 않으면 칩으로 돌려드립니다.<br>· 유효기간: 충전한 칩 5년 · 보너스 칩 1년. 자세한 내용은 <a href="refund/">환불 규정</a>을 확인해 주세요.</p>
 </div>
</section>
"""

SHOPJS = """<script src="https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2"></script><script src="os.js"></script>
<script>
/* 칩 상점 (2026-10-23) */
(async function(){
 const sb = supabase.createClient(OS_URL, OS_ANON), box = document.getElementById("items"), E = osEsc;
 const [{ data: it }, { data: ss }] = await Promise.all([sb.from("shop_items").select("*").order("sort"), sb.auth.getSession()]);
 const u = ss.session && ss.session.user; let bal = null, mine = new Set();
 async function load() {
  if (!u) return;
  const [{ data: b }, { data: l }] = await Promise.all([sb.rpc("chip_balance"), sb.from("chip_ledger").select("item_key,status").not("item_key", "is", null)]);
  bal = b || 0; mine = new Set((l || []).filter((x) => x.status !== "취소").map((x) => x.item_key));
  document.getElementById("wbal").innerHTML = `<b>${bal}</b> 칩 · <a href="account/">내역 보기</a>`;
 }
 function draw() {
  box.innerHTML = (it || []).map((x) => `<div class="item ${x.active ? "" : "soon"} ${mine.has(x.key) ? "mine" : ""}"><span class="tier">${E(x.tier || "")}</span>
   <div><b>${E(x.name)}</b><p>${E(x.summary || "")}</p></div>
   <div class="get"><span class="c">${x.chips ? x.chips + " 칩" : "무료"}</span>${!x.active ? "<button disabled>출시 예정</button>" : mine.has(x.key) ? "<button disabled>받음 ✓</button>" : `<button data-k="${E(x.key)}">받기</button>`}</div></div>`).join("");
  box.querySelectorAll("button[data-k]").forEach((b) => b.onclick = () => get(b.dataset.k));
 }
 async function get(k) {
  const x = it.find((y) => y.key === k);
  if (!u) { sessionStorage.setItem("after_login", location.href); return location.href = "account/"; }
  if (!confirm(`'${x.name}'을(를) ${x.chips ? x.chips + "칩으로 " : ""}받을까요?\\n\\n받은 상품은 바로 내 OS에 설치되는 디지털 상품이라 취소·환불되지 않습니다.`)) return;
  const { data, error } = await sb.rpc("buy_item", { k });
  if (error) { alert(error.message.includes("부족") ? error.message + "\\n칩을 먼저 충전해 주세요." : error.message); return; }
  alert(`받았습니다! 담당 매니저가 1영업일 안에 대표님 OS에 설치해 드려요.\\n남은 칩: ${data.balance}`);
  await load(); draw();
 }
 await load(); draw();
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
    nav = ('<div class="links"><a href="os/"%s>OS</a><a href="how/"%s>HOW</a><a href="shop/"%s>SHOP</a><a href="how/#faq">FAQ</a><a href="about/"%s>ABOUT</a><a href="#apply">APPLY</a></div>'
           % (on("os"), on("how"), on("shop"), on("about")))
    t = t.replace(NAV_OLD, nav, 1)
    # 메인 섹션 링크(#what 등)가 다른 페이지로 옮겨간 것 바로잡기
    for a, b in [('href="#price"', 'href="shop/"' if pg != "home" else 'href="#price"'), ('href="#how"', 'href="how/"'), ('href="#faq"', 'href="how/#faq"'),
                 ('href="#what"', 'href="os/"'), ('href="#mobile"', 'href="os/#mobile"'), ('href="#screens"', 'href="os/#screens"'), ('href="#about"', 'href="about/"')]:
        t = t.replace(a, b)
    # 새 칸 넣기
    price_end = t.index("</section>", t.index('id="price"')) + len("</section>")
    t = t[:price_end] + "\n" + TEASER + SHOP + t[price_end:]
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
    if pg == "shop":
        t = t.replace("</body>", SHOPJS + "</body>")
    d = os.path.join(R, path)
    os.makedirs(d, exist_ok=True)
    open(os.path.join(d, "index.html"), "w").write(t)
    return path or "index.html"

for p in PAGES:
    print("만듦", build(p))
