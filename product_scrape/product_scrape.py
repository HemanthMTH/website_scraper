import json
import time
import re

from googlesearch import search
from difflib import SequenceMatcher

request = re.compile(r"([^\w ]+)|(\s{2,})")
href = re.compile(r"^((https?://)?(www\.)?([\w.\-_]+)(\.\w+)).*$")


def similarity(content, url):

    return SequenceMatcher(None, content, url).ratio()

def similarity_filter(content, cites, threshold = .6):

    best_url = None
    best_similarity = threshold
        
    for c in cites:

        m = href.match(c)

        if m is None:
            break

        domain = m.group(4)

        content_list = request.sub(" ", content).split()
        if len(content_list) > 1:
            content_list.append("".join(content_list))

        for piece in content_list:
            sim = similarity(piece, domain)

            if sim > best_similarity or domain in piece:

                w3 = m.group(3)
                if w3 is None:
                    w3 = ""

                best_url = f"https://{w3}{m.group(4)}{m.group(5)}"
                best_similarity = sim

    return best_url

def scrap_sites_urls(manufacturer, keyword, index):

    print("Current Index:", index, "Total records:", len(product_details))

    term = str(manufacturer + keyword)
    l = []
    for i in search(term,num=10, stop=10, pause=2):
        l.append(i)
    if len(l) == 0:
        return manufacturer, keyword, None

    site = similarity_filter(manufacturer, l)

    return manufacturer, keyword, site

def get_website(record):
    
    return record["website"]

if __name__ == '__main__':

    f = open("test.json")
    products = json.load(f)

    product_details = set([(r['manufacturer'], r['keyword'])
                        for r in products
                        if r['manufacturer'] is not None])

    print('Started getting site URls..')
    start = time.time()

    webs = [scrap_sites_urls(*j, i) for i, j in enumerate(product_details)] 

    for item in products:
        for manufacturer, keyword, site in webs:
            if manufacturer == item["manufacturer"] and keyword == item["keyword"]:
                item["website"] = site



    with open("websites.txt", "w") as f:
                records = [get_website(r) for r in products if get_website(r) is not None ]
                l = []
                for r in records:
                    if r in l:
                        continue
                    else:
                        l.append(r)
                        f.write("%s\n" % r)


    with open("final.json", "w") as f:
                json.dump(products, f, indent=2)

    end = time.time()

    print("Completed!!")
    print("Time elapsed:", end - start)