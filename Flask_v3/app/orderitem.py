from flask import Blueprint, request, render_template

from functions.read_data import ReadData
from functions.calc_pages import calc_pages

orderitem_bp = Blueprint('orderitem', __name__)
dbdata = ReadData()

@orderitem_bp.route('/orderitem/')
def orderitem():
    page = request.args.get('page', default=1, type=int)

    per_page = 10

    headers, datas = dbdata.read_data_db('SELECT * FROM order_item')

    total_pages, page, page_data = calc_pages(datas, per_page, page)

    return render_template('orderitem.html', headers=headers, page_data=page_data, total_pages=total_pages, current_page=page)

@orderitem_bp.route('/orderitem_detail/<id>')
def orderitem_detail(id):
    
    query = """
    SELECT oi.*, i.name
    FROM order_item oi
    JOIN 'order' o ON o.id = oi.order_id
    JOIN item i ON i.id = oi.item_id
    WHERE o.id = ? 
    """
    
    headers, datas =dbdata.read_data_db(query, (id, ))
    
    row = datas[0] # user_detail > orderid로 들어갔을때 0개로 가져오면 안 될듯...
    
    return render_template('orderitem_detail.html', data=row, headers=headers)

