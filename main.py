import os
import json
import sqlite3
import datetime
import pandas as pd
from menu import menuSystem
from utils import humanTime, get_encryption_key, decrypt_password, today

os.system("cls||clear")#clear terminal
# Print banner
print(r"""

 ▄████▄   ██░ ██  ██▀███   ▒█████   ███▄ ▄███▓▓█████      ██████  ██▓███  ▓█████  ▄████▄  ▄▄▄█████▓▓█████  ██▀███
▒██▀ ▀█  ▓██░ ██▒▓██ ▒ ██▒▒██▒  ██▒▓██▒▀█▀ ██▒▓█   ▀    ▒██    ▒ ▓██░  ██▒▓█   ▀ ▒██▀ ▀█  ▓  ██▒ ▓▒▓█   ▀ ▓██ ▒ ██▒
▒▓█    ▄ ▒██▀▀██░▓██ ░▄█ ▒▒██░  ██▒▓██    ▓██░▒███      ░ ▓██▄   ▓██░ ██▓▒▒███   ▒▓█    ▄ ▒ ▓██░ ▒░▒███   ▓██ ░▄█ ▒
▒▓▓▄ ▄██▒░▓█ ░██ ▒██▀▀█▄  ▒██   ██░▒██    ▒██ ▒▓█  ▄      ▒   ██▒▒██▄█▓▒ ▒▒▓█  ▄ ▒▓▓▄ ▄██▒░ ▓██▓ ░ ▒▓█  ▄ ▒██▀▀█▄
▒ ▓███▀ ░░▓█▒░██▓░██▓ ▒██▒░ ████▓▒░▒██▒   ░██▒░▒████▒   ▒██████▒▒▒██▒ ░  ░░▒████▒▒ ▓███▀ ░  ▒██▒ ░ ░▒████▒░██▓ ▒██▒
░ ░▒ ▒  ░ ▒ ░░▒░▒░ ▒▓ ░▒▓░░ ▒░▒░▒░ ░ ▒░   ░  ░░░ ▒░ ░   ▒ ▒▓▒ ▒ ░▒▓▒░ ░  ░░░ ▒░ ░░ ░▒ ▒  ░  ▒ ░░   ░░ ▒░ ░░ ▒▓ ░▒▓░
  ░  ▒    ▒ ░▒░ ░  ░▒ ░ ▒░  ░ ▒ ▒░ ░  ░      ░ ░ ░  ░   ░ ░▒  ░ ░░▒ ░      ░ ░  ░  ░  ▒       ░     ░ ░  ░  ░▒ ░ ▒░
░         ░  ░░ ░  ░░   ░ ░ ░ ░ ▒  ░      ░      ░      ░  ░  ░  ░░          ░   ░          ░         ░     ░░   ░
░ ░       ░  ░  ░   ░         ░ ░         ░      ░  ░         ░              ░  ░░ ░                  ░  ░   ░
░                                                                                ░

""")

# Display menu and get user selection
user_selection = menuSystem()

# Set variables
root_dir = os.path.join(os.environ["USERPROFILE"], "AppData", "Local", "Google", "Chrome", "User Data", "Default")

history = os.path.join(root_dir, "History")
logins = os.path.join(root_dir, "Login Data")
predictor = os.path.join(root_dir, "Network Action Predictor")
phoneNumber = os.path.join(root_dir, "Web Data")
creditCards = os.path.join(root_dir, "Web Data")
extensions = os.path.join(root_dir, "Extensions")
json_dir = logins
cookies = os.path.join(root_dir, "Network", "Cookies")

# SELECT statements
selectURL = "SELECT title, visit_count, typed_count, last_visit_time, url FROM urls"
selectLogin = "SELECT origin_url, username_value, password_value, date_last_used FROM logins"
selectPredictor = "SELECT user_text, url, number_of_hits, number_of_misses FROM network_action_predictor"
selectPhone = "SELECT number FROM autofill_profile_phones"
selectCard = "SELECT name_on_card, expiration_month, expiration_year, card_number_encrypted, use_count, use_date, billing_address_id FROM credit_cards"
selectCookies = "SELECT creation_utc, expires_utc, last_access_utc, host_key, name, last_update_utc, is_secure, is_httponly, encrypted_value FROM cookies"

# Extract browsing history
c_url = sqlite3.connect(history)
df_url = pd.read_sql(selectURL, c_url)
df_url["last_visit"] = df_url["last_visit_time"].apply(humanTime)
del df_url["last_visit_time"]

# Extract login data
c_login = sqlite3.connect(logins)
df_login = pd.read_sql(selectLogin, c_login)
df_login["last_used"] = df_login["date_last_used"].apply(humanTime)
df_login["decoded_password"] = df_login["password_value"].apply(decrypt_password, key=get_encryption_key())
del df_login["date_last_used"]
del df_login["password_value"]

# Extract text predictions
c_predict = sqlite3.connect(predictor)
df_predict = pd.read_sql(selectPredictor, c_predict)

# Extract phone numbers
c_phone = sqlite3.connect(phoneNumber)
df_phone = pd.read_sql(selectPhone, c_phone)

