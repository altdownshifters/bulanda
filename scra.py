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
    resp = scraper.post(url_sign, json=payl)
    if resp.status_code == 200:
        scraper.headers.update({"Authorization": f"Bearer {resp.json()['accessToken']}"})
        return scraper
    else:
        raise Exception(f"Failed to sign in: {resp.status_code} - {resp.text}")

if __name__ == "__main__":
    print(create_scra())