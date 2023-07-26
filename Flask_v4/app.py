from flask import Flask
from flask_sqlalchemy import SQLAlchemy
# import os

from views.user import user_bp
from views.store import store_bp
from views.order import order_bp
from views.orderitem import orderitem_bp
from views.item import item_bp

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///HugeCrm.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


# Blueprint 등록
app.register_blueprint(user_bp)
app.register_blueprint(store_bp)
app.register_blueprint(order_bp)
app.register_blueprint(orderitem_bp)
app.register_blueprint(item_bp)

@app.route('/<path:path>')
def catch_all(path):
    return f"404 - Page not found for URL: /{path}", 404

if __name__ == "__main__":
    app.run()