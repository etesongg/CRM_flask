import sqlite3
import csv
class ReadData:
    def read_csv(self, filename):
        data = []
            
        with open(filename, 'r', encoding='utf8') as file:
            csv_data = csv.DictReader(file)
            headers = [header.strip() for header in csv_data.fieldnames]
            for row in csv_data:
                clean_row = {key.strip(): value.strip() for key, value in row.items()}
                data.append(clean_row)
        
        return headers, data

    # HugeCrm.db            crm.db
    # user 1000             user 1000
    # store 100             store 1000
    # order 3000            order 10000
    # item 40               item 50
    # order item 12000      order item 15000
    def read_data_db(self, query, where=None):
        conn = sqlite3.connect('db/HugeCrm.db')
        conn.row_factory = sqlite3.Row # dict로 row 바로 받기 
        cursor = conn.cursor()

        if where:
            cursor.execute(query, where)
        else:
            cursor.execute(query)
        
        datas = [dict(element) for element in cursor.fetchall()]
        headers = [header for header in datas[0]]
        # print(datas)
        # print(type(datas))
        conn.close()

        return headers, datas


    def make_chart(self, query, where=None):
        conn = sqlite3.connect('db/HugeCrm.db')
        cursor = conn.cursor()
        if where:
            cursor.execute(query, where)
        else:
            cursor.execute(query)
        rows = cursor.fetchall()
        conn.close()

        labels = []
        values = []

        for row in rows:
            lable, value = row
            labels.append(lable)
            values.append(value)

        return rows, labels, values
    
    def make_mixchart(self, query, where=None):
        conn = sqlite3.connect('db/HugeCrm.db')
        cursor = conn.cursor()
        if where:
            cursor.execute(query, where)
        else:
            cursor.execute(query)
        rows = cursor.fetchall()
        conn.close()

        labels = []
        values = []
        values2 = []
        # ('2022-03', 7000, 2)
        for row in rows:
            lable, value, value2 = row
            labels.append(lable)
            values.append(value)
            values2.append(value2)

        return rows, labels, values, values2