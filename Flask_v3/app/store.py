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

    # 월간 매출액
    query = """
    SELECT SUBSTR(o.ordered_at, 1, 7) AS Month, sum(i.unit_price) AS Revenue, count(*) AS Count
    FROM store s
    JOIN 'order' o ON s.id = o.store_id
    JOIN order_item oi ON o.id = oi.order_id
    JOIN item i ON oi.item_id = i.id
    WHERE s.id = ?
    GROUP BY Month
    """

    month_headers, month_data = dbdata.read_data_db(query, (id, ))

    # 단골고객
    query = """
    SELECT u.id AS user_id, u.name AS name, count(*) AS frequency
    FROM store s
    JOIN 'order' o ON s.id = o.store_id
    JOIN user u ON o.user_id = u.id
    WHERE s.id = ?
    GROUP BY user_id
    limit 10
    """

    freq_headers, freq_data = dbdata.read_data_db(query, (id, ))

    return render_template('store_detail.html', user=row, headers=headers, month_headers=month_headers, month_data=month_data, freq_headers=freq_headers, freq_data=freq_data)