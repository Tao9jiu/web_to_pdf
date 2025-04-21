from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse, urlunparse
import time

def crawl_website(base_url, start_path, output_file="docs.txt", skip_patterns=None):
    """
    Crawl a website using depth-first search and save all links to a file
    
    Args:
        base_url (str): Base URL of the website
        start_path (str): Starting path for crawling
        output_file (str, optional): Output filename, defaults to "docs.txt"
        skip_patterns (list, optional): List of patterns to skip in URLs
    """
    # Initialize sets to track processed URLs
    processed = set()  # URLs that have been processed
    all_links = set()  # All valid documentation links found
    
    # Normalize start_path
    if not start_path.startswith('/'):
        start_path = '/' + start_path
    if not start_path.endswith('/'):
        start_path = start_path + '/'
    
    # Construct the starting URL
    start_url = urljoin(base_url, start_path)
    print(f"\n🌐 Starting crawl from: {start_url}")
    
    def normalize_url(url):
        """Normalize URL by removing fragment and ensuring path ends with /"""
        parsed = urlparse(url)
        # Remove fragment
        parsed = parsed._replace(fragment='')
        # Ensure path ends with /
        path = parsed.path
        if not path.endswith('/'):
            path = path + '/'
        parsed = parsed._replace(path=path)
        return urlunparse(parsed)
    
    def should_skip_url(url):
        """Check if URL should be skipped based on patterns"""
        if skip_patterns:
            for pattern in skip_patterns:
                if pattern in url:
                    print(f"⏩ Skipping URL with pattern '{pattern}': {url}")
                    return True
        return False
    
    def is_valid_subpage(url):
        """Check if URL is a valid subpage under the base path"""
        parsed = urlparse(url)
        path = parsed.path
        
        # Check if URL is under the base path
        if not path.startswith(start_path):
            return False
            
        # Check if it's a documentation page (not a resource file)
        if any(ext in path.lower() for ext in ['.jpg', '.png', '.gif', '.css', '.js']):
            return False
            
        return True
    
    def get_links_from_page(page, url):
        """Extract all links from a page"""
        try:
            print(f"\n📄 Processing page: {url}")
            # Navigate to the page
            page.goto(url, wait_until='networkidle', timeout=30000)
            page.wait_for_load_state('networkidle', timeout=30000)
            time.sleep(2)  # Wait for dynamic content
            
            # Get page content
            content = page.content()
            soup = BeautifulSoup(content, 'html.parser')
            
            links = set()
            for a_tag in soup.find_all('a', href=True):
                href = a_tag['href']
                
                # Skip empty or anchor links
                if not href or href.startswith('#'):
                    continue
                
                # Convert relative URLs to absolute
                full_url = urljoin(base_url, href)
                
                # Skip if not from the same domain
                if urlparse(full_url).netloc != urlparse(base_url).netloc:
                    continue
                
                # Normalize URL
                normalized_url = normalize_url(full_url)
                
                # Skip if already processed or should be skipped
                if normalized_url in processed or should_skip_url(normalized_url):
                    continue
                
                # Add to links if it's a valid subpage
                if is_valid_subpage(normalized_url):
                    links.add(normalized_url)
                    print(f"✅ Found subpage: {normalized_url}")
            
            return links
        except Exception as e:
            print(f"⚠️ Error processing {url}: {e}")
            return set()
    
    def dfs_crawl(page, url):
        """Depth-first search crawl starting from a URL"""
        if url in processed:
            return
            
        # Mark as processed
        processed.add(url)
        all_links.add(url)
        
        # Get links from current page
        links = get_links_from_page(page, url)
        
        # Recursively process each link
        for link in links:
            if link not in processed:
                dfs_crawl(page, link)
    
    # Start crawling
    with sync_playwright() as p:
        print("\n🚀 Launching browser...")
        browser = p.chromium.launch(
            headless=True,
            args=['--disable-gpu', '--no-sandbox', '--disable-dev-shm-usage']
        )
        context = browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        )
        page = context.new_page()
        
        try:
            # Start DFS from the initial URL
            dfs_crawl(page, start_url)
        finally:
            browser.close()
            print("\n🔒 Browser closed")
    
    # Save results
    print(f"\n💾 Saving results to {output_file}...")
    with open(output_file, "w", encoding="utf-8") as f:
        for url in sorted(all_links):
            # Skip URLs containing '/?q='
            if '/?q=' in url:
                continue
            f.write(url)
            f.write("\n")
    
    print("\n✅ Crawling completed:")
    print(f"  - Total pages processed: {len(processed)}")
    print(f"  - Unique pages found: {len(all_links)}")
    print(f"  - Results saved to: {output_file}")

def main():
    # Default parameters
    BASE_URL = "https://langchain-ai.github.io"
    START_PATH = "/langgraph/"
    SKIP_PATTERNS = ["#__codelineno"]  # Default skip patterns
    
    crawl_website(BASE_URL, START_PATH, skip_patterns=SKIP_PATTERNS)

if __name__ == "__main__":
    main()
