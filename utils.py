import requests
import zipfile
import io
from tqdm import tqdm

import settings

CVIOLET = '\33[35m'
CEND = '\33[0m'

CURL = '\33[4m'


def get_api_url():
    return "%s/%s/" % (settings.API_URL, settings.API_VERSION)


def get_jurisdictions():
    url = get_api_url() + 'jurisdictions'
    response = requests.get(url)
    return response.json()['results']


def print_info(instruction):
    """
    Colorize print output for instructions
    """
    print(CVIOLET + instruction + CEND)


def get_cases(jurisdiction):
    bulk_url = settings.API_BULK_URL + "/?body_format=text&filter_type=jurisdiction"
    bulk_api_results = requests.get(bulk_url)
    found = False
    for jur in bulk_api_results.json()['results']:
        if jurisdiction in jur['file_name']:
            found = True
            break

    if not found:
        raise Exception("Jurisdiction not found. Please check spelling.")

    r = requests.get(jur['download_url'])
    z = zipfile.ZipFile(io.BytesIO(r.content))
    print_info("extracting %s into /data dir" % jur['file_name'])
    z.extractall(path=settings.DATA_DIR)



# TODO:
# / ftp style browser: bulk/massachusetts/latest
