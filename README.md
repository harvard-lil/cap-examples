# CAP examples

A repository of examples of what can be done with Caselaw Access Project data.
- [CAP Github repo](https://github.com/harvard-lil/capstone)
- [CAP homepage](https://case.law/)

## Interested in contributing your own examples?
1. Fork this repository
2. Add your work
3. Make sure to add any requirements your project needs to [requirements.in](requirements.in)
4. Run ```pip-compile --output-file requirements.txt requirements.in```
5. Add a link in the [Projects section](#projects)
6. Create a [pull request](https://github.com/harvard-lil/cap-examples/compare)
7. Thank you for contributing!


## Install
`3.5.4` is the python version we're currently using on CAP, so to keep things simple, we'll be using the same version for these examples.
 
We recommend installing pyenv — [follow instructions to install here](https://github.com/pyenv/pyenv). 

Install your python version using pyenv and activate your virtual environment:
```
$ pyenv install 3.5.4 
$ pyenv virtualenv 3.5.4 capexamples
$ pyenv activate capexamples
(capexamples) $ 
```

Set up! 
```
(capexamples) $ pip install -r requirements.txt && fab setup
```

## Downloading bulk data

#### Helper methods to download whitelisted bulk data 
Download the Illinois dataset
```
(capexamples) $ fab get_cases_from_bulk:Illinois
```

Or, download the Arkansas dataset
```
(capexamples) $ fab get_cases_from_bulk:Arkansas
```
 
## Using the API
[Read our API documentation.](https://case.law/api/)

In order to download [non-whitelisted](https://case.law/api/#limits) cases, you must [register for an API key](https://case.law/user/register/).

Once you have your API key, copy and paste it into your secret keys file [settings.py](config/settings.py).


## Projects
- [Bulk Case Extract](bulk_extract/extract_cases.ipynb) - Get cases from our api's /bulk endpoint. Extract cases into a dataframe.  
- [Full Text Search](full_text_search/full_text_search.ipynb) - Get all cases that include a keyword.
- [Full Text Search with Context](api_text_search/api_text_search.py) - Like full text search, only this time using your API key to get the context around the word.
- [Bulk Exploration: ngrams](bulk_exploration/ngrams.ipynb) – Use the open Arkansas bulk cases to explore interesting words.
- [Bulk Exploration: ngrams and Justice Cartwright](bulk_exploration/cartwright.ipynb) – Use the open Illinois bulk cases to explore interesting words, and look at a Judge's opinion publishing history.  
- [map_courts](map_courts/map_courts.ipynb) - Map all the courts on a U.S. map.
