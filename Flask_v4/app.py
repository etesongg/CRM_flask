from flask import Flask
import os

from views.user import user_bp
from views.store import store_bp
from views.order import order_bp
from views.orderitem import orderitem_bp
from views.item import item_bp

from models.model import db


app = Flask(__name__)

app.instance_path = os.getcwd()
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db/HugeCrm.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# db = SQLAlchemy(app)
# sqlalchemy db를 초기화 하는 법
db.init_app(app)

# Blueprint 등록
app.register_blueprint(user_bp)
app.register_blueprint(store_bp)
app.register_blueprint(order_bp)
app.register_blueprint(orderitem_bp)
app.register_blueprint(item_bp)

@app.route('/<path:path>')
def catch_all(path):
    return f"404 - Page not found for URL: /{path}", 404

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host="0.0.0.0",port=5004,debug=True)