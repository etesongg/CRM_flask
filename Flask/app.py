from flask import Flask, request, render_template, url_for
import csv
import math


app = Flask(__name__)


@app.route('/')
def index():
    page = request.args.get('page', default=1, type=int)
    search_name = request.args.get('name', default ="", type=str) 
    search_gender = request.args.get('gender', default="", type=str)
    
    per_page = 10

    # csv 파일 읽기
    data = []
    
    with open('user.csv', 'r', encoding='utf8') as file:
        csv_data = csv.DictReader(file)
        headers = [header.strip() for header in csv_data.fieldnames]
        for row in csv_data:
            clean_row = {key.strip(): value.strip() for key, value in row.items()}
            data.append(clean_row)
    
    # 검색 결과에 따른 데이터 보여주기
    filter_data = []
    if search_name: 
        if search_gender: 
            for row in data:
                if search_name in row['Name'] and search_gender in row['Gender']: # search_name 값 O, search_gneder 값 O
                    filter_data.append(row)
        else:
            for row in data:
                if search_name in row['Name']: # search_name 값 O, search_gneder 값 x
                    filter_data.append(row)     
    else: 
        if search_gender:
            for row in data:
                if search_gender in row['Gender']: # search_name 값 x, search_gneder 값 O
                    filter_data.append(row)
        else: # search_name 값 x, search_gneder 값 x
            filter_data = data

    # 페이지 나누기
    total_pages = math.ceil((len(filter_data) / per_page)) # math.ceil 소수점 이하를 올림한다
    start_index = per_page * (page -1)
    end_index = start_index + per_page
    page_data = filter_data[start_index:end_index]
    
    return render_template('users.html', headers=headers, page_data=page_data, total_pages=total_pages, search_name=search_name, search_gender=search_gender, url_for=url_for, current_page=page)

@app.route('/user/<id>')
def user_detail(id):
    with open('user.csv', 'r', encoding='utf8') as file:
        csv_data = csv.DictReader(file)
        headers = [header.strip() for header in csv_data.fieldnames]
        for row in csv_data:
            if row['Id'] == id:
                user_data = row
                break
    return render_template('user_detail.html', user=user_data, headers=headers)

@app.route('/store/')
def store():
    page = request.args.get('page',default=1, type=int)

    data = []
    per_page = 10
    with open('store.csv', 'r', encoding='utf8') as file:
        csv_data = csv.DictReader(file)
        headers = [header.strip() for header in csv_data.fieldnames]
        for row in csv_data:
            data.append(row)    

    total_pages = math.ceil((len(data) / per_page)) 
    start_index = per_page * (page -1)
    end_index = start_index + per_page
    page_data = data[start_index:end_index]

    return render_template('store.html', headers=headers, page_data=page_data, total_pages=total_pages, url_for=url_for, current_page=page)
                           
@app.route('/order/')
def order():
    page = request.args.get('page', default=1, type=int)

    data = []
    per_page = 10
    with open('order.csv', 'r', encoding='utf8') as file:
        csv_data = csv.DictReader(file)
        headers = [header.strip() for header in csv_data.fieldnames]
        for row in csv_data:
            data.append(row)

    total_pages = math.ceil((len(data)) / per_page)
    start_index = per_page * (page -1)
    end_index = start_index + per_page
    page_data = data[start_index:end_index]

    return render_template('order.html', headers=headers, page_data=page_data, total_pages=total_pages, url_for=url_for, current_page=page)

@app.route('/orderitem/')
def orderitem():
    page = request.args.get('page', default=1, type=int)

    data = []
    per_page = 10
    with open('orderitem.csv', 'r', encoding='utf8') as file:
        csv_data = csv.DictReader(file)
        headers = [header.strip() for header in csv_data.fieldnames ]
        for row in csv_data:
            data.append(row)

    total_pages = math.ceil((len(data)) / per_page)
    start_index = per_page * (page -1)
    end_index = start_index + per_page
    page_data = data[start_index:end_index]

    return render_template('orderitem.html', headers=headers, page_data=page_data, total_pages=total_pages, url_for=url_for, current_page=page)

@app.route('/item/')
def item():
    page = request.args.get('page', default=1, type=int)

    data = []
    per_page = 10
    with open('item.csv', 'r', encoding='utf8') as file:
        csv_data = csv.DictReader(file)
        headers = [header.strip() for header in csv_data.fieldnames]
        for row in csv_data:
            data.append(row)

    total_pages = math.ceil((len(data)) / per_page)
    start_index = per_page * (page -1)
    end_index = start_index + per_page
    page_data = data[start_index:end_index]

    return render_template('item.html', headers=headers, total_pages=total_pages, page_data=page_data, url_for=url_for, current_page=page)



if __name__ == "__main__":
    app.run(debug=True)