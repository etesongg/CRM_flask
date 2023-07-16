from flask import Blueprint, request, render_template

from functions.read_data import read_csv
from functions.calc_pages import calc_pages

orderitem_bp = Blueprint('orderitem', __name__)

@orderitem_bp.route('/orderitem/')
def orderitem():
    page = request.args.get('page', default=1, type=int)

    per_page = 10

    headers, data = read_csv('csv/orderitem.csv')

    total_pages, page, page_data = calc_pages(data, per_page, page)

    return render_template('orderitem.html', headers=headers, page_data=page_data, total_pages=total_pages, current_page=page)