import os

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../data')

API_URL = "https://api.case.law"
API_VERSION = "v1"
API_BULK_URL = API_URL + "/" + API_VERSION + "/" + "bulk"
# claim your key at https://case.law/user/details
API_KEY = "123"