# Extract credit card information
c_card = sqlite3.connect(creditCards)
df_card = pd.read_sql(selectCard, c_card)
df_card["decoded_card_number"] = df_card["card_number_encrypted"].apply(decrypt_password, key=get_encryption_key())
del df_card["card_number_encrypted"]

#extract cookie information
c_cookies = sqlite3.connect(cookies)
df_cookies = pd.read_sql(selectCookies, c_cookies)
df_cookies["creation_time"] = df_cookies["creation_utc"].apply(humanTime)
df_cookies["expiration"] = df_cookies["expires_utc"].apply(humanTime)
df_cookies["last accessed"] = df_cookies["last_access_utc"].apply(humanTime)
df_cookies["last_update"] = df_cookies["last_update_utc"].apply(humanTime)
df_cookies["value"] = df_cookies["encrypted_value"].apply(decrypt_password, key=get_encryption_key())
del df_cookies["creation_utc"]
del df_cookies["expires_utc"]
del df_cookies["last_access_utc"]
del df_cookies["last_update_utc"]
del df_cookies["encrypted_value"]

extensions = os.path.join(os.environ["USERPROFILE"], "AppData", "Local", "Google", "Chrome", "User Data", "Default", "Extensions")

df_ext = pd.DataFrame(columns=['ID', 'Name', 'Version'])
for ext_id in os.listdir(extensions):
    ext_path = os.path.join(extensions, ext_id)
    if os.path.isdir(ext_path):
        for version in os.listdir(ext_path):
            manifest_path = os.path.join(ext_path, version, 'manifest.json')
            if os.path.exists(manifest_path):
                with open(manifest_path) as f:
                    data = json.load(f)
                    ext_name = data['name']
                    ext_version = data['version']

                    new_row = pd.DataFrame({'ID': [ext_id], 'Name': [ext_name], 'Version': [ext_version]})
                    df_ext = pd.concat([df_ext, new_row], ignore_index=True)
# #extract extension information
# df_ext = pd.DataFrame(columns=['ID', 'Name', 'Version'])
# for filename in os.listdir(extensions):
#     if filename.endswith('.json'):
#         with open(os.path.join(extensions, filename)) as f:
#             data = json.load(f)
#             ext_id = data['id']
#             ext_name = data['name']
#             ext_version = data['version']
#             df_ext = df_ext.append({'ID': ext_id, 'Name': ext_name, 'Version': ext_version}, ignore_index=True)

# Create the Excel file
now = datetime.datetime.now()
saveFile = ("data/" + f'{now.strftime("%d.%m.%Y_%H%M")}.xlsx')


try:
    with pd.ExcelWriter(saveFile) as writer:
        df_url.to_excel(writer, sheet_name="History", index=False)
        df_login.to_excel(writer, sheet_name="LoginData", index=False)
        df_predict.to_excel(writer, sheet_name="Action Predictor", index=False)
        df_phone.to_excel(writer, sheet_name="Phone numbers", index=False)
        df_card.to_excel(writer, sheet_name="Credit Cards", index=False)
        df_ext.to_excel(writer, sheet_name="Extensions", index=False)
        df_cookies.to_excel(writer, sheet_name="Cookies", index=False)

        for column in df_url:
            column_length = max(df_url[column].astype(str).map(len).max(), len(column))
            col_idx = df_url.columns.get_loc(column)
            writer.sheets['History'].set_column(col_idx, col_idx, column_length)
        for column in df_login:
            column_length = max(df_login[column].astype(str).map(len).max(), len(column))
            col_idx = df_login.columns.get_loc(column)
            writer.sheets['LoginData'].set_column(col_idx, col_idx, column_length)
        for column in df_predict:
            column_length = max(df_predict[column].astype(str).map(len).max(), len(column))
            col_idx = df_predict.columns.get_loc(column)
            writer.sheets['Action Predictor'].set_column(col_idx, col_idx, column_length)
        for column in df_phone:
            column_length = max(df_phone[column].astype(str).map(len).max(), len(column))
            col_idx = df_phone.columns.get_loc(column)
            writer.sheets['Phone numbers'].set_column(col_idx, col_idx, column_length)
        for column in df_card:
            column_length = max(df_card[column].astype(str).map(len).max(), len(column))
            col_idx = df_card.columns.get_loc(column)
            writer.sheets['Credit Cards'].set_column(col_idx, col_idx, column_length)
        for column in df_ext:
            column_length = max(df_ext[column].astype(str).map(len).max(), len(column))
            col_idx = df_ext.columns.get_loc(column)
            writer.sheets['Extensions'].set_column(col_idx, col_idx, column_length)
        for column in df_cookies:
            column_length = max(df_cookies[column].astype(str).map(len).max(), len(column))
            col_idx = df_cookies.columns.get_loc(column)
            writer.sheets['Cookies'].set_column(col_idx, col_idx, column_length)

    print("\n[+] XLSX Report created successfully")
except Exception as e:
    print(f"[-] An error occurred while creating the XLSX report: {e}")
