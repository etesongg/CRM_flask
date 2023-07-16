from flask import Blueprint, request, render_template

from functions.read_csv import read_data_db
from functions.calc_pages import calc_pages


user_bp = Blueprint('user', __name__)

@user_bp.route('/')
def index():
    page = request.args.get('page', default=1, type=int)
    search_name = request.args.get('name', default ="", type=str).strip() 
    search_gender = request.args.get('gender', default="", type=str)

    per_page = 10

    # csv 파일 읽기
    headers, data = read_data_db()

    # 검색 결과에 따른 데이터 보여주기
    filter_data = []
    for row in data:
        if not search_name: # search_name x
            if not search_gender: # search_name x, search_gender x
                filter_data.append(row)
            else:
                if search_gender in row['Gender']: # search_name x, search_gender o
                    filter_data.append(row)
        else: # search_name o
            if search_name in row['Name']: # search_name o
                if not search_gender: # search_name o, search_gender x
                    filter_data.append(row)
                else:
                    if search_gender in row['Gender']: # search_name o, search_gender o
                        filter_data.append(row)

    # 페이지 계산
    total_pages, page, page_data = calc_pages(filter_data, per_page, page)
    
    return render_template('users.html', headers=headers, page_data=page_data, total_pages=total_pages, search_name=search_name, search_gender=search_gender, current_page=page)

@user_bp.route('/user_detail/<id>')
def user_detail(id):
    headers, data = read_data_db()

    for row in data:
        if row['id'] == id:
            user_data = row
            break
    return render_template('user_detail.html', user=user_data, headers=headers)