import streamlit as st
from scra import create_scra

# CHANGE_LOCATION_URL = "https://ieics.kephis.org/kephis-api/staffProfile/staffProfile"
LOCATION_UPDATE_URL = "https://ieics.kephis.org/kephis-api/staffProfile/updateStaffProfile"

st.set_page_config(page_title="User Validation", page_icon="✓")

def check_location_page():
    st.title("Check Location")
    st.write("Enter the user details")

    with st.form("validate_user"):
        region_id = st.text_input("Region ID", value="21")
        office_location_id = st.text_input("Office location ID", value="1153")
        users_id = st.text_input("User ID", value="263358")
        submitted = st.form_submit_button("Validate user", type="primary")

    if submitted:
        region = region_id.strip()
        office = office_location_id.strip()
        user = users_id.strip()

        if not region or not office or not user:
            st.error("All fields are required.")
            return

        payload = {
            "region_id": region,
            "office_location_id": office,
            "users_id": user,
            # "active": True,
            # "staffProfile_id": 6904
        }
        #{"region_id":"53","office_location_id":"1156","users_id":243868283,"active":true,"staffProfile_id":6904}

        with st.spinner("Sending user details..."):
            try:
                scraper = create_scra()
                response = scraper.post(LOCATION_UPDATE_URL, json=payload)
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


PAGES = {"Check Location": check_location_page}

page_name = st.sidebar.radio("Pages", options=list(PAGES))
PAGES[page_name]()