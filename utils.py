import os
import requests
import zipfile
import certifi
import urllib3

from urllib3.exceptions import MaxRetryError
from tqdm import tqdm

try:
    from config import settings
except ImportError:
    # error triggered on setup.
    # settings should exist after.
    pass

CVIOLET = '\33[35m'
CEND = '\33[0m'

CURL = '\33[4m'


def get_api_url(resource=None):
    root_url = "%s/%s/" % (settings.API_URL, settings.API_VERSION)
    if not resource:
        return root_url

    return root_url + resource + '/'


def get_jurisdictions():
    url = get_api_url() + 'jurisdictions'
    response = requests.get(url)
    return response.json()['results']


def print_info(instruction):
    """
    Colorize print output for instructions
    """
    print(CVIOLET + instruction + CEND)


def get_cases_from_bulk(jurisdiction="Illinois", data_format="json"):
    body_format = "xml" if data_format == "xml" else "text"
    bulk_url = settings.API_BULK_URL + "/?body_format=%s&filter_type=jurisdiction" % body_format
    bulk_api_results = requests.get(bulk_url)
    found = False

    for jur in bulk_api_results.json()['results']:
        if jurisdiction in jur['file_name']:
            found = True
            break

    if not found:
        raise Exception("Jurisdiction not found. Please check spelling.")

    filename = os.path.join(settings.DATA_DIR, jur['file_name'])

    http = urllib3.PoolManager(
        cert_reqs='CERT_REQUIRED',
        ca_certs=certifi.where())

    headers = {'AUTHORIZATION': 'Token {}'.format(settings.API_KEY)}
    try:
        resp = http.request("GET", jur["download_url"],
                            preload_content=False,
                            headers=headers)
    except MaxRetryError as err:
        print("Writing of file was interrupted.\n\n%s" % err)
        return

    if resp.status != 200:
        raise Exception("Something went wrong.\n\n%s" % resp.data)

    print_info("downloading %s into ../data dir" % jur['file_name'])
    with open(filename, 'wb') as f:
        for chunk in tqdm(resp.stream(1024)):
            f.write(chunk)

    print_info("extracting %s into ../data dir" % jur['file_name'])
    with zipfile.ZipFile(filename, 'r') as zip_ref:
        zip_ref.extractall(settings.DATA_DIR)

    print_info("Done.")

    decompressed_dir = filename.split('.zip')[0]
    return os.path.join(decompressed_dir + '/data/data.jsonl.xz')


def get_and_extract_from_bulk(jurisdiction="Illinois", data_format="json"):
    dir_exists = False
    data_format = "xml" if data_format == "xml" else "text"  # xml or json

    for filename in os.listdir(settings.DATA_DIR):
        if jurisdiction in filename and "-" + data_format in filename:
            if os.path.exists(os.path.join(settings.DATA_DIR, filename + '/data/data.jsonl.xz')):
                dir_exists = True
                break

    if dir_exists:
        dir_path = os.path.join(settings.DATA_DIR, filename)
    else:
        print_info("Getting compressed file for %s from /bulk endpoint.\nThis might take a while." % jurisdiction)
        dir_path = get_cases_from_bulk(jurisdiction=jurisdiction, data_format=data_format)

    compressed_file = os.path.join(settings.DATA_DIR, dir_path)

    return compressed_file


def get_cases_from_api(**kwargs):
    """
    Get back json of the first 100 cases unless a cursor argument is provided
    """
    api_url = get_api_url(resource='cases')
    filters = "?format=json&"
    for key, val in kwargs.items():
        filters += "%s=%s&" % (key, val)

    api_url += filters

    headers = {'AUTHORIZATION': 'Token {}'.format(settings.API_KEY)}
    response = requests.get(api_url, headers=headers)
    if response.status_code != 200:
        raise Exception("Something went wrong.\n\n%s" % response.reason)

    return response.json()
