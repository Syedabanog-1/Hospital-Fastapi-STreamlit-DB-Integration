import streamlit as st
import requests

BASE_URL = "http://localhost:8000"  # Update this if deploying to a server

st.title("🏥 Hospital Record Dashboard")

menu = st.sidebar.selectbox("Select Option", ["Manage Doctors", "Manage Patients"])

# === Doctor Section ===
if menu == "Manage Doctors":
    st.header("👨‍⚕️ Doctor Management")

    action = st.selectbox("Choose Action", ["Add", "View", "Update", "Delete"])

    if action == "Add":
        id = st.number_input("Doctor ID", min_value=1)
        name = st.text_input("Name")
        specialty = st.text_input("Specialty")
        if st.button("Add Doctor"):
            res = requests.post(f"{BASE_URL}/doctors/", json={"id": id, "name": name, "specialty": specialty})
            st.success(res.json().get("message"))

    elif action == "View":
        res = requests.get(f"{BASE_URL}/doctors/")
        doctors = res.json()
        st.table(doctors)

    elif action == "Update":
        id = st.number_input("Doctor ID to Update", min_value=1)
        name = st.text_input("Updated Name")
        specialty = st.text_input("Updated Specialty")
        if st.button("Update Doctor"):
            res = requests.put(f"{BASE_URL}/doctors/{id}", json={"id": id, "name": name, "specialty": specialty})
            st.success(res.json().get("message"))

    elif action == "Delete":
        id = st.number_input("Doctor ID to Delete", min_value=1)
        if st.button("Delete Doctor"):
            res = requests.delete(f"{BASE_URL}/doctors/{id}")
            st.success(res.json().get("message"))

# === Patient Section ===
if menu == "Manage Patients":
    st.header("🧑‍🦽 Patient Management")

    action = st.selectbox("Choose Action", ["Add", "View", "Update", "Delete"])

    if action == "Add":
        id = st.number_input("Patient ID", min_value=1)
        name = st.text_input("Name")
        disease = st.text_input("Disease")
        if st.button("Add Patient"):
            res = requests.post(f"{BASE_URL}/patients/", json={"id": id, "name": name, "disease": disease})
            st.success(res.json().get("message"))

    elif action == "View":
        res = requests.get(f"{BASE_URL}/patients/")
        patients = res.json()
        st.table(patients)

    elif action == "Update":
        id = st.number_input("Patient ID to Update", min_value=1)
        name = st.text_input("Updated Name")
        disease = st.text_input("Updated Disease")
        if st.button("Update Patient"):
            res = requests.put(f"{BASE_URL}/patients/{id}", json={"id": id, "name": name, "disease": disease})
            st.success(res.json().get("message"))

    elif action == "Delete":
        id = st.number_input("Patient ID to Delete", min_value=1)
        if st.button("Delete Patient"):
            res = requests.delete(f"{BASE_URL}/patients/{id}")
            st.success(res.json().get("message"))
