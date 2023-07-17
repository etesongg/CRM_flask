from flask import Blueprint, request, render_template
from functions.read_data import read_data_db
from functions.calc_pages import calc_pages

item_bp = Blueprint('item', __name__)

@item_bp.route('/item/')
def item():
    page = request.args.get('page', default=1, type=int)

    per_page = 10

    headers, data = read_data_db('SELECT * FROM item')

    total_pages, page, page_data = calc_pages(data, per_page, page)

    return render_template('item.html', headers=headers, total_pages=total_pages, page_data=page_data, current_page=page)

@item_bp.route('/item_detail/<id>')
def item_detail(id):
    query = "SELECT * FROM item WHERE id = ?"
    headers, data = read_data_db(query, (id, ))
    
    for row in data:
        dict_data = row
        break
    
    return render_template('item_detail.html', user=dict_data, headers=headers)
