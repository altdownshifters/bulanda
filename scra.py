import cloudscraper
import ssl
import urllib3
 
#  config initialization
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
ctx = ssl._create_unverified_context()
scraper = cloudscraper.create_scraper(ssl_context=ctx, browser={
            'browser': 'firefox',
            'platform': 'darwin',
            'desktop': True
        })
scraper.verify = False

def create_scra():
    url_sign = "https://ieics.kephis.org/kephis-api/api/auth/signin"
    payl = {"username":"skpl","password":"Matakosana"}
    scraper.post(url_sign, data=payl)
    
    

    return scraper

if __name__ == "__main__":
    scrap = create_scra()
    resp = scrap.get("https://ieics.kephis.org/kephis-api/api/validateuser")

    print(resp.text)