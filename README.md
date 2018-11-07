# CAP examples

A repository of examples of what can be done with Caselaw Access Project data

3.5.4 is the python version we're currently using on CAP, so to keep things simple, we'll be using the same version for these examples.
 
We recommend installing pyenv ([follow instructions to install here](https://github.com/pyenv/pyenv)). 

Install your python version using pyenv and activate your virtual environment:
```
$ pyenv install 3.5.4 
$ pyenv 3.5.4 capexamples
$ pyenv activate capexamples
(capexamples) $ 
```

Set up! 
```
(capexamples) $ fab setup
```

## Downloading bulk data

#### Helper methods to download whitelisted bulk data 
Download the Illinois dataset
```
(capexamples) $ fab get_data:Illinois
```

Or, download the Arkansas dataset
```
(capexamples) $ fab get_data:Arkansas
```
 
## Using the API
[Read our API documentation](https://case.law/api/)

In order to download [non-whitelisted](https://case.law/api/#limits) cases, you must [register for an API key](https://case.law/user/register/).

Once you have your API key, copy and paste it into your secret keys file [settings.py](settings.py).



