from flask import Blueprint, request, render_template

from functions.calc_pages import calc_pages
from models.model import Order, OrderItem

order_bp = Blueprint('order', __name__)

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
    data = OrderItem.query \
            .join(Order, Order.id == OrderItem.order_id) \
            .with_entities(
                Order.id,
                Order.ordered_at,
                Order.user_id,
                Order.store_id
            ) \
            .filter(OrderItem.order_id == id) \
            .first()
    headers = ['Id', 'Ordered_At', 'User_Id', 'Store_Id']
    print(data)

    return render_template('order_detail.html', data=data, headers=headers)

