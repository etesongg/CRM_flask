import datetime

from flask import Blueprint, request, render_template

from functions.read_data import ReadData
from functions.calc_pages import calc_pages

from models.model import Item, Order, OrderItem
from sqlalchemy import func

item_bp = Blueprint('item', __name__)
dbdata = ReadData()

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
    query = """
    SELECT SUBSTR(o.ordered_at, 1, 7) AS Month, sum(i.unit_price) AS TotalRevenue, count(*) AS ItemCount
    FROM 'order' o
    JOIN order_item oi ON o.id = oi.order_id
    JOIN item i ON oi.item_id = i.id
    WHERE i.id = ?
    GROUP BY Month
    """
    month_headers, month_data = dbdata.read_data_db(query, (id, ))

    # month_data = Order.query \
    #             .join(OrderItem, Order.id == OrderItem.order_id) \
    #             .join(Item, OrderItem.item_id == Item.id) \
    #             .with_entities(
    #                 func.SUBSTRING(Order.ordered_at, 1, 7).label('Month'),
    #                 func.sum(Item.unit_price).label('TotalRevenue'),
    #                 func.count().label('ItemCount')
    #             ) \
    #             .filter(Item.id == id) \
    #             .group_by(func.SUBSTRING(Order.ordered_at, 1, 7)) \
    #             .all()
    # month_headers = ['Month', 'Total Revenue', 'Item Count']
    # 그래프
    rows, lables, values, values2 = dbdata.make_mixchart(query, (id, )) # row = ('2022-03', 7000, 2)

    return render_template('item_detail.html', data=data, headers=headers, month_headers=month_headers, month_data=month_data, rows=rows, labels=lables, values=values, values2=values2)
