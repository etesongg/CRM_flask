from flask import Blueprint, request, render_template

from functions.read_data import read_data_db, make_graph
from functions.calc_pages import calc_pages


user_bp = Blueprint('user', __name__)

@user_bp.route('/')
def index():
    page = request.args.get('page', default=1, type=int)
    search_name = request.args.get('name', default ="", type=str).strip() 
    search_gender = request.args.get('gender', default="", type=str)

    per_page = 10

    # db 읽기
    headers, data = read_data_db("SELECT * FROM user")
    
    # 검색 결과에 따른 데이터 보여주기
    filter_data = []
    for row in data:
        if not search_name: # search_name x
            if not search_gender: # search_name x, search_gender x
                filter_data.append(row)
            else:
                if search_gender in row['gender']: # search_name x, search_gender o
                    filter_data.append(row)
        else: # search_name o
            if search_name in row['name']: # search_name o
                if not search_gender: # search_name o, search_gender x
                    filter_data.append(row)
                else:
                    if search_gender in row['gender']: # search_name o, search_gender o
                        filter_data.append(row)

    # 페이지 계산
    total_pages, page, page_data = calc_pages(filter_data, per_page, page)

    # 그래프
    query = """
        SELECT CASE WHEN age < 20 THEN '10대'
        WHEN age BETWEEN 20 AND 29 THEN '20대'
        WHEN age BETWEEN 30 AND 39 THEN '30대'
        WHEN age BETWEEN 40 AND 49 THEN '40대'
        WHEN age BETWEEN 50 AND 59 THEN '50대'
        WHEN age >= 60 THEN '60대 이상'
        END AS age_group, count(*) AS age_count
        FROM user
        GROUP BY age_group;
    """
    rows, labels, values = make_graph(query)
    
    return render_template('users.html', headers=headers, page_data=page_data, total_pages=total_pages, search_name=search_name, search_gender=search_gender, current_page=page, rows=rows, labels=labels, values=values)

@user_bp.route('/user_detail/<id>')
def user_detail(id):
    headers, data = read_data_db("SELECT * FROM user")

    for row in data:
        if row['id'] == id:
            # user_data = row
            break
    
    return render_template('user_detail.html', user=row, headers=headers)