import streamlit as st
import os
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

st.set_page_config(page_title="Monthly Maintenance Record", page_icon="🚛", layout="centered")

st.title("🚛 Monthly Maintenance Record")
st.write("Please fill in the details below to instantly generate your maintenance report as a PDF.")

# Session State başlatma (Bilgileri hafızada tutmak için)
if "saved_owner" not in st.session_state:
    st.session_state["saved_owner"] = ""
if "saved_address" not in st.session_state:
    st.session_state["saved_address"] = ""
if "saved_make" not in st.session_state:
    st.session_state["saved_make"] = ""
if "saved_year" not in st.session_state:
    st.session_state["saved_year"] = ""
if "saved_vin" not in st.session_state:
    st.session_state["saved_vin"] = ""
if "saved_driver" not in st.session_state:
    st.session_state["saved_driver"] = ""

with st.form("maintenance_form"):
    st.subheader("1. Company & Vehicle Details (Remembered)")
    c1, c2 = st.columns(2)
    with c1:
        owner = st.text_input("Owner", value=st.session_state["saved_owner"], placeholder="Enter Owner / Company Name")
        address = st.text_input("Address", value=st.session_state["saved_address"], placeholder="Enter Address (Street, City, State, Zip)")
        make = st.text_input("Make", value=st.session_state["saved_make"], placeholder="Enter Vehicle Make (e.g., Freightliner)")
    with c2:
        year = st.text_input("Year", value=st.session_state["saved_year"], placeholder="Enter Vehicle Year (e.g., 2013)")
        vin = st.text_input("VIN", value=st.session_state["saved_vin"], placeholder="Enter VIN Number")
        driver = st.text_input("Driver", value=st.session_state["saved_driver"], placeholder="Enter Driver Name / ID")
    
    st.subheader("2. Month & Year Selection")
    col1, col2 = st.columns(2)
    with col1:
        month = st.text_input("Month (e.g., November)", value="November")
    with col2:
        year_val = st.text_input("Year (e.g., 2026)", value="2026")
     
    st.subheader("3. 4-Week Maintenance and Repair Log")
     
    records = []
    for i in range(1, 5):
        st.markdown(f"**Week {i}**")
        w_col1, w_col2, w_col3 = st.columns(3)
        with w_col1:
            d_val = st.text_input(f"Date {i}", key=f"date_{i}", placeholder="e.g., 9.1.2026, 9/1/25")
        with w_col2:
            m_val = st.text_input(f"Mileage {i}", key=f"mil_{i}", placeholder="e.g., 851000")
        with w_col3:
            desc_val = st.text_input(f"Description {i}", key=f"desc_{i}", placeholder="e.g., oil change")
        records.append((d_val, m_val, desc_val))

    st.subheader("4. Signature & Footer Details")
    sig_col1, sig_col2 = st.columns(2)
    with sig_col1:
        signature_name = st.text_input("Signature Name (Full Name)", value=driver)
    with sig_col2:
        current_system_date = datetime.now().strftime("%m.%d.%Y")
        bottom_date = st.text_input("Form Date (Auto-filled)", value=current_system_date)

    submitted = st.form_submit_button("Generate & Download PDF Report")

