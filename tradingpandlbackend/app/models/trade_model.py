from . import db 

class Trade(db.Model):
    __tablename__ = 'trades'
    
    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.String(255), db.ForeignKey('users.uuid'), nullable=False)  # Reference uuid
    symbol = db.Column(db.String(50))
    isin = db.Column(db.String(50))
    trade_date = db.Column(db.Date)
    exchange = db.Column(db.String(50))
    segment = db.Column(db.String(50))
    series = db.Column(db.String(50))
    trade_type = db.Column(db.String(10))
    quantity = db.Column(db.Integer)
    price = db.Column(db.Float)
    trade_id = db.Column(db.String(50))
    order_execution_time = db.Column(db.DateTime)
