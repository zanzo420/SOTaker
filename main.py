import re
import urllib.parse
import urllib.request

import bs4
import json
import requests


def loadJson(url):
    res = requests.get(url)
    js = res.text
    obj_ = json.loads(js)
    return obj_


def get_question_ids(searchfor):
    query = urllib.parse.urlencode({'q': searchfor})
    url = 'http://ajax.googleapis.com/ajax/services/search/web?v=1.0&%s' % query
    search_response = urllib.request.urlopen(url)
    search_results = search_response.read().decode("utf8")
    results = json.loads(search_results)
    data = results['responseData']
    hits = data['results']
    ids_ = ""
    for h in hits:
        id_ = re.search(r"/(\d+)/", h["url"])
        if id_:
            ids_ += id_.group(1) + ";"
    return ids_[:len(ids_)-1]

# TODO user input
input_ = input("Search for: ")
search_term = input_.replace(' ', '+')
ids = get_question_ids(search_term + " site:stackoverflow.com")
# key for Stack Exchange API
key = "ByWaOHYZMBBi5O4eNX6DyA(("
searchurl = "https://api.stackexchange.com/2.2/questions/"+ids+\
            "/answers?order=desc&sort=activity&site=stackoverflow&filter=!bJDus)chijK43X@key="+key
obj = loadJson(searchurl)

if "error_id" in obj:
    print("ERROR: " + obj["error_name"])
    print(obj["error_message"])
    exit(0)

score = -10000
best_answer = ""
highest_score_answer = ""
for i in range(len(obj["items"])):
    if item["score"] < score:
        continue
    item = obj["items"][i]
    score = item["score"]
    body = item["body"]
    highest_score_answer = body
    if item["is_accepted"] == "True":
        best_answer = body

if best_answer == "":
    best_answer = highest_score_answer

soup = bs4.BeautifulSoup(best_answer, "html.parser")
longest = 0
best_snippet = ""
if len(soup.find_all("code")) == 0:
    print(soup.text)
else:
    # bias towards answers more towards the end (since usually the final answer is at the bottom)
    # also bias towards longer snippets of code
    count = 1

    for link in soup.find_all("code"):
        code = link.contents[0]
        length = len(code)
        count += 0.1
        if length * count > longest:
            longest = length
            best_snippet = code
    print(best_snippet)

