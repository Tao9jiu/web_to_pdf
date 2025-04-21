from crawler import crawl_website
from pdf_generator import generate_pdf_from_urls
import argparse

def crawl_and_generate_pdf(base_url, start_path, output_filename, skip_patterns, cookie_accept_button_text):
    """
    Crawl a website and generate a PDF file
    
    Args:
        base_url (str): Base URL of the website
        start_path (str): Starting path for crawling
        output_filename (str, optional): Output PDF filename, defaults to 'document.pdf'
        skip_patterns (list, optional): List of patterns to skip in URLs, defaults to ["#_", "?q="]
        cookie_accept_button_text (str, optional): Text of the cookie accept button, defaults to "Accept"
    
    Returns:
        bool: Whether the entire process was successful
    """
    try:
        # Step 1: Crawl the website
        print(f"Starting website crawl from {base_url}{start_path}...")
        urls = crawl_website(base_url, start_path, skip_patterns=skip_patterns)
        
        if not urls:
            print("⚠️ No URLs found, please check input parameters")
            return False
            
        # Step 2: Generate PDF
        # Read URLs from docs.txt
        print("Reading URLs from docs.txt...")
        with open("docs.txt", "r", encoding="utf-8") as f:
            urls = [line.strip() for line in f if line.strip()]
        print("\nStarting PDF generation...")
        success = generate_pdf_from_urls(urls, output_filename, cookie_accept_button_text)
        
        if success:
            print(f"✅ Process completed! PDF file generated: {output_filename}")
        else:
            print("❌ PDF generation failed")
            
        return success
        
    except Exception as e:
        print(f"❌ Error occurred: {str(e)}")
        return False
def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description='Crawl a website and generate PDF documentation')
    parser.add_argument('--base-url', type=str, default="https://langchain-ai.github.io",
                      help='Base URL of the website to crawl')
    parser.add_argument('--start-path', type=str, default="/langgraph/",
                      help='Starting path for crawling')
    parser.add_argument('--output', type=str, default="documentation.pdf",
                      help='Output PDF filename')
    parser.add_argument('--skip-patterns', type=str, nargs='+', default=["#_", "?q="],
                      help='Patterns to skip in URLs (space-separated)')
    parser.add_argument('--cookie-accept-button-text', type=str, default="Accept",
                      help='Text of the cookie accept button')
    # Parse arguments
    args = parser.parse_args()
    
    # Run the crawler and PDF generator
    crawl_and_generate_pdf(args.base_url, args.start_path, args.output, args.skip_patterns, args.cookie_accept_button_text)

if __name__ == "__main__":
    main() 