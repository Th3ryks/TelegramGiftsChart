from typing import List, Dict, Tuple

# ----- Type Aliases -----
PriceData = List[Dict[str, float | str]]
PriceRange = Tuple[float, float]

def format_price_data(price_data: PriceData) -> PriceData:
    """
    Format raw price data into a standardized structure.
    
    Args:
        price_data: List of dictionaries containing date and price
        
    Returns:
        Formatted price data with consistent types
    """
    formatted_data = []
    for item in price_data:
        formatted_data.append({
            'date': item['date'],
            'price': float(item['price'])
        })
    return formatted_data

def calculate_average_price(price_data: PriceData) -> float:
    """
    Calculate the average price from price data.
    
    Args:
        price_data: List of dictionaries containing price information
        
    Returns:
        Average price, or 0 if no data
    """
    if not price_data:
        return 0.0
    total_price = 0.0
    for item in price_data:
        total_price += float(item['price'])
    return total_price / len(price_data)

def get_price_range(price_data: PriceData) -> PriceRange:
    """
    Get the minimum and maximum prices from price data.
    
    Args:
        price_data: List of dictionaries containing price information
        
    Returns:
        Tuple of (min_price, max_price), or (0, 0) if no data
    """
    if not price_data:
        return (0.0, 0.0)
    prices = [float(item['price']) for item in price_data]
    return (min(prices), max(prices))