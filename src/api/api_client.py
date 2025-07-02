import portalsmp.portalsapi as portalsapi
from datetime import datetime, timezone, timedelta
import asyncio
from typing import List, Dict, Union, Optional, TypedDict

# ----- Constants -----
PRICE_HISTORY_LIMIT = 1000000
DATE_FORMAT = "%Y-%m-%dT%H:%M:%S.%fZ"
HOURS_TO_FETCH = 12
NUMBER_OF_POINTS = 80
HOURS_INTERVAL = HOURS_TO_FETCH / (NUMBER_OF_POINTS - 1)

# ----- Type Aliases -----
class PriceData(TypedDict):
    priceUsd: float
    listed_at: str

PriceHistory = List[PriceData]

def get_auth_data(api_id: int, api_hash: str) -> Optional[str]:
    """Get authentication data for the Portals API"""
    try:
        return asyncio.run(portalsapi.update_auth(api_id, api_hash))
    except Exception as e:
        print(f"Error getting auth data: {e}")
        return None

def get_current_price(gift_name: str, auth_data: Optional[str]) -> Optional[float]:
    """Get current price for a gift"""
    if auth_data is None:
        print("Error: auth_data is None")
        return None
        
    try:
        result = portalsapi.marketActivity(
            sort="price_asc",
            activityType="listing",
            limit=1,
            gift_name=gift_name,
            authData=auth_data
        )
        if isinstance(result, list) and len(result) > 0:
            return float(result[0]["price"]) if result[0].get("price") else None
        return None
    except Exception as e:
        print(f"Error getting current price: {e}")
        return None

def get_price_history(gift_name: str, auth_data: Optional[str], time_range: str = "12h") -> PriceHistory:
    """
    Get price history for a gift from the Portals API.
    Always returns 12-hour history with 5 points.
    """
    if auth_data is None:
        print("Error: auth_data is None")
        return []
        
    try:
        # ----- Fetch market activity data -----
        results = portalsapi.marketActivity(
            sort="price_asc",
            activityType="listing",
            limit=PRICE_HISTORY_LIMIT,
            gift_name=gift_name,
            authData=auth_data
        )
        
        if isinstance(results, str):
            print(f"Error: API returned string instead of list: {results}")
            return []
        if not isinstance(results, list):
            print(f"Error: API returned unexpected type: {type(results)}")
            return []
        
        now = datetime.now(timezone.utc)
        chart_time = now - timedelta(hours=HOURS_TO_FETCH)
        
        print(f"Current time: {now}")
        print(f"Filtering data between {chart_time} and {now}")
        
        all_data: List[PriceData] = []
        
        for item in results:
            try:
                listed_at = datetime.strptime(str(item["listed_at"]), DATE_FORMAT).replace(tzinfo=timezone.utc)
                if listed_at >= chart_time and listed_at <= now:
                    all_data.append({
                        "priceUsd": float(item["price"]),
                        "listed_at": item["listed_at"]
                    })
            except (ValueError, KeyError) as e:
                print(f"Error processing data point: {e}")
                continue
        
        if not all_data:
            print("No data points found in the specified time range")
            return []
            
        all_data.sort(key=lambda x: datetime.strptime(str(x["listed_at"]), DATE_FORMAT))
        
        if len(all_data) > NUMBER_OF_POINTS:
            step = len(all_data) // NUMBER_OF_POINTS
            filtered_data = [all_data[i] for i in range(0, len(all_data), step)]
            if len(filtered_data) > NUMBER_OF_POINTS:
                filtered_data = filtered_data[:NUMBER_OF_POINTS]
            return filtered_data
        
        return all_data
        
    except Exception as e:
        print(f"Error fetching price history: {e}")
        return []