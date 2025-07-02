import os
import json
import logging
import uuid
from datetime import datetime, timezone, timedelta
from typing import Dict, List, cast, Optional, Any

from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiogram.types import FSInputFile, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, Message
from aiogram.utils.keyboard import InlineKeyboardBuilder
from dotenv import load_dotenv
from PIL import Image
from io import BytesIO

from src.generators.chart_generator import generate_chart_image, PriceData as ChartPriceData
from src.generators.card_generator import draw_card
from src.api.api_client import get_price_history, get_current_price, PriceData as ApiPriceData, get_auth_data
from src.database.database import init_db, update_last_success, get_last_success_time

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
token = os.getenv("TELEGRAM_BOT_TOKEN")
if not token:
    raise ValueError("TELEGRAM_BOT_TOKEN not found in environment variables ❌")
    
bot = Bot(token=token)
dp = Dispatcher()

# Load gifts data
with open('src/config/gifts.json', 'r') as f:
    gifts_data = json.load(f)

# Gift name mappings for better user experience
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

# Create reverse mapping for gift names
gifts_names = {v.lower(): k for k, v in gifts_data.items()}

# Get API credentials
api_id = int(os.getenv("API_ID", "0"))
api_hash = os.getenv("API_HASH", "")

# Get auth data once at startup
AUTH_DATA = get_auth_data(api_id, api_hash)
if not AUTH_DATA:
    raise ValueError("Failed to get auth data. Check your API credentials ❌")

# Cast AUTH_DATA to str since we checked it's not None
AUTH_DATA = cast(str, AUTH_DATA)

TON_TO_STARS = 0.0053
TON_TO_USD = 2.90

# Rate limiting
RATE_LIMIT_SECONDS = 10

# Initialize database
init_db()

@dp.message(CommandStart())
async def start_command(message: types.Message):
    """Handle the /start command"""
    user_name = message.from_user.first_name if message.from_user else "there"
    await message.answer(
        f"Hi {user_name}! I'm the Telegram Gift Price Bot 🎁\n\n"
        "I can show you price cards for Telegram gifts with modern cool chart photos 📊\n\n"
        "Just send me the name of any Telegram gift to see its price chart! ✨\n\n"
        "For example, try: 'Plush Pepe 🐸', 'Crystal Ball 🔮', 'Heart Locket 💝', etc."
    )

async def generate_and_send_chart(chat_id: int, gift_name: str, message_id: Optional[int] = None) -> bool:
    """Generate and send chart image"""
    try:
        # Get price history from API
        api_price_data = get_price_history(gift_name, AUTH_DATA)
        if not api_price_data:
            await bot.send_message(chat_id, f"Sorry, I couldn't find any price history for '{gift_name}' in the last 12 hours. Please try again later! 📈")
            if message_id is not None:
                await bot.delete_message(chat_id, message_id)
            return False

        # Sort data by time
        api_price_data = sorted(api_price_data, key=lambda x: x["listed_at"])

        # Get current price and update data if needed
        current_price = get_current_price(gift_name, AUTH_DATA)
        if current_price is None:
            await bot.send_message(chat_id, "Sorry, couldn't get current price. Please try again later! 📈")
            if message_id is not None:
                await bot.delete_message(chat_id, message_id)
            return False

        price_ton = float(current_price)
        
        # Add current price to data if different from last point
        if api_price_data and float(api_price_data[-1]["priceUsd"]) != price_ton:
            current_time = datetime.now(timezone.utc)
            api_price_data.append(cast(ApiPriceData, {
                "priceUsd": price_ton,
                "listed_at": current_time.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
            }))
            api_price_data = sorted(api_price_data, key=lambda x: x["listed_at"])

        # Convert API data to chart format
        price_data: List[ChartPriceData] = [
            cast(ChartPriceData, {
                "priceUsd": float(item["priceUsd"]),
                "listed_at": str(item["listed_at"])
            })
            for item in api_price_data
        ]

        # Generate chart
        chart_image = generate_chart_image(1500, 220, price_data)
        
        if chart_image:
            # Calculate prices
            price_stars = int(price_ton / TON_TO_STARS)
            price_usd = price_ton * TON_TO_USD

            # Calculate price change percentage
            percent_change = 0.0
            if len(price_data) > 1:
                max_historical_price = float(max(item["priceUsd"] for item in price_data))
                percent_change = ((price_ton - max_historical_price) / max_historical_price) * 100

            # Generate the full card
            card = draw_card(
                gift_name=gift_name,
                price_stars=price_stars,
                chart_img=chart_image,
                dt=datetime.now(timezone.utc),
                percent_change=percent_change,
                asset_dir="assets"
            )
            
            if card:
                # Generate unique temporary filename
                temp_file = f"temp_card_{uuid.uuid4()}.png"
                try:
                    # Save image to temporary file
                    card.save(temp_file, format='PNG')
                    
                    # Send the image
                    await bot.send_photo(
                        chat_id,
                        FSInputFile(temp_file),
                        caption=f"Price chart for 🎁 {gift_name} (12h) ✨"
                    )
                    
                    # Delete processing message if exists
                    if message_id is not None:
                        await bot.delete_message(chat_id, message_id)
                    return True
                finally:
                    # Clean up temporary file
                    if os.path.exists(temp_file):
                        os.remove(temp_file)
            else:
                await bot.send_message(chat_id, "Sorry, I couldn't generate the card. Please try again later! 😔")
                if message_id is not None:
                    await bot.delete_message(chat_id, message_id)
                return False
        else:
            await bot.send_message(chat_id, "Sorry, I couldn't generate the chart. Please try again later! 😔")
            if message_id is not None:
                await bot.delete_message(chat_id, message_id)
            return False
    except Exception as e:
        logging.error(f"Error processing gift request: {e}")
        await bot.send_message(chat_id, "Sorry, something went wrong while processing your request. Please try again later! 😔")
        if message_id is not None:
            await bot.delete_message(chat_id, message_id)
        return False

