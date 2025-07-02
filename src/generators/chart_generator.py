from PIL import Image, ImageDraw, ImageFont
import random
from datetime import datetime, timezone, timedelta
import os
from typing import List, Dict, Tuple, Optional, Union, TypedDict

# ----- Type Aliases -----
class PriceData(TypedDict):
    priceUsd: float
    listed_at: str

# ----- Constants -----
FONT_PATH = "/System/Library/Fonts/SF-Pro-Rounded-Black.otf"
FALLBACK_FONT_PATH = "/System/Library/Fonts/SFNSDisplay.ttf"

PRICE_FONT_SIZE = 20
TIME_FONT_SIZE = 16

GREEN_COLOR = (46, 204, 113)
RED_COLOR = (231, 76, 60)
TIME_LABEL_COLOR = "#7C7C7C"

LEFT_PADDING = 80
RIGHT_PADDING = 150
BOTTOM_PADDING = 25
TOP_PADDING = 50

LINE_WIDTH = 7
MARKER_SIZE = 7
FILL_OPACITY = 15
MARKER_OUTER_OPACITY = 220
PRICE_LABEL_OFFSET = 20

TIME_POINTS = [12, 9, 6, 3, 0]
TIME_RANDOM_OFFSET = (-10, 10)

DATE_FORMAT = "%Y-%m-%dT%H:%M:%S.%fZ"
TIME_LABEL_FORMAT = '%H:%M'

def generate_chart_image(
    width: int,
    height: int,
    chart_data: List[PriceData],
    max_price: float = 0,
    color: Tuple[int, int, int] = GREEN_COLOR,
    font_size: int = 40,
    time_font_path: str = FALLBACK_FONT_PATH,
    time_font_size: int = 20,
) -> Optional[Image.Image]:
    """
    Generate a price chart image.
    
    Args:
        width: Chart width in pixels
        height: Chart height in pixels
        chart_data: List of price data points
        max_price: Maximum price to display (0 for auto-scaling)
        color: RGB color tuple for the chart
        font_size: Font size for price labels
        time_font_path: Path to font file for time labels
        time_font_size: Font size for time labels
        
    Returns:
        PIL Image object or None if error occurs
    """
    # ----- Create base image -----
    chart_img = Image.new('RGBA', (width, height))
    draw = ImageDraw.Draw(chart_img)

    # ----- Load fonts -----
    try:
        price_font = ImageFont.truetype(FONT_PATH, PRICE_FONT_SIZE)
        time_font = ImageFont.truetype(FONT_PATH, TIME_FONT_SIZE)
    except Exception as e:
        print(f"Error loading font {FONT_PATH}: {e}")
        try:
            price_font = ImageFont.truetype(FALLBACK_FONT_PATH, PRICE_FONT_SIZE)
            time_font = ImageFont.truetype(FALLBACK_FONT_PATH, TIME_FONT_SIZE)
        except Exception as e:
            print(f"Error loading fallback font: {e}")
            return None

    # ----- Generate or process data points -----
    if not chart_data:
        num_points = 24
        prices = [random.uniform(5, 15) for _ in range(num_points)]
        times = [f"{i:02d}:00" for i in range(num_points)]
    else:
        prices = [float(point["priceUsd"]) for point in chart_data]
        times = [point["listed_at"] for point in chart_data]

    # ----- Calculate price change and set color -----
    price_change = prices[-1] - prices[0] if prices else 0
    color = GREEN_COLOR if price_change >= 0 else RED_COLOR

    # ----- Calculate price range and padding -----
    min_price = min(prices) if prices else 0
    max_price = max(prices) if prices else 0
    price_range = max_price - min_price
    padding = price_range * 0.1 if price_range > 0 else 1
    adjusted_min = min_price - padding
    adjusted_max = max_price + padding
    adjusted_range = adjusted_max - adjusted_min

    max_price_idx = prices.index(max_price)
    min_price_idx = prices.index(min_price)

    # ----- Calculate chart dimensions -----
    num_points = len(prices)
    effective_width = width - LEFT_PADDING - RIGHT_PADDING
    effective_height = height - TOP_PADDING - BOTTOM_PADDING

    # ----- Generate chart points -----
    points = []
    for i, price in enumerate(prices):
        x = i * (effective_width / (num_points - 1)) + LEFT_PADDING
        normalized_price = (price - adjusted_min) / adjusted_range if adjusted_range > 0 else 0.5
        y = effective_height - (normalized_price * effective_height)
        y = max(2, min(height - BOTTOM_PADDING - 2, y))
        points.append((x, y))

    marker_points = [0]
    if num_points >= 8:
        marker_points += [num_points // 4, num_points // 2, (num_points * 3) // 4]
    marker_points.append(num_points - 1)

    # ----- Draw filled area under curve -----
    fill_points = points.copy()
    fill_points.append((points[-1][0], height))
    fill_points.append((points[0][0], height))
    fill_color = color + (FILL_OPACITY,)
    draw.polygon(fill_points, fill=fill_color)

    # ----- Draw line segments -----
    for i in range(len(points) - 1):
        draw.line([points[i], points[i+1]], fill=color, width=LINE_WIDTH)

    # ----- Draw markers and price labels -----
    for idx in marker_points:
        if idx < len(points):
            x, y = points[idx]
            draw.ellipse(
                (x - MARKER_SIZE, y - MARKER_SIZE, x + MARKER_SIZE, y + MARKER_SIZE),
                fill=(255, 255, 255, MARKER_OUTER_OPACITY),
                outline=color
            )
            inner_size = MARKER_SIZE // 2
            draw.ellipse(
                (x - inner_size, y - inner_size, x + inner_size, y + inner_size),
                fill=color
            )

    # ----- Add time labels -----
    if chart_data and len(chart_data) >= 2:
        num_labels = 5
        step = (len(chart_data) - 1) / (num_labels - 1)
        
        timestamp_positions = {}
        
        for i in range(num_labels):
            idx = min(int(i * step), len(chart_data) - 1)
            point_time = datetime.strptime(chart_data[idx]["listed_at"], DATE_FORMAT).replace(tzinfo=timezone.utc)
            time_str = point_time.strftime(TIME_LABEL_FORMAT)
            
            x = LEFT_PADDING + (i * (effective_width / (num_labels - 1)))
            x = max(LEFT_PADDING, min(x, width - RIGHT_PADDING - 10))
            
            if time_str not in timestamp_positions:
                timestamp_positions[time_str] = []
            timestamp_positions[time_str].append(x)
        
        for time_str, positions in timestamp_positions.items():
            avg_x = sum(positions) / len(positions)
            
            bbox = draw.textbbox((0, 0), time_str, font=time_font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            
            text_x = avg_x - text_width / 2
            if text_x < LEFT_PADDING:
                text_x = LEFT_PADDING
            elif text_x + text_width > width - RIGHT_PADDING:
                text_x = width - RIGHT_PADDING - text_width
            
            draw.text(
                (text_x, height - BOTTOM_PADDING + 5),
                time_str,
                fill=TIME_LABEL_COLOR,
                font=time_font
            )

    # ----- Add price labels for min and max points -----
    for idx, price, is_max in [(max_price_idx, max_price, True), (min_price_idx, min_price, False)]:
        x, y = points[idx]
        price_str = f"{price:.2f}" if price < 20 else f"{price:.1f}"
            
        bbox = draw.textbbox((0, 0), price_str, font=price_font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        text_x = width - RIGHT_PADDING + 10
        text_y = y - text_height/2
        
        draw.text(
            (text_x, text_y),
            price_str,
            font=price_font,
            fill=TIME_LABEL_COLOR
        )

    return chart_img