import csv
import json
import sys
import argparse
import urllib.request
import logging

"""
    This demonstration script fetches search results from the CAP cases endpoint and writes a subset of their fields to
    a CSV file. It uses only the Python 3 standard library, so no additional installation is required.
    
    There is not currently a command line option to select which fields are included, so changing the fields requires
    manually editing the script.
    
    Usage:
    
        $ python api_to_csv.py -h
        usage: api_to_csv.py [-h] [--api-key API_KEY] [--out-path OUT_PATH] url
        
        Print CAPAPI query to CSV.
        
        positional arguments:
          url                  target url, e.g.
                               https://api.case.law/v1/cases/?search=first+amendment
        
        optional arguments:
          -h, --help           show this help message and exit
          --api-key API_KEY    api key (optional; only needed if requesting full text)
          --out-path OUT_PATH  output path (default stdout)
        
        example:
          python api_to_csv.py --out-path first_amendment_cases.csv https://api.case.law/v1/cases/?search=first+amendment
"""


logger = logging.getLogger('api_to_csv')


def get_results(url, api_key=None):
    """
        Yield each individual case result from the target URL.
    """
    headers = {}
    if api_key:
        headers['Authorization'] = 'Token {}'.format(api_key)
    page_count = 1
    while True:
        logger.info("Fetching page %s" % page_count)
        response = urllib.request.urlopen(urllib.request.Request(url, headers=headers))
        page = json.loads(response.read().decode('utf-8'))
        for result in page['results']:
            yield result
        url = page['next']
        if not url:
            break
        page_count += 1


def api_query_to_csv(url, api_key=None, out_path=None):
    """
        Write all case results from URL to out_path, defaulting to stdout.
    """
    if out_path:
        out_file = open(out_path, 'w', encoding='utf-8')
    else:
        out_file = sys.stdout
    out = csv.writer(out_file)
    out.writerow(['id', 'frontend_url', 'name', 'name_abbreviation', 'citation', 'decision_date', 'jurisdiction'])
    for result in get_results(url, api_key):
        out.writerow([
            result['id'],
            result['frontend_url'],
            result['name'],
            result['name_abbreviation'],
            next((cite['cite'] for cite in result['citations'] if cite['type'] == 'official'), ''),
            result['decision_date'],
            result['jurisdiction']['name'],
        ])


def main():
    """
        Parse command line arguments and call api_query_to_csv.
    """
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description='Print CAPAPI query to CSV.',
        epilog="""example:\n  python api_to_csv.py --out-path first_amendment_cases.csv https://api.case.law/v1/cases/?search=first+amendment"""
    )
    parser.add_argument('url', help='target url, e.g. https://api.case.law/v1/cases/?search=first+amendment')
    parser.add_argument('--api-key', help='api key (optional; only needed if requesting full text)')
    parser.add_argument('--out-path', help='output path (default stdout)')
    args = parser.parse_args()
    logging.basicConfig(level=logging.INFO)
    api_query_to_csv(args.url, args.api_key, args.out_path)


if __name__ == '__main__':
    main()