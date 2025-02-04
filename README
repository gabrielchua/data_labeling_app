# Data Labelling App

This Streamlit application is designed for data labelling tasks. It allows users to label text data across several categories, including hate speech, insults, sexual content, physical violence, self-harm, and other misconduct.  The app integrates with Google Sheets for data storage and retrieval.

## Features

*   **User Authentication:** Password protection to ensure only authorized personnel can access the labelling interface.
*   **Data Loading from Google Sheets:** Fetches data directly from a specified Google Sheet.
*   **Interactive Labelling:** Provides a user-friendly interface with clear categories and options for labelling.
*   **Data Saving to Google Sheets:** Saves the labelled data, along with timestamps and labeller identity, back to a designated Google Sheet.
*   **Session Management:** Remembers the last labelled index for each labeller, allowing them to resume where they left off.
*   **Definitions:** Collapsible definitions box for quick reference.

## Setup Instructions

1.  **Install Dependencies:**

    ```bash
    pip install streamlit gspread pandas google-auth
    ```

2.  **Google Cloud Project Setup:**

    *   Create a Google Cloud project.
    *   Enable the Google Sheets API and Google Drive API.
    *   Create a service account with access to the Google Sheets API and Google Drive API.
    *   Download the service account credentials JSON file.

3.  **Secrets Management:**

    *   Create a `.streamlit/secrets.toml` file in your app's directory.
    *   Add the following secrets, replacing the placeholder values with your actual credentials:

        ```toml
        GOOGLE_SHEET_URL = "YOUR_GOOGLE_SHEET_URL"
        GCP_SERVICE_ACCOUNT = "YOUR_GCP_SERVICE_ACCOUNT"
        password = "YOUR_PASSWORD"
        ```

4.  **Google Sheet Setup:**

    *   Create a Google Sheet to store your data.
    *   Share the sheet with the client email address from your service account credentials, giving it editor permissions.
    *   Update the `GOOGLE_SHEET_URL` in your `secrets.toml` file with the URL of your Google Sheet.
    *   Ensure your Google Sheet has a worksheet named "sampled\_30" (or change the `INPUT_SHEET_NAME` constant in `app.py`).
    *   Ensure your Google Sheet has a worksheet named "sample\_30\_labelled" (or change the `OUTPUT_SHEET_NAME` constant in `app.py`).

5.  **Run the App:**

    ```bash
    streamlit run app.py
    ```

## Configuration

The following constants can be configured in the `app.py` file:

*   `LABELLERS`: A list of valid labeller names.
*   `INPUT_SHEET_NAME`: The name of the worksheet containing the data to be labelled.
*   `OUTPUT_SHEET_NAME`: The name of the worksheet where labelled data will be saved.

## Notes

*   The application uses Streamlit's session state to maintain the current index and other state variables.
*   Error handling is implemented to catch common issues, such as connection errors with Google Sheets.
