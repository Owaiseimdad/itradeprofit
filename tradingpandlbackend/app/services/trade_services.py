import pandas as pd
from app.utils.math_utils import round_value, serialize_result
import pandas as pd
from app.models import db, Trade
from .trade_services_without_date import calculate_pnl_without_date 

def calculate_pnl(df):
    # Ensure 'quantity' is integer and 'price' is float
    df['quantity'] = df['quantity'].astype(int)
    df['price'] = df['price'].astype(float)

    # Dictionary to store P&L by date and overall
    pnl_by_date = {}
    overall_pnl = {'buy': 0, 'sell': 0, 'pnl': 0}

    # Group trades by date
    for date, group in df.groupby(df['trade_date'].dt.date):
        daily_summary = {}
        # Process each trade for the current date
        for _, row in group.iterrows():
            symbol = row['symbol']
            quantity = row['quantity']
            price = row['price']
            trade_type = row['trade_type']
            trade_value = round_value(quantity * price)

            # Initialize symbol entry if it doesn't exist
            if symbol not in daily_summary:
                daily_summary[symbol] = {'buy': 0, 'sell': 0, 'buy_quantity': 0, 'sell_quantity': 0}

            if trade_type == 'buy':
                daily_summary[symbol]['buy'] += trade_value
                daily_summary[symbol]['buy_quantity'] += quantity
            elif trade_type == 'sell':
                daily_summary[symbol]['sell'] += trade_value
                daily_summary[symbol]['sell_quantity'] += quantity

        # Calculate P&L for each symbol on the current date
        date_pnl = {'date': date, 'symbols': {}}
        for symbol, data in daily_summary.items():
            total_buy_cost = round_value(data['buy'])
            total_sell_revenue = round_value(data['sell'])
            symbol_pnl = round_value(total_sell_revenue - total_buy_cost)

            date_pnl['symbols'][symbol] = {
                'buy': total_buy_cost,
                'sell': total_sell_revenue,
                'pnl': symbol_pnl
            }

            # Add to overall totals
            overall_pnl['buy'] += total_buy_cost
            overall_pnl['sell'] += total_sell_revenue
            overall_pnl['pnl'] += symbol_pnl

        # Save daily P&L data
        pnl_by_date[date] = date_pnl

    # Round final overall P&L values
    overall_pnl = {k: round_value(v) for k, v in overall_pnl.items()}

    return {
        'pnl_by_date': pnl_by_date,
        'overall_pnl': overall_pnl
    }

def read_trades_from_csv(file):
    df = pd.read_csv(file)
    df['trade_date'] = df['trade_date'].str.strip()
    df['order_execution_time'] = df['order_execution_time'].str.strip()
    df['trade_date'] = pd.to_datetime(df['trade_date'], errors='coerce', dayfirst=True)
    df['order_execution_time'] = pd.to_datetime(df['order_execution_time'], errors='coerce')
    return df

def validate_trade_data(df):
    required_columns = ['symbol', 'isin', 'trade_date', 'exchange', 'segment', 'series', 'trade_type', 'quantity', 'price', 'trade_id', 'order_id', 'order_execution_time']
    if not all(col in df.columns for col in required_columns):
        raise ValueError('CSV file is missing one or more required columns.')

    if any(df['symbol'].str.len() > 100): 
        raise ValueError('One or more symbols exceed the allowed length.')
    
    if any(df['trade_type'].str.len() > 20):
        raise ValueError('One or more trade types exceed the allowed length.')

def save_trades(df, user_id):
    trades_to_add = []
    for _, row in df.iterrows():
        trade = Trade(
            symbol=row['symbol'],
            isin=row['isin'],
            trade_date=row['trade_date'],
            exchange=row['exchange'],
            segment=row['segment'],
            series=row['series'],
            trade_type=row['trade_type'],
            quantity=row['quantity'],
            price=row['price'],
            trade_id=row['trade_id'],
            order_execution_time=row['order_execution_time'],
            uuid=user_id
        )
        trades_to_add.append(trade)
    
    db.session.bulk_save_objects(trades_to_add)
    db.session.commit()

def process_trades(file, user_id):
    df = read_trades_from_csv(file)
    validate_trade_data(df)
    save_trades(df, user_id)
    pnl_result = calculate_pnl(df)
    pnl_plain = calculate_pnl_without_date(df)
    return serialize_result({'PnL':pnl_result, 'Pnl_no_date':pnl_plain})


def serialize_all_trade(trade):
    return {
        'id': trade.id,
        'symbol': trade.symbol,
        'isin': trade.isin,
        'trade_date': trade.trade_date,
        'exchange': trade.exchange,
        'segment': trade.segment,
        'series': trade.series,
        'trade_type': trade.trade_type,
        'quantity': trade.quantity,
        'price': trade.price,
        'trade_id': trade.trade_id,
        'order_id': trade.order_id,
        'order_execution_time': trade.order_execution_time
    }