"""
app.py
"""

# Standard imports
import hmac
import json
import time

# Third party imports
import gspread
import streamlit as st
import pandas as pd
from datetime import datetime
from gspread.exceptions import WorksheetNotFound
from google.oauth2 import service_account

# Local imports
from constants import definitions

# =============================================================================
# CONSTANTS
# =============================================================================

LABELLERS = [
    "Gabriel",
    "Jessica",
    "Jiayi",
    "Leanne",
    "Pradyu", 
    "Shaun"
]

GOOGLE_SHEET_URL = st.secrets["GOOGLE_SHEET_URL"]
GOOGLE_CREDENTIALS = st.secrets["GCP_SERVICE_ACCOUNT"]

INPUT_SHEET_NAME = "sampled_30"
OUTPUT_SHEET_NAME = "sample_30_labelled"

# =============================================================================
# PASSWORD CHECK
# =============================================================================

def check_password():
    """Returns `True` if the user had the correct password."""

    def password_entered():
        """Checks whether a password entered by the user is correct."""
        if hmac.compare_digest(st.session_state["password"], st.secrets["password"]):
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # Don't store the password.
        else:
            st.session_state["password_correct"] = False

    # Return True if the password is validated.
    if st.session_state.get("password_correct", False):
        return True

    # Show input for password.
    st.text_input(
        "Password", type="password", on_change=password_entered, key="password"
    )
    if "password_correct" in st.session_state:
        st.error("😕 Password incorrect")
    return False


if not check_password():
    st.stop()  # Do not continue if check_password is not True.


# =============================================================================
# HELPERS
# =============================================================================

# Function to load the data (and cache it so we don't re-read on every run)
@st.cache_data
def load_data():
    try:
        # Create credentials object
        credentials = service_account.Credentials.from_service_account_info(
            json.loads(GOOGLE_CREDENTIALS),
            scopes=[
                "https://www.googleapis.com/auth/spreadsheets",
                "https://www.googleapis.com/auth/drive",
            ],
        )
        
        # Create authorized client with retry mechanism
        gc = gspread.authorize(credentials)
        
        # Open spreadsheet
        sheet = gc.open_by_url(GOOGLE_SHEET_URL)
        input_worksheet = sheet.worksheet(INPUT_SHEET_NAME)
        data = input_worksheet.get_all_records()
        df = pd.DataFrame(data)
        return df, sheet
    except Exception as e:
        st.error(f"Failed to connect to Google Sheets: {str(e)}")
        st.stop()

# Helper to save labelled data
def save_labelled_data(row):
    # Create credentials object
    credentials = service_account.Credentials.from_service_account_info(
        json.loads(GOOGLE_CREDENTIALS),
        scopes=[
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive",
        ],
    )
    
    # Create authorized client with retry mechanism
    gc = gspread.authorize(credentials)

    sheet = gc.open_by_url(GOOGLE_SHEET_URL)
    ws = sheet.worksheet(OUTPUT_SHEET_NAME)
    ws.append_row(list(row.values()))

# Function to get the last labelled index for a labeller
def get_last_labelled_index(labeller):
    try:
        # Create credentials object
        credentials = service_account.Credentials.from_service_account_info(
            json.loads(GOOGLE_CREDENTIALS),
            scopes=[
                "https://www.googleapis.com/auth/spreadsheets",
                "https://www.googleapis.com/auth/drive",
            ],
        )
        
        # Create authorized client with retry mechanism
        gc = gspread.authorize(credentials)

        sheet = gc.open_by_url(GOOGLE_SHEET_URL)
        ws = sheet.worksheet(OUTPUT_SHEET_NAME)
        data = ws.get_all_records()
        if not data:
            return -1
        labeller_data = [row for row in data if row['labeller'] == labeller]
        if not labeller_data:
            return -1
        return max(row['attempt_id'] for row in labeller_data)
    except WorksheetNotFound:
        return -1

# =============================================================================
# INITIAL SETUP & SESSION STATE
# =============================================================================

# Initialize session state variables
if 'index' not in st.session_state:
    st.session_state.index = 0

# Initialize pill states
for category in ['hateful', 'insult', 'sexual', 'physical_violence', 'self_harm', 'misconduct']:
    if f'{category}_selected' not in st.session_state:
        st.session_state[f'{category}_selected'] = None

# =============================================================================
# SIDEBAR / HEADER COMPONENTS
# =============================================================================

st.title("Data Labelling App")

# 1. Labeller identity (you can also use a selectbox if you prefer a fixed list)
st.markdown("#### Please select your name")
labeller = st.selectbox("Your name:", options=LABELLERS, placeholder="Select your name", index=None)

