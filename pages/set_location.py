from helpers.scra import create_scra, get_staff_profile_id, get_office_locations_ids




st.set_page_config(page_title="Bulanda", page_icon="😋")

def set_location_page():
    set_location_url = "https://ieics.kephis.org/kephis-api/staffProfile/staffProfile"
    update_location_url = "https://ieics.kephis.org/kephis-api/staffProfile/updateStaffProfile"

    st.title("Set or Update Location")
    st.write("Enter the user details below.")

    office_locations = get_office_locations_ids()

    with st.form("location_form"):
        selected_location = st.selectbox("Office location", options=list(office_locations.keys()))
        users_id = st.text_input("User ID", value="263358")
        submitted = st.form_submit_button("Submit Location", type="primary")

    if not submitted:
        return

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

    scraper = create_scra()

    with st.spinner("Processing request..."):
        # Step 1: Attempt to set location
        response = scraper.post(set_location_url, json=payload)
        res_data = response.json() if response.status_code == 200 else {}

        # Check if set location failed or signaled that an update is required
        needs_update = (
            response.status_code != 200 
            or "user profile already set" in str(res_data.get("message", "")).lower()
            or "user profile already set" in str(res_data.get("data", "")).lower()
        )

        # Step 2: Fallback to update location if condition triggers
        if needs_update:
            payload.update({
                "active": True,
                "staffProfile_id": get_staff_profile_id(user)
            })
            response = scraper.post(update_location_url, json=payload)

        # Step 3: Handle Final Response
        try:
            response.raise_for_status()
            data = response.json()
            
            # Extract success message dynamically depending on API structure
            success_msg = (
                data.get("officeLocation", {}).get("name") 
                if isinstance(data.get("officeLocation"), dict) 
                else data.get("data", "Location set/updated successfully.")
            )
            
            st.success(f"Success: {success_msg}")
            st.json(data)
            
        except Exception as exc:
            try:
                err_data = response.json()
                st.error(err_data.get("data", err_data.get("message", f"Error: {exc}")))
            except Exception:
                st.error(f"Request failed with status {response.status_code}: {exc}")


def block_user():
    st.title("Block User")
    st.write("User block")

    with st.form("block_form"):
        users_id = st.text_input("User ID", value="263358")
        submitted = st.form_submit_button("Block User", type="primary")


def unblock_user():
    st.title("Unblock User")
    st.write("User unblock")

    with st.form("unblock_form"):
        users_id = st.text_input("User ID", value="263358")
        submitted = st.form_submit_button("Unblock User", type="primary")

PAGES = {
    "Set Location": set_location_page,
    "Block User": block_user,
    "Unblock User": unblock_user
}

page_name = st.sidebar.radio("Menu", options=list(PAGES))
PAGES[page_name]()
