import json
import requests
from io import BytesIO
from PIL import Image

# ----- Constants -----
GIFTS_JSON_DEFAULT_PATH = "src/config/gifts.json"
GIFT_IMAGE_API_URL = "https://api.changes.tg/original/{}.png"

def get_gift_id_by_name(gift_name: str, gifts_json_path: str = GIFTS_JSON_DEFAULT_PATH) -> str | None:
    """
    Find gift ID by its name in the gifts JSON file.
    
    Args:
        gift_name: Name of the gift to search for
        gifts_json_path: Path to the gifts JSON file
        
    Returns:
        Gift ID if found, None otherwise
    """
    with open(gifts_json_path, "r", encoding="utf-8") as f:
        gifts = json.load(f)
    for gid, name in gifts.items():
        if name.lower() == gift_name.lower():
            return gid
    return None

def fetch_gift_image_by_id(gift_id: str) -> Image.Image | None:
    """
    Fetch gift image from the API by its ID.
    
    Args:
        gift_id: ID of the gift to fetch
        
    Returns:
        PIL Image if successful, None otherwise
    """
    url = GIFT_IMAGE_API_URL.format(gift_id)
    response = requests.get(url)
    if response.status_code == 200:
        return Image.open(BytesIO(response.content)).convert("RGBA")
    return None
