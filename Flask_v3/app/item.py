from flask import Blueprint, request, render_template

from functions.read_data import ReadData
from functions.calc_pages import calc_pages

item_bp = Blueprint('item', __name__)
dbdata = ReadData()

@item_bp.route('/item/')
def item():
    page = request.args.get('page', default=1, type=int)

    per_page = 10

    headers, data = dbdata.read_data_db('SELECT * FROM item')

    total_pages, page, page_data = calc_pages(data, per_page, page)

    return render_template('item.html', headers=headers, total_pages=total_pages, page_data=page_data, current_page=page)

@item_bp.route('/item_detail/<id>')
def item_detail(id):
    query = "SELECT * FROM item WHERE id = ?"
    headers, data = dbdata.read_data_db(query, (id, ))
    
    for row in data:
        dict_data = row
        break

    # 월간 매출액
    query = """
    SELECT SUBSTR(o.ordered_at, 1, 7) AS Month, sum(i.unit_price) AS TotalRevenue, count(*) AS ItemCount
    FROM 'order' o
    JOIN order_item oi ON o.id = oi.order_id
    JOIN item i ON oi.item_id = i.id
    WHERE i.id = ?
    GROUP BY Month
    """
    mon_headers, mon_data = dbdata.read_data_db(query, (id, ))
    print(mon_data)
    print(type(mon_data))
    for d in mon_data:
        print(d)

    # for row in mon_data:
    #     dict_mon_data = row
        
    # print(row)
    return render_template('item_detail.html', user=dict_data, headers=headers, mon_headers=mon_headers, mon_data=mon_data)
