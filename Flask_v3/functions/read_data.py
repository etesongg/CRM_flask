import sqlite3
import csv

def read_csv(filename):
    data = []
        
    with open(filename, 'r', encoding='utf8') as file:
        csv_data = csv.DictReader(file)
        headers = [header.strip() for header in csv_data.fieldnames]
        for row in csv_data:
            clean_row = {key.strip(): value.strip() for key, value in row.items()}
            data.append(clean_row)
    
    return headers, data

def read_data_db(query, search=None):
    conn = sqlite3.connect('db/crm.db')
    cursor = conn.cursor()

    if search:
        cursor.execute(query, search)
    else:
        cursor.execute(query)

    rows = cursor.fetchall()

    headers = [header[0] for header in cursor.description]
    print(headers)
    data = []   
    for row in rows:
        clean_row = {}
        for i, value in enumerate(row): # enumerate: 인덱스 원소 동시 접근
            if isinstance(value, str): # 타입 확인
                clean_row[headers[i]] = value.strip()
            else:
                clean_row[headers[i]] = value
        data.append(clean_row)

    conn.close()

    return headers, data