@dp.message()
async def handle_gift_request(message: types.Message):
    """Handle gift name messages"""
    if not message.text:
        await message.answer("Please send me a text message with the gift name! 🎁")
        return
    
    if not message.from_user:
        await message.answer("Error identifying user ❌")
        return
    
    user_id = message.from_user.id
    
    # Check rate limit only if there was a successful request
    last_success = get_last_success_time(user_id)
    if last_success is not None:
        time_since_last = datetime.now().timestamp() - last_success
        if time_since_last < RATE_LIMIT_SECONDS:
            await message.answer(f"Please wait {RATE_LIMIT_SECONDS - int(time_since_last)} seconds before making another request ⏳")
            return
        
    # Clean up the gift name
    gift_name = message.text.strip()
    if gift_name.lower().endswith(" 12h"):
        gift_name = gift_name[:-4]
    gift_name = gift_name.strip()
    gift_name_lower = gift_name.lower()
    
    # Try to find the gift in our mapping first
    mapped_name = GIFT_NAME_MAP.get(gift_name_lower)
    if mapped_name:
        gift_name = mapped_name
        gift_name_lower = mapped_name.lower()
    
    # Check if the gift exists
    if gift_name_lower not in gifts_names:
        # Get list of similar gifts for suggestion
        similar_gifts = []
        # First check GIFT_NAME_MAP for similar names
        for key, value in GIFT_NAME_MAP.items():
            if any(word in key for word in gift_name_lower.split()):
                if value not in similar_gifts:
                    similar_gifts.append(value)
        # Then check original names if we don't have enough suggestions
        if len(similar_gifts) < 5:
            for name in gifts_data.values():
                if name not in similar_gifts and any(word in name.lower() for word in gift_name_lower.split()):
                    similar_gifts.append(name)
                if len(similar_gifts) >= 5:
                    break
        
        suggestion_text = "\n\nDid you mean one of these? 🤔\n" + "\n".join([f"• {name} ✨" for name in similar_gifts[:5]]) if similar_gifts else ""
        
        await message.answer(
            f"Sorry, I couldn't find '{gift_name}'. Please check the gift name and try again! 🔍" + suggestion_text
        )
        return

    # Send processing message
    processing_msg = await message.answer(f"Generating price chart for {gift_name} 🎨...")
    
    # Generate and send chart
    success = await generate_and_send_chart(message.chat.id, gift_name, processing_msg.message_id)
    
    # Update rate limit only on success
    if success:
        update_last_success(user_id)

async def main():
    """Main function to start the bot"""
    await dp.start_polling(bot)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main()) 