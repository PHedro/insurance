### Usage:
Install Python 3.8.5 or greater, you can do it via pyenv https://github.com/pyenv/pyenv#installation and virtualenv
```commandline
pyenv install 3.8.5
pyenv virtualenv 3.8.5 insurance
```
Activate the virtualenv
```commandline
pyenv activate insurance
```
Clone the project
```commandline
git clone git@github.com:PHedro/insurance.git
```
Go to the project folder (the one where you can find the README file)
```commandline
cd /path/to/project/ 
```
Install the project requirements (remember to activate the virtualenv)
```commandline
pip install -r requirements.txt
```

To execute `sample_usage.py`, after activating your virtualenv and changing directory to the same directory as the script and having installed the requirements:
```commandline
python sample_usage.py
```
Or from anywhere, but with virtualenv activated:
```commandline
python /path/to/project/sample_usage.py
```
You will see a similar output to this one:
```
$ python sample_usage.py 
  DealId  Company           Peril       Location
--------  ----------------  ----------  ----------
       1  WestCoast         Earthquake  USA
       2  WestCoast         Hailstone   Canada
       5  GeorgiaInsurance  Hurricane   USA


Peril         Loss
----------  ------
Earthquake    3500
Hurricane     3000

```

Running tests, from the project folder (the one containing README.md):
```commandline
python -m unittest discover -v 
```
