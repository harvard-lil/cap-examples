import json
import requests
import settings
import utils


def extract(word="witchcraft", snippets=True):
    """
    Get cases that have the word you're looking for.
    If snippets is True, save only the context of the word
    otherwise, save the entire casebody
    """
    url = utils.get_api_url() + 'cases?full_case=true&search=%s' % word
    headers = {'AUTHORIZATION': 'Token {}'.format(settings.API_KEY)}
    response = requests.get(url, headers=headers)
    res = response.json()

    word_results = {}

    warning_printed = False
    while True:
        for case in res['results']:
            case_data = {
                "id": case["id"],
                "name": case["name"],
                "name_abbreviation": case["name_abbreviation"],
                "context": "",
                "decision_date": case["decision_date"],
                "url": case["url"],
                "citations": case["citations"],
                "times_appeared": 0
            }

            jur_slug = case["jurisdiction"]["slug"]

            try:
                opinions = case['casebody']['data']['opinions']
                text = ''

                # add all opinions and head matter up to one giant string
                for opinion in opinions:
                    text += opinion['text']

                text += case['casebody']['data']['head_matter']
                if snippets:
                    context, times_appeared = get_word_context(word, text)
                    case_data["context"] = context if context else ""
                    case_data["times_appeared"] = times_appeared if times_appeared else 0

                else:
                    case_data['casebody'] = case['casebody']

            except Exception as e:
                if snippets:
                    case_data['context'] = False
                    case_data['times_appeared'] = 0
                else:
                    case_data['casebody'] = False
                if not warning_printed:
                    utils.print_info("\nWarning: Something went wrong -- your daily limit may have run out.\nPlease check your account: https://case.law/user/details")
                    print("\nError:", e)
                    warning_printed = True
            if jur_slug in word_results.keys():
                word_results[jur_slug].append(case_data)
            else:
                word_results[jur_slug] = [case_data]

        try:
            next_result = requests.get(res['next'], headers=headers)
            res = next_result.json()
        except:
            break
    filename = "%s/%s.json" % (settings.DATA_DIR, word)
    with open(filename, "w+") as f:
        json.dump(word_results, f)

    utils.print_info("\n>> Written to file %s" % filename)


def get_word_context(word, casebody):
    """
    Return snippet around word and times the word appeared in the case
    """
    words = casebody.split(" ")
    lower_words = casebody.lower().split(" ")
    times_appeared = 0
    # iterate through entire list of words
    # because word might be a substring, or could have an ocr error that
    # is unaccounted for
    indexes = []
    for i, w in enumerate(lower_words):
        if word in w:
            times_appeared += 1
            indexes.append(i)

    # for now keep it semi-simple with one instance
    index = indexes[0]
    if index >= 10:
        start = index - 10
    else:
        start = 0
    if len(lower_words) >= index + 10:
        end = index + 10
    else:
        end = len(lower_words)

    return " ".join(words[start:end]), times_appeared
