import requests
import re
from bs4 import BeautifulSoup

all_frnds = []
cookie = {'cookie': 'ps_l=1;datr=UGbcZuD5dPZ4rXRgsa7V-ur9;fr=1MtIg67GOvdODnLUl.AWW-N4ni345mnnWO6FevYMMCoJQ.Bm7X9_..AAA.0.0.Bm7YC8.AWXb-fdKxIc;vpd=v1%3B800x360x4;xs=30%3AtLwOgS1zwe4MPg%3A2%3A1725720167%3A-1%3A5124%3A%3AAcVpl_KlIVdzIJfCyngroihBcoO2NK4jpRQOZbRHP01Q;fbl_st=100632696%3BT%3A28780673;locale=en_GB;c_user=100090240011166;presence=C%7B%22lm3%22%3A%22sc.8122780797761457%22%2C%22t3%22%3A%5B%7B%22o%22%3A0%2C%22i%22%3A%22sc.7991385284264373%22%7D%2C%7B%22o%22%3A0%2C%22i%22%3A%22sc.7648576715208256%22%7D%2C%7B%22o%22%3A0%2C%22i%22%3A%22sc.7731547596880538%22%7D%5D%2C%22utc3%22%3A1726842587726%2C%22v%22%3A1%7D;dpr=1.5;m_page_voice=100090240011166;ps_n=1;sb=UGbcZkQEtIo6RnHJSuYVMo1V;wd=1280x594;wl_cbv=v2%3Bclient_version%3A2625%3Btimestamp%3A1726840433'}

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

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:126.0) Gecko/20100101 Firefox/126.1',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/png,image/svg+xml,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Referer': 'https://mbasic.facebook.com/xspoilt',
    'Alt-Used': 'mbasic.facebook.com',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-User': '?1',
    'Priority': 'u=0, i',
}

url = 'https://mbasic.facebook.com/xspoilt'
resp = requests.get(url, headers=headers, cookies=cookie).text
soup = BeautifulSoup(resp, 'html.parser')

# Find the link to the friends list
a_tag = soup.find('a', class_='cr', string='Friends')
frnd_list = "https://mbasic.facebook.com" + a_tag['href'] if a_tag else None

# Get the number of friends
resp2 = requests.get(frnd_list, headers=headers, cookies=cookie).text
frnd_count = int(value(resp2, 'k">Friends (', ')</h3>'))
print(f"[+] Total Friends : {frnd_count}")

# Initialize friend collection and start crawling
total_friends_collected = 0
next_page_url = frnd_list

while total_friends_collected < frnd_count and next_page_url:
    resp2 = requests.get(next_page_url, headers=headers, cookies=cookie).text
    soup2 = BeautifulSoup(resp2, 'html.parser')

    # Extract friends on the current page
    frnds = find_all(resp2, '<a class="ci"', '/a><div')
    for frnd in frnds:
        name = value(frnd, '0">', '<')
        profile = "https://mbasic.facebook.com" + value(frnd, 'href="', '"')
        all_frnds.append((name, profile))
        total_friends_collected += 1
        print(f"Name : {name}")
        print(f"Link : {profile}")
        print("---------------------------------------------------")
        if total_friends_collected >= frnd_count:
            break
    a_tag2 = soup2.find('a', string=soup2.find('span', string='See more friends'))
    next_page_url = "https://mbasic.facebook.com" + a_tag2['href'] if a_tag2 else None

print(f"[+] All {total_friends_collected} friends collected.")
