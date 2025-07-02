from PIL import Image, ImageDraw, ImageFont
import os
from datetime import datetime
import random
import colorsys
from typing import Optional
from src.utils.gift_image_utils import get_gift_id_by_name, fetch_gift_image_by_id

# ----- Constants -----
CARD_SIZE = (1119, 645)
BG_SIZE = (1280, 800)
CARD_RADIUS = 69
CARD_COLOR = (255, 255, 255, 255)

# Font sizes
TITLE_FONT_SIZE = 70
TON_FONT_SIZE = 100
STARS_FONT_SIZE = 40
USD_FONT_SIZE = 40
TIME_FONT_SIZE = 18
PERCENT_FONT_SIZE = 36

# Colors
TITLE_COLOR = "#3B3B3B"
TIME_COLOR = "#7C7C7C"
POSITIVE_CHANGE_COLOR = (46, 204, 113)
NEGATIVE_CHANGE_COLOR = (231, 76, 60)

# Image positions
GIFT_IMAGE_SIZE = (120, 120)
GIFT_IMAGE_POS = (40, 40)
TITLE_POS = (180, 60)
TON_ICON_SIZE = (130, 130)
TON_ICON_POS = (70, 165)
TON_PRICE_POS = (190, 170)
USD_LABEL_POS = (120, 290)
STARS_LABEL_POS = (375, 290)
CHART_MARGIN = 120
CHART_HEIGHT = 180
CHART_BOTTOM_MARGIN = 220

# Frame settings
FRAME_SIZE = (140, 50)
FRAME_MARGIN = 30
FRAME_RADIUS = 15

# ----- Color schemes for background -----
BACKDROP_COLORS = [
    {"name": "Black", "hex": {"centerColor": "#363738", "edgeColor": "#0e0f0f"}},
    {"name": "Electric Purple", "hex": {"centerColor": "#ca70c6", "edgeColor": "#9662d4"}},
    {"name": "Lavender", "hex": {"centerColor": "#b789e4", "edgeColor": "#8a5abc"}},
    {"name": "Cyberpunk", "hex": {"centerColor": "#858ff3", "edgeColor": "#865fd3"}},
    {"name": "Electric Indigo", "hex": {"centerColor": "#a980f3", "edgeColor": "#5b62d8"}},
    {"name": "Neon Blue", "hex": {"centerColor": "#7596f9", "edgeColor": "#6862e4"}},
    {"name": "Navy Blue", "hex": {"centerColor": "#6c9edd", "edgeColor": "#5c6ec9"}},
    {"name": "Sapphire", "hex": {"centerColor": "#58a3c8", "edgeColor": "#5379c2"}},
    {"name": "Sky Blue", "hex": {"centerColor": "#58b4c8", "edgeColor": "#538bc2"}},
    {"name": "Azure Blue", "hex": {"centerColor": "#5db1cb", "edgeColor": "#448bab"}},
    {"name": "Mint", "hex": {"centerColor": "#5dc8b1", "edgeColor": "#4abf9c"}}
]

def format_number(n):
    return f"{n:,}".replace(",", " ")

def draw_gradient(size, color1, color2):
    base = Image.new('RGB', size, color1)
    top = Image.new('RGB', size, color2)
    mask = Image.linear_gradient('L').resize(size)
    return Image.composite(top, base, mask)

def get_text_size(draw, text, font):
    bbox = draw.textbbox((0, 0), text, font=font)
    return bbox[2] - bbox[0], bbox[3] - bbox[1]

def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def random_backdrop_pair():
    color = random.choice([c for c in BACKDROP_COLORS if "hex" in c])
    center = hex_to_rgb(color["hex"]["centerColor"])
    edge = hex_to_rgb(color["hex"]["edgeColor"])
    return center, edge

