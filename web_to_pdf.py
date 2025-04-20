from crawler import crawl_website
from pdf_generator import generate_pdf_from_urls
import argparse

def crawl_and_generate_pdf(base_url, start_path, output_filename='document.pdf'):
    """
    Crawl a website and generate a PDF file
    
    Args:
        base_url (str): Base URL of the website
        start_path (str): Starting path for crawling
        output_filename (str, optional): Output PDF filename, defaults to 'document.pdf'
    
    Returns:
        bool: Whether the entire process was successful
    """
    try:
        # Step 1: Crawl the website
        print("Starting website crawl...")
        urls = crawl_website(base_url, start_path)
        
        if not urls:
            print("⚠️ No URLs found, please check input parameters")
            return False
            
        # Step 2: Generate PDF
        print("\nStarting PDF generation...")
        success = generate_pdf_from_urls(urls, output_filename)
        
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
    parser.add_argument('--base-url', type=str, default="https://python.langchain.com",
                      help='Base URL of the website to crawl')
    parser.add_argument('--start-path', type=str, default="/docs/how_to/installation/",
                      help='Starting path for crawling')
    parser.add_argument('--output', type=str, default="documentation.pdf",
                      help='Output PDF filename')
    
    # Parse arguments
    args = parser.parse_args()
    
    # Run the crawler and PDF generator
    crawl_and_generate_pdf(args.base_url, args.start_path, args.output)

if __name__ == "__main__":
    main() 