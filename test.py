from scra import create_scra

scrap = create_scra()
scrap.verify = False
print(scrap.cookies.get_dict())
upUrl = "https://ieics.kephis.org/kephis-api/api/validateuser"


uData = {"region_id":"21","office_location_id":"1153","users_id":267845151}

resp = scrap.get(upUrl)

print(resp.text)

