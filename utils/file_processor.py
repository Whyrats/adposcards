import pandas as pd

def process_file(file_path):
    df = pd.read_excel(file_path)
    results = []
    
    # Определяем названия столбцов на английском и русском
    english_headers = {
        "Card Number": "Card Number",
        "Expiration Date": "Expiration Date",
        "CVV": "CVV"
    }
    
    russian_headers = {
        "Card Number": "Номер карты",
        "Expiration Date": "Срок действия",
        "CVV": "CVV"
    }
    
    # Определяем текущие заголовки
    headers = {}
    for column in df.columns:
        if column in english_headers.values():
            headers[column] = column
        elif column in russian_headers.values():
            for key, value in russian_headers.items():
                if value == column:
                    headers[english_headers[key]] = column
    
    # Проверка наличия всех необходимых заголовков
    required_headers = ["Card Number", "Expiration Date", "CVV"]
    for header in required_headers:
        if header not in headers:
            raise ValueError(f"Отсутствует обязательный столбец: {header}")

    # Обрабатываем строки в таблице
    for index, row in df.iterrows():
        card_number = str(row[headers["Card Number"]])
        expiration_date = row[headers["Expiration Date"]].split('/')
        month = expiration_date[0]
        year = expiration_date[1]
        cvv = str(row[headers["CVV"]]).zfill(3)
        result = f"{card_number};{month};{year};{cvv}"
        results.append(result)
        
    return results
