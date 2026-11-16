#!/usr/bin/env python3
"""AI·PDF 파일에서 그림 꺼내기 — 일러스트레이터 없이 (맥·윈도우 공통, 2026-11-14)
일러스트레이터 .ai 는 기본으로 'PDF 호환'이 켜져 저장되므로 안에 PDF 가 들어 있다.
대지(페이지)마다 큰 PNG · 투명 PNG · 벡터 PDF(그 대지만)로 꺼낸다.

사용: python AI파일_꺼내기.py 파일.ai [출력폴더] [--가로 3000] [--쪽 2,3]
  - 출력폴더를 안 주면 파일 옆에 '<파일이름>_꺼낸그림' 폴더를 만든다
  - --쪽 을 주면 그 대지만 (1부터 셈)
무료 도구만 쓴다: pypdfium2(Apache-2.0/BSD) · pypdf(BSD) · Pillow — 상업 사용 가능
"""
import os, sys, shutil, tempfile


def need(mod, pkg):
    try:
        return __import__(mod)
    except ImportError:
        print(f"필요한 무료 도구({pkg})를 설치합니다…")
        import subprocess
        subprocess.run([sys.executable, "-m", "pip", "install", "--user", "--quiet", pkg])
        # 처음 설치하면 '개인용 도구 폴더'가 막 생겨 이미 켜진 파이썬이 못 찾음 → 폴더를 알려 주고 다시 찾기 (2026-11-16 윈도우 첫 실행 오류)
        import site, importlib
        try:
            site.addsitedir(site.getusersitepackages())
        except Exception:
            pass
        importlib.invalidate_caches()
        return __import__(mod)


def main():
    args = [a for a in sys.argv[1:]]
    if not args:
        print(__doc__); return 1
    width, pages = 3000, None
    if "--가로" in args:
        i = args.index("--가로"); width = int(args[i + 1]); del args[i:i + 2]
    if "--쪽" in args:
        i = args.index("--쪽"); pages = [int(x) for x in args[i + 1].split(",")]; del args[i:i + 2]
    src = os.path.abspath(args[0])
    out = os.path.abspath(args[1]) if len(args) > 1 else os.path.splitext(src)[0] + "_꺼낸그림"
    os.makedirs(out, exist_ok=True)

    with open(src, "rb") as f:
        head = f.read(8)
    if not head.startswith(b"%PDF"):
        print("❌ 이 AI 파일은 'PDF 호환'이 꺼진 채 저장돼 열 수 없어요.")
        print("   보낸 분께 '일러스트레이터에서 PDF 호환 파일 만들기를 켜고 다시 저장해 주세요'라고 부탁하세요.")
        return 2

    pdfium = need("pypdfium2", "pypdfium2")
    pypdf = need("pypdf", "pypdf")
    need("PIL", "Pillow")   # 사진 도구도 없으면 함께 설치
    from PIL import Image, ImageChops

    # 한글 경로 문제를 피하려고 임시 복사본으로 연다
    tmp = os.path.join(tempfile.mkdtemp(), "src.pdf")
    shutil.copyfile(src, tmp)
    doc = pdfium.PdfDocument(tmp)
    reader = pypdf.PdfReader(tmp)
    base = os.path.splitext(os.path.basename(src))[0]
    n = len(doc)
    todo = pages or list(range(1, n + 1))
    made = []
    for p in todo:
        if not 1 <= p <= n:
            continue
        page = doc[p - 1]
        w, h = page.get_size()
        img = page.render(scale=width / w).to_pil().convert("RGB")
        # 흰 여백 잘라내고 조금 여유
        diff = ImageChops.difference(img, Image.new("RGB", img.size, "white")).convert("L").point(lambda v: 255 if v > 10 else 0)
        box = diff.getbbox()
        if box:
            m = int(min(img.size) * 0.03)
            box = (max(0, box[0] - m), max(0, box[1] - m), min(img.width, box[2] + m), min(img.height, box[3] + m))
            img = img.crop(box)
        name = f"{base}_{p}쪽"
        img.save(os.path.join(out, name + "_흰배경.png"), dpi=(300, 300))
        # 투명: 흰색일수록 투명하게
        rgba = img.convert("RGBA")
        r_, g_, b_, _a = rgba.split()   # getdata 는 Pillow 14(2027)에서 없어짐 → 채널 계산으로
        alpha = ImageChops.invert(ImageChops.darker(ImageChops.darker(r_, g_), b_)).point(lambda v: min(255, v * 255 // 40))
        rgba.putalpha(alpha)
        rgba.save(os.path.join(out, name + "_투명.png"), dpi=(300, 300))
        # 벡터 PDF: 그 대지만 — 아무리 키워도 안 깨짐(현수막 등 큰 인쇄용)
        wr = pypdf.PdfWriter(); wr.add_page(reader.pages[p - 1])
        with open(os.path.join(out, name + "_벡터.pdf"), "wb") as f:
            wr.write(f)
        made.append(name)
        print(f"✅ {p}쪽 → {name}_흰배경.png · _투명.png · _벡터.pdf ({img.width}×{img.height})")
    print(f"\n📁 {out}  ({len(made)}쪽 / 전체 {n}쪽)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
