import streamlit as st
import pdfplumber
import re
import pandas as pd
from fuzzywuzzy import process, fuzz

# Permanent Master List (Embedded)
master_list = {
    "Rozo Alejandro": "5-3",
    "Ruiz Mario": "5-1",
    "Serpa Sergio": "5-2",
    "Ochoa Tomas": "5-3",
    "Aguirre Caiza Paula": "11-5",
    "Arias Tomas": "5-1",
    "Chokkar Rudransha": "5-1",
    "Choudhary Rayansh": "5-1",
    "Benejam Graterol Gabriela De Dios": "5-1",
    "De la Rosa Tomás": "5-1",
}

# Define valid grades
valid_grades = ["QUINTO", "SEXTO", "SEPTIMO", "OCTAVO", "NOVENO", "DECIMO", "ONCE"]

# Function to normalize names
def normalize_name(name):
    name = name.lower().strip()
    name = re.sub(r'[^a-záéíóúñ ]', '', name)
    return name

# Function to split name into components
def split_name_parts(name):
    return set(normalize_name(name).split())

# Function to extract student names and grades from text
def extract_students_info(text):
    pattern = r"Pasajero:\\s([A-ZÁÉÍÓÚÑ ]+)\\sCurso:\\s([A-ZÁÉÍÓÚÑ]+)"
    matches = re.findall(pattern, text)
    students_info = [(match[0].strip(), match[1].strip()) for match in matches]
    return students_info

# Function to find the best match in the master list
def find_best_match(name, grade):
    pdf_name_parts = split_name_parts(name)
    best_match = None
    highest_score = 0

    for master_name in master_list.keys():
        master_name_parts = split_name_parts(master_name)
        common_parts = pdf_name_parts.intersection(master_name_parts)
        score = len(common_parts) / max(len(pdf_name_parts), len(master_name_parts)) * 100

        # Use fuzzy matching as a fallback
        fuzzy_score = fuzz.token_sort_ratio(name, master_name)
        final_score = max(score, fuzzy_score)

        if final_score > highest_score:
            highest_score = final_score
            best_match = master_name

    assigned_class = master_list.get(best_match, "Not Found") if highest_score > 40 else "Not Found"

    # Final check: Grade-Level Consistency
    if assigned_class != "Not Found" and assigned_class.split('-')[0] != str(valid_grades.index(grade) + 5):
        possible_matches = [key for key in master_list.keys() if master_list[key].startswith(str(valid_grades.index(grade) + 5) + '-')]
        best_match, score = process.extractOne(name, possible_matches, scorer=fuzz.token_sort_ratio)
        assigned_class = master_list.get(best_match, "Not Found") if score > 40 else "Not Found"

    return assigned_class

# Streamlit UI
st.title("Student List Extractor")

uploaded_file = st.file_uploader("Upload a PDF", type="pdf")

if uploaded_file:
    with pdfplumber.open(uploaded_file) as pdf:
        full_text = "\\n".join([page.extract_text() for page in pdf.pages if page.extract_text()])

    students_list = extract_students_info(full_text)
    df = pd.DataFrame(students_list, columns=["Name", "Grade"])
    df = df[df["Grade"].isin(valid_grades)].drop_duplicates()

    progress_bar = st.progress(0)
    total_students = len(df)

    for i, row in df.iterrows():
        df.at[i, "Class"] = find_best_match(row["Name"], row["Grade"])
        progress_bar.progress((i + 1) / total_students)

    if "Class" in df.columns:
    df["Sort_Class"] = df["Class"].apply(lambda x: (int(x.split('-')[0]), int(x.split('-')[1])) if isinstance(x, str) and '-' in x else (99, 99))
    df.sort_values(by=["Sort_Class", "Name"], ascending=[True, True], inplace=True)
    df.drop(columns=["Sort_Class"], inplace=True)

    st.dataframe(df)

    if st.button("Copy to Clipboard"):
        df.to_clipboard(index=False, header=False)
        st.success("Copied to clipboard!")
