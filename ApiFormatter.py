import json
import requests
import sys
import getopt
from urllib.parse import urlparse

URL = "https://hacker-news.firebaseio.com/v0/"


# make the api request
def get_url(url):
    response = requests.get(url)
    content = response.content.decode("utf8")
    return content

# formate the request response into a python object


def get_json_from_url(url):
    content = get_url(url)
    js = json.loads(content)
    return js

# api to get the list of ids for the top news on hacker news


def get_topnews_id():
    url = URL+"topstories.json"
    js = get_json_from_url(url)
    return js

# get the single post details


def get_post_details(id):
    url = URL+"item/"+str(id)+".json"
    js = get_json_from_url(url)
    return js


def main(argv):
    amount = 100
    new_ids = get_topnews_id()
    results = []

# check the flag and if is correct
    try:
        opts, args = getopt.getopt(argv, "posts", "posts=")
    except getopt.GetoptError:
        print("Error in the flags")
        sys.exit(2)
    for opt, arg in opts:
        if opt == '--posts':
            if(not str.isdigit(arg)):
                print("Error in the flags")
                sys.exit(2)
            amount = int(arg)
            if (amount > 100):
                print("Error in the flags")
                sys.exit(2)
    new_ids = new_ids[0:amount]
# For each id in the top news get the details and it push them into a list after checking that data is as expected
    for index, new in enumerate(new_ids, start=1):
        newDet = get_post_details(new)
        if("score" not in newDet or not isinstance(newDet["score"], int)):
            newDet["score"] = 0
        else:
            if(newDet["score"] < 0):
                newDet["score"] = 0
        if("descendants" not in newDet or not isinstance(newDet["descendants"], int)):
            newDet["descendants"] = 0
        else:
            if(newDet["descendants"] < 0):
                newDet["descendants"] = 0
        if("title" not in newDet or not isinstance(newDet["title"], str)):
            newDet["title"] = "N/A"
        else:
            if(len(newDet["title"]) > 256):
                newDet["title"] = "N/A"
        if("author" not in newDet or not isinstance(newDet["author"], str)):
            newDet["author"] = "N/A"
        else:
            if(len(newDet["author"]) > 256):
                newDet["author"] = "N/A"
        if("url" not in newDet or not isinstance(newDet["url"], str)):
            newDet["url"] = "N/A"
        else:
            url = urlparse(newDet["url"])
            if(not url.scheme or not url.netloc):
                newDet["url"] = "N/A"
        el = {
            "title": newDet["title"],
            "uri": newDet["url"],
            "author": newDet["by"],
            "points": newDet["score"],
            "comments": newDet["descendants"],
            "rank": index
        }
        results.append(el)
# Return the object in a readable way
    print(json.dumps(results, indent=4))


if __name__ == "__main__":
    main(sys.argv[1:])
