import streamlit as st
from helpers.scra import create_scra, get_staff_profile_id, get_office_locations_ids




st.set_page_config(page_title="Bulanda", page_icon="😋")

def set_location_page():
    put_location_url = "https://ieics.kephis.org/kephis-api/staffProfile/staffProfile"
    st.title("Give Location")
    st.write("Enter the user details")

    with st.form("put location"):
        office_locations = get_office_locations_ids()
        selected_location = st.selectbox("Office location", options=list(office_locations.keys()))
        users_id = st.text_input("User ID", value="263358")
        submitted = st.form_submit_button("Set Location", type="primary")

    if submitted:
        region = office_locations[selected_location]['region_id']
        office = office_locations[selected_location]['office_id']
        user = users_id.strip()

        if not region or not office or not user:
            st.error("All fields are required.")
            return

        payload = {
            "region_id": region,
            "office_location_id": office,
            "users_id": user,
        }

        with st.spinner("Sending user details..."):
            try:
                scraper = create_scra()
                response = scraper.post(put_location_url, json=payload)
                response.raise_for_status()
            except Exception as exc:
                try:
                    resp_data = response.json()
                    st.error(resp_data.get("data", f"Error: {exc}"))
                except Exception:
                    st.error(f"Request failed: {exc}")
            else:
                data = response.json()
                st.success(data.get("data", "User validated successfully"))
                st.json(data)


def update_location_page():
    office_locations = get_office_locations_ids()
    location_update_url = "https://ieics.kephis.org/kephis-api/staffProfile/updateStaffProfile"
    st.title("Update Location")
    st.write("Enter the user details")

    with st.form("put location"):
        selected_location = st.selectbox("Office location", options=list(office_locations.keys()))
        
        users_id = st.text_input("User ID", value="263358")
        submitted = st.form_submit_button("Update Location", type="primary")

    if submitted:
        region = office_locations[selected_location]['region_id']
        office = office_locations[selected_location]['office_id']
        user = users_id.strip()

        if not region or not office or not user:
            st.error("All fields are required.")
            return

        payload = {
            "region_id": region,
            "office_location_id": office,
            "users_id": user,
            "active":True,
            "staffProfile_id":get_staff_profile_id(user)
        }

        with st.spinner("Sending user details..."):
            try:
                scraper = create_scra()
                response = scraper.post(location_update_url, json=payload)
                response.raise_for_status()
            except Exception as exc:
                try:
                    resp_data = response.json()
                    st.error(resp_data.get("data", f"Error: {exc}"))
                except Exception:
                    st.error(f"Request failed: {exc}")
            else:
                data = response.json()
                st.success(data.get("officeLocation", "").get("name", "User set successfully"))
                st.json(data)


PAGES = {
    "Set Location": set_location_page,
    "Update Location": update_location_page,
}

page_name = st.sidebar.radio("Menu", options=list(PAGES))
PAGES[page_name]()
