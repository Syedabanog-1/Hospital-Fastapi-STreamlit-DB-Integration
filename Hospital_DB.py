import streamlit as st
import requests
import pandas as pd
from fpdf import FPDF
from io import BytesIO
import tempfile

# === Sidebar Configuration (Moved to Top) ===
st.sidebar.header("🔧 Settings")
default_url = "http://localhost:8000"
BASE_URL = st.sidebar.text_input("FastAPI Base URL", default_url)

# === Login Setup ===
def login():
    st.title("🔐 Admin Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        try:
            res = requests.post(f"{BASE_URL}/auth/login", json={"username": username, "password": password})
            if res.status_code == 200:
                st.session_state["logged_in"] = True
                st.rerun()  # ✅ UPDATED
            else:
                st.error("Invalid credentials")
        except Exception as e:
            st.error(f"Login failed: {e}")

def logout():
    if st.sidebar.button("🚪 Logout"):
        st.session_state["logged_in"] = False
        st.rerun()  # ✅ UPDATED

# === Check Login ===
if not st.session_state.get("logged_in", False):
    login()
    st.stop()
else:
    logout()

# === Health Check ===
def check_api_health():
    try:
        res = requests.get(f"{BASE_URL}/doctors/")
        return res.status_code in [200, 404] or isinstance(res.json(), list)
    except Exception:
        return False

if not check_api_health():
    st.error("❌ Could not connect to FastAPI backend. Check the BASE URL.")
    st.stop()
else:
    st.success("✅ FastAPI backend is running.")

st.title("🏥 Hospital Record Dashboard")
menu = st.sidebar.selectbox("Select Option", ["Manage Doctors", "Manage Patients"])

# === Helper Functions ===
def show_message(response):
    try:
        data = response.json()
    except Exception:
        st.error(f"Unexpected Error: {response.text}")
        return
    if response.status_code in (200, 201):
        st.success(data.get("message", "Success"))
    else:
        st.error(f"Error {response.status_code}: {data.get('detail', response.text)}")

def export_to_csv(data, filename):
    df = pd.DataFrame(data)
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button("Download CSV", data=csv, file_name=filename, mime='text/csv')

def export_to_pdf(data, title):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt=title, ln=True, align='C')
    for item in data:
        for key, value in item.items():
            pdf.cell(200, 10, txt=f"{key.capitalize()}: {value}", ln=True)
        pdf.cell(200, 5, txt="", ln=True)
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
        pdf.output(tmp_file.name)
        with open(tmp_file.name, "rb") as f:
            st.download_button("Download PDF", data=f.read(), file_name=f"{title}.pdf", mime="application/pdf")

# === Doctor Management ===
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
                search_name = st.text_input("Search by Name").lower()
                search_specialty = st.text_input("Search by Specialty").lower()
                filtered = [doc for doc in doctors if search_name in doc["name"].lower() and search_specialty in doc["specialty"].lower()]
                st.table(filtered if filtered else doctors)
                export_to_csv(filtered if filtered else doctors, "doctors.csv")
                export_to_pdf(filtered if filtered else doctors, "Doctors Report")
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
                if name: update_data["name"] = name
                if specialty: update_data["specialty"] = specialty
                res = requests.put(f"{BASE_URL}/doctors/{id}", json=update_data)
                show_message(res)

    elif action == "Delete":
        id = st.number_input("Doctor ID to Delete", min_value=1, key="delete_doctor_id")
        if st.button("Delete Doctor"):
            res = requests.delete(f"{BASE_URL}/doctors/{id}")
            show_message(res)

# === Patient Management ===
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
                search_name = st.text_input("Search by Name").lower()
                search_disease = st.text_input("Search by Disease").lower()
                filtered = [pat for pat in patients if search_name in pat["name"].lower() and search_disease in pat["disease"].lower()]
                st.table(filtered if filtered else patients)
                export_to_csv(filtered if filtered else patients, "patients.csv")
                export_to_pdf(filtered if filtered else patients, "Patients Report")
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
                if name: update_data["name"] = name
                if disease: update_data["disease"] = disease
                res = requests.put(f"{BASE_URL}/patients/{id}", json=update_data)
                show_message(res)

    elif action == "Delete":
        id = st.number_input("Patient ID to Delete", min_value=1, key="delete_patient_id")
        if st.button("Delete Patient"):
            res = requests.delete(f"{BASE_URL}/patients/{id}")
            show_message(res)
