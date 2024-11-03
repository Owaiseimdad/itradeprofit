from datetime import datetime, date

def round_value(value, decimals=2):
    """
    Round a number to a specified number of decimal places.
    
    :param value: The number to round.
    :param decimals: The number of decimal places to round to (default is 4).
    :return: The rounded number."""
    
    return round(value, decimals)

def parse_date(date_str):
    # Convert date from DD-MM-YYYY to YYYY-MM-DD
    return datetime.strptime(date_str, "%d-%m-%Y").strftime("%Y-%m-%d")


def serialize_result(result):
    if isinstance(result, dict):
        return {serialize_key(k): serialize_result(v) for k, v in result.items()}
    elif isinstance(result, list):
        return [serialize_result(item) for item in result]
    elif isinstance(result, (datetime, date)):
        return result.strftime('%Y-%m-%d')
    return result

def serialize_key(key):
    # If the key is a date, format it
    if isinstance(key, (datetime, date)):
        return key.strftime('%Y-%m-%d')
    return key