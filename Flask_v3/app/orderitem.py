from flask import Blueprint, request, render_template

from functions.read_data import read_data_db
from functions.calc_pages import calc_pages

orderitem_bp = Blueprint('orderitem', __name__)

@orderitem_bp.route('/orderitem/')
def orderitem():
    page = request.args.get('page', default=1, type=int)

    per_page = 10

    headers, data = read_data_db('SELECT * FROM order_item')

    total_pages, page, page_data = calc_pages(data, per_page, page)

    return render_template('orderitem.html', headers=headers, page_data=page_data, total_pages=total_pages, current_page=page)

@orderitem_bp.route('/order_detail/<id>')
def order_detail(id):
    query = """
    SELECT o.*
    FROM order_item oi
    JOIN 'order' o ON o.id = oi.order_id
    WHERE oi.order_id = ? 
    """

    headers, data =read_data_db(query, (id, ))
    data = str(data).split(',')

    return render_template('order_detail.html', data=data, headers=headers)