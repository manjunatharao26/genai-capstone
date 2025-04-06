import requests
from bs4 import BeautifulSoup

def get_pega_mission_steps(base_url):
    response = requests.get(base_url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Extract step URLs
    step_links = []
    for link in soup.find_all('a', href=True):
        href = link['href']
        if "/module/" in href and href.startswith("/module/"):
            full_url = "https://academy.pega.com" + href
            if full_url not in step_links:
                step_links.append(full_url)

    # Get content from each step
    step_contents = []
    for url in step_links:
        step_response = requests.get(url)
        step_soup = BeautifulSoup(step_response.content, 'html.parser')
        step_text = step_soup.get_text(separator="\n")
        step_contents.append({
            "url": url,
            "text": step_text.strip()
        })

    return step_contents
