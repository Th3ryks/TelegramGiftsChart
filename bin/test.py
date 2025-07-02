from src.api.api_client import get_price_history, get_current_price, get_auth_data, PriceData as ApiPriceData
from src.generators.chart_generator import generate_chart_image, PriceData as ChartPriceData
from src.generators.card_generator import draw_card
import os
from dotenv import load_dotenv
from datetime import datetime, timezone
import sys
from typing import Tuple, Dict, Optional, cast, List, TypedDict
from PIL import Image

# ----- Constants -----
# Environment variables
ENV_VARS = {
    "API_ID": "API_ID",
    "API_HASH": "API_HASH",
    "PHONE_NUMBER": "PHONE_NUMBER"
}

# Price conversion rates
TON_TO_STARS = 0.0053
TON_TO_USD = 2.9

# File paths
CARD_OUTPUT_PATH = "card.png"
ASSETS_DIR = "assets"
GIFTS_JSON_PATH = "src/config/gifts.json"

# Date format
DATE_FORMAT = "%Y-%m-%dT%H:%M:%S.%fZ"

# Chart dimensions
CHART_WIDTH = 1500
CHART_HEIGHT = 220

# ----- Gift name mappings -----
GIFT_NAME_MAP: Dict[str, str] = {
    # Jack in the Box variations
    "jack in the box": "Jack-in-the-Box",
    "jack-in the box": "Jack-in-the-Box",
    "jack-in-the box": "Jack-in-the-Box",
    "jack": "Jack-in-the-Box",
    "jack box": "Jack-in-the-Box",
    "jitb": "Jack-in-the-Box",
    
    # B-Day Candle variations
    "b day candle": "B-Day Candle",
    "b day-candle": "B-Day Candle",
    "bday candle": "B-Day Candle",
    "birthday candle": "B-Day Candle",
    "candle": "B-Day Candle",
    
    # Plush Pepe variations
    "plush": "Plush Pepe",
    "pepe": "Plush Pepe",
    "pepe plush": "Plush Pepe",
    "plush pepe": "Plush Pepe",
    "frog plush": "Plush Pepe",
    "frog": "Plush Pepe",

    # Crystal Ball variations
    "crystal": "Crystal Ball",
    "crystal ball": "Crystal Ball",
    "ball": "Crystal Ball",
    "magic ball": "Crystal Ball",
    "fortune ball": "Crystal Ball",

    # Heart Locket variations
    "heart": "Heart Locket",
    "locket": "Heart Locket",
    "heart locket": "Heart Locket",
    "heart-locket": "Heart Locket",
    
    # Toy Bear variations
    "teddy": "Toy Bear",
    "bear": "Toy Bear",
    "teddy bear": "Toy Bear",
    "toy bear": "Toy Bear",
    
    # Lush Bouquet variations
    "bouquet": "Lush Bouquet",
    "flowers": "Lush Bouquet",
    "flower": "Lush Bouquet",
    "flower bouquet": "Lush Bouquet",
    "lush bouquet": "Lush Bouquet",
    
    # Perfume Bottle variations
    "perfume": "Perfume Bottle",
    "fragrance": "Perfume Bottle",
    "scent": "Perfume Bottle",
    "perfume bottle": "Perfume Bottle",
    
    # Diamond Ring variations
    "diamond": "Diamond Ring",
    "ring": "Diamond Ring",
    "diamond ring": "Diamond Ring",
    
    # Santa Hat variations
    "santa": "Santa Hat",
    "santa hat": "Santa Hat",
    "christmas hat": "Santa Hat",
    
    # Signet Ring variations
    "signet": "Signet Ring",
    "signet ring": "Signet Ring",
    
    # Precious Peach variations
    "peach": "Precious Peach",
    "precious peach": "Precious Peach",
    
    # Spiced Wine variations
    "wine": "Spiced Wine",
    "spiced wine": "Spiced Wine",
    "mulled wine": "Spiced Wine",
    
    # Jelly Bunny variations
    "bunny": "Jelly Bunny",
    "jelly": "Jelly Bunny",
    "jelly bunny": "Jelly Bunny",
    
    # Durov's Cap variations
    "cap": "Durov's Cap",
    "durov": "Durov's Cap",
    "durovs cap": "Durov's Cap",
    "durov cap": "Durov's Cap",
    
    # Eternal Rose variations
    "rose": "Eternal Rose",
    "eternal rose": "Eternal Rose",
    "forever rose": "Eternal Rose",
    
    # Berry Box variations
    "berry": "Berry Box",
    "berries": "Berry Box",
    "berry box": "Berry Box",
    
    # Vintage Cigar variations
    "cigar": "Vintage Cigar",
    "vintage cigar": "Vintage Cigar",
    
    # Magic Potion variations
    "potion": "Magic Potion",
    "magic potion": "Magic Potion",
    
    # Kissed Frog variations
    "kissed": "Kissed Frog",
    "kissed frog": "Kissed Frog",
    
    # Hex Pot variations
    "hex": "Hex Pot",
    "hex pot": "Hex Pot",
    "pot": "Hex Pot",
    
    # Evil Eye variations
    "evil": "Evil Eye",
    "eye": "Evil Eye",
    "evil eye": "Evil Eye",
    
    # Sharp Tongue variations
    "tongue": "Sharp Tongue",
    "sharp tongue": "Sharp Tongue",
    
    # Trapped Heart variations
    "trapped": "Trapped Heart",
    "trapped heart": "Trapped Heart",
    
    # Skull Flower variations
    "skull": "Skull Flower",
    "skull flower": "Skull Flower",
    
    # Scared Cat variations
    "cat": "Scared Cat",
    "scared cat": "Scared Cat",
    "scaredy cat": "Scared Cat",
    
    # Spy Agaric variations
    "agaric": "Spy Agaric",
    "spy": "Spy Agaric",
    "spy agaric": "Spy Agaric",
    "mushroom": "Spy Agaric",
    
    # Homemade Cake variations
    "cake": "Homemade Cake",
    "homemade": "Homemade Cake",
    "homemade cake": "Homemade Cake",
    
    # Genie Lamp variations
    "genie": "Genie Lamp",
    "lamp": "Genie Lamp",
    "genie lamp": "Genie Lamp",
    "magic lamp": "Genie Lamp",
    
    # Lunar Snake variations
    "lunar": "Lunar Snake",
    "lunar snake": "Lunar Snake",
    
    # Party Sparkler variations
    "sparkler": "Party Sparkler",
    "party sparkler": "Party Sparkler",
    "sparkle": "Party Sparkler",
    
    # Jester Hat variations
    "jester": "Jester Hat",
    "jester hat": "Jester Hat",
    
    # Witch Hat variations
    "witch": "Witch Hat",
    "witch hat": "Witch Hat",
    
    # Hanging Star variations
    "star": "Hanging Star",
    "hanging star": "Hanging Star",
    
    # Love Candle variations
    "love candle": "Love Candle",
    
    # Cookie Heart variations
    "cookie": "Cookie Heart",
    "cookie heart": "Cookie Heart",
    "heart cookie": "Cookie Heart",
    
    # Snow Globe variations
    "snow": "Snow Globe",
    "globe": "Snow Globe",
    "snow globe": "Snow Globe",
    
    # Holiday Drink variations
    "drink": "Holiday Drink",
    "holiday": "Holiday Drink",
    "holiday drink": "Holiday Drink",
    
    # Light Sword variations
    "sword": "Light Sword",
    "light": "Light Sword",
    "light sword": "Light Sword",
    "lightsaber": "Light Sword",
    
    # Bow Tie variations
    "bow": "Bow Tie",
    "tie": "Bow Tie",
    "bow tie": "Bow Tie",
    
    # Nail Bracelet variations
    "bracelet": "Nail Bracelet",
    "nail": "Nail Bracelet",
    "nail bracelet": "Nail Bracelet"
}

