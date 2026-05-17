"""
Regenerate raster assets (OG image and favicons) from Inter variable font.

Usage:
    python3 scripts/generate_images.py

Inputs:
    /tmp/InterVariable.ttf  (download from https://rsms.me/inter/font-files/InterVariable.ttf)

Outputs (project root):
    og.png                  1200x630, wordmark on warm off-white
    favicon.ico             32x32, lowercase "p" on near-black
    apple-touch-icon.png    180x180
    icon-192.png            192x192
"""

from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
FONT_PATH = "/tmp/InterVariable.ttf"

BG = (250, 250, 247)        # #FAFAF7
TEXT = (26, 26, 26)         # #1A1A1A


def load_inter(size, weight):
    font = ImageFont.truetype(FONT_PATH, size=size)
    font.set_variation_by_axes([weight])
    return font


def draw_tracked_text(draw, xy, text, font, fill, tracking_em):
    """Pillow can't set letter-spacing; render char-by-char with manual offset."""
    x, y = xy
    em = font.size
    extra = tracking_em * em
    for char in text:
        draw.text((x, y), char, font=font, fill=fill)
        bbox = draw.textbbox((0, 0), char, font=font)
        x += (bbox[2] - bbox[0]) + extra


def measure_tracked(text, font, tracking_em):
    em = font.size
    extra = tracking_em * em
    img = Image.new("RGB", (1, 1))
    d = ImageDraw.Draw(img)
    width = 0
    height = 0
    for i, char in enumerate(text):
        bbox = d.textbbox((0, 0), char, font=font)
        width += (bbox[2] - bbox[0])
        if i < len(text) - 1:
            width += extra
        height = max(height, bbox[3] - bbox[1])
    return width, height


def generate_og():
    W, H = 1200, 630
    img = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(img)

    size = 96
    tracking = -0.02
    font = load_inter(size, 600)

    text = "Palouse Labs"
    text_w, _ = measure_tracked(text, font, tracking)
    # Use font's ascent for vertical centering on cap-height baseline
    ascent, descent = font.getmetrics()
    text_h = ascent + descent
    x = (W - text_w) // 2
    y = (H - text_h) // 2

    draw_tracked_text(draw, (x, y), text, font, TEXT, tracking)
    img.save(ROOT / "og.png", "PNG", optimize=True)
    print(f"  og.png ({W}x{H})")


def render_p_icon(size):
    img = Image.new("RGBA", (size, size), (26, 26, 26, 255))
    draw = ImageDraw.Draw(img)
    # Inter "p" at this size with bold weight; tuned for optical centering
    font_size = int(size * 0.7)
    font = load_inter(font_size, 700)
    bbox = draw.textbbox((0, 0), "p", font=font)
    w = bbox[2] - bbox[0]
    h = bbox[3] - bbox[1]
    # The "p" descender pulls visual weight downward; nudge up to compensate
    x = (size - w) // 2 - bbox[0]
    y = (size - h) // 2 - bbox[1] - int(size * 0.06)
    draw.text((x, y), "p", font=font, fill=BG)
    return img


def generate_favicons():
    # favicon.ico — multi-resolution
    sizes_for_ico = [16, 32, 48]
    images = [render_p_icon(s) for s in sizes_for_ico]
    images[0].save(
        ROOT / "favicon.ico",
        format="ICO",
        sizes=[(s, s) for s in sizes_for_ico],
        append_images=images[1:],
    )
    print("  favicon.ico (16, 32, 48)")

    apple = render_p_icon(180)
    apple.save(ROOT / "apple-touch-icon.png", "PNG", optimize=True)
    print("  apple-touch-icon.png (180x180)")

    icon192 = render_p_icon(192)
    icon192.save(ROOT / "icon-192.png", "PNG", optimize=True)
    print("  icon-192.png (192x192)")


if __name__ == "__main__":
    print("Generating images:")
    generate_og()
    generate_favicons()
    print("Done.")
