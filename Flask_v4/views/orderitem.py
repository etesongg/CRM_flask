from flask import Blueprint, request, render_template

from functions.read_data import ReadData
from functions.calc_pages import calc_pages

from models.model import OrderItem, Order, Item

orderitem_bp = Blueprint('orderitem', __name__)
dbdata = ReadData()

@orderitem_bp.route('/orderitem/')
def orderitem():
    page = request.args.get('page', default=1, type=int)

    per_page = 10

    # headers, datas = dbdata.read_data_db('SELECT * FROM order_item')

    datas = OrderItem.query.all()
    headers = ['Id', 'Order_Id', 'Item_Id']

    total_pages, page, page_data = calc_pages(datas, per_page, page)

    return render_template('orderitem.html', headers=headers, page_data=page_data, total_pages=total_pages, current_page=page)

@orderitem_bp.route('/orderitem_detail/<id>')
def orderitem_detail(id):
    datas = OrderItem.query \
            .join(Order, Order.id == OrderItem.order_id) \
            .join(Item, Item.id == OrderItem.item_id) \
            .with_entities(
                OrderItem.id,
                OrderItem.order_id,
                OrderItem.item_id,
                Item.name
            ) \
            .filter(Order.id == id) \
            .all()
    headers = ['Id', 'Order_Id', 'Item_Id', 'Name']
      
    return render_template('orderitem_detail.html', data=datas, headers=headers)

