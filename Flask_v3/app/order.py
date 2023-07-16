from flask import Blueprint, request, render_template

from functions.read_data import read_csv
from functions.calc_pages import calc_pages

order_bp = Blueprint('order', __name__)

@order_bp.route('/order/')
def order():
    page = request.args.get('page', default=1, type=int)

    per_page = 10

    headers, data = read_csv('csv/order.csv')

    total_pages, page, page_data = calc_pages(data, per_page, page)

    return render_template('order.html', headers=headers, page_data=page_data, total_pages=total_pages, current_page=page)