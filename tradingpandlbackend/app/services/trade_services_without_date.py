from app.utils.math_utils import round_value

def calculate_pnl_without_date(df):
    # Ensure 'quantity' is integer and 'price' is float
    df['quantity'] = df['quantity'].astype(int)
    df['price'] = df['price'].astype(float)

    # Dictionary to store P&L by symbol
    pnl_by_symbol = {}

    # Process each trade in the DataFrame
    for _, row in df.iterrows():
        symbol = row['symbol']
        quantity = row['quantity']
        price = row['price']
        trade_type = row['trade_type']
        trade_value = round_value(quantity * price)

        # Initialize symbol entry if it doesn't exist
        if symbol not in pnl_by_symbol:
            pnl_by_symbol[symbol] = {'buy': 0, 'sell': 0}

        if trade_type == 'buy':
            pnl_by_symbol[symbol]['buy'] += trade_value
        elif trade_type == 'sell':
            pnl_by_symbol[symbol]['sell'] += trade_value

    # Separate valid and invalid results
    valid_results = []
    invalid_results = []

    for symbol, totals in pnl_by_symbol.items():
        total_buy = round_value(totals['buy'])
        total_sell = round_value(totals['sell'])
        symbol_pnl = round_value(total_sell - total_buy)

        if total_buy > 0 and total_sell > 0:
            valid_results.append({
                'symbol': symbol,
                'buy': total_buy,
                'sell': total_sell,
                'pnl': symbol_pnl
            })
        else:
            invalid_results.append({
                'symbol': symbol,
                'buy': total_buy,
                'sell': total_sell,
                'pnl': symbol_pnl  # You can choose to omit pnl for invalids if needed
            })

    return {"valid":valid_results, "invalid":invalid_results}
