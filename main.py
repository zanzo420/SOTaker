import requests, json, bs4

def loadJson(url):
    res = requests.get(url)
    js = res.text
    obj = json.loads(js)
    return obj


# TODO user input
search_term = "async java".replace(' ', '+')
searchurl = "https://api.stackexchange.com/2.2/search/advanced?order=desc&sort=activity&q=" + search_term + \
            "&answers=1&site=stackoverflow&filter=!mVN)3JfAau"
obj = loadJson(searchurl)
answer_id = 0
question_title = ""
for i in range(len(obj["items"])):
    if "accepted_answer_id" in obj["items"][i]:
        answer_id = obj["items"][i]['accepted_answer_id']
        question_title = obj["items"][i]["title"]

print(answer_id)
print("//" + question_title)
answer_url = "https://api.stackexchange.com/2.2/answers/" + str(answer_id) + \
            "?order=desc&sort=activity&site=stackoverflow&filter=!9YdnSMKKT"
obj = loadJson(answer_url)
answer_body = obj["items"][0]["body"]
soup = bs4.BeautifulSoup(answer_body, "html.parser")
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