if submitted:
    # Bilgileri sonraki ay için hafızaya kaydet
    st.session_state["saved_owner"] = owner
    st.session_state["saved_address"] = address
    st.session_state["saved_make"] = make
    st.session_state["saved_year"] = year
    st.session_state["saved_vin"] = vin
    st.session_state["saved_driver"] = driver

    output_pdf_path = f"{month}_{year_val}_{driver.replace(' ', '_')}_Maintenance_Report.pdf"
     
    c = canvas.Canvas(output_pdf_path, pagesize=letter)
     
    # Header Titles
    c.setFont("Helvetica-Bold", 12)
    c.drawString(40, 750, "MONTHLY MAINTENANCE RECORD")
     
    c.setFont("Helvetica-Bold", 10)
    c.drawString(410, 750, "MONTH")
    c.setLineWidth(1)
    c.line(455, 748, 525, 748)
    c.drawString(470, 752, month)
     
    c.drawString(535, 750, "YEAR")
    c.line(565, 748, 605, 748)
    c.drawString(572, 752, year_val)

    # Dynamic Company & Vehicle Info Fields (Owner, Make, VIN)
    c.setFont("Helvetica-Bold", 9)
    c.drawString(40, 715, "OWNER")
    c.line(110, 713, 290, 713)
    if owner:
        c.drawString(120, 717, owner)
     
    c.drawString(330, 715, "MAKE")
    c.line(390, 713, 470, 713)
    if make:
        c.drawString(400, 717, make)
     
    if vin:
        c.setFont("Helvetica", 8)
        c.drawString(485, 717, vin)

    # Address & Year Info Fields
    c.drawString(40, 690, "ADDRESS")
    c.line(110, 688, 290, 688)
    if address:
        c.drawString(120, 692, address)
     
    c.drawString(330, 690, "YEAR")
    c.line(390, 688, 470, 688)
    if year:
        c.drawString(410, 692, year)

    c.line(110, 665, 290, 665)
    
    # Driver Alanı
    c.drawString(330, 665, "DRIVER")
    c.line(390, 663, 470, 663)
    if driver:
        c.drawString(410, 667, driver)

    c.drawString(40, 635, "Annual Inspection Due")
    c.line(145, 633, 220, 633)

    # Table Frame
    c.rect(38, 360, 555, 240)
    c.line(135, 360, 135, 600)  
    c.line(235, 360, 235, 600)  
    c.line(38, 560, 593, 560)

    c.setFont("Helvetica-Bold", 9)
    c.drawString(65, 575, "DATE")
    c.drawString(155, 575, "MILEAGE")
    c.drawString(355, 575, "MAINTENANCE / REPAIRS - DESCRIBE BELOW")

    row_y = 560
    for _ in range(7):
        row_y -= 28
        c.line(38, row_y, 593, row_y)

    # Table Records (Filled up to 7 rows)
    full_records = list(records)
    while len(full_records) < 7:
        full_records.append(("", "", ""))

    c.setFont("Helvetica", 9)
    start_y = 540
    row_height = 28
     
    for idx, (d_val, m_val, des_val) in enumerate(full_records):
        current_y = start_y - (idx * row_height)
        if d_val:
            c.drawString(43, current_y, d_val)
        if m_val:
            c.drawString(145, current_y, m_val)
        if des_val:
            c.drawString(245, current_y, des_val)

    # Footer Notes & Signatures
    c.setFont("Helvetica", 8)
    c.drawString(40, 335, "Please describe all maintenance / repairs performed on this vehicle for the month.")
     
    c.setFont("Helvetica", 7)
    c.drawString(40, 290, "This document must be completed once each month and submitted to the Safety Department by the 10th day")
    c.drawString(40, 280, "of the following month. Repairs and maintenance listed on this form are subject to verification by a qualified")
    c.drawString(40, 270, "representative of George Hildebrandt, Inc.")

    # Owner's Signature Section
    c.setFont("Helvetica-Bold", 9)
    c.drawString(40, 215, "Owner's Signature")
    c.line(40, 205, 220, 205)
     
    if signature_name:
        c.setFont("Helvetica", 9)
        c.drawString(140, 215, signature_name)

    c.setFont("Helvetica", 7)
    c.drawString(40, 180, "File: safety/monthly maintenance reports 1/2010")

    # Right-side Date Field & Line
    c.setFont("Helvetica-Bold", 9)
    c.line(320, 205, 420, 205)
     
    if bottom_date:
        c.setFont("Helvetica", 9)
        c.drawString(340, 215, bottom_date)
         
    c.drawString(320, 190, "Date")

    c.save()
     
    st.success("Report successfully generated!")
    with open(output_pdf_path, "rb") as pdf_file:
        st.download_button(
            label="📄 Download PDF Report",
            data=pdf_file,
            file_name=output_pdf_path,
            mime="application/pdf"
        )