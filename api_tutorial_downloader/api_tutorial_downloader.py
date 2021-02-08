import requests
import json
import time
from tqdm import tqdm

"""
This script is intended to be a code accompaniment to the Caselaw Access Project API Documentation: 

https://case.law/docs/ 

If properly configured, should download all of the cases for a given reporter and store them in JSON format. 

It's primarily a demonstration tool and largely untested. It's certainly not the most efficient design for most 
purposes— bulk data likely satisfies your need more efficiently and there are likely bugs or edge cases that could trip 
it up. Please use it as a guide to learn how to make this sort of tool for yourself rather than as a tool. We're 
grateful for bug reports but won't provide any support in configuring or using this script. That said, feel free to use
any code in here without attribution.

By default, it does not download full case text— it only downloads metadata. You can set it to download case text by 
changing the full_case variable to True. Unless you have an academic researcher account, your API key will only allow 
you to download 500 full case texts per day for cases after 1923. Case texts before 1923 and all metadata are not at all
throttled. Please read the docs https://case.law/docs/ for more info on these limits.
"""


def main():

    # CONFIGURATION

    sleep_delay = .25  # Our API is pretty robust, but please be kind
    reporter = '983'  # The numerical ID of the reporter you'd like to download
    start_year = 1754  # This is set to the earliest decision date of this reporter. The only
    offset = 10  # the initial value of the offset from the start year. So if the start_year is 1754, that's 1754-1764
    full_case = False  # See the docs to see the limits on this! Some are totally unrestricted, some aren't.
    page_size = 1000  # The number of cases that the script will retrieve at once. Current request size limits in docs
    api_key = None  # Available in your user account page. More details about API auth in docs
    minimum_set_size = 9000
    maximum_set_size = 9999  # api limit is 10k. We'll get any set of cases between 9000 and 9999

    # Let's get started

    while start_year <= 2018:  # this limits the script when years less than 2018. Check the docs for data scope.

        # get a properly formatted URL from our little function towards the end of the script
        url = prep_url(reporter, start_year, offset, full_case, page_size)

        # make the request
        results = requests.get(url).json()

        # let's check if we have enough cases to meed the minimum_set_size
        while int(results['count']) < minimum_set_size:
            # this runs if we have fewer than minimum_set_size results in our query

            # if there's an extreme discrepency, crank up the offset a little to save time
            if results['count'] < minimum_set_size / 2:
                offset += 10
            if results['count'] < minimum_set_size / 1.5:
                offset += 5
            else:
                offset += 1

            # lets the user know that we didn't have enough cases in that year range
            print("{} results. Expanding to {}-{} to reach {}".format(
                results['count'],
                start_year,
                start_year + offset,
                minimum_set_size
            ))

            # lets make a new URL with the adjusted years, run another query, and let the while loop see if we're good
            url = prep_url(reporter, start_year, offset, False, page_size)

            # make the request. We're passing False for the API Key argument becasue you never need to authenticate
            # to make a simple metadata request
            results = api_request(url, False)

            time.sleep(sleep_delay) # slight pause

        while results['count'] > maximum_set_size:

            # if we're at a 1 year offset and this still doesn't work, you're going to have to switch to months,
            # or maybe even days depending on whatever filtering criteria you build in!
            if offset == 1:
                raise Exception("this script only works in whole-year increments, "
                                "and you might need a more granular time period")

            # if there's an extreme discrepency, crank up the offset a little
            if results['count'] > maximum_set_size * 2:
                offset -= 10
            if results['count'] > maximum_set_size * 1.5:
                offset -= 5
            else:
                offset -= 1

            # lets the user know that we had too many cases in that year range
            print("{} results. Reducing to {}-{} to reach {}".format(
                results['count'],
                start_year,
                start_year + offset,
                maximum_set_size
            ))

            # lets make a new URL with the adjusted years, run another query, and let the while loop see if we're good
            url = prep_url(reporter, start_year, offset, False, page_size)

            # make the request. We're passing False for the API Key argument becasue you never need to authenticate
            # to make a simple metadata request
            results = api_request(url, False)

            time.sleep(sleep_delay)

        # Ok! We've gone through both of those while loops, ensuring that we should never have too many cases, but will
        # not have a super small number, either. (though in some instances we could have fewer than minimum_set_size!)

        # Let's let the user know
        print("{} - {} has {} results: Retrieving.".format(
            start_year,
            start_year + offset,
            results['count'],
            start_year,
            start_year + offset, maximum_set_size
        ))

        # make a URL with all of our options
        url = prep_url(reporter, start_year, offset, full_case, page_size)

        # make the request, passing the api key just in case someone has set one
        results = api_request(url, api_key)

        # we're going to limit out requests to 1000 per "page" and combine them in this variable
        aggregate_results = results['results']

        # nicer to look at  a progress bar than guess if you script froze. The total is the total number of hits for
        # our year-range query. The update is adding the number of hits we got in the request we just got
        progress_bar = tqdm(total=results['count'])
        progress_bar.update(len(results['results']))

        # if there's a 'next' URL and we have more than 0 results, let's try to get the next set
        while 'next' in results and results['next'] and len(results['results']) > 0:
            # grab em, aggregate em, and update the progress bar
            results = api_request(results['next'], api_key)
            aggregate_results += results['results']
            progress_bar.update(len(results['results']))

            time.sleep(sleep_delay)

        # no more for this year range.

        # Let's kill the progress bar
        progress_bar.close()

        # Now let's write the file out
        write(reporter, start_year, offset, aggregate_results)

        # And then make sure we get an updated start_year so we're picking up where we left off when the loop runs again
        start_year += offset + 1

        # Now let's go back up to 'while start_year <=' to start the whole thing over again!


def api_request(url, api_key=None):
    """
        This function takes a url and returns the parsed json object. If necessary, it submits the auth header
    """
    if api_key:
        return requests.get(url, headers={'Authorization': 'Token ' + api_key}).json()
    else:
        return requests.get(url).json()


def prep_url(reporter=None, start_year=None, offset=None, full_case=False, page_size=None):
    """
        This takes the values passed to it and constructs a URL based on them, adding parameters as-needed.
    """
    reporter_arg = "?reporter={}".format(reporter) if start_year else "?"
    start_year_arg = "&decision_date__gte={}".format(start_year) if start_year else ""
    end_year_arg = "&decision_date__lte={}".format(start_year + offset) if start_year and offset else ""
    full_case = "&full_case={}".format(full_case) if full_case else ""
    page_size = "&page_size={}".format(page_size) if page_size else ""
    return 'https://api.case.law/v1/cases/{}{}{}{}{}'.format(
        reporter_arg, start_year_arg, end_year_arg, full_case, page_size)


def write(reporter, start_year, offset, dump_object):
    """
        This function generates an appropriate file name, and writes out the results passed to it in dump_object.
    """
    file_name = "Reporter_{}_{}-{}.json".format(reporter, start_year, start_year + offset)
    print("Saving {}".format(file_name))
    with open(file_name, "w+") as json_file:
        json.dump(dump_object, json_file)


if __name__ == '__main__':
    main()
