
# Python Wrapper
Simple Python bindings for tasks including getting a court case, getting judges, getting jurisdictions, downloading court cases to a CSV file, and more.

## Getting Started
To start using the Python bindings, simply instantiate the API with your authentication key.
```python
cap = Cap("AUTHENTICATION_TOKEN_HERE")
```
## Usage & Examples
You can search for a single-case if you know its ID.

```python
cap.get_case(435800)
```

<details>
<summary>View Response</summary>

```js
{'citations': [{'cite': '1 Ill. 34', 'type': 'official'}],
 'court': {'id': 8772,
  'name': 'Illinois Supreme Court',
  'name_abbreviation': 'Ill.',
  'slug': 'ill',
  'url': 'https://api.case.law/v1/courts/ill/'},
 'decision_date': '1820-12',
 'docket_number': '',
 'first_page': '34',
 'id': 435800,
 'jurisdiction': {'id': 29,
  'name': 'Ill.',
  'name_long': 'Illinois',
  'slug': 'ill',
  'url': 'https://api.case.law/v1/jurisdictions/ill/',
  'whitelisted': True},
 'last_page': '34',
 'name': 'John Thornton and others, Appellants, v. George Smiley and John Bradshaw, Appellees',
 'name_abbreviation': 'Thornton v. Smiley',
 'reporter': {'full_name': 'Illinois Reports',
  'url': 'https://api.case.law/v1/reporters/1058/'},
 'url': 'https://api.case.law/v1/cases/435800/',
 'volume': {'url': 'https://api.case.law/v1/volumes/32044057891608/',
  'volume_number': '1'}}
  ```  
</details>  
<br />
Otherwise, you can run search queries to retrieve lists that match specified parameters. For example, you can search for all courts with "bankruptcy" in the text:

```python
cap.search_cases(search_term="bankruptcy")
# returns the first 100 cases with the word 'bankruptcy' in the heading or full text
```
<details>
<summary>View Response</summary>

```js
{'count': None,
 'next': 'https://api.case.law/v1/cases/?cursor=cD00MjE3LjA%3D&search=bankruptcy',
 'previous': None,
 'results': [{'citations': [{'cite': '59 Mass. App. Dec. 100',
     'type': 'official'}],
   'court': {'id': 15176,
    'name': 'Massachusetts Appellate Decisions',
    'name_abbreviation': 'Mass. App. Dec.',
    'slug': 'mass-app-dec',
    'url': 'https://api.case.law/v1/courts/mass-app-dec/'},
   'decision_date': '1976-11-09',
   'docket_number': 'No. 8394; No. 750',
   'first_page': '100',
   'id': 2,
   'jurisdiction': {'id': 4,
    'name': 'Mass.',
    'name_long': 'Massachusetts',
    'slug': 'mass',
    'url': 'https://api.case.law/v1/jurisdictions/mass/',
    'whitelisted': False},
   'last_page': '109',
   'name': 'MERRIMACK VALLEY NATIONAL BANK v. G. STEWART BAIRD, JR. ET AL',
   'name_abbreviation': 'Merrimack Valley National Bank v. Baird',
   'reporter': {'full_name': 'Massachusetts Appellate Decisions',
    'url': 'https://api.case.law/v1/reporters/579/'},
   'url': 'https://api.case.law/v1/cases/2/',
   'volume': {'url': 'https://api.case.law/v1/volumes/32044026226753/',
    'volume_number': '59'}},
    and so on
  ```
</details>
<br />

Acceptable search parameters include: search term (returns cases where that search term is featured anywhere in the full body of the text), jurisdiction (slug of specified jurisdiction), court (slug of specified court), decision_date_min (returns cases only dated past this date; must be formatted YYYY-MM-DD), and decision_date_min (returns cases only dated before this date; must be formatted YYYY-MM-DD).

Another example:

```python
cap.search_cases(jurisdiction="ark")
# returns the first 100 cases from Arkansas
```

<details>
		<summary>View Response</summary>

```js
{'count': 3644,
 'next': 'https://api.case.law/v1/cases/?cursor=bz05JnA9MjAxMC0wMy0wNA%3D%3D&decision_date_min=2010-01-01&jurisdiction=ark',
 'previous': None,
 'results': [{'citations': [{'cite': '374 S.W.3d 38', 'type': 'official'},
    {'cite': '2010 Ark. App. 18', 'type': 'parallel'}],
   'court': {'id': 13370,
    'name': 'Arkansas Court of Appeals',
    'name_abbreviation': 'Ark. Ct. App.',
    'slug': 'ark-ct-app',
    'url': 'https://api.case.law/v1/courts/ark-ct-app/'},
   'decision_date': '2010-01-06',
   'docket_number': 'No. CA 09-435',
   'first_page': '38',
   'id': 7121492,
   'jurisdiction': {'id': 34,
    'name': 'Ark.',
    'name_long': 'Arkansas',
    'slug': 'ark',
    'url': 'https://api.case.law/v1/jurisdictions/ark/',
    'whitelisted': True},
   'last_page': '44',
   'name': 'ALL CREATURES ANIMAL HOSPITAL, INC. and Marion Smith, Appellants v. FINOVA CAPITAL CORPORATION, Appellee',
   'name_abbreviation': 'All Creatures Animal Hospital, Inc. v. Finova Capital Corp.',
   'reporter': {'full_name': 'South Western Reporter Third Series',
    'url': 'https://api.case.law/v1/reporters/612/'},
   'url': 'https://api.case.law/v1/cases/7121492/',
   'volume': {'url': 'https://api.case.law/v1/volumes/32044132267543/',
    'volume_number': '374'}},
    and so on...
    
  ```
  </details>
  <br />
  

