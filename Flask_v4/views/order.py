from flask import Blueprint, request, render_template

from functions.read_data import ReadData
from functions.calc_pages import calc_pages

from models.model import Order, OrderItem

order_bp = Blueprint('order', __name__)
dbdata = ReadData()

@order_bp.route('/order/')
def order():
    page = request.args.get('page', default=1, type=int)

    per_page = 10

    datas = Order.query.all()
    headers = ['Id', 'Ordered_At', 'User_Id', 'Store_Id']

    total_pages, page, page_data = calc_pages(datas, per_page, page)

    return render_template('order.html', headers=headers, page_data=page_data, total_pages=total_pages, current_page=page)

@order_bp.route('/order_detail/<id>')
def order_detail(id):
    query = """
    SELECT o.*
    FROM order_item oi
    JOIN 'order' o ON o.id = oi.order_id
    WHERE oi.order_id = ? 
    """

    data = OrderItem.query \
            .join(Order, Order.id == OrderItem.order_id) \
            .filter(OrderItem.order_id == id) \
            .all()
    headers = ['Id', 'Order_Id', 'Item_Id', 'Name']
    print(data)

    return render_template('order_detail.html', data=data, headers=headers)

