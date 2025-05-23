from playwright.sync_api import sync_playwright
from PyPDF2 import PdfMerger
import os

def save_webpage_as_pdf(page, url, output_file, cookie_accept_button_text):
    """Save a single webpage as PDF"""
    max_retries = 3
    retry_count = 0
    
    while retry_count < max_retries:
        try:
            # Visit the page with timeout
            page.goto(url, wait_until='networkidle', timeout=30000)
            
            # Wait for the page to fully load
            page.wait_for_load_state('networkidle', timeout=30000)
            page.wait_for_timeout(2000)  # Additional 2-second wait to ensure dynamic content loads
            
            # Try to find and click any "Accept" buttons (e.g. for cookie notices)
            try:
                # Try different selectors for accept buttons
                accept_selectors = [
                    f"button:has-text('{cookie_accept_button_text}')",
                    f"[role='button']:has-text('{cookie_accept_button_text}')",
                ]
                
                for selector in accept_selectors:
                    try:
                        accept_button = page.locator(selector).first
                        if accept_button and accept_button.is_visible():
                            accept_button.click()
                            print(f"Clicked Accept button using selector: {selector}")
                            page.wait_for_timeout(2000)
                            break
                    except Exception as e:
                        continue
                
            except Exception as e:
                print(f"Error handling Accept button: {str(e)}")
                page.wait_for_timeout(2000)
            
            # PDF settings
            pdf_options = {
                'scale': 1,
                'margin': {
                    'top': '0.4in',
                    'right': '0.4in',
                    'bottom': '0.4in',
                    'left': '0.4in'
                },
                'print_background': True,
                'prefer_css_page_size': True,
                'format': 'A4'
            }
            
            # Save as PDF
            page.pdf(path=output_file, **pdf_options)
            return True
            
        except Exception as e:
            retry_count += 1
            print(f"Attempt {retry_count}/{max_retries} failed for {url}: {str(e)}")
            if retry_count < max_retries:
                print("Retrying...")
                page.wait_for_timeout(5000)  # Wait 5 seconds before retry
            else:
                print(f"Failed to process {url} after {max_retries} attempts")
                return False
    
    return False

def generate_pdf_from_urls(urls, output_filename, cookie_accept_button_text):
    """
    Generate PDF file from a list of URLs
    
    Args:
        urls (list): List of webpage URLs to convert to PDF
        output_filename (str, optional): Output PDF filename, defaults to 'document.pdf'
    
    Returns:
        bool: Whether PDF generation was successful
    """
    # Create temporary directory
    temp_dir = 'temp_pdfs'
    os.makedirs(temp_dir, exist_ok=True)
    
    successful_pdfs = []
    
    # Process webpages using Playwright
    with sync_playwright() as p:
        # Launch browser with higher resolution for better quality
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            device_scale_factor=2
        )
        page = context.new_page()
        
        # Process each URL
        total_urls = len(urls)
        for i, url in enumerate(urls, 1):
            output_file = os.path.join(temp_dir, f'page_{i}.pdf')
            print(f"Processing ({i}/{total_urls}): {url}")
            
            if save_webpage_as_pdf(page, url, output_file, cookie_accept_button_text):
                successful_pdfs.append(output_file)
        
        browser.close()
    
    # Merge PDF files
    if successful_pdfs:
        print("\nMerging PDF files...")
        merger = PdfMerger()
        for pdf in successful_pdfs:
            merger.append(pdf)
        
        merger.write(output_filename)
        merger.close()
        print(f"PDF merge completed! Output file: {output_filename}")
    
    # Clean up temporary files
    print("Cleaning up temporary files...")
    for pdf in successful_pdfs:
        try:
            os.remove(pdf)
        except Exception as e:
            print(f"Error deleting temporary file {pdf}: {str(e)}")
    
    try:
        os.rmdir(temp_dir)
    except Exception as e:
        print(f"Error deleting temporary directory: {str(e)}")
    
    return len(successful_pdfs) > 0

def main():
    # Read URL list
    with open('docs.txt', 'r') as f:
        urls = [line.strip() for line in f if line.strip()]
    
    generate_pdf_from_urls(urls, 'document.pdf', 'Accept')

if __name__ == "__main__":
    main()
