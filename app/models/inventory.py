from app.extensions import db
from datetime import datetime

class InventoryItem(db.Model):
    __tablename__ = 'inventory_items'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.Integer, default=0)
    description = db.Column(db.Text)
    category = db.Column(db.String(50), default='general')
    unit = db.Column(db.String(20), default='unit')
    min_stock = db.Column(db.Integer, default=10)
    reorder_qty = db.Column(db.Integer, default=50)
    avg_daily_use = db.Column(db.Float, default=0.0)
    supplier = db.Column(db.String(100))
    cost_per_unit = db.Column(db.Numeric(10, 2), default=0.0)
    location = db.Column(db.String(100), default='Main Storage')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_by = db.Column(db.Integer, db.ForeignKey('employees.id'))
    updated_by = db.Column(db.Integer, db.ForeignKey('employees.id'))

    # Relationships
    creator = db.relationship('Employee', foreign_keys=[created_by], backref=db.backref('created_items', lazy='select'))
    updater = db.relationship('Employee', foreign_keys=[updated_by], backref=db.backref('updated_items', lazy='select'))
    logs = db.relationship('InventoryLog', backref=db.backref('item', lazy='select'), lazy='select')

    def __repr__(self):
        return f"<Inventory {self.name} ({self.quantity})>"

class InventoryLog(db.Model):
    __tablename__ = 'inventory_logs'

    id = db.Column(db.Integer, primary_key=True)
    action = db.Column(db.String(50))
    item_id = db.Column(db.Integer, db.ForeignKey('inventory_items.id'), nullable=False)
    change_amount = db.Column(db.Integer, nullable=False)
    new_quantity = db.Column(db.Integer, nullable=False)
    reason = db.Column(db.String(200), default='Adjustment')
    user_id = db.Column(db.Integer, db.ForeignKey('employees.id'), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    user = db.relationship('Employee', backref=db.backref('inventory_logs', lazy='select'))

    def __repr__(self):
        return f"<InventoryLog {self.change_amount} → {self.new_quantity}>"
