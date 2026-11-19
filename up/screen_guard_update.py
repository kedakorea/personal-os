# -*- coding: utf-8 -*-
"""퍼스널 OS 업데이트 — 화면 지킴이 + 잠금 횟수 기기별 (2026-11-19)
- 화면 파일(elvin_web.html)이 깨져 잠금 화면에 갇히면 서버가 저절로 정상판으로 되돌린다
- 비밀번호를 틀려 잠길 때 그 기기만 잠긴다(휴대폰·컴퓨터 따로)
매니저가 이 파일을 받아 `python3 screen_guard_update.py` 로 돌린다(윈도우는 python). 원본은 .os_데이터/백업_화면지킴이_* 에 보관.
"""
import base64, json, os, re, shutil, subprocess, sys, time, py_compile
P = json.loads(base64.b64decode("eyJibG9jayI6ICIjIOyeoOq4iCDtmp/siJjripQg6riw6riw67OE66GcIOyEvOuLpCAoMjAyNi0xMS0xOSDsgqzqs6A6IO2ctOuMgO2PsOuPhCDthYzsnbzsiqTsvIDsnbzsnYQg6rGw7LOQIDEyNy4wLjAuMSDroZwg65Ok7Ja07JmAXG4jIOy7tO2TqO2EsOyZgCDti4DrprAg7Zqf7IiY6rCAIO2VqeyzkOyguCDrkZgg64ukIOyeoOqyvOuLpCkg4oCUIOuztOuCuCDqs7Mg7KO87IaMICsg67iM65287Jqw7KCAIOyiheulmOuhnCDquLDquLDrpbwg64KY64iI64ukXG5kZWYgbG9ja19rZXkoaGFuZGxlcik6XG4gICAgaCA9IGhhbmRsZXIuaGVhZGVyc1xuICAgIGlwID0gKGguZ2V0KFwiWC1Gb3J3YXJkZWQtRm9yXCIpIG9yIFwiXCIpLnNwbGl0KFwiLFwiKVswXS5zdHJpcCgpIG9yIGhhbmRsZXIuY2xpZW50X2FkZHJlc3NbMF1cbiAgICB1YSA9IGhhc2hsaWIuc2hhMSgoaC5nZXQoXCJVc2VyLUFnZW50XCIpIG9yIFwiXCIpLmVuY29kZShcInV0Zi04XCIsIFwicmVwbGFjZVwiKSkuaGV4ZGlnZXN0KClbOjEwXVxuICAgIHJldHVybiBpcCArIFwifFwiICsgdWFcblxuXG4jIOKUgOKUgCDtmZTrqbQg7KeA7YK07J20ICgyMDI2LTExLTE5IOyCrOqzoDog66ek64uI7KCA6rCAIO2ZlOuptCDtjIzsnbzsnYQg6rOg7LmY64ukIOyKpO2BrOumve2KuOqwgCDquajsoLggW+yXtOq4sF3qsIAg66i57KeAIOyViuqzoFxuIyAgICDrqqjrk6Ag6riw6riw6rCAIOyeoOq4iCDtmZTrqbTsl5Ag6rCH7ZiU64ukKSDigJQg7ISc67KE6rCAIO2ZlOuptOydhCDrs7Trgrwg65WMIOyekeydgCDqsJDsi5wg7Iqk7YGs66a97Yq466W8IOuUsOuhnCDrgbzsm4wg64Sj64qU64ukLlxuIyAgICDtmZTrqbQg7Iqk7YGs66a97Yq46rCAIOygleyDgeycvOuhnCDrj4zrqbQo66Gc6re47J24IOyDge2DnCkg6re4IO2MkOydhCAn7KCV7IOB7YyQJ+ycvOuhnCDsoIDsnqXtlZjqs6AsXG4jICAgIOq5qOyhjOycvOuptCDsoIDsoIjroZwg7KCV7IOB7YyQ7Jy866GcIOuQmOuPjOumsCDrkqQg7IOI66Gc6rOg7Lmo7ZWc64ukLiDqsJDsi5wg7Iqk7YGs66a97Yq464qUIO2ZlOuptCDtjIzsnbwg67CWKOyEnOuyhCnsl5Ag7J6I7Ja0IOqwmeydtCDquajsp4Dsp4Ag7JWK64qU64ukLlxuV0VCX0dPT0QgPSBvcy5wYXRoLmpvaW4oREFUQSwgXCLtmZTrqbRf7KCV7IOB7YyQLmh0bWxcIilcbldFQl9HVUFSRCA9IGJcIlwiXCI8c2NyaXB0Pi8qIFxceGVkXFx4OTlcXHg5NFxceGViXFx4YTlcXHhiNCBcXHhlY1xceGE3XFx4ODBcXHhlZFxceDgyXFx4YjRcXHhlY1xceDlkXFx4YjQgKi8oZnVuY3Rpb24oKXtpZih3aW5kb3cuX193ZylyZXR1cm47d2luZG93Ll9fd2c9MTtcbmZ1bmN0aW9uIHNob3codCl7dHJ5e3ZhciBkPWRvY3VtZW50LmNyZWF0ZUVsZW1lbnQoXCJkaXZcIik7ZC5zdHlsZS5jc3NUZXh0PVwicG9zaXRpb246Zml4ZWQ7bGVmdDowO3JpZ2h0OjA7dG9wOjA7ei1pbmRleDoyMTQ3NDgzNjQ3O2JhY2tncm91bmQ6I2ZkZWNlYTtjb2xvcjojYTEyNzFiO2ZvbnQ6NzAwIDE0cHggc2Fucy1zZXJpZjtwYWRkaW5nOjEycHggMTZweDt0ZXh0LWFsaWduOmNlbnRlcjtsaW5lLWhlaWdodDoxLjVcIjtkLnRleHRDb250ZW50PXQ7ZG9jdW1lbnQuYm9keS5hcHBlbmRDaGlsZChkKX1jYXRjaChlKXt9fVxuYWRkRXZlbnRMaXN0ZW5lcihcImxvYWRcIixmdW5jdGlvbigpe3NldFRpbWVvdXQoZnVuY3Rpb24oKXt2YXIgaz1cIndnX2hlYWxcIixvaz0odHlwZW9mIGJvb3Q9PT1cImZ1bmN0aW9uXCIpfHx3aW5kb3cuX19hcHBPSztcbmlmKG9rKXt0cnl7c2Vzc2lvblN0b3JhZ2UucmVtb3ZlSXRlbShrKX1jYXRjaChlKXt9ZmV0Y2goXCIvYXBpL3dlYi9va1wiLHttZXRob2Q6XCJQT1NUXCIsY3JlZGVudGlhbHM6XCJzYW1lLW9yaWdpblwifSkuY2F0Y2goZnVuY3Rpb24oKXt9KTtyZXR1cm59XG52YXIgdHJpZWQ9ZmFsc2U7dHJ5e3RyaWVkPXNlc3Npb25TdG9yYWdlLmdldEl0ZW0oayl9Y2F0Y2goZSl7fVxuaWYodHJpZWQpe3Nob3coXCJcXHVENjU0XFx1QkE3NCBcXHVEMzBDXFx1Qzc3Q1xcdUM1RDAgXFx1QkIzOFxcdUM4MUNcXHVBQzAwIFxcdUM3ODhcXHVDNUI0XFx1QzY5NC4gXFx1QjlFNFxcdUIyQzhcXHVDODAwXFx1QzVEMFxcdUFDOEMgJ1xcdUQ2NTRcXHVCQTc0IFxcdUQzMENcXHVDNzdDXFx1Qzc0NCBcXHVDODE1XFx1QzBDMVxcdUQzMTBcXHVDNzNDXFx1Qjg1QyBcXHVCNDE4XFx1QjNDQ1xcdUI4MjQgXFx1QzkxOCdcXHVCNzdDXFx1QUNFMCBcXHVENTU4XFx1QUM3MFxcdUIwOTggXFx1QjNDNFxcdUM2QzBcXHVDNzQ0IFxcdUM2OTRcXHVDQ0FEXFx1RDU3NCBcXHVDOEZDXFx1QzEzOFxcdUM2OTQuXCIpO3JldHVybn1cbnRyeXtzZXNzaW9uU3RvcmFnZS5zZXRJdGVtKGssXCIxXCIpfWNhdGNoKGUpe31cbmZldGNoKFwiL2FwaS93ZWIvaGVhbFwiLHttZXRob2Q6XCJQT1NUXCJ9KS50aGVuKGZ1bmN0aW9uKHIpe3JldHVybiByLmpzb24oKX0pLnRoZW4oZnVuY3Rpb24oail7aWYoai5yZXN0b3JlZClsb2NhdGlvbi5yZWxvYWQoKTtlbHNlIHNob3coXCJcXHVENjU0XFx1QkE3NCBcXHVEMzBDXFx1Qzc3Q1xcdUM1RDAgXFx1QkIzOFxcdUM4MUNcXHVBQzAwIFxcdUM3ODhcXHVCMjk0XFx1QjM3MCBcXHVCNDE4XFx1QjNDQ1xcdUI5QjQgXFx1QzgxNVxcdUMwQzFcXHVEMzEwXFx1Qzc3NCBcXHVDNUM2XFx1QzVCNFxcdUM2OTQuIFxcdUIzQzRcXHVDNkMwXFx1Qzc0NCBcXHVDNjk0XFx1Q0NBRFxcdUQ1NzQgXFx1QzhGQ1xcdUMxMzhcXHVDNjk0LlwiKX0pLmNhdGNoKGZ1bmN0aW9uKCl7fSl9LDE1MDApfSl9KSgpOzwvc2NyaXB0PlwiXCJcIlxuXG5cbmRlZiB3ZWJfd2l0aF9ndWFyZChyYXcpOlxuICAgIGkgPSByYXcuZmluZChiXCI8aGVhZD5cIilcbiAgICBpZiBpIDwgMDpcbiAgICAgICAgcmV0dXJuIFdFQl9HVUFSRCArIHJhd1xuICAgIGkgKz0gbGVuKGJcIjxoZWFkPlwiKVxuICAgIHJldHVybiByYXdbOmldICsgV0VCX0dVQVJEICsgcmF3W2k6XVxuXG5cbmRlZiB3ZWJfbWFya19nb29kKCk6XG4gICAgXCJcIlwi66Gc6re47J247ZWcIOq4sOq4sOyXkOyEnCDtmZTrqbQg7Iqk7YGs66a97Yq46rCAIOygleyDgeycvOuhnCDrj4zslZjri6Qg4oaSIOyngOq4iCDtjJDsnYQg7KCV7IOB7YyQ7Jy866GcIOuztOq0gC5cIlwiXCJcbiAgICB0cnk6XG4gICAgICAgIGN1ciA9IG9wZW4oV0VCLCBcInJiXCIpLnJlYWQoKVxuICAgICAgICBpZiBub3Qgb3MucGF0aC5leGlzdHMoV0VCX0dPT0QpIG9yIG9wZW4oV0VCX0dPT0QsIFwicmJcIikucmVhZCgpICE9IGN1cjpcbiAgICAgICAgICAgIHRtcCA9IFdFQl9HT09EICsgXCIudG1wXCJcbiAgICAgICAgICAgIG9wZW4odG1wLCBcIndiXCIpLndyaXRlKGN1cilcbiAgICAgICAgICAgIG9zLnJlcGxhY2UodG1wLCBXRUJfR09PRClcbiAgICBleGNlcHQgRXhjZXB0aW9uOlxuICAgICAgICBwYXNzXG5cblxuZGVmIHdlYl9oZWFsKCk6XG4gICAgXCJcIlwi7ZmU66m0IOyKpO2BrOumve2KuOqwgCDquajsoYzri6Qg4oaSIOq5qOynhCDtjJDsnYAg65Sw66GcIOuRkOqzoCDsoJXsg4HtjJDsnLzroZwg65CY64+M66aw64ukLlwiXCJcIlxuICAgIHRyeTpcbiAgICAgICAgaWYgbm90IG9zLnBhdGguZXhpc3RzKFdFQl9HT09EKTpcbiAgICAgICAgICAgIHJldHVybiBGYWxzZVxuICAgICAgICBjdXIgPSBvcGVuKFdFQiwgXCJyYlwiKS5yZWFkKClcbiAgICAgICAgZ29vZCA9IG9wZW4oV0VCX0dPT0QsIFwicmJcIikucmVhZCgpXG4gICAgICAgIGlmIGN1ciA9PSBnb29kOlxuICAgICAgICAgICAgcmV0dXJuIEZhbHNlXG4gICAgICAgIG9wZW4ob3MucGF0aC5qb2luKERBVEEsIFwi7ZmU66m0X+qzoOyepeuCnO2MkF8lcy5odG1sXCIgJSB0aW1lLnN0cmZ0aW1lKFwiJXklbSVkXyVIJU0lU1wiKSksIFwid2JcIikud3JpdGUoY3VyKVxuICAgICAgICB0bXAgPSBXRUIgKyBcIi50bXBcIlxuICAgICAgICBvcGVuKHRtcCwgXCJ3YlwiKS53cml0ZShnb29kKVxuICAgICAgICBvcy5yZXBsYWNlKHRtcCwgV0VCKVxuICAgICAgICB0cnk6XG4gICAgICAgICAgICB3aXRoIG9wZW4ob3MucGF0aC5qb2luKERBVEEsIFwi7ZmU66m07KeA7YK07J20LmxvZ1wiKSwgXCJhXCIsIGVuY29kaW5nPVwidXRmLThcIikgYXMgZjpcbiAgICAgICAgICAgICAgICBmLndyaXRlKHRpbWUuc3RyZnRpbWUoXCIlWS0lbS0lZCAlSDolTTolU1wiKSArIFwiIO2ZlOuptCDsiqTtgazrpr3tirjqsIAg6rmo7KC4IOygleyDge2MkOycvOuhnCDrkJjrj4zrprxcXG5cIilcbiAgICAgICAgZXhjZXB0IEV4Y2VwdGlvbjpcbiAgICAgICAgICAgIHBhc3NcbiAgICAgICAgcmV0dXJuIFRydWVcbiAgICBleGNlcHQgRXhjZXB0aW9uOlxuICAgICAgICByZXR1cm4gRmFsc2VcblxuXG4iLCAicnVsZSI6ICItICoq7ZmU66m0IO2MjOydvChgZWx2aW5fd2ViLmh0bWxgwrdgLm9zX+2CpO2KuC9f7JuQ67O4L2VsdmluX3dlYi5odG1sYCnsnYQg6rOg7LmgIOuVjCDigJQg7J6g6riIIO2ZlOuptCDrqLzsoIAg7KeA7YKk6riwKiogKDIwMjYtMTEtMTkg7Iuk7KCcIOyCrOqzoDog7IOI67K97JeQIO2ZlOuptOydhCDqs6DsuZjri6Qg7Iqk7YGs66a97Yq46rCAIOq5qOyguCBb7Je06riwXSDrsoTtirzsnbQg66i57KeAIOyViuyVmOqzoCwg7Lu07ZOo7YSwwrftnLTrjIDtj7DsnbQg64+Z7Iuc7JeQIOyeoOq4iCDtmZTrqbTsl5Ag6rCH7ZiU64ukKVxuICAxLiDqs6DsuZjquLAg7KCE7JeQIOyngOq4iCDtjIzsnbzsnYQgYC5vc1/rjbDsnbTthLAv7ZmU66m0X+uwseyXhV9ZWU1NRERfSEhNTS5odG1sYCDroZwg67O17IKs7ZW0IOuRlOuLpC5cbiAgMi4g6rOg7LmcIOuSpCAqKuuwmOuTnOyLnCDtmZXsnbgqKu2VnOuLpDog67iM65287Jqw7KCAKO2XpOuTnOumrOyKpCDqsIDriqUp66GcIGBodHRwOi8vMTI3LjAuMC4xOjg3NjVgIOulvCDsl7TslrQg4pGgIOy9mOyGlOyXkCDruajqsIQg7Jik66WYKFN5bnRheEVycm9yIOuTsSnqsIAg7JeG64qU7KeAIOKRoSDsnqDquIgg7ZmU66m07JeQ7IScIOu5hOuwgOuyiO2YuOulvCDrhKPsnLzrqbQg7Je066as64qU7KeAIOKRoiDsl7TrprAg65KkIOuMgO2ZlCDrqqnroZ3snbQg65yo64qU7KeALiDtlZjrgpjrnbzrj4Qg7JWIIOuQmOuptCDqt7gg7J6Q66as7JeQ7IScIDHrsogg67Cx7JeF7Jy866GcIOuQmOuPjOumrOqzoCB7e+2YuOy5rX196ruYIOyVjOumsOuLpC5cbiAgMy4ge3vtmLjsua19feydtCDso7zrrLTsi5zripQg7Iuc6rCEwrfqt7zrrLTsi5zqsIQg67CW7JeQ64qUIO2ZlOuptCDtjIzsnbzsnYQg6rOg7LmY7KeAIOyViuuKlOuLpCjrrLjsoJzqsIAg7IOd6rKo64+EIOuwlOuhnCDslYwg7IiYIOyXhuuLpCkuXG4gIDQuIOyEnOuyhOyXkOuKlCAn7ZmU66m0IOyngO2CtOydtCfqsIAg65Ok7Ja0IOyeiOuLpDog66Gc6re47J247ZWcIOq4sOq4sOyXkOyEnCDtmZTrqbTsnbQg7KCV7IOB7Jy866GcIOuPjOuptCBgLm9zX+uNsOydtO2EsC/tmZTrqbRf7KCV7IOB7YyQLmh0bWxgIOuhnCDrs7TqtIDtlZjqs6AsIO2ZlOuptCDsiqTtgazrpr3tirjqsIAg6rmo7KeA66m0IOyggOygiOuhnCDsoJXsg4HtjJDsnLzroZwg65CY64+M66aw64ukKOq5qOynhCDtjJDsnYAgYO2ZlOuptF/qs6DsnqXrgpztjJBfKi5odG1sYCwg6riw66GdIGDtmZTrqbTsp4DtgrTsnbQubG9nYCkuIOyngO2CtOydtOqwgCDrkJjrj4zroLjri6TrqbQg66y07JeH7J20IOq5qOyhjOuKlOyngCDqs6DsnqXrgpztjJDqs7wg67mE6rWQ7ZW0IOqzoOy5nCDrkqQgMuuyiCDtmZXsnbjsnYQg64uk7IucIO2VnOuLpC4g7KeA7YK07J2066W8IOuBhOqxsOuCmCDsp4DsmrDsp4Ag7JWK64qU64ukLlxuLSDsnqDquIgg67mE67CA67KI7Zi466W8IDXrsogg7YuA66as66m0ICoq6re4IOq4sOq4sOunjCoqIDEw67aEIOyeoOq4tOuLpCgyMDI2LTExLTE567aA7YSwIOq4sOq4sOuzhCkuIHt77Zi47LmtfX3snbQgXCLslYgg7Je066aw64ukXCLqs6Ag7ZWY7Iuc66m0IOu5hOuwgOuyiO2YuOu2gO2EsCDsnZjsi6ztlZjsp4Ag66eQ6rOgLCDqsJnsnYAg7Lu07ZOo7YSw7JeQ7IScIGAvYXBpL2xvZ2luYCDsnYQg7KeB7KCRIOu2iOufrCjshKTsoJUuanNvbiDruYTrsIDrsojtmLjroZwpIOyEnOuyhOqwgCBgb2tgIOulvCDso7zripTsp4Ag66i87KCAIOuzuOuLpCDigJQgYG9rYCDsnbjrjbAg7ZmU66m07J20IOyViCDsl7TrpqzrqbQg7ZmU66m0IO2MjOydvCDrrLjsoJzri6QuIn0=").decode("utf-8"))
HOME = os.path.expanduser("~"); OS_DIR = os.path.join(HOME, "퍼스널OS"); DATA = os.path.join(OS_DIR, ".os_데이터")
WIN = os.name == "nt"; SRV = os.path.join(OS_DIR, "elvin_server.py"); py = sys.executable
TEST = "--test" in sys.argv
def say(t): print(t, flush=True)
if not os.path.exists(SRV):
    say("❌ ~/퍼스널OS/elvin_server.py 를 찾지 못했습니다."); sys.exit(1)
bk = os.path.join(DATA, "백업_화면지킴이_" + time.strftime("%y%m%d_%H%M")); os.makedirs(bk, exist_ok=True)
shutil.copy2(SRV, bk); say("📦 원본 보관: " + bk)
s = open(SRV, encoding="utf-8").read()
if "def web_with_guard(" in s:
    i = s.index("# 잠금 횟수는 기기별로 센다"); j = s.index("def blocked_for(ip):", i)
    s = s[:i] + P["block"] + s[j:]; say("✔ 지킴이 코드를 최신으로 바꿈")
else:
    if "def blocked_for(ip):" not in s:
        say("❌ 서버 구조가 달라 넣지 못했습니다(원본 그대로)"); sys.exit(2)
    s = s.replace("def blocked_for(ip):", P["block"] + "def blocked_for(ip):", 1)
    s, n1 = re.subn(r'(with open\(WEB, "rb"\) as f:\s*\n\s*self\._bytes\()f\.read\(\)', r"\1web_with_guard(f.read())", s, count=1)
    m = re.search(r'\n( +)if path == "/api/login":\n( +)ip = self\.client_address\[0\]', s)
    if not n1 or not m:
        say("❌ 서버 구조가 달라 넣지 못했습니다(원본 그대로)"); sys.exit(2)
    ind, ind2 = m.group(1), m.group(2)
    routes = ("\n{0}if path == \"/api/web/heal\":\n{1}self._json({{\"restored\": web_heal()}})\n{1}return\n"
              "{0}if path == \"/api/web/ok\":\n{1}if is_logged_in(self):\n{1}    web_mark_good()\n{1}self._json({{\"ok\": True}})\n{1}return\n"
              "{0}if path == \"/api/login\":\n{1}ip = lock_key(self)").format(ind, ind2)
    s = s[:m.start()] + routes + s[m.end():]
    say("✔ 서버: 화면 지킴이 + 기기별 잠금 추가")
