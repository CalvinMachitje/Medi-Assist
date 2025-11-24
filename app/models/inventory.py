# app/models/inventory.py
from app.extensions import db
from datetime import datetime
from flask_login import current_user


class InventoryItem(db.Model):
    __tablename__ = 'inventory_items'

    id = db.Column(db.Integer, primary_key=True)
    item_name = db.Column(db.String(100), nullable=False, index=True)
    description = db.Column(db.Text, nullable=True)
    category = db.Column(db.String(50), default='general')  # e.g., medicine, consumable, equipment
    unit = db.Column(db.String(20), default='unit')  # e.g., box, vial, pack, piece
    quantity = db.Column(db.Integer, default=0, nullable=False)
    min_stock = db.Column(db.Integer, default=10, nullable=False)  # Low stock threshold
    reorder_qty = db.Column(db.Integer, default=50, nullable=False)  # Suggested reorder amount
    avg_daily_use = db.Column(db.Float, default=0.0)  # Auto-calculated or manual
    supplier = db.Column(db.String(100), nullable=True)
    cost_per_unit = db.Column(db.Numeric(10, 2), default=0.00)
    location = db.Column(db.String(100), default='Main Storage')

    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    updated_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)

    # Relationships
    creator = db.relationship('User', foreign_keys=[created_by], backref='created_items')
    updater = db.relationship('User', foreign_keys=[updated_by], backref='updated_items')

    def __repr__(self):
        return f"<Inventory {self.item_name} ({self.quantity}{self.unit})>"

    @property
    def status(self):
        if self.quantity == 0:
            return "Out of Stock"
        elif self.quantity <= self.min_stock:
            return "Low Stock"
        else:
            return "In Stock"

    @property
    def days_left(self):
        if self.avg_daily_use <= 0:
            return float('inf')
        return round(self.quantity / self.avg_daily_use, 1)

    @property
    def is_low(self):
        return self.quantity <= self.min_stock

    @property
    def total_value(self):
        return round(float(self.quantity) * float(self.cost_per_unit), 2)

    def update_stock(self, qty_change, reason="Manual adjustment", user_id=None):
        """Adjust stock and log the change"""
        old_qty = self.quantity
        self.quantity += qty_change
        self.updated_at = datetime.utcnow()
        self.updated_by = user_id or (current_user.id if current_user.is_authenticated else None)

        # Log the change
        log = InventoryLog(
            item_id=self.id,
            change_amount=qty_change,
            new_quantity=self.quantity,
            reason=reason,
            user_id=self.updated_by
        )
        db.session.add(log)
        db.session.commit()

    def to_dict(self):
        return {
            'id': self.id,
            'item_name': self.item_name,
            'quantity': self.quantity,
            'unit': self.unit,
            'min_stock': self.min_stock,
            'reorder_qty': self.reorder_qty,
            'avg_daily_use': round(self.avg_daily_use, 2),
            'days_left': self.days_left if self.days_left != float('inf') else 'N/A',
            'status': self.status,
            'supplier': self.supplier or '—',
            'cost_per_unit': float(self.cost_per_unit),
            'total_value': self.total_value,
            'location': self.location
        }


# Optional: Track stock movements (highly recommended for audit)
class InventoryLog(db.Model):
    __tablename__ = 'inventory_logs'

    id = db.Column(db.Integer, primary_key=True)
    item_id = db.Column(db.Integer, db.ForeignKey('inventory_items.id'), nullable=False)
    change_amount = db.Column(db.Integer, nullable=False)  # Can be negative
    new_quantity = db.Column(db.Integer, nullable=False)
    reason = db.Column(db.String(200), default='Adjustment')
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, index=True)

    item = db.relationship('InventoryItem', backref='logs')
    user = db.relationship('User', backref='inventory_actions')

    def __repr__(self):
        return f"<Stock Change: {self.change_amount} → {self.new_quantity}>"