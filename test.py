import requests

# https://sns-api.bonfida.com/v2/arb/me-listings?categories=<comma separated categories>
url = "https://sns-api.bonfida.com/v2/arb/me-listings?categories=9-club,99-club,english-nouns"
r = requests.get(url)

for x in r.json():
    print(x)