if not labeller:
    st.warning("Please select your name to begin labelling.")
    st.stop()

# 2. Collapsible box for definitions (placeholder text)
with st.expander("Definitions"):
    st.info(definitions)

st.divider()

# =============================================================================
# LOAD DATA & SET INDEX
# =============================================================================

df, sheet = load_data()

# If there are no records, inform the user.
if df.empty:
    st.error("No data found!")
    st.stop()

# Initialize or update session state index based on last labelled example
if 'index' not in st.session_state or st.session_state.get('current_labeller') != labeller:
    last_index = get_last_labelled_index(labeller)
    st.session_state.index = last_index + 1
    st.session_state.current_labeller = labeller

# =============================================================================
# DISPLAY CURRENT RECORD & LABELLING WIDGETS
# =============================================================================

if st.session_state.index < len(df):
    record = df.iloc[st.session_state.index]
    st.success(f"#### {record['text']}")

    st.markdown("#### Please label the above text. Choose only 1 option per category.")

    col1, col2 = st.columns(2)

    with col1:
        # --- Hateful ---
        hateful_options = ["discriminatory", "hate speech", "NIL"]
        hateful_label = st.pills("**1. Hateful**", hateful_options, selection_mode="single", key=f"hateful_{st.session_state.index}")

        # --- Insults ---
        insult_options = ["insult", "NIL"]
        insult_label = st.pills("**2. Insults**", insult_options, selection_mode="single", key=f"insult_{st.session_state.index}")

        # --- Sexual ---
        sexual_options = ["not appropriate for minors", "not appropriate for all ages", "NIL"]
        sexual_label = st.pills("**3. Sexual**", sexual_options, selection_mode="single", key=f"sexual_{st.session_state.index}")

    with col2:
        # --- Physical violence ---
        physical_violence_options = ["physical violence", "NIL"]
        physical_violence_label = st.pills("**4. Physical Violence**", physical_violence_options, selection_mode="single", key=f"physical_violence_{st.session_state.index}")

        # --- Self-harm ---
        self_harm_options = ["ideation/intent", "actual self-harm/sucide", "NIL"]
        self_harm_label = st.pills("**5. Self-harm**", self_harm_options, selection_mode="single", key=f"self_harm_{st.session_state.index}")

        # --- All other misconduct ---
        misconduct_options = ["generally not socially accepted", "illegal", "NIL"]
        misconduct_label = st.pills("**6. All Other Misconduct**", misconduct_options, selection_mode="single", key=f"misconduct_{st.session_state.index}")

    # =============================================================================
    # SUBMIT BUTTON: Save label data
    # =============================================================================

    if st.button("Submit Label 📝"):
        if not labeller:
            st.error("Please enter your labeller identity above before submitting your label.")
        elif not all([hateful_label, insult_label, sexual_label, physical_violence_label, self_harm_label, misconduct_label]):
            st.error("Please provide labels for all categories before submitting.")
        else:



            # map the human readable labels to the standardised labels
            for label in [hateful_label, insult_label, sexual_label, physical_violence_label, self_harm_label, misconduct_label]:
                if label == "NIL":
                    label = "FALSE"
                elif label == "discriminatory":
                    label = "level_1_discriminatory"
                elif label == "hate speech":
                    label = "level_2_hate_speech"
                elif label == "not appropriate for minors":
                    label = "level_1_not_appropriate_for_minors"
                elif label == "not appropriate for all ages":
                    label = "level_2_not_appropriate_for_all_ages"
                elif label == "ideation/intent":
                    label = "level_1_self_harm_intent"
                elif label == "actual self-harm/sucide":
                    label = "level_2_self_harm_action"
                elif label == "generally not socially accepted":
                    label = "level_1_not_socially_accepted"
                elif label == "illegal":
                    label = "level_2_illegal_activities"

            # Prepare a dictionary of all data to be saved.
            row = {
                "timestamp": datetime.now().isoformat(),
                "labeller": labeller,
                "prompt_id": record["prompt_id"],
                "attempt_id": st.session_state.index,
                "original_id": record["original_id"],
                "text": record["text"],
                "hateful": hateful_label,
                "insults": insult_label,
                "sexual": sexual_label,
                "physical_violence": physical_violence_label,
                "self_harm": self_harm_label,
                "all_other_misconduct": misconduct_label,
            }

            # Save the data to Google Sheets
            save_labelled_data(row)

            st.success("Label submitted successfully! Next example incoming 🔍")

            time.sleep(2)

            # Move on to the next record
            st.session_state.index += 1

            # Reload the app
            st.rerun()
else:
    st.markdown("## You have finished labelling all records. Thank you!")
