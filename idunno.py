import requests

url = "https://www.fantasysharks.com/apps/Projections/WeeklyProjections.php"

querystring = {"pos":"ALL","format":"json"}

session = requests.Session()
# telling the site the request is coming from insomnia instead of python or whatever
session.headers.update({"User-Agent": "insomnia/2021.5.3"}) # this is kind of the key
r = session.get(url=url, params=querystring)

print(r.status_code) # this returns 200 !
json_data = r.json()
for item in json_data:
    print(item)