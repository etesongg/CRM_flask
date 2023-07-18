from flask import Blueprint, request, render_template

from functions.read_data import ReadData
from functions.calc_pages import calc_pages

store_bp = Blueprint('store', __name__)
dbdata = ReadData()

@store_bp.route('/store/')
def store():
    page = request.args.get('page',default=1, type=int)

    per_page = 10

    headers, datas = dbdata.read_data_db("SELECT * FROM store")
    
    total_pages, page, page_data = calc_pages(datas, per_page, page)

    return render_template('store.html', headers=headers, page_data=page_data, total_pages=total_pages, current_page=page)

@store_bp.route('/store_detail/<id>')
def store_detail(id):
    print(id)
    query = "SELECT * FROM store WHERE id = ?"
    headers, datas = dbdata.read_data_db(query, (id, ))

    row = datas[0]

    return render_template('store_detail.html', user=row, headers=headers)