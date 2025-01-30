Google Colab Pdf Extractor
1
2
3
4
5
6
7
8
9
10
11
12
13
14
15
16
17
18
19
20
21
22
23
24
25
26
27
28
29
30
31
32
33
34
35
36
37
38
39
40
41
42
43
44
45
46
47
48
49
50
51
52
53
54
55
56
57
58
59
60
61
62
63
64
65
66
67
68
69
70
71
72
73
74
75
76
77
78
79
80
81
82
83
84
85
86
87
88
89
90
91
92
93
94
95
96
97
98
99
100
import streamlit as st
import pdfplumber
import pandas as pd
import re
import numpy as np
import gspread
from google.oauth2 import service_account
from fuzzywuzzy import process, fuzz

# Authenticate Google Sheets
st.title("Student List Extractor")

# Load Google Sheets credentials
credentials = service_account.Credentials.from_service_account_info(st.secrets["gcp_service_account"], scopes=["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"])
gc = gspread.authorize(credentials)

# Permanent Master List (Same as in your original script)
master_list = {
    "Arias Tomas": "5-1",
    "Chokkar Rudransha": "5-1",
    "Choudhary Rayansh": "5-1",
    "Benejam Graterol Gabriela De Dios": "5-1",
    "De la Rosa Tomás": "5-1",
    # (Truncated for brevity, insert the full master list here)
}

# Define valid grades
valid_grades = ["QUINTO", "SEXTO", "SEPTIMO", "OCTAVO", "NOVENO", "DECIMO", "ONCE"]

def normalize_name(name):
    name = name.lower().strip()
    name = re.sub(r'[^a-záéíóúñ ]', '', name)
    return name

def split_name_parts(name):
    return set(normalize_name(name).split())

def extract_students_info(text):
    pattern = r"Pasajero:\s([A-ZÁÉÍÓÚÑ ]+)\sCurso:\s([A-ZÁÉÍÓÚÑ]+)"
    matches = re.findall(pattern, text)
    students_info = [(match[0].strip(), match[1].strip()) for match in matches]
    return students_info

def find_best_match(name, grade):
    pdf_name_parts = split_name_parts(name)
    best_match = None
    highest_score = 0

    for master_name in master_list.keys():
        master_name_parts = split_name_parts(master_name)
        common_parts = pdf_name_parts.intersection(master_name_parts)
        score = len(common_parts) / max(len(pdf_name_parts), len(master_name_parts)) * 100

        fuzzy_score = fuzz.token_sort_ratio(name, master_name)
        final_score = max(score, fuzzy_score)

        if final_score > highest_score:
            highest_score = final_score
            best_match = master_name

    assigned_class = master_list.get(best_match, "Not Found") if highest_score > 40 else "Not Found"
    
    if assigned_class != "Not Found" and assigned_class.split('-')[0] != str(valid_grades.index(grade) + 5):
        possible_matches = [key for key in master_list.keys() if master_list[key].startswith(str(valid_grades.index(grade) + 5) + '-')]
        best_match, score = process.extractOne(name, possible_matches, scorer=fuzz.token_sort_ratio)
        assigned_class = master_list.get(best_match, "Not Found") if score > 40 else "Not Found"
    
    return assigned_class

# File uploader
uploaded_file = st.file_uploader("Upload a PDF", type="pdf")

if uploaded_file:
    with pdfplumber.open(uploaded_file) as pdf:
        full_text = "\n".join([page.extract_text() for page in pdf.pages if page.extract_text()])

    students_list = extract_students_info(full_text)
    df = pd.DataFrame(students_list, columns=["Name", "Grade"])
    df = df[df["Grade"].isin(valid_grades)].drop_duplicates()

    for i, row in df.iterrows():
        df.at[i, "Class"] = find_best_match(row["Name"], row["Grade"])

    df = df.sort_values(by=["Class", "Name"], ascending=[True, True])

    st.write("### Processed Student List")
    st.dataframe(df)

    # Save to Google Sheets
    def save_to_sheets(df):
        spreadsheet = gc.create("Early Bus List")
        worksheet = spreadsheet.get_worksheet(0)
        worksheet.update([df.columns.values.tolist()] + df.values.tolist())
        return spreadsheet

    if st.button("Save to Google Sheets & Open"):
        spreadsheet = save_to_sheets(df)
        sheet_url = f"https://docs.google.com/spreadsheets/d/{spreadsheet.id}/edit"
        st.markdown(f"[Open Google Sheet]({sheet_url})", unsafe_allow_html=True)


