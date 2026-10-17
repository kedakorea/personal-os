// 퍼스널 OS 사이트 공용 (2026-10-17) — 백엔드 주소·호출·제안서 그리기
const OS_URL = "https://ergkmihtllkpuiaevvcv.supabase.co";
const OS_ANON = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImVyZ2ttaWh0bGxrcHVpYWV2dmN2Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3OTIyMTc5MDMsImV4cCI6MjEwNzc5MzkwM30.DRB657px48hlg6tmPp16RK2YVfjh6OXDoHXAsono7AY";
async function osCall(body, jwt) {
  const r = await fetch(OS_URL + "/functions/v1/os", { method: "POST",
    headers: { "Content-Type": "application/json", apikey: OS_ANON, Authorization: "Bearer " + (jwt || OS_ANON) },
    body: JSON.stringify(body) });
  let d = {}; try { d = await r.json(); } catch (e) { d = { ok: false, error: "응답을 읽지 못했습니다" }; }
  if (!r.ok && d.ok !== false) d = { ok: false, error: "서버 오류 " + r.status };
  return d;
}
const osEsc = (t) => String(t ?? "").replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));
function osProposal(d, chief, opt) {
  if (!d) return "";
  // 설계 안의 {{호칭}}·{{실장}} 같은 빈칸은 화면에서 실제 말로 보여 준다
  const st = d.설정 || {}, fillT = (v) => typeof v === "string" ? v.split("{{호칭}}").join(st.호칭 || "대표님").split("{{실장}}").join(chief || st.실장 || "매니저").split("{{직함}}").join(st.직함 || "매니저") : Array.isArray(v) ? v.map(fillT) : (v && typeof v === "object") ? Object.fromEntries(Object.entries(v).map(([k, x]) => [k, k === "지침" ? x : fillT(x)])) : v;
  d = fillT(d);
  const ed = opt && opt.edit, ce = ed ? ' contenteditable="true" spellcheck="false"' : "";
  const title = (d.설정 && d.설정.직함) || "매니저";
  const dep = (d.부서 || []).map((x, i) => {
    const sys = (x.폴더 || "").startsWith("00");
    return `<div class="pc" data-i="${i}">${ed && !sys ? `<button class="px" type="button" title="이 부서 빼기">✕</button>` : ""}<div class="no">${osEsc((x.폴더 || "").split("_")[0])}</div><h4 data-e="이름"${sys ? "" : ce}>${osEsc((x.이름 || x.폴더 || "").replace(/^\S+\s/, ""))}</h4><p data-e="일"${ce}>${osEsc(x.일 || "")}</p>${x.예 || ed ? `<div class="ex">“<span data-e="예"${ce}>${osEsc(x.예 || "")}</span>”</div>` : ""}</div>`;
  }).join("") + (ed ? `<button class="padd" type="button" data-add="부서">＋ 부서 추가</button>` : "");
  const li = (a, key) => (a || []).map((x) => `<li${ce}>${osEsc(x)}</li>`).join("") + (ed ? `</ul><button class="padd sm" type="button" data-add="${key}">＋ 항목 추가</button><ul style="display:none">` : "");
  return `<div class="prop${ed ? " edit" : ""}"><div class="plab">PERSONAL OS · PROPOSAL</div>
    <h2><em>${osEsc(d.고객 || "")}</em>의 퍼스널 OS를 이렇게 세팅합니다</h2><p class="plead" data-e="한줄"${ce}>${osEsc(d.한줄 || "")}</p>
    <h3>① ${osEsc(title)}</h3><div class="pchief">${chief ? `<b>${osEsc(chief)} ${osEsc(title)}</b>` : (d.실장후보 || []).map((c) => `<span><b>${osEsc(c.이름)}</b> · ${osEsc(c.뜻 || "")}</span>`).join("")}</div>
    <h3>② 부서 — 일을 나눠 맡습니다</h3><div class="pboss">${osEsc(d.고객 || "")}<small>지시는 ${osEsc(title)}에게 한마디로</small></div><div class="pgrid">${dep}</div>
    <div class="ptwo"><div><h3>③ 알아서 하는 일</h3><ul data-l="자동업무">${li(d.자동업무, "자동업무")}</ul></div><div><h3>④ 꼭 확인받고 하는 일</h3><ul data-l="승인선목록">${li(d.승인선목록, "승인선목록")}</ul></div></div>
    <div class="pfoot">BRANDiUM · 주식회사 캐다 · 퍼스널 OS</div></div>`;
}
// 화면에서 고친 제안서를 설계 데이터로 다시 모은다
function osCollect(root, d) {
  const old = d.부서 || [], out = JSON.parse(JSON.stringify(d));
  const t = (el) => (el ? el.innerText.replace(/\s+/g, " ").trim() : "");
  out.한줄 = t(root.querySelector('[data-e="한줄"]')) || d.한줄;
  let n = 0;
  out.부서 = [...root.querySelectorAll(".pc")].map((c) => {
    const o = c.dataset.i !== undefined && c.dataset.i !== "" ? old[+c.dataset.i] : null;
    const name = t(c.querySelector('[data-e="이름"]')) || "새 부서", job = t(c.querySelector('[data-e="일"]')), ex = t(c.querySelector('[data-e="예"]'));
    if (o && (o.폴더 || "").startsWith("00")) return Object.assign({}, o, { 일: job || o.일, 예: ex });
    n++; const no = String(n).padStart(2, "0"), clean = name.replace(/[\\/:*?"<>|\s]/g, "");
    const base = o ? Object.assign({}, o) : { 말: [name], 지침: `## 맡는 일\n${job}\n\n## 일하는 방식\n- 처음 하는 종류의 일이면 초안을 먼저 보여 드리고 확인받은 뒤 완성한다.\n\n## 기준·양식\n- 첫 작업 때 채운다.\n\n## 주의\n- 밖으로 보내는 일은 {{호칭}} 확인 후에만 한다.` };
    return Object.assign(base, { 폴더: `${no}_${clean}`, 이름: `${no} ${name}`, 일: job, 예: ex });
  });
  for (const key of ["자동업무", "승인선목록"]) { const ul = root.querySelector(`ul[data-l="${key}"]`); if (ul) out[key] = [...root.querySelectorAll(`ul[data-l="${key}"] li`)].map(t).filter(Boolean); }
  return out;
}
function osEditBind(root, onChange) {
  root.addEventListener("click", (e) => {
    const x = e.target.closest(".px"); if (x) { x.closest(".pc").remove(); onChange(); return; }
    const a = e.target.closest("[data-add]"); if (!a) return;
    if (a.dataset.add === "부서") { a.insertAdjacentHTML("beforebegin", `<div class="pc"><button class="px" type="button">✕</button><div class="no">새</div><h4 data-e="이름" contenteditable="true">새 부서</h4><p data-e="일" contenteditable="true">맡을 일을 적어 주세요</p><div class="ex">“<span data-e="예" contenteditable="true">이렇게 지시할 거예요</span>”</div></div>`); const h = a.previousElementSibling.querySelector("h4"); h.focus(); document.getSelection().selectAllChildren(h); }
    else { const ul = root.querySelector(`ul[data-l="${a.dataset.add}"]`); ul.insertAdjacentHTML("beforeend", `<li contenteditable="true"></li>`); ul.lastElementChild.focus(); }
    onChange();
  });
  let tm = null; root.addEventListener("input", () => { clearTimeout(tm); tm = setTimeout(onChange, 1200); });
  root.addEventListener("keydown", (e) => { if (e.key === "Enter" && e.target.isContentEditable) { e.preventDefault(); e.target.blur(); } });
  root.addEventListener("focusout", () => { clearTimeout(tm); tm = setTimeout(onChange, 300); });
}
const OS_PROP_CSS = `.prop{background:#fff8e6;border:2px solid #432f2e;border-radius:20px;padding:26px 22px;color:#432f2e}
.plab{font:700 12px 'Josefin Sans',Pretendard;letter-spacing:.16em;opacity:.55}.prop h2{font-size:clamp(22px,4.6vw,32px);line-height:1.35;margin:8px 0 10px;font-weight:900}
.prop h2 em{font-style:normal;background:#ffd84d;padding:0 6px}.plead{font-size:16px;line-height:1.7;opacity:.85}
.prop h3{font-size:18px;margin:22px 0 10px}.pchief{display:flex;flex-wrap:wrap;gap:8px}.pchief>span,.pchief>b{background:#fff;border:2px solid #432f2e;border-radius:14px;padding:10px 14px;font-size:15px;line-height:1.5}.pchief>span b{font-size:18px}
.pboss{width:fit-content;margin:0 auto 12px;background:#432f2e;color:#fff8e6;border-radius:14px;padding:10px 22px;font-weight:800;text-align:center}.pboss small{display:block;font-size:12px;font-weight:500;opacity:.75}
.pgrid{display:grid;grid-template-columns:repeat(auto-fill,minmax(180px,1fr));gap:10px}.pc{background:#fff;border:2px solid #432f2e;border-radius:14px;padding:14px}
.pc .no{font:700 12px 'Josefin Sans';opacity:.5}.pc h4{font-size:19px;margin:2px 0 4px}.pc p{font-size:14.5px;line-height:1.5}.pc .ex{margin-top:8px;font-size:13px;background:#fff1c2;border-radius:8px;padding:6px 9px}
.ptwo{display:grid;grid-template-columns:1fr 1fr;gap:14px}.ptwo ul{background:#fff;border:2px solid #432f2e;border-radius:14px;padding:12px 14px 12px 30px;font-size:15px;line-height:1.7}
.prop.edit [contenteditable]{outline:1.5px dashed #c9b28f;outline-offset:2px;border-radius:6px;cursor:text}.prop.edit [contenteditable]:focus{outline:2px solid #ffd84d;background:#fffdf3}.pc{position:relative}.px{position:absolute;top:6px;right:6px;width:26px;height:26px;border-radius:50%;border:1.5px solid #432f2e;background:#fff;cursor:pointer;font-size:12px}.padd{border:2px dashed #432f2e;border-radius:14px;background:transparent;font:700 15px Pretendard;color:#432f2e;cursor:pointer;min-height:90px}.padd.sm{min-height:0;padding:8px 12px;margin-top:8px;font-size:13px}.ptwo li{margin:2px 0}\n@media(max-width:560px){.ptwo{grid-template-columns:1fr}}.pfoot{margin-top:18px;font-size:12px;opacity:.6}`;
