from bs4 import BeautifulSoup
import urllib.request
import warnings
from bs4 import XMLParsedAsHTMLWarning

# Suppressing the warning from BeautifulSoup
warnings.filterwarnings("ignore", category=XMLParsedAsHTMLWarning)

seed_url = "https://press.un.org/en"
base_url = "https://press.un.org"

urls = [seed_url]
seen = set([seed_url])  # using a set for faster look-up times
opened = []
press_releases = []
maxNumUrl = 1000  # Increase this if you're not getting 10 results
maxPressReleases = 10

print("Starting with url=" + str(urls))

while len(urls) > 0 and len(press_releases) < maxPressReleases and len(opened) < maxNumUrl:
    curr_url = urls.pop(0)
    try:
        req = urllib.request.Request(curr_url, headers={'User-Agent': 'Mozilla/5.0'})
        webpage = urllib.request.urlopen(req).read()
        opened.append(curr_url)
    except Exception as ex:
        print(f"Unable to access {curr_url} due to {ex}")
        continue

    soup = BeautifulSoup(webpage, 'html.parser')

    # Check for the "PRESS RELEASE" tag to identify press release pages
    press_release_tag = soup.find('a', href="/en/press-release", hreflang="en")
    if press_release_tag and "crisis" in soup.text.lower():
        press_releases.append(curr_url)

    for tag in soup.find_all('a', href=True):
        childUrl = tag['href']
        if childUrl.startswith('#'):
            continue
        childUrl = urllib.parse.urljoin(base_url, childUrl)
        if base_url in childUrl and childUrl not in seen:
            urls.append(childUrl)
            seen.add(childUrl)

print(f"Found {len(press_releases)} press releases:")
for pr in press_releases:
    print(pr)