def normalize_gift_name(raw_name: str) -> Tuple[str, str]:
    """
    Normalize gift name and generate image filename.
    
    Args:
        raw_name: Raw gift name input
        
    Returns:
        Tuple of (normalized_name, image_filename)
    """
    normalized = GIFT_NAME_MAP.get(raw_name.lower(), raw_name.title().replace(" ", " "))
    return normalized, f"{normalized}.png"

def get_env_var(name: str) -> str:
    """Get environment variable with error handling."""
    value = os.getenv(name)
    if value is None:
        print(f"Error: Environment variable {name} is not set")
        sys.exit(1)
    return value

def convert_price_data(api_data: List[ApiPriceData]) -> List[ChartPriceData]:
    """Convert API price data to chart price data format."""
    return [cast(ChartPriceData, {
        "priceUsd": float(item["priceUsd"]),
        "listed_at": item["listed_at"]
    }) for item in api_data]

def main() -> None:
    """Main application entry point."""
    # ----- Load environment variables -----
    load_dotenv()
    
    api_id = int(get_env_var(ENV_VARS["API_ID"]))
    api_hash = get_env_var(ENV_VARS["API_HASH"])
    phone_number = get_env_var(ENV_VARS["PHONE_NUMBER"])

    # ----- Get authentication data -----
    auth_data = get_auth_data(api_id, api_hash)
    if not auth_data:
        print("Error: Failed to get auth data")
        sys.exit(1)

    # ----- Process gift name -----
    raw_gift_name = "frog"
    gift_name, gift_image_filename = normalize_gift_name(raw_gift_name)
    print(f"Raw gift name: {raw_gift_name}, Normalized gift_name: {gift_name}, Image filename: {gift_image_filename}")

    # ----- Fetch price history -----
    print("\n=== Price History API Response ===")
    api_data = get_price_history(gift_name, auth_data)
    print("Price history data points:")
    for point in api_data:
        print(f"Time: {point['listed_at']}, Price: {point['priceUsd']} TON")
    print("================================\n")

    api_data = sorted(api_data, key=lambda x: x["listed_at"])

    # ----- Update with current price -----
    print("\n=== Current Price API Response ===")
    current_price = get_current_price(gift_name, auth_data)
    if current_price is None:
        print("Error: Could not get current price")
        sys.exit(1)
    price_ton = float(current_price)
    print(f"Current price: {price_ton} TON")
    print("================================\n")

    if api_data and float(api_data[-1]["priceUsd"]) != price_ton:
        current_time = datetime.now(timezone.utc)
        api_data.append(cast(ApiPriceData, {
            "priceUsd": price_ton,
            "listed_at": current_time.strftime(DATE_FORMAT)
        }))
        api_data = sorted(api_data, key=lambda x: x["listed_at"])

    # ----- Generate price chart -----
    chart_data = convert_price_data(api_data)
    max_price = float(max(item["priceUsd"] for item in chart_data)) if chart_data else 0.0
    chart_img = generate_chart_image(CHART_WIDTH, CHART_HEIGHT, chart_data)
    if chart_img is None:
        print("Error: Failed to generate chart image")
        sys.exit(1)

    # ----- Calculate prices -----
    price_stars = int(price_ton / TON_TO_STARS)
    price_usd = price_ton * TON_TO_USD
    print(f"Formatted prices: TON={price_ton:.2f}, USD={price_usd:.2f}")

    # ----- Calculate price change percentage -----
    percent = 0.0
    if len(chart_data) > 1:
        max_historical_price = float(max(item["priceUsd"] for item in chart_data))
        percent = ((price_ton - max_historical_price) / max_historical_price) * 100
        print(f"Max historical price: {max_historical_price}, Current price: {price_ton}, Percent change: {percent}%")

    # ----- Generate and save card -----
    dt = datetime.now(timezone.utc)
    card = draw_card(
        gift_name=gift_name,
        gift_image_filename=gift_image_filename,
        price_stars=price_stars,
        chart_img=chart_img,
        dt=dt,
        percent_change=percent,
        asset_dir=ASSETS_DIR
    )
    card.save(CARD_OUTPUT_PATH)
    print(f"Image saved as {CARD_OUTPUT_PATH}")

if __name__ == "__main__":
    main()