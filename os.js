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
function osProposal(d, chief) {
  if (!d) return "";
  const dep = (d.부서 || []).map((x) => `<div class="pc"><div class="no">${osEsc((x.폴더 || "").split("_")[0])}</div><h4>${osEsc((x.이름 || x.폴더 || "").replace(/^\S+\s/, ""))}</h4><p>${osEsc(x.일 || "")}</p>${x.예 ? `<div class="ex">“${osEsc(x.예)}”</div>` : ""}</div>`).join("");
  const li = (a) => (a || []).map((x) => `<li>${osEsc(x)}</li>`).join("");
  return `<div class="prop"><div class="plab">PERSONAL OS · PROPOSAL</div>
    <h2><em>${osEsc(d.고객 || "")}</em>의 퍼스널 OS를 이렇게 세팅합니다</h2><p class="plead">${osEsc(d.한줄 || "")}</p>
    <h3>① 매니저</h3><div class="pchief">${chief ? `<b>${osEsc(chief)}</b>` : (d.실장후보 || []).map((c) => `<span><b>${osEsc(c.이름)}</b> · ${osEsc(c.뜻 || "")}</span>`).join("")}</div>
    <h3>② 부서 — 매니저가 일을 나눠 맡깁니다</h3><div class="pboss">${osEsc(d.고객 || "")}<small>지시는 매니저에게 한마디로</small></div><div class="pgrid">${dep}</div>
    <div class="ptwo"><div><h3>③ 알아서 하는 일</h3><ul>${li(d.자동업무)}</ul></div><div><h3>④ 꼭 확인받고 하는 일</h3><ul>${li(d.승인선목록)}</ul></div></div>
    <div class="pfoot">BRANDiUM · 주식회사 캐다 · 퍼스널 OS</div></div>`;
}
const OS_PROP_CSS = `.prop{background:#fff8e6;border:2px solid #432f2e;border-radius:20px;padding:26px 22px;color:#432f2e}
.plab{font:700 12px 'Josefin Sans',Pretendard;letter-spacing:.16em;opacity:.55}.prop h2{font-size:clamp(22px,4.6vw,32px);line-height:1.35;margin:8px 0 10px;font-weight:900}
.prop h2 em{font-style:normal;background:#ffd84d;padding:0 6px}.plead{font-size:16px;line-height:1.7;opacity:.85}
.prop h3{font-size:18px;margin:22px 0 10px}.pchief{display:flex;flex-wrap:wrap;gap:8px}.pchief>span,.pchief>b{background:#fff;border:2px solid #432f2e;border-radius:14px;padding:10px 14px;font-size:15px;line-height:1.5}.pchief>span b{font-size:18px}
.pboss{width:fit-content;margin:0 auto 12px;background:#432f2e;color:#fff8e6;border-radius:14px;padding:10px 22px;font-weight:800;text-align:center}.pboss small{display:block;font-size:12px;font-weight:500;opacity:.75}
.pgrid{display:grid;grid-template-columns:repeat(auto-fill,minmax(180px,1fr));gap:10px}.pc{background:#fff;border:2px solid #432f2e;border-radius:14px;padding:14px}
.pc .no{font:700 12px 'Josefin Sans';opacity:.5}.pc h4{font-size:19px;margin:2px 0 4px}.pc p{font-size:14.5px;line-height:1.5}.pc .ex{margin-top:8px;font-size:13px;background:#fff1c2;border-radius:8px;padding:6px 9px}
.ptwo{display:grid;grid-template-columns:1fr 1fr;gap:14px}.ptwo ul{background:#fff;border:2px solid #432f2e;border-radius:14px;padding:12px 14px 12px 30px;font-size:15px;line-height:1.7}
@media(max-width:560px){.ptwo{grid-template-columns:1fr}}.pfoot{margin-top:18px;font-size:12px;opacity:.6}`;
