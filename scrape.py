import weasyprint
import requests
from urllib.parse import urljoin
import os

def convert_url_to_pdf(url, output_filename):
    """Convert a web page to PDF"""
    try:
        # Fetch the HTML content
        response = requests.get(url)
        response.raise_for_status()
        
        # Convert to PDF
        html = weasyprint.HTML(string=response.text, base_url=url)
        html.write_pdf(f"uploads/{output_filename}")
        print(f"✅ Saved: {output_filename}")
        
    except Exception as e:
        print(f"❌ Error converting {url}: {e}")

def convert_adnoc_pages():
    """Convert key ADNOC pages to PDF"""
    
    # Correct ADNOC pages based on actual website structure
    pages = {
        "adnoc_homepage.pdf": "https://www.adnoc.ae/en",
        "adnoc_who_we_are.pdf": "https://www.adnoc.ae/en/our-story/who-we-are", 
        "adnoc_sustainability_strategy.pdf": "https://www.adnoc.ae/en/2030-sustainability-strategy",
        "adnoc_sustainability_report.pdf": "https://www.adnoc.ae/en/sustainability-report",
        "adnoc_news.pdf": "https://www.adnoc.ae/en/news-and-media",
        "adnoc_onshore.pdf": "https://www.adnoc.ae/en/ADNOC-Onshore/About-Us/Who-We-Are",
        "adnoc_offshore.pdf": "https://www.adnoc.ae/en/Adnoc-Offshore/About-Us/Who-We-Are",
        "adnoc_refining.pdf": "https://www.adnoc.ae/adnoc-refining/about-us/who-we-are"
    }
    
    # Create uploads directory
    os.makedirs("uploads", exist_ok=True)
    
    print("🚀 Converting ADNOC pages to PDF...")
    for filename, url in pages.items():
        convert_url_to_pdf(url, filename)
    
    print(f"\n✅ Converted {len(pages)} pages to PDF in uploads/ directory")

if __name__ == "__main__":
    # Install: pip install weasyprint
    convert_adnoc_pages()