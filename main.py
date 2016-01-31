import requests, json, bs4

#TODO user input
searchterm = "multiple inheritance java"

searchterm = searchterm.replace(' ', ';')
searchurl = "https://api.stackexchange.com/2.2/search/advanced?order=desc&sort=activity&q=" + searchterm +\
            "&answers=1&site=stackoverflow&filter=!mVN)3JfAau"
res = requests.get(searchurl)
js = res.text
obj = json.loads(js)
answer_id = 0
question_title = ""
for i in range(len(obj["items"])):
    if "accepted_answer_id" in obj["items"][i]:
        answer_id = obj["items"][i]['accepted_answer_id']
        question_title = obj["items"][i]["title"]
        break

print(question_title)
answerurl = "https://api.stackexchange.com/2.2/answers/" + str(answer_id) + \
            "?order=desc&sort=activity&site=stackoverflow&filter=!9YdnSMKKT"
res = requests.get(answerurl)
js = res.text
obj = json.loads(js)
answer_body = obj["items"][0]["body"]
soup = bs4.BeautifulSoup(answer_body, "html.parser")
longest = 0
best = ""
for link in soup.find_all("code"):
    if len(link.contents[0]) > longest:
        longest = len(link.contents[0])
        best = link.contents[0]
print(best)