You can mix and match as many search parameters as you want.

```python
cap.search_cases(search_term="bankruptcy", jurisdiction="ark", 
				decision_date_min="1950-01-01", decision_date_max="2000-01-01")
```

<details>
		<summary>View Response</summary>

```js
{'count': 273,
 'next': 'https://api.case.law/v1/cases/?cursor=cD0xNzA5MzA3LjA%3D&decision_date_max=2000-01-01&decision_date_min=1950-01-01&jurisdiction=ark&search=bankruptcy',
 'previous': None,
 'results': [{'citations': [{'cite': '336 Ark. 432', 'type': 'official'},
    {'cite': '985 S.W.2d 314', 'type': 'parallel'}],
   'court': {'id': 8808,
    'name': 'Arkansas Supreme Court',
    'name_abbreviation': 'Ark.',
    'slug': 'ark',
    'url': 'https://api.case.law/v1/courts/ark/'},
   'decision_date': '1999-02-18',
   'docket_number': '98-126',
   'first_page': '432',
   'id': 51189,
   'jurisdiction': {'id': 34,
    'name': 'Ark.',
    'name_long': 'Arkansas',
    'slug': 'ark',
    'url': 'https://api.case.law/v1/jurisdictions/ark/',
    'whitelisted': True},
   'last_page': '435',
   'name': 'Mattie ALLISON v. Alvin LONG and Shirley Long, Husband & Wife; the Unknown Heirs at Law of Grant Long, Jr., Deceased; the Unknown Heirs at Law of Jo Ann Long, Deceased; John A. Eason; Ruby J. Eason; and Any Other Person Who Might Claim An Interest',
   'name_abbreviation': 'Allison v. Long',
   'reporter': {'full_name': 'Arkansas Reports',
    'url': 'https://api.case.law/v1/reporters/368/'},
   'url': 'https://api.case.law/v1/cases/51189/',
   'volume': {'url': 'https://api.case.law/v1/volumes/32044056076631/',
    'volume_number': '336'}},
    
	and so on...
    
  ```
</details>
<br />

## Downloading Data as CSV

You can download search queries as CSV files with the `download_to_csv` method. To use, pass in a search query JSON retrieved from the `search_cases` method, then pass that into the `download_to_csv` method along with a filename  Note that you must set `full_case=True` in your search query in order for this function to work. 

```python
search_results = cap.search_cases(jurisdiction="ark", decision_date_min="2010-01-01", full_case=True)
cap.download_to_csv(search_results, filename="21ark")
# downloads all cases in Arkansas from 2010 to later to a CSV file
```

<details>
<summary>View Response</summary>
	
```js
Downloaded 3644 court cases to file 21ark.csv.
```
</details>

## Downloading Data from Multiple Different Courts

To retrieve data from multiple different courts, use the `search_mltpl_courts` method, and pass in the list of courts along with any other search parameters you need. You can also systematically retrieve a list of courts that match a certain parameter by using `get_courts` with the parameter `slugs_only=True`. Finally, you can enter these results into the `download_mltpl_courts` method.

In summary, if you would like to download, for example, all court cases that contain the word 'company' from courts that have 'bankruptcy' in the court name, you would call:

```python
bankruptcy_courts = cap.get_courts(name="bankruptcy", slugs_only=True)
bankruptcy_apis = cap.search_mltpl_courts(bankruptcy_courts, search_term="company", full_case=True)
cap.download_mltpl_courts(bankruptcy_apis, "bank.csv")
```


<details>
<summary>View Response</summary>
	
```js
bankr-d-conn
Downloaded 3 rows, 3 total.
bankr-d-del
Downloaded 3 rows, 6 total.
bankr-d-idaho
Downloaded 1 rows, 7 total.
bankr-d-md
Downloaded 1 rows, 8 total.
bankr-d-mass
Downloaded 1 rows, 9 total.
bankr-d-mont
Downloaded 1 rows, 10 total.
bankr-dnd
Downloaded 1 rows, 11 total.
bankr-ed-mich
Downloaded 1 rows, 12 total.
bankr-edny
Downloaded 1 rows, 13 total.
bankr-ed-pa
Downloaded 1 rows, 14 total.
bankr-ed-tex
Downloaded 1 rows, 15 total.
bankr-md-fla
Downloaded 3 rows, 18 total.
bankr-md-la
Downloaded 1 rows, 19 total.
bankr-md-pa
Downloaded 1 rows, 20 total.
bankr-nd-cal
Downloaded 1 rows, 21 total.
bankr-nd-ill
Downloaded 3 rows, 24 total.
bankr-nd-ind
Downloaded 1 rows, 25 total.
bankr-ndny
Downloaded 1 rows, 26 total.
bankr-nd-ohio
Downloaded 1 rows, 27 total.
bankr-nd-okla
Downloaded 1 rows, 28 total.
bankr-sd-fla
Downloaded 1 rows, 29 total.
bankr-sdny
Downloaded 3 rows, 32 total.
bankr-sd-ohio
Downloaded 2 rows, 34 total.
bankr-sd-tex
Downloaded 2 rows, 36 total.
bankr-wd-mich
Downloaded 1 rows, 37 total.
bankr-wd-pa
Downloaded 1 rows, 38 total.
bankr-wd-va
Downloaded 1 rows, 39 total.
Downloaded 39 total court cases to file bank.csv.
```
</details>

