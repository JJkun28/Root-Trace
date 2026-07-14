#!/usr/bin/env python3
"""录制族谱编辑器操作并生成 README 演示 GIF。"""

from __future__ import annotations

import asyncio
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
OUTPUT = ROOT / "images" / "README.gif"
URL = "http://127.0.0.1:8765/index.html"
VIEWPORT = {"width": 1100, "height": 700}


def load_font(size: int) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    for path in (
        Path(r"C:\Windows\Fonts\msyh.ttc"),
        Path(r"C:\Windows\Fonts\simhei.ttf"),
        Path(r"C:\Windows\Fonts\simkai.ttf"),
    ):
        if path.is_file():
            try:
                return ImageFont.truetype(str(path), size=size, index=0)
            except Exception:
                try:
                    return ImageFont.truetype(str(path), size=size)
                except Exception:
                    continue
    return ImageFont.load_default()


def add_caption(png_path: Path, text: str, title: str = "") -> Image.Image:
    img = Image.open(png_path).convert("RGB")
    draw = ImageDraw.Draw(img)
    w, h = img.size
    bar_h = 78 if title else 58
    overlay = Image.new("RGBA", (w, bar_h), (26, 26, 26, 210))
    img.paste(overlay, (0, h - bar_h), overlay)
    draw = ImageDraw.Draw(img)
    font = load_font(24)
    title_font = load_font(18)
    if title:
        draw.text((24, h - bar_h + 10), title, fill="#F3E9D5", font=title_font)
        draw.text((24, h - bar_h + 34), text, fill="#FFFFFF", font=font)
    else:
        draw.text((24, h - bar_h + 16), text, fill="#FFFFFF", font=font)
    return img


async def click_node_by_name(page, name: str) -> bool:
    return await page.evaluate(
        """(name) => {
            for (const node of document.querySelectorAll('g.node')) {
                const tspan = node.querySelector('text.node-label tspan');
                if (!tspan || !tspan.textContent.trim().includes(name)) continue;
                const target = node.querySelector('image') || node.querySelector('circle');
                if (!target) return false;
                target.dispatchEvent(new MouseEvent('click', { bubbles: true, cancelable: true, view: window }));
                return true;
            }
            return false;
        }""",
        name,
    )


async def click_plus_by_name(page, name: str) -> bool:
    return await page.evaluate(
        """(name) => {
            for (const node of document.querySelectorAll('g.node')) {
                const tspan = node.querySelector('text.node-label tspan');
                if (!tspan || !tspan.textContent.trim().includes(name)) continue;
                const plus = node.querySelector('.plus-label');
                if (!plus) return false;
                plus.dispatchEvent(new MouseEvent('click', { bubbles: true, cancelable: true, view: window }));
                return true;
            }
            return false;
        }""",
        name,
    )


async def click_button(page, label: str) -> bool:
    return await page.evaluate(
        """(label) => {
            for (const btn of document.querySelectorAll('form button')) {
                if (btn.textContent.trim() === label) {
                    btn.click();
                    return true;
                }
            }
            return false;
        }""",
        label,
    )


async def capture(page, path: Path) -> None:
    await page.screenshot(path=str(path), full_page=False)


async def main() -> int:
    from playwright.async_api import async_playwright

    tmp_dir = ROOT / "images" / "_gif_frames"
    tmp_dir.mkdir(parents=True, exist_ok=True)

    async with async_playwright() as p:
        try:
            browser = await p.chromium.launch(channel="msedge", headless=True)
        except Exception:
            browser = await p.chromium.launch(channel="chrome", headless=True)
        page = await browser.new_page(viewport=VIEWPORT)
        await page.goto(URL, wait_until="networkidle", timeout=30000)
        await page.wait_for_timeout(1200)

        frames: list[Image.Image] = []
        durations: list[int] = []

        async def shot(name: str) -> Path:
            path = tmp_dir / f"{name}.png"
            await capture(page, path)
            return path

        # 1. 初始画面
        p1 = await shot("01_initial")
        frames.append(add_caption(p1, "打开 index.html，从 input.js 加载族谱数据", "族谱编辑器"))
        durations.append(2800)

        # 2. 点击子女节点，展开配偶与下一代
        ok = await click_node_by_name(page, "拧巴茄子七")
        if not ok:
            print("警告：未找到节点「拧巴茄子七」", file=sys.stderr)
        await page.wait_for_timeout(1500)
        p2 = await shot("02_expand_child")
        frames.append(add_caption(p2, "点击节点圆圈，展开查看配偶与子女"))
        durations.append(2600)

        # 3. 打开编辑面板
        await click_plus_by_name(page, "拧巴茄子七")
        await page.wait_for_timeout(900)
        p3 = await shot("03_editor")
        frames.append(add_caption(p3, "点击 + 打开编辑表单，可修改姓名、称谓、生日等"))
        durations.append(2800)

        # 4. 展开全部子女
        await click_button(page, "All children")
        await page.wait_for_timeout(1500)
        p4 = await shot("04_all_children")
        frames.append(add_caption(p4, "一键展开全部子女，浏览更大范围的家族关系"))
        durations.append(2600)

        # 5. 切回上一代并展开父母
        await page.evaluate("document.querySelectorAll('form').forEach(f => f.remove())")
        ok = await click_node_by_name(page, "锅底虾煤饼")
        await page.wait_for_timeout(1200)
        await click_plus_by_name(page, "锅底虾煤饼")
        await page.wait_for_timeout(700)
        await click_button(page, "All children")
        await page.wait_for_timeout(1500)
        p5 = await shot("05_multi_gen")
        frames.append(add_caption(p5, "支持多世代浏览，节点头像与称谓实时显示"))
        durations.append(2800)

        # 6. 收尾：强调可导出
        p6 = await shot("06_final")
        frames.append(
            add_caption(
                p6,
                "编辑后可复制数据；运行 generate_pdf.py 导出中式族谱 PDF",
                "数据编辑 · PDF 导出",
            )
        )
        durations.append(3200)

        await browser.close()

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    frames[0].save(
        OUTPUT,
        save_all=True,
        append_images=frames[1:],
        duration=durations,
        loop=0,
        optimize=True,
    )
    print(f"已生成：{OUTPUT}（{len(frames)} 帧）")
    return 0


if __name__ == "__main__":
    raise SystemExit(asyncio.run(main()))
