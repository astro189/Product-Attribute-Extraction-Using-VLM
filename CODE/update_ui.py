import firebase_admin
from firebase_admin import credentials, db
import json

def run_ui():
    cred_dict = {
        "type": "service_account",
        "project_id": "flipkartgridred",
        "private_key_id": "3b4001e7f86ab722e9b74f4dbf8a86756a48543e",
        "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQCw7yyU3qD/1Mtx\nuXNhblllPrB3kSr+wWnMQbx25kQLfhNPxdi1b0OHCDAcopX1PMDNyrlImGQCAM+K\ngTe+daxkypoWbrsJj7+v6KWHWvmw7MzQCC47vdCWCKEzE88cGxaZwXNOQMNmxrxe\ng056xAWredfcnbK7oi9w769XctVKME/M8XrpRT0CqLZzfWUS+5xfdZK49FSi1O7n\nxxaeJsNztgQtR4QPrP0b+FM9N4tNXZkHgVi8+uTaq18HdCsCpIQDqM5E2kXokJ+L\nmIzqOs8ETCPRmqz3gHz5+2I4N24LJGUAEs4e6MC/vvemws8ZYr2ZhhBJmJAimTL4\nHSIiZGV/AgMBAAECggEAQY3kBSY1HYRgejq9MpCZg4cGB87b0Laldb23T5BCDsX/\n7rL9dz+Jk+qnNLzSdaG0R6sAGhMIHqvhOU5l8mWT4WYlUAFnwAOoAEtgpPVChNg/\njCYzxwOtWCFLZGrG9gFdTstbZtdc7mPcn+Hjfl3JQf6rSTyOX7GYBS5w1yQfPVRq\nJs6H0eSGpFfNdmtZFqxacnl1de88HP2hKhV0x+h5ZuNT7XI7vglqoOONHenPfITF\n9A4tFc5fulsxtqOtSvXXwGw0Shi2R925++q4DmuTfVGqvtPsc+sMfdqSdiein+AJ\n6fAoZfV6rq/AU3bmEX17hkw3kRlO7xNA0lTmf/cgRQKBgQDenEMReCr+QYGYLlav\nfiGpscJIURCa0hkoFiE2tY01XPbjPEqYa8XxYfrnOeJHURdAFVMDGhkOXc05DcgE\nOXU1FFm7K408F8txcUtQviHcaDBuO95asgSn3IrEMrXh/UQ75KUeI4qcjquIzhRz\nfg/0QknxqGTvxbkFb1n9+wJxKwKBgQDLeQ1FcDEyZ53t7vFrapyF7IhKq6cU+89G\nN+c+IgOsIfI0ynu0Egsrb8lOyx+xPTjlFeDU1nrmnbsr0rj06n/P/9388zg2QOJt\nj0DMw0m8hR9yNbqvKuI6I5y3IJWxG4Q9AziRdsUHccdvAJWAmnKhqMGPAnDtqlPy\nSXL9Y3yq/QKBgQCmoDJ3fgo4XJIDdhP+shvCaELzXHJgYIjh/4aG6+gxnE9UkcmI\nQ4tbfaqPrz0XgrQzjIKhXMSKg13cqdsghl2cCIqN1jCWXX0zgckNO/QehYJS0M9D\n9eIUP7lC2G5aJPgRGLkbUSEsxIHTGeYm+KI6g+/TSeebrdUrI0kqGdufFwKBgFOD\nbOoKQXcRxmWJRDe1e2cQjWQwjhRzwkBs45HB/kXhbPsz/JANM95xNGwNvQVPPpHw\nZ+aT3b/YD6HODLIhqbIir+eJoJHMEeOr/4nLwfEJpr2GxgftjwsT4NfdHPOjeqRc\nNRSnbfk/Pv8Ve0dcnR4zGLbs5pL17Ryt/u93rQy1AoGANx2832HRW2aoZH+g03vg\nxXPICOSKyhZeUK/Tzfdpj2jVYJMf6Is+T1yNzgv4NMhrad2QFb3jPLtURP0pwdlG\nnW1rslP4/IdRt/zceBoa+bA9bD759FysKzO2CHxspiNoJzkirRSlj8jn60uQ3bSj\nHHs+0c/7sHKwhPVIWAMDlIQ=\n-----END PRIVATE KEY-----\n",
        "client_email": "firebase-adminsdk-ndwm4@flipkartgridred.iam.gserviceaccount.com",
        "client_id": "106841674203166213315",
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-ndwm4%40flipkartgridred.iam.gserviceaccount.com",
        "universe_domain": "googleapis.com"
    }


    cred = credentials.Certificate(cred_dict)
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://flipkartgridred-default-rtdb.asia-southeast1.firebasedatabase.app/'
    })

    json_file_path = 'label_updated.json' 

    with open(json_file_path, 'r') as json_file:
        json_data = json.load(json_file)

    if isinstance(json_data, list):
        last_entry = json_data[-1]
    else:
        last_entry = json_data

    ref = db.reference('/')

    new_product_ref = ref.push(last_entry)

    print(f"Data uploaded successfully. New product key: {new_product_ref.key}")
