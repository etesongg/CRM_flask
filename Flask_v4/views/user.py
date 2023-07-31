from flask import Blueprint, request, render_template

from functions.read_data import ReadData
from functions.calc_pages import calc_pages

from sqlalchemy import case, func, desc

from models.model import User, Order, Store


user_bp = Blueprint('user', __name__)
dbdata = ReadData()

@user_bp.route('/')
def index():
    page = request.args.get('page', default=1, type=int)
    search_name = request.args.get('name', default ="", type=str).strip() 
    search_gender = request.args.get('gender', default="", type=str)

    per_page = 10

    # 검색 결과에 따른 데이터 보여주기    
    users_seach = User.query.filter(User.name.like('%'+search_name+'%'), User.gender.like(search_gender+'%')).all()
        
    # 페이지 계산
    total_pages, page, page_data = calc_pages(users_seach, per_page, page)

    headers = ['Id', 'Name', 'Gender', 'Age', 'Birthdate', 'Address']

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
    # 그래프 쿼리 sqlalchemy로 만들긴 했는데 나머지 페이지 기본적인거 다 하고 그래프 하기,,
    
    # bar_result = User.query(
    #     case(
    #             (User.age < 20, '10대'),
    #             (User.age.between(20, 29), '20대'),
    #             (User.age.between(30, 39), '30대'),
    #             (User.age.between(40, 49), '40대'),
    #             (User.age.between(50, 59), '50대'),
    #             (User.age >= 60, '60대 이상'),
    #             else_='기타'
    #         ).label('age_group'),
    #         func.count().label('age_count')
    #     ).group_by('age_group').all()

    rows, labels, values = dbdata.make_chart(query)

    count_data = User.query.count()

    return render_template('users.html', headers=headers, page_data=page_data, total_pages=total_pages, search_name=search_name, search_gender=search_gender, current_page=page, rows=rows, labels=labels, values=values, count_data=count_data)

@user_bp.route('/user_detail/<id>')
def user_detail(id):

    data = User.query.filter(User.id == id).first()
    headers = ['Name', 'Gender', 'Age',	'Birthdate', 'Address']

    # 주문 정보
    query = """ 
    SELECT o.id AS OrderId, o.ordered_at AS PurchasedDate, o.store_id AS PurchsedLocation
    FROM user u 
    JOIN 'order' o ON u.id = o.user_id
    JOIN store s ON o.store_id = s.id
    WHERE u.id = ?
    ORDER BY PurchasedDate DESC
    """
    # order_headers, order_data = dbdata.read_data_db(query, (id, ))

    order_data = User.query \
                .join(Order, User.id == Order.user_id) \
                .join(Store, Store.id == Order.store_id) \
                .with_entities(
                    Order.id.label('OrderId'),
                    Order.ordered_at.label('PurchasedDate'),
                    Order.store_id.label('PurchasedLocation')
                ) \
                .filter(User.id == id) \
                .order_by(desc('PurchasedDate')).all()
    order_headers = ['OrderId','PurchasedDate', 'PurchasedLocation']

    # 자주 방문한 매장 Top 5
    query = """
    SELECT s.name AS name, count(*) AS count
    FROM user u
    JOIN 'order' o ON o.user_id = u.id
    JOIN store s ON s.id = o.store_id
    WHERE u.id = ?
    GROUP BY s.name
    ORDER BY count
    limit 5
    """
    _, visit_stores = dbdata.read_data_db(query, (id, ))

    # 자주 주문한 상품명 Top 5
    query = """
    SELECT i.name AS name, count(*) AS count
    FROM user u
    JOIN 'order' o ON o.user_id = u.id
    JOIN store s ON s.id = o.store_id
    JOIN order_item oi ON o.id = oi.order_id
    JOIN item i ON oi.item_id = i.id
    WHERE u.id = ?
    GROUP BY i.name
    ORDER BY count
    limit 5
    """
    _, order_items = dbdata.read_data_db(query, (id, ))
 
    return render_template('user_detail.html', data=data, headers=headers, order_headers=order_headers, order_data=order_data, visit_stores=visit_stores, order_items=order_items)