from flask import Blueprint, request, render_template
from sqlalchemy import func

from functions.calc_pages import calc_pages
from models.model import Item, Order, OrderItem


item_bp = Blueprint('item', __name__)

@item_bp.route('/item/')
def item():
    page = request.args.get('page', default=1, type=int)

    per_page = 10

    data = Item.query.all()
    headers = ['Id', 'Name', 'Type', 'Unit_Price']
    total_pages, page, page_data = calc_pages(data, per_page, page)

    return render_template('item.html', headers=headers, total_pages=total_pages, page_data=page_data, current_page=page)

@item_bp.route('/item_detail/<id>')
def item_detail(id):
    data = Item.query \
            .with_entities(
                Item.type,
                Item.unit_price
            ) \
            .filter(Item.id == id) \
            .first()
    headers = ['Type', 'Unit_Price']

    # 월간 매출액
    month_datas = Order.query \
                .join(OrderItem, Order.id == OrderItem.order_id) \
                .join(Item, OrderItem.item_id == Item.id) \
                .with_entities(
                    func.SUBSTRING(Order.ordered_at, 1, 7).label('Month'),
                    func.sum(Item.unit_price).label('TotalRevenue'),
                    func.count().label('ItemCount')
                ) \
                .filter(Item.id == id) \
                .group_by('Month') \
                .all()  
    month_headers = ['Month', 'Total Revenue', 'Item Count']
    
    labels = []
    values = []
    values2 = []
    for month_data in month_datas:
        label, value, value2 = month_data
        labels.append(label)
        values.append(value)
        values2.append(value2)

    return render_template('item_detail.html', data=data, headers=headers, month_headers=month_headers, month_datas=month_datas, rows=month_datas, labels=labels, values=values, values2=values2)
