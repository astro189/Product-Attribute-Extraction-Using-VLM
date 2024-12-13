import firebase_admin
from firebase_admin import credentials, db
import json

def run_ui():
    cred_dict = {
    }

# Initialize Firebase app with the credentials
    cred = credentials.Certificate(cred_dict)
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://flipkartgridred-default-rtdb.asia-southeast1.firebasedatabase.app/'
    })

    json_file_path = 'product_info.json' 

    with open(json_file_path, 'r') as json_file:
        json_data = json.load(json_file)

    if isinstance(json_data, list):
        last_entry = json_data[-1]
    else:
        last_entry = json_data

    ref = db.reference('/')

    new_product_ref = ref.push(last_entry)

    print(f"Data uploaded successfully. New product key: {new_product_ref.key}")

if __name__ == "__main__":
    run_ui()