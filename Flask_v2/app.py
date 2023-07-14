from flask import Flask

from app.user import user_bp
from app.store import store_bp
from app.order import order_bp
from app.orderitem import orderitem_bp
from app.item import item_bp

app = Flask(__name__)

# Blueprint 등록
app.register_blueprint(user_bp)
app.register_blueprint(store_bp)
app.register_blueprint(order_bp)
app.register_blueprint(orderitem_bp)
app.register_blueprint(item_bp)

if __name__ == "__main__":
    app.run(host="0.0.0.0",port=5001,debug=True)