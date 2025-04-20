import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from tqdm import tqdm

def crawl_website(base_url, start_path, output_file="docs.txt"):
    """
    Crawl a website and save all links to a file
    
    Args:
        base_url (str): Base URL of the website
        start_path (str): Starting path for crawling
        output_file (str, optional): Output filename, defaults to "docs.txt"
    
    Returns:
        list: List of all crawled URLs
    """
    visited = set()
    collected = []

    def get_links_from_page(url):
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            links = set()
            for a_tag in soup.find_all('a', href=True):
                href = a_tag['href']
                if href.startswith(start_path):
                    full_url = urljoin(base_url, href)
                    links.add(full_url)
            return links
        except Exception as e:
            print(f"⚠️ Error fetching {url}: {e}")
            return set()

    # Start crawling from the homepage
    to_visit = get_links_from_page(base_url + start_path)

    print(f"🔗 Found {len(to_visit)} page links, starting to crawl content...")

    for url in tqdm(sorted(to_visit)):
        if url not in visited:
            visited.add(url)

    # Save to text file
    with open(output_file, "w", encoding="utf-8") as f:
        for url in visited:
            f.write(url)
            f.write("\n")

    print(f"✅ Crawling completed, saved to {output_file}")
    return list(visited)

def main():
    # Default parameters
    BASE_URL = "https://python.langchain.com"
    START_PATH = "/docs/"
    
    crawl_website(BASE_URL, START_PATH)

if __name__ == "__main__":
    main()
