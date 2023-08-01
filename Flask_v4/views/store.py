from flask import Blueprint, request, render_template

from functions.calc_pages import calc_pages

from sqlalchemy import func, desc
from models.model import Store, Order, User, OrderItem, Item

store_bp = Blueprint('store', __name__)

@store_bp.route('/store/')
def store():
    page = request.args.get('page',default=1, type=int)

    per_page = 10

    datas = Store.query.all()
    headers = ['Id', 'Name', 'Type', 'Address']

    total_pages, page, page_data = calc_pages(datas, per_page, page)

    return render_template('store.html', headers=headers, page_data=page_data, total_pages=total_pages, current_page=page)

@store_bp.route('/store_detail/<id>')
def store_detail(id):

    data = Store.query.filter(Store.id == id).first()
    headers = ['Name', 'Type', 'Address']

    # 단골 고객
    freq_data = Store.query \
                .join(Order, Store.id == Order.store_id) \
                .join(User, Order.user_id == User.id) \
                .with_entities(
                    User.id.label('user_id'),
                    User.name.label('name'),
                    func.count().label("frequency")
                ) \
                .filter(Store.id == id) \
                .group_by('user_id') \
                .order_by(User.name) \
                .limit(8).all()      
    freq_headers = ['User_Id', 'Name', 'Count']

    # 월간 매출액 detail
    month = request.args.get('month')
    
    if month:
        # 월간 매출액(일별)
        option = 0
        month_data = Store.query \
                    .join(Order, Order.store_id == Store.id) \
                    .join(OrderItem, Order.id == OrderItem.order_id) \
                    .join(Item, OrderItem.item_id == Item.id) \
                    .with_entities(
                        func.SUBSTRING(Order.ordered_at, 1, 10).label('Month'),
                        func.sum(Item.unit_price).label('Revenue'),
                        func.count().label('count')
                    ) \
                    .filter(Store.id == id, func.SUBSTRING(Order.ordered_at, 1, 7) == month) \
                    .group_by(func.SUBSTRING(Order.ordered_at, 1, 10)) \
                    .order_by(desc('Month')) \
                    .all()
        month_headers = ['Month', 'Revenue', 'Count']

    else:
        # 월간 매출액
        option = 1
        month_data = Store.query \
                    .join(Order, Store.id == Order.store_id) \
                    .join(OrderItem, Order.id == OrderItem.order_id) \
                    .join(Item, OrderItem.item_id == Item.id) \
                    .with_entities(
                        func.SUBSTRING(Order.ordered_at, 1, 7).label('Month'),
                        func.sum(Item.unit_price).label('Revenue'),
                        func.count().label('count')
                    ) \
                    .filter(Store.id == id) \
                    .group_by(func.SUBSTRING(Order.ordered_at, 1, 7)) \
                    .all()
        month_headers = ['Month', 'Revenue', 'Count']

    return render_template('store_detail.html', data=data, headers=headers, month_headers=month_headers, month_data=month_data, freq_headers=freq_headers, freq_data=freq_data, option=option)