def draw_card(
    gift_name: str,
    price_stars: int,
    chart_img: Image.Image,
    dt: datetime,
    asset_dir: str = "src/assets",
    gift_image_filename: Optional[str] = None,
    percent_change: float = 0.0
):
    card_pos = ((BG_SIZE[0] - CARD_SIZE[0]) // 2, (BG_SIZE[1] - CARD_SIZE[1]) // 2)

    # ----- Generate background -----
    color1, color2 = random_backdrop_pair()
    bg = draw_gradient(BG_SIZE, color1, color2).convert("RGBA")

    # ----- Load fonts -----
    font_dir = "/Library/Fonts" if os.path.exists("/Library/Fonts") else ""
    font_path = os.path.join(font_dir, "SF-Pro-Rounded-Black.otf")
    try:
        Title_Font = ImageFont.truetype(font_path, TITLE_FONT_SIZE)
        TON_Font = ImageFont.truetype(font_path, TON_FONT_SIZE)
        Stars_Font = ImageFont.truetype(font_path, STARS_FONT_SIZE)
        USD_Font = ImageFont.truetype(font_path, USD_FONT_SIZE)
        Time_Font = ImageFont.truetype(font_path, TIME_FONT_SIZE)
        Percent_Font = ImageFont.truetype(font_path, PERCENT_FONT_SIZE)
    except:
        Title_Font = TON_Font = Stars_Font = USD_Font = Time_Font = Percent_Font = ImageFont.load_default()

    # ----- Create card with rounded corners -----
    card = Image.new("RGBA", CARD_SIZE, 0)
    mask = Image.new("L", CARD_SIZE, 0)
    draw_mask = ImageDraw.Draw(mask)
    draw_mask.rounded_rectangle([0, 0, CARD_SIZE[0], CARD_SIZE[1]], CARD_RADIUS, fill=255)
    card_draw = ImageDraw.Draw(card)
    card_draw.rectangle([0, 0, CARD_SIZE[0], CARD_SIZE[1]], fill=CARD_COLOR)
    card.putalpha(mask)

    # ----- Add gift image -----
    gift_img = None
    gift_id = get_gift_id_by_name(gift_name)
    if gift_id:
        gift_img = fetch_gift_image_by_id(gift_id)
    if gift_img is None and gift_image_filename:
        gift_img_path = os.path.join(asset_dir, gift_image_filename)
        if os.path.exists(gift_img_path):
            gift_img = Image.open(gift_img_path).convert("RGBA")
    if gift_img:
        gift_img = gift_img.resize(GIFT_IMAGE_SIZE)
        card.paste(gift_img, GIFT_IMAGE_POS, gift_img)

    # ----- Add gift name -----
    display_name = gift_name.replace("-", " - ").title().replace(" - ", "-")
    card_draw.text(TITLE_POS, display_name, font=Title_Font, fill=TITLE_COLOR)

    # ----- Add TON and USD prices -----
    ton_icon = Image.open(os.path.join(asset_dir, "ton.png")).convert("RGBA").resize(TON_ICON_SIZE)
    card.paste(ton_icon, TON_ICON_POS, ton_icon)

    price_ton = round(price_stars * 0.0053, 2)
    ton_str = f"{price_ton}"
    card_draw.text(TON_PRICE_POS, ton_str, font=TON_Font, fill=(20, 20, 20))

    price_usd = round(price_ton * 2.9, 2)
    usd_label = f"$ {price_usd}"
    card_draw.text(USD_LABEL_POS, usd_label, font=USD_Font, fill=(20, 20, 20))

    stars_label = f"★ {price_stars}"
    card_draw.text(STARS_LABEL_POS, stars_label, font=Stars_Font, fill=(20, 20, 20))

    # ----- Add price chart -----
    chart_img = chart_img.resize((CARD_SIZE[0]-CHART_MARGIN, CHART_HEIGHT))
    card.paste(chart_img, (60, CARD_SIZE[1]-CHART_BOTTOM_MARGIN), chart_img)

    # ----- Add timestamp -----
    dt_str = dt.strftime("%d %b %Y • %H:%M UTC")
    w, h = get_text_size(card_draw, dt_str, Time_Font)
    card_draw.text(((CARD_SIZE[0]-w)//2, CARD_SIZE[1]-30), dt_str, font=Time_Font, fill=TIME_COLOR)

    # ----- Add price change percentage -----
    percent_text = "0"
    color = (0, 0, 0)
    if abs(percent_change) >= 0.005:
        percent_value = round(percent_change, 2)
        percent_text = f"{percent_value:+.2f}%"
        color = POSITIVE_CHANGE_COLOR if percent_value > 0 else NEGATIVE_CHANGE_COLOR

    # ----- Add percentage frame -----
    frame_x = CARD_SIZE[0] - FRAME_SIZE[0] - FRAME_MARGIN
    frame_y = FRAME_MARGIN

    frame_mask = Image.new("L", FRAME_SIZE, 0)
    frame_mask_draw = ImageDraw.Draw(frame_mask)
    frame_mask_draw.rounded_rectangle([0, 0, FRAME_SIZE[0], FRAME_SIZE[1]], radius=FRAME_RADIUS, fill=255)

    frame = Image.new("RGBA", FRAME_SIZE, 0)
    frame_draw = ImageDraw.Draw(frame)
    frame_draw.rounded_rectangle([0, 0, FRAME_SIZE[0], FRAME_SIZE[1]], radius=FRAME_RADIUS, fill=(255, 255, 255, 255))
    
    card.paste(frame, (frame_x, frame_y), frame_mask)

    # ----- Add percentage text -----
    text_w, text_h = get_text_size(card_draw, percent_text, Percent_Font)
    text_x = frame_x + (FRAME_SIZE[0] - text_w) / 2
    text_y = frame_y + (FRAME_SIZE[1] - text_h) / 2 - 2

    card_draw.text((text_x, text_y), percent_text, font=Percent_Font, fill=color)

    # ----- Add watermark -----
    watermark_text = "@GiftChartBot"
    watermark_font = ImageFont.truetype(font_path, 50)
    watermark_bbox = draw_mask.textbbox((0, 0), watermark_text, font=watermark_font)
    watermark_width = watermark_bbox[2] - watermark_bbox[0]
    watermark_x = (BG_SIZE[0] - watermark_width) // 2
    watermark_y = 10
    bg_draw = ImageDraw.Draw(bg)
    bg_draw.text((watermark_x, watermark_y), watermark_text, font=watermark_font, fill=(255, 255, 255))

    # ----- Compose final image -----
    bg.alpha_composite(card, card_pos)

    return bg