import requests
from collections import OrderedDict


def search_story(keyword):
    starting_url = 'https://api.case.law/v1/cases/?search=' + keyword

    jurisdictions = {}
    results_count = 0

    def get_pages(url):
        while True:
            result = requests.get(url).json()
            yield result
            url = result['next']
            if not url:
                break

    def get_results(url):
        for page in get_pages(url):
            for result in page['results']:
                yield result

    for case in get_results(starting_url):

        results_count += 1

        id = case['id']
        name = case['name_abbreviation']
        jurisdiction = case['jurisdiction']['name']
        date = case['decision_date']
        url = case['url']

        if jurisdiction not in jurisdictions:
            jurisdictions[jurisdiction] = {'name': jurisdiction, 'count': 1, 'oldest_case_id': id,
                                           'oldest_case_name': name, 'oldest_case_date': date, 'oldest_case_url': url}

        else:
            new_count = jurisdictions[jurisdiction]['count'] + 1
            if jurisdictions[jurisdiction]['oldest_case_date'] > date:
                jurisdictions[jurisdiction] = {'name': jurisdiction, 'count': new_count, 'oldest_case_id': id,
                                               'oldest_case_name': name, 'oldest_case_date': date,
                                               'oldest_case_url': url}

    print('\n' + 'Results for keyword: ' + keyword)
    print('Total cases: ' + str(results_count))

    results_sorted = OrderedDict(sorted(jurisdictions.items(), key=lambda kv: kv[1]['oldest_case_date']))

    print('\n')
    print('Jurisdiction-by-Jurisdiction Results' + '\n')

    for values in results_sorted.values():
        print(values['name'] + ': ' + str(values['count']))
        print('Oldest case: ' + values['oldest_case_name'] + '(' + values['oldest_case_date'] + ')')
        print('Link: ' + values['oldest_case_url'])
        print('\n')


search_story('turkey')
