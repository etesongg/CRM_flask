from flask import Blueprint, request, render_template

from functions.read_data import ReadData
from functions.calc_pages import calc_pages

order_bp = Blueprint('order', __name__)
dbdata = ReadData()

@order_bp.route('/order/')
def order():
    page = request.args.get('page', default=1, type=int)

    per_page = 10

    headers, datas = dbdata.read_data_db("SELECT * FROM 'order'")

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

    headers, datas =dbdata.read_data_db(query, (id, ))

    row = datas[0]

    return render_template('order_detail.html', data=row, headers=headers)

