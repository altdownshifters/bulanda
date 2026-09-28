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
    """Get token"""
    url_sign = "https://ieics.kephis.org/kephis-api/api/auth/signin"
    payl = {"username":"Gayle75","password":"Matakosana"}
    resp = scraper.post(url_sign, json=payl)
    if resp.status_code == 200:
        scraper.headers.update({"Authorization": f"Bearer {resp.json()['accessToken']}"})
        return scraper
    else:
        raise Exception(f"Failed to sign in: {resp.status_code} - {resp.text}")


def get_staff_profile_id(user_id):
    """
    Get staff profile data by user ID.
    
    params: user_id (str or int)
    return: dict or None
    """
    url = "https://ieics.kephis.org/kephis-api/staffProfile/getStaffProfileByUser"
    params = {
        "userID": user_id
    }
    session = create_scra()  # Replaced non-standard variable name  
    try:
        response = session.get(url, params)
        response.raise_for_status()  # Raises an exception for 4xx/5xx HTTP errors
        data = response.json()
        if data and isinstance(data, list):
            staff_profile_id = data[0].get('staffProfile_id')
        else:
            staff_profile_id = None
        return staff_profile_id
    except Exception as e:
        print(f"Error: {e}")
        return None


def get_office_locations_ids():
    """Office locations with their ids and region ids"""
    
    url = "https://ieics.kephis.org/kephis-api/officeLocation/officeLocationList?pageNo=0&pageSize=10000"
    session = create_scra()
    office_locations = {}
    try:
        response = session.get(url)
        response.raise_for_status()
        dataz = response.json()
        for data in dataz:
            office_locations.update({data.get("name"):{"office_id":data.get("office_location_id"), "region_id": data.get("region").get("regionID")}})
        return office_locations
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    print(get_office_locations_ids())