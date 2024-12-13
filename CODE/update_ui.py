import firebase_admin
from firebase_admin import credentials, db
import json

def run_ui():
    cred_dict = {
    # "type": "service_account",
    # "project_id": "flipkartgridred",
    # "private_key_id": "e35f50c1ac859882c8339fba67eb4a4a10d0dedc",
    # "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQDIlVhFWYh2F8OG\nOW6Oyt91/yCkpfMRkons35YE/ahfQ86/oHv0Us22U/QwyCU/RgZHnXJ/3i8KD0jv\nGur41fgksEM07YIHFiO+MZ+p/hYIL2kZQPSFzmPjvOakflZu5bSOl7vUUJ/omhi4\nUVwRqu+fmX03ETO4zGshbZSWFr7/ypm1hVVQnE/3AZo02loyL8KR7zxDBDbxeLB8\nd0nZXJnzHP8hMRTfhHDVIQRaLA4ZMHR47qsdgh/244/kxbXAo2NXXVtGVQTuk3gr\naU42NQPTjT87L6Jx6IIOTqeG5LgQQnKkkxrHyj+u+Z9XCuYmLA58Ngw4Fkl1aQFV\n9mUqMAJlAgMBAAECggEAAZGYjlwSWF6Kiwr5gEUPeMpxrz8UkXkrlsHk5lv7SMtz\nvtOztkDo3dmhIPLDVSU9nHGNWSPGtbzgMtEyhXqUQemkxc35ugdZvjaAebpvGzu5\n6bL7kwmpaarj/R4FnCSlxBSeKR18Tx+CvN8vzUMgpcAeyHh4hsB4wD6C0jTLHPPm\nV8SDjGAGYf8Fh0O2O4H3xjXoPlbaNJ9q4SiAQPW5u15NzLpFftlejW8M4kyy7woP\nE00UEqhAhudkkHg5Zsk9u96k1UR31uu6urTBk6YqveAxQ2rvNxysmkwivwlGs0KQ\nqr+FtqoRCosYqfgaRpL3FDK7ILg+vKoa9Vfs0ZppgQKBgQD9tGxuf8IuX2uiEl8B\nxGii96Tss2rf/0VT9MCr14kZOvVZ0MH30u8pM6zBi7Jew/30mNIWsyWcfN6ixTsO\nHSp8yKo06pG2pOaVCx5n1uCzi+6zsKMDTy7pk5ogKw+OvrT6Qkdzy9gOGkOHMGmq\ntTOpLZIaMhF3H/V9Bdni9mQtBQKBgQDKZeSUBEmTZwwiY+begcRf1SnXWI4iiw57\n0car7aLgWK9b4Mwfiq439+RswLLlIKWYVegr/onC4qsDDpwzQnp45hUxKzh1Yl00\nQ8oCasdFb9SxzkQM8A6zk0D3NPmIDwwz23VSGBS/dJD5tOzqopLmzqbyIaLBV4cg\n6ysF2dV94QKBgBz00stp2YfhbC97WUyiVi8DhNdfQvt97zO945+5YfR3PjmaEglv\nEczqEPWmNB2M0RdxucjNeaV6uw5o5Gyf95F2dbbEbw0hlQ+9zSKc69iSSBRKPNDL\n4NbX+ediAsyQB6fomK8mvOofJUXwyJ6rP9I3WU2UGVo3U5WJbWzyIkzhAoGBAJg3\nWVkYgF0jOrUCfTcKUS3hmr4iE4NXIWVttwTGi6A+EmP/BIUUP0JIZLqFkgVQMDoJ\nIbs0i1bOMd7ytfa3IHScVYPNBYECoSYVdW+r7oICQOwYPIWeZPAY5tsENEZnSr4V\nZn5/LdtvRzkFIMi1y9VZxaSEN2tA8JeJRan40d8BAoGARWFEnctDEYpveKdfh6SC\naDGOztDhKeAOMnk/SVkPbQuwlfVKsK1TZp5QkZ4ME24kN+6Q7GvW3PtRs+dVRoJO\nLHGo7W9pyHz0zia2UryyIGMpDJ5n2o4b52FX79AvmezimZF3LLxC8tNBnkBQt96i\naMekjf/M9iBwbwdniWLBRLA=\n-----END PRIVATE KEY-----\n",
    # "client_email": "firebase-adminsdk-ndwm4@flipkartgridred.iam.gserviceaccount.com",
    # "client_id": "106841674203166213315",
    # "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    # "token_uri": "https://oauth2.googleapis.com/token",
    # "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    # "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-ndwm4%40flipkartgridred.iam.gserviceaccount.com",
    # "universe_domain": "googleapis.com"
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