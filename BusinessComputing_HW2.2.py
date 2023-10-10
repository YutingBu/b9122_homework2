from bs4 import BeautifulSoup
import requests

seed_url_eu = "https://www.europarl.europa.eu/news/en/press-room"
plenary_press_releases = []
desired_num_releases = 10  # Set the desired number of press releases to extract

def extract_eu_parliament_press_releases(seed_url, keyword, num_releases):
    press_releases = []
    response = requests.get(seed_url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Find press releases related to plenary sessions
    for plenary_session in soup.find_all('span', class_='ep_name'):
        if 'Plenary session' in plenary_session.get_text():
            # Get the parent link for the press release
            press_release_link = plenary_session.find_next('a', href=True)
            if press_release_link:
                press_release_url = press_release_link['href']
                press_releases.append(press_release_url)
                if len(press_releases) >= num_releases:
                    break
    
    return press_releases

plenary_press_releases = extract_eu_parliament_press_releases(seed_url_eu, "crisis", desired_num_releases)

# Print the collected press release links
print("Press Release Links:")
for link in plenary_press_releases:
    print(link)

print("Number of press releases containing 'crisis':", len(plenary_press_releases))
