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
  #print('Total results: %s' % data['cursor']['estimatedResultCount'])
  hits = data['results']
  #print('Top %d hits:' % len(hits))
  ids = ""
  for h in hits:
      print(' ', h['url'])
      id = re.search(r"/(\d+)/", h["url"])
      if id:
          ids+=id.group(1) + ";"
  return ids[:len(ids)-1]

# TODO user input
search_term = "quicksort java implementation".replace(' ', '+')
ids = get_question_ids(search_term + " site:stackoverflow.com")
searchurl = "https://api.stackexchange.com/2.2/questions/"+ids+"/answers?order=desc&sort=activity&site=stackoverflow&filter=!bJDus)chijK43X"
obj = loadJson(searchurl)

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
    # bias towards answers more towards the end
    count = 1
    for link in soup.find_all("code"):
        code = link.contents[0]
        length = len(code)
        count += 0.1
        if length * count > longest:
            longest = length
            best = code
    print(best)
