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

    def read_data_db(self, query, where=None):
        conn = sqlite3.connect('db/crm.db')
        cursor = conn.cursor()

        if where:
            cursor.execute(query, where)
        else:
            cursor.execute(query)

        rows = cursor.fetchall()

        headers = [header[0] for header in cursor.description]
        
        data = []   
        for row in rows:
            clean_row = {}
            for i, value in enumerate(row):
                if isinstance(value, str):
                    clean_row[headers[i]] = value.strip()
                else:
                    clean_row[headers[i]] = value
            data.append(clean_row)

        conn.close()

        return headers, data


    def make_chart(self, query, where=None):
        conn = sqlite3.connect('db/crm.db')
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
        conn = sqlite3.connect('db/crm.db')
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