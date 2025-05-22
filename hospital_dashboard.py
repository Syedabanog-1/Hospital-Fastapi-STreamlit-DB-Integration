import streamlit as st
import requests

BASE_URL = "http://localhost:8000"

st.title("🏥 Hospital Record Dashboard")

menu = st.sidebar.selectbox("Select Option", ["Manage Doctors", "Manage Patients"])

def show_message(response):
    if response.status_code in (200, 201):
        st.success(response.json().get("message", "Success"))
    else:
        st.error(f"Error {response.status_code}: {response.text}")

if menu == "Manage Doctors":
    st.header("👨‍⚕️ Doctor Management")
    action = st.selectbox("Choose Action", ["Add", "View", "Update", "Delete"], key="doctor_action")

    if action == "Add":
        id = st.number_input("Doctor ID", min_value=1, key="add_doctor_id")
        name = st.text_input("Name", key="add_doctor_name")
        specialty = st.text_input("Specialty", key="add_doctor_specialty")
        if st.button("Add Doctor"):
            if not name or not specialty:
                st.warning("Please provide both name and specialty.")
            else:
                res = requests.post(f"{BASE_URL}/doctors/", json={"id": id, "name": name, "specialty": specialty})
                show_message(res)

    elif action == "View":
        res = requests.get(f"{BASE_URL}/doctors/")
        if res.status_code == 200:
            doctors = res.json()
            if doctors:
                st.table(doctors)
            else:
                st.info("No doctors found.")
        else:
            st.error(f"Failed to fetch doctors. Status code: {res.status_code}")

    elif action == "Update":
        id = st.number_input("Doctor ID to Update", min_value=1, key="update_doctor_id")
        name = st.text_input("Updated Name", key="update_doctor_name")
        specialty = st.text_input("Updated Specialty", key="update_doctor_specialty")
        if st.button("Update Doctor"):
            if not name and not specialty:
                st.warning("Please provide at least one field to update.")
            else:
                update_data = {}
                if name:
                    update_data["name"] = name
                if specialty:
                    update_data["specialty"] = specialty
                res = requests.put(f"{BASE_URL}/doctors/{id}", json=update_data)
                show_message(res)

    elif action == "Delete":
        id = st.number_input("Doctor ID to Delete", min_value=1, key="delete_doctor_id")
        if st.button("Delete Doctor"):
            res = requests.delete(f"{BASE_URL}/doctors/{id}")
            show_message(res)

elif menu == "Manage Patients":
    st.header("🧑‍🦽 Patient Management")
    action = st.selectbox("Choose Action", ["Add", "View", "Update", "Delete"], key="patient_action")

    if action == "Add":
        id = st.number_input("Patient ID", min_value=1, key="add_patient_id")
        name = st.text_input("Name", key="add_patient_name")
        disease = st.text_input("Disease", key="add_patient_disease")
        if st.button("Add Patient"):
            if not name or not disease:
                st.warning("Please provide both name and disease.")
            else:
                res = requests.post(f"{BASE_URL}/patients/", json={"id": id, "name": name, "disease": disease})
                show_message(res)

    elif action == "View":
        res = requests.get(f"{BASE_URL}/patients/")
        if res.status_code == 200:
            patients = res.json()
            if patients:
                st.table(patients)
            else:
                st.info("No patients found.")
        else:
            st.error(f"Failed to fetch patients. Status code: {res.status_code}")

    elif action == "Update":
        id = st.number_input("Patient ID to Update", min_value=1, key="update_patient_id")
        name = st.text_input("Updated Name", key="update_patient_name")
        disease = st.text_input("Updated Disease", key="update_patient_disease")
        if st.button("Update Patient"):
            if not name and not disease:
                st.warning("Please provide at least one field to update.")
            else:
                update_data = {}
                if name:
                    update_data["name"] = name
                if disease:
                    update_data["disease"] = disease
                res = requests.put(f"{BASE_URL}/patients/{id}", json=update_data)
                show_message(res)

    elif action == "Delete":
        id = st.number_input("Patient ID to Delete", min_value=1, key="delete_patient_id")
        if st.button("Delete Patient"):
            res = requests.delete(f"{BASE_URL}/patients/{id}")
            show_message(res)