tmp = SRV + ".새판"; open(tmp, "w", encoding="utf-8").write(s)
try:
    py_compile.compile(tmp, doraise=True); os.replace(tmp, SRV)
except Exception as e:
    os.remove(tmp); say("❌ 문법 확인 실패(원본 그대로): %s" % str(e)[:200]); sys.exit(3)
# 매니저 규칙
cm = os.path.join(OS_DIR, "CLAUDE.md")
try:
    c = open(cm, encoding="utf-8").read()
    if "화면 지킴이" not in c:
        ho = "대표님"
        try: ho = json.load(open(os.path.join(OS_DIR, "설정.json"), encoding="utf-8")).get("호칭") or ho
        except Exception: pass
        open(cm, "a", encoding="utf-8").write("\n\n## 화면 파일 고칠 때 (2026-11-19 업데이트)\n" + P["rule"].replace("{{호칭}}", ho) + "\n")
        say("✔ 매니저 규칙: 화면 고친 뒤 잠금 화면 확인")
except Exception as e:
    say("⚠ 규칙 추가 실패: %s" % e)
if TEST:
    say("✅ (시험) 서버 다시 띄우기는 건너뜀"); sys.exit(0)
if WIN:
    rs = os.path.join(OS_DIR, ".os_키트", "윈도우_서버재시작.py")
    if os.path.exists(rs): subprocess.Popen([py, rs]); say("🔄 25초 뒤(답이 끝난 뒤) 앱 서버를 다시 띄웁니다")
    else: say("⚠ 컴퓨터를 한 번 다시 시작해 주세요(서버 새로 켜기)")
else:
    d = os.path.join(OS_DIR, "부서", "00_비서실"); ft, rs = os.path.join(d, "떼어내기.py"), os.path.join(d, "서버재시작.sh")
    if os.path.exists(ft) and os.path.exists(rs): subprocess.Popen([py, ft, rs]); say("🔄 25초 뒤(답이 끝난 뒤) 앱 서버를 다시 띄웁니다")
    else:
        subprocess.Popen(["/bin/bash", "-c", "sleep 30; launchctl kickstart -k gui/%s/com.personalos.server" % os.getuid()], start_new_session=True); say("🔄 30초 뒤 앱 서버를 다시 띄웁니다")
say("✅ 끝 — 서버가 다시 켜지면 앱을 한 번 새로고침해 주세요. 그때부터 지금 화면이 '정상판'으로 보관됩니다.")
