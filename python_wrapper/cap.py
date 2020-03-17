import io
import csv
import requests
import datetime

from config import settings


class Cap(object):
    """
    Used for accessing the API from the Harvard Law Caselaw Access Project.
    """

    def __init__(self):
        """
        Used for authentication.
        """
        self.API_KEY = settings.API_KEY
        self.header = {'AUTHORIZATION': 'Token {}'.format(self.API_KEY)}

    def _get_api_url(self):
        """
        Internal method for retrieving base API URL from settings.
        """
        return "%s/%s/" % (settings.API_URL, settings.API_VERSION)

    def _request(self, url):
        """
        Internal method for making API requests.
        """
        response = requests.get(url, headers=self.header)

        if str(response.status_code).startswith('2'):
            return response

        raise Exception("URI request returned an error. Error Code " + str(response.status_code))

    def _build_uri(self, uri_base, params):
        """
        Internal method for constructing search query URIs with multiple parameters.
        """
        if not params:
            return uri_base
        else:
            uri_extension = "?"
            for param in params:
                uri_extension = uri_extension + param + "&"
            uri_extension = uri_extension[:-1]  # clip off the final & 
            uri = uri_base + uri_extension
            return uri

    def _extract_from_paginated(self, first_page, attribute_name):
        """
        Internal method for retrieving a list of each specified attribute from a given paginated JSON.
        e.g.: _extract_from_paginated(some_paginated_list, "name") would return an array with the list of 
        all the court names from the given paginated list.
        """
        names = []
        current_page = first_page

        while True:
            names = names + [court[attribute_name] for court in current_page["results"]]
            try:
                next_result = self._request(current_page["next"])
                current_page = next_result.json()
            except:
                break

        return names

    def get_case(self, case_id, full_case=False):
        """
        Single case endpoint; retrieve a case by its numeric ID.
        
        :param case_id: numeric ID used to identify case 
        :type case_id: str|int
        :param full_case: when set to true, this parameter loads the full text. default False.
                          keep in mind this counts toward daily limit for non-research accounts.
        :type full_case: boolean
        
        :return: Case information in JSON
        """
        url = self._get_api_url() + "cases/" + str(case_id)

        if (full_case):
            url = url + "/?full_case=true"

        case = self._request(url)
        return case.json()

    def search_cases(self, search_term="", jurisdiction="", court="", decision_date_min="", decision_date_max="",
                     full_case=False, uri_only=False):
        """
        Full case search endpoint; retrieve list of cases matching specified parameters.
        All parameters optional (and defined as empty by default). 
        
        :param search_term: search by given word; full text search query.
                            multiple search terms can be used by adding a space (ie, "Florida bankruptcy"
                            will only return cases that contain both Florida AND bankruptcy)
        :type case_id: str
        :param jurisdiction: search by jurisdiction; takes a jurisdiction slug
        :type jurisdiction: str
        :param court: Search by court; takes a court slug. Can only specify one slug.
                      See multi_search_cases to specifiy multiple court slugs.
        :type court: str
        :param decision_date_min: search by earliest date; YYYY-MM-DD format
        :type decision_date_min: string
        :param decision_date_max: search by maximum date; YYYY-MM-DD format
        :type decision_date_max: string
        :param full_case: when set to true, full text and body will be loaded for all cases.
                          default 'false'. keep in mind this counts toward daily limit for non-research 
                          accounts.
        :type full_case: boolean
        :param uris_only: When set to True, returns only the URI, not the results of the URI request.
        :type uris_only: boolean
        
        :return: Paginated and ordered JSON list with case info JSON for each case
        """
        url_base = self._get_api_url() + "cases/"
        url_queries = []

        if search_term:
            url_queries.append("search=%s&full_case=true" % search_term)

        if jurisdiction:
            jurisdiction = jurisdiction.lower()
            valid_jurisdictions = [elem['slug'] for elem in self.get_jurisdictions()["results"]]
            if jurisdiction not in valid_jurisdictions:
                raise Exception("Jurisdiction not recognized. Check spelling?")
            url_queries.append("jurisdiction=%s" % jurisdiction)

        if court:
            court = court.lower()
            url_queries.append("court=%s" % court)

        if decision_date_min:
            try:
                datetime.datetime.strptime(decision_date_min, "%Y-%m-%d")
                url_queries.append("decision_date_min=%s" % decision_date_min)
            except:
                raise Exception("Invalid decision_date_min. Make sure date is formatted YYYY-MM-DD.")

        if decision_date_max:
            try:
                datetime.datetime.strptime(decision_date_max, "%Y-%m-%d")
                url_queries.append("decision_date_max=%s" % decision_date_max)
            except:
                raise Exception("Invalid decision_date_max. Make sure date is formatted YYYY-MM-DD.")

        if full_case:
            url_queries.append("full_case=true")

        uri = self._build_uri(url_base, url_queries)

        if uri_only:
            return uri

        search_results = self._request(uri)
        return search_results.json()

    def search_mltpl_courts(self, court_list, search_term="", jurisdiction="", decision_date_min="",
                            decision_date_max="", full_case=False):
        """
        Full case search that can ALSO accept multiple court slugs in the form of an array.
        Used for retrieving data from multiple courts at one time. 
        Returns an array of the first page of paginated API search results for each specified court slug.
        NOTE that you will be returned an array of URLs rather than the full JSON for each slug
        to prevent overloading memory. 
        
        
        :param court_list: A list of court slugs that you wish to search for. 
        :type court_list: list of strings
        :param search_term: search by given word; full text search query.
                            multiple search terms can be used by adding a space (ie, "Florida bankruptcy"
                            will only return cases that contain both Florida AND bankruptcy)
        :type case_id: str
        :param jurisdiction: search by jurisdiction; takes a jurisdiction slug
        :type jurisdiction: str
        :param court: search by court; takes a court slug
        :type court: str
        :param decision_date_min: search by earliest date; YYYY-MM-DD format
        :type decision_date_min: string
        :param decision_date_max: search by maximum date; YYYY-MM-DD format
        :type decision_date_max: string
        :param full_case: when set to true, full text and body will be loaded for all cases.
                          default 'false'. keep in mind this counts toward daily limit for non-research 
                          accounts.
        :type full_case: boolean
        
        :return: An array of URIs. Does NOT return the full JSON.
        """
        results = []
        for court in court_list:
            results.append(self.search_cases(search_term=search_term, jurisdiction=jurisdiction, court=court,
                                             decision_date_min=decision_date_min,
                                             decision_date_max=decision_date_max, full_case=full_case,
                                             uri_only=True))

        return results

    def get_courts(self, name="", abbreviation="", jurisdiction="", slugs_only=False):
        """
        Court search endpoint; retrieves list of courts matching specified parameters.
        All parameters optional, so calling empty function returns entire list of courts.
        
        :param name: searches court with matching names; returns courts that contain this parameter
                     as a substing so exact court name not necessary
        :type name: str
        :param abbreviataion: search by court's official abbreviation; like 'name', searches as
                              substring so exact match not necessary
        :param jurisdiction: search by jurisdiction; takes a jurisdiction slug
        :type jurisdiction: str
        :param slugs_only: toggle to retrieve only the slugs of the specified courts rather than
                           the full JSON
        :type slugs_only: boolean
        
        :return: JSON list of courts.
        """
        url_base = self._get_api_url() + "courts/"
        url_queries = []

        if name:
            url_queries.append("name=%s" % name)

        if abbreviation:
            url_queries.append("name_abbreviation=%s" % abbreviations)

        if jurisdiction:
            jurisdiction = jurisdiction.lower()
            valid_jurisdictions = [elem['slug'] for elem in self.get_jurisdictions()["results"]]
            if jurisdiction not in valid_jurisdictions:
                raise Exception("Jurisdiction not recognized. Check spelling?")
            url_queries.append("jurisdiction=%s" % jurisdiction)

        uri = self._build_uri(url_base, url_queries)
        courts = self._request(uri)

        if slugs_only:
            names = self._extract_from_paginated(courts.json(), "slug")
            return names

        print(uri)
        return courts.json()

    def get_jurisdictions(self, name="", full_name="", whitelisted=""):
        """
        Jurisdiction search endpoint; returns list of jurisdictions.
        
        :return: JSON list of jurisdictions.
        """
        url = self._get_api_url() + 'jurisdictions'
        jurisdictions = self._request(url)
        return jurisdictions.json()

    def get_reporters(self):
        """
        Reporters search endpoint; returns list of reporters.
        
        :return: JSON list of reporters.
        """
        url = self._get_api_url() + 'reporters'
        reporters = self._request(url)
        return reporters.json()

    def get_volumes(self):
        """
        Volumes search endpoint; returns list of volumes.  
        """
        url = self._get_url() + 'volumes'
        volumes = self._request(url)
        return volumes.json()

    def get_citations(self):
        """
        Citations search endpoint; returns list of citations. 
        """
        url = self._get_url() + 'citations'
        citations = self._request(url)
        return citations.json()

    def download_to_csv(self, search_results, filename):
        """
        Input a JSON list of search results (full_text MUST be set to true) and downloads the search results
        as a .csv file. 
        
        :param search_results: JSON search result retrieved using the 'search_cases' method that you wish to
                                download. Search results CAN be paginated; function will iterate through all
                                search result pages.
        :type search_results: JSON
        :param filename: desired filename for downloaded data (make sure to include '.csv' extension)
        :type filename: str
        :param multi: sets whether or not
        
        :return: null
        """

        current_page = search_results

        with open(filename, "w") as csvfile:
            fieldnames = ["id", "name", "name_abbreviation", "decision_date", "court_id", "court_name", "court_slug",
                          "judges", "attorneys", "citations", "url", "head", "body"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            while True:
                for case in current_page["results"]:
                    case_data = {
                        "id": case["id"],
                        "name": case["name"],
                        "name_abbreviation": case["name_abbreviation"],
                        "decision_date": case["decision_date"],
                        "court_id": case["court"]["id"],
                        "court_name": case["court"]["name"],
                        "court_slug": case["court"]["slug"],
                        "judges": str(case["casebody"]["data"]["judges"]),
                        "attorneys": str(case["casebody"]["data"]["attorneys"]),
                        "citations": str(case["citations"]),
                        "url": case["url"],
                        "head": case["casebody"]["data"]["head_matter"],
                        "body": case["casebody"]["data"]["opinions"][0]["text"]
                    }
                    writer.writerow(case_data)

                try:
                    next_result = self._request(current_page["next"])
                    current_page = next_result.json()

                except:
                    break

        print("Downloaded " + str(search_results["count"]) + " court cases to file " + filename + ".")

    def download_mltpl_courts(self, search_results, filename):
        """
        Use for downloading  
        Input a JSON list of URI search results from multi_search_cases (full_text MUST be set to true) and 
        downloads the search results as a .csv file. 
        
        :param search_results: JSON search result retrieved using the 'search_cases' method that you wish to
                                download
        :type search_results: JSON
        :param filename: desired filename of downloaded data
        :type filename: str
        
        :return: null
        """

        court_index = 0
        row_count = 0
        search_results = search_results
        current_uri = search_results[court_index]

        downloaded_count = 0

        with open(filename, "w", encoding='utf-8') as csvfile:
            fieldnames = ["id", "name", "name_abbreviation", "decision_date", "court_id", "court_name",
                          "court_slug", "judges", "attorneys", "citations", "url", "head", "body"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            current_page = self._request(current_uri).json()

            while True:
                try:
                    if current_page["count"] > 0:
                        for case in current_page["results"]:
                            case_data = {
                                "id": case["id"],
                                "name": case["name"],
                                "name_abbreviation": case["name_abbreviation"],
                                "decision_date": case["decision_date"],
                                "court_id": case["court"]["id"],
                                "court_name": case["court"]["name"],
                                "court_slug": case["court"]["slug"],
                                "judges": str(case["casebody"]["data"]["judges"]),
                                "attorneys": str(case["casebody"]["data"]["attorneys"]),
                                "citations": str(case["citations"]),
                                "url": case["url"],
                                "head": case["casebody"]["data"]["head_matter"],
                                "body": case["casebody"]["data"]["opinions"][0]["text"]
                            }
                            writer.writerow(case_data)

                    downloaded_count = downloaded_count + len(current_page["results"])
                    next_result = self._request(current_page["next"])
                    current_page = next_result.json()

                except:
                    if len(current_page["results"]) != 0:
                        print("Downloaded " + current_page["results"][0]["court"]['slug'] + " (" +
                              str(downloaded_count) + " total rows)")
                    court_index = court_index + 1
                    row_count = row_count + current_page["count"]
                    if (court_index + 1 <= len(search_results)):
                        current_uri = search_results[court_index]
                        current_page = self._request(current_uri).json()

                    else:
                        break

        print("Downloaded " + str(downloaded_count) + " court cases to file " + filename + ".")
