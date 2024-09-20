import requests
import re
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

keyword = input("Enter Keyword to search : ")
resp = requests.get(f"https://www.youtube.com/results?search_query={keyword}").text
videos = find_all(resp, '{"videoRenderer":{', '"longBylineText":')
print(f"Total Videos : {len(videos)}")
print("----------------------")
for video in videos:
    title = value(video, '"title":{"runs":[{"text":"', '"}],"')
    videolink = "https://www.youtube.com/watch?v=" + value(video, '"videoId":"', '","')
    print(f"Title : {title}")
    print(f"Video Link : {videolink}")
    print("-----------------------------")
