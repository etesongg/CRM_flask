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