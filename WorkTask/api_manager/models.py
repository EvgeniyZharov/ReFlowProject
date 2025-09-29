from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class WBAccount(db.Model):
    __tablename__ = 'wb_accounts'
    
    id = db.Column(db.Integer, primary_key=True)
    api_key = db.Column(db.String(255), unique=True, nullable=False)
    account_name = db.Column(db.String(100))
    company_name = db.Column(db.String(100))
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_sync = db.Column(db.DateTime)
    
    cards = db.relationship('WBCard', backref='account', lazy=True)
    sync_logs = db.relationship('SyncLog', backref='account', lazy=True)


class WBCard(db.Model):
    __tablename__ = 'wb_cards'
    
    id = db.Column(db.Integer, primary_key=True)
    account_id = db.Column(db.Integer, db.ForeignKey('wb_accounts.id'), nullable=False)
    nm_id = db.Column(db.Integer, nullable=False)
    sku = db.Column(db.String(100))
    imt_name = db.Column(db.String(500))
    subject_name = db.Column(db.String(200))
    brand_name = db.Column(db.String(200))
    current_price = db.Column(db.Numeric(10, 2))
    original_price = db.Column(db.Numeric(10, 2))
    total_quantity = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    sizes = db.relationship('WBSize', backref='card', lazy=True)
    images = db.relationship('WBImage', backref='card', lazy=True)

class WBSize(db.Model):
    __tablename__ = 'wb_sizes'
    
    id = db.Column(db.Integer, primary_key=True)
    card_id = db.Column(db.Integer, db.ForeignKey('wb_cards.id'), nullable=False)
    size_name = db.Column(db.String(50))
    size_sku = db.Column(db.String(100))
    quantity = db.Column(db.Integer)
    barcode = db.Column(db.String(100))

class WBImage(db.Model):
    __tablename__ = 'wb_images'
    
    id = db.Column(db.Integer, primary_key=True)
    card_id = db.Column(db.Integer, db.ForeignKey('wb_cards.id'), nullable=False)
    image_url = db.Column(db.Text, nullable=False)

class SyncLog(db.Model):
    __tablename__ = 'sync_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    account_id = db.Column(db.Integer, db.ForeignKey('wb_accounts.id'), nullable=False)
    status = db.Column(db.String(20))
    cards_processed = db.Column(db.Integer)
    error_message = db.Column(db.Text)
    sync_date = db.Column(db.DateTime, default=datetime.utcnow)




    