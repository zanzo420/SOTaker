import requests, json, bs4
import re
import urllib.request, urllib.parse

def loadJson(url):
    res = requests.get(url)
    js = res.text
    obj = json.loads(js)
    return obj

def get_question_ids(searchfor):
  query = urllib.parse.urlencode({'q': searchfor})
  url = 'http://ajax.googleapis.com/ajax/services/search/web?v=1.0&%s' % query
  search_response = urllib.request.urlopen(url)
  search_results = search_response.read().decode("utf8")
  results = json.loads(search_results)
  data = results['responseData']
  hits = data['results']
  ids = ""
  for h in hits:
      id = re.search(r"/(\d+)/", h["url"])
      if id:
          ids+=id.group(1) + ";"
  return ids[:len(ids)-1]

# TODO user input
input = input("Search for: ")
search_term = input.replace(' ', '+')
ids = get_question_ids(search_term + " site:stackoverflow.com")
#key for Stack Exchange API
key = "ByWaOHYZMBBi5O4eNX6DyA((";
searchurl = "https://api.stackexchange.com/2.2/questions/"+ids+"/answers?order=desc&sort=activity&site=stackoverflow&filter=!bJDus)chijK43X@key="+key
obj = loadJson(searchurl)

if "error_id" in obj:
    print("ERROR: " + obj["error_name"])
    print(obj["error_message"])
    exit(0)

score = -10000
best_answer = ""
for i in range(len(obj["items"])):
    item = obj["items"][i]
    body = item["body"]
    if item["is_accepted"] == "False" or item["score"] < score:
        continue
    score = item["score"]
    best_answer = body

soup = bs4.BeautifulSoup(best_answer, "html.parser")
longest = 0
best = ""
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
            best = code
    print(best)