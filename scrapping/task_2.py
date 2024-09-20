import requests
import re

posts = []
url_pattern = re.compile(r'https://trickbd.com/.*?/(\d{7})$')


def context(html):
    pattern = r'<div class="post_content">(.*?)</div>'
    content = re.search(pattern, html, re.DOTALL)
    if content:
        return content.group(1).strip()
    else:
        return None
def value(text, frst, last):
    frst = re.escape(frst)
    last = re.escape(last)
    pattern = fr'{frst}(.*?){last}'
    match = re.search(pattern, text)
    if match:
        return match.group(1)
    return None

def find_all(text, frst, last):
    frst = re.escape(frst)
    last = re.escape(last)
    pattern = fr'{frst}(.*?){last}'
    matches = re.findall(pattern, text)
    return matches

keywords = input("Enter Word (separated by comma): ").replace(" ", "")
keywords = keywords.split(",")
count = int(input("Enter Count For Each Word: "))

print(f"[+] Extracting Categories")
resp = requests.get("https://trickbd.com/categories").text
links = find_all(resp, '<a href="', '">')

for keyword in keywords:
    print(f"[+] Extracting Posts for '{keyword}'...")
    i = 0
    for link in links:
        if keyword in link:
            while i < count:
                resp1 = requests.get(link).text
                post_links = find_all(resp1, '<a href="', '">')
                for post in list(set(post_links)):
                    if url_pattern.search(post):
                        content = context(requests.get(post).text)
                      #  print(content)
                        filename = f"{keyword}_{i+1}.txt"
                        open(filename, 'a', encoding='utf-8').write(str(content))
                        print(f"Content Saved To : {filename}\nFrom Post : {post}\n------------------")
                        i += 1
                        if i >= count:
                            break
                if i >= count:
                    break
