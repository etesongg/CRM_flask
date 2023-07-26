from app import db

class UserDb(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.String(64), primary_key = True)
    name = db.Column(db.String(16))
    gender = db.Column(db.String(16))
    age = db.Column(db.Integer())
    birthdate = db.Column(db.String(32))
    address = db.Column(db.String(64))
    orderR = db.relationship('Order', backref='user')

class StoreDb(db.Model):
    __tablename__ = 'store'
    id = db.Column(db.String(64), primary_key=True)
    name = db.Column(db.String(32), nullable=False)
    type = db.Column(db.String(32), nullable=False)
    address = db.Column(db.String(64), nullable=False)
    orderR = db.relationship('Order', backref='store')

class OrderDb(db.Model):
    __tablename__ = 'order'
    id = db.Column(db.String(64), db.ForeignKey('order_item.order_id'), primary_key=True)
    ordered_at = db.Column(db.String(64), nullable=False)
    user_id = db.Column(db.String(64), db.ForeignKey('user.id'), nullable=False)
    store_id = db.Column(db.String(64), db.ForeignKey('store.id'), nullable=False)
    order_itemR = db.relationship('OrderItem', backref='order')
    
    
class ItemDb(db.Model):
    __tablename__ = 'item'
    id = db.Column(db.String(64), primary_key=True)
    name = db.Column(db.String(32), nullable=False)
    type = db.Column(db.String(32), nullable=False)
    unit_price = db.Column(db.Integer(), nullable=False)
    order_itemR = db.relationship('OrderItem',backref='item')

class OrderItemDb(db.Model):
    __tablename__ = 'order_item'
    id = db.Column(db.String(64), primary_key=True)
    order_id = db.Column(db.String(64), db.ForeignKey('order.id'), nullable=False)
    item_id = db.Column(db.String(64), db.ForeignKey('item.id'),nullable=False)
