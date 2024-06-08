import pandas as pd

def process_file(file_path):
    df = pd.read_excel(file_path)
    results = []
    
    for index, row in df.iterrows():
        card_number = str(row['Card Number'])
        expiration_date = row['Expiration Date'].split('/')
        month = expiration_date[0]
        year = expiration_date[1]
        cvv = str(row['CVV']).zfill(3)
        result = f"{card_number};{month};{year};{cvv}"
        results.append(result)
        
    return results
