


"""
Feature Test
"""


"""
https://docs.google.com/spreadsheets/d/10dvNLvLIxPXKPtJZZDx9vOAOPXqpAMCEccp27OdkMA0/edit?gid=1951528466#gid=1951528466
"""

import os.path
import json
import datetime
import time
import urllib.request
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

os.chdir(r"C:\Core_Vitals_Extraction")

start_time = time.time()

# Define constants
SPREADSHEET_ID = '10dvNLvLIxPXKPtJZZDx9vOAOPXqpAMCEccp27OdkMA0'  # Replace with your spreadsheet ID
CREDENTIALS_FILE = 'NEW.json'  # Path to credentials file
API_KEY = 'AIzaSyC5ypQ_GD1MQO9uuDuockZ_lAK2DOFkAEI' # Your API key

# URLs to check
URLS = {
    'HLE_Main': 'https://www.homeloanexperts.com.au/',
    'HLE_New': 'https://www.homeloanexperts.com.au/home-new/',
    'YTD_Calculator': 'https://www.homeloanexperts.com.au/mortgage-calculators/ytd-calculator/',
    'INV_Prop_Calc': 'https://www.homeloanexperts.com.au/investment-loans/investment-property-calculator/',
    'Partner_Buyout': 'https://www.homeloanexperts.com.au/home-loan-articles/buying-out-a-partner-on-a-mortgage/',
    'Waived_LMI': 'https://www.homeloanexperts.com.au/waived-lmi/',
    'Add_Partner_Title': 'https://www.homeloanexperts.com.au/managing-your-home-loan/adding-partner-to-property-title/',
    'LVR_Calculator': 'https://www.homeloanexperts.com.au/mortgage-calculators/lvr-calculator/',
    'Cost_Build_House': 'https://www.homeloanexperts.com.au/home-loan-articles/how-much-does-it-cost-to-build-a-house/',
    # 'Banks_Calc_BorrowCap': 'https://www.homeloanexperts.com.au/how-much-can-i-borrow/how-do-banks-calculate-my-borrowing-power/', ## This link screws up the execution of this script :(
    'Takeover_Parents_Mortgage': 'https://www.homeloanexperts.com.au/home-loan-articles/taking-over-your-parents-mortgage/',
    'LMI_Premium_Rates': 'https://www.homeloanexperts.com.au/lenders-mortgage-insurance/lmi-premium-rates/',
    'Trust_Loans': 'https://www.homeloanexperts.com.au/trust-loans/',
    ## The below were added September 10th 2024
    'Positive_CF':'https://www.homeloanexperts.com.au//blog/property-market/where-to-find-positive-cashflow-properties-in-australia-in-2023',
    'Fixed_Rate_Cut':'https://www.homeloanexperts.com.au//blog/interest-rate/major-banks-cut-fixed-rates',
    'Blog':'https://www.homeloanexperts.com.au/blog/',
    'Free_Quote':'https://www.homeloanexperts.com.au/free-quote',
    'Home_Guarantee':'https://www.homeloanexperts.com.au//home-guarantee-scheme-lpnew',
    'Generic_Expat_lpnew':'https://www.homeloanexperts.com.au//generic-expat-lpnew',
    'Homestart_Finance':'https://www.homeloanexperts.com.au/lender-reviews-new/homestart-finance/',
    'ING_Home_Loan_Review':'https://www.homeloanexperts.com.au//lender-reviews/ing-home-loan-review'
}
                                                                                                                                                                              
API_BASE_URL = 'https://www.googleapis.com/pagespeedonline/v5/runPagespeed'
RATE_LIMIT = 60  # Number of API calls allowed per minute
DELAY_BETWEEN_CALLS = 60 / RATE_LIMIT  # Calculate delay needed between API calls to stay within limit

def get_credentials():
    SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
    creds = None
    if os.path.exists(CREDENTIALS_FILE):
        creds = Credentials.from_authorized_user_file(CREDENTIALS_FILE, SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
        with open(CREDENTIALS_FILE, "w") as token:
            token.write(creds.to_json())
    return creds

def get_row_count(service, sheet_name):
    values = service.spreadsheets().values().get(
        spreadsheetId=SPREADSHEET_ID, range=f"{sheet_name}!A:A"
    ).execute().get('values', [])
    return len(values)

def set_values(service, range_name, values):
    service.spreadsheets().values().update(
        spreadsheetId=SPREADSHEET_ID,
        valueInputOption='USER_ENTERED',
        range=range_name,
        body=dict(majorDimension='ROWS', values=values)
    ).execute()

def fetch_page_speed_data(page_url, strategy, retries=3):
    url = f'{API_BASE_URL}?url={page_url}&strategy={strategy}&category=performance&category=best-practices&key={API_KEY}'
    for attempt in range(retries):
        try:
            with urllib.request.urlopen(url) as response:
                return json.loads(response.read())
        except urllib.error.HTTPError as e:
            print(f"HTTP error: {e.code} - {e.reason}")
            if attempt < retries - 1:
                print(f"Retrying... ({attempt + 1}/{retries})")
                time.sleep(2)  # wait before retrying
            else:
                raise
        except Exception as e:
            print(f"Error fetching data: {e}")
            if attempt < retries - 1:
                print(f"Retrying... ({attempt + 1}/{retries})")
                time.sleep(2)
            else:
                raise

def get_performance_scores(data):
    try:
        performance_score = data["lighthouseResult"]["categories"]["performance"]["score"]
        if performance_score is not None:
            performance_score *= 100
        else:
            performance_score = "N/A"
    except KeyError:
        performance_score = "N/A"

    try:
        best_practices_score = data["lighthouseResult"]["categories"]["best-practices"]["score"]
        if best_practices_score is not None:
            best_practices_score *= 100
        else:
            best_practices_score = "N/A"
    except KeyError:
        best_practices_score = "N/A"

    return performance_score, best_practices_score

def process_data(data, experience_key):
    metrics = data.get(experience_key, {}).get("metrics", {})

    scores = {
        "CLS": metrics.get("CUMULATIVE_LAYOUT_SHIFT_SCORE", {}).get("percentile", 0) / 100,
        "TTFB": metrics.get("EXPERIMENTAL_TIME_TO_FIRST_BYTE", {}).get("percentile", 0) / 1000,
        "FCP": metrics.get("FIRST_CONTENTFUL_PAINT_MS", {}).get("percentile", 0) / 1000,
        "FID": metrics.get("FIRST_INPUT_DELAY_MS", {}).get("percentile", "N/A"),
        "INP": metrics.get("INTERACTION_TO_NEXT_PAINT", {}).get("percentile", "N/A"),
        "LCP": metrics.get("LARGEST_CONTENTFUL_PAINT_MS", {}).get("percentile", 0) / 1000
    }

    if scores["FID"] != "N/A":
        scores["FID"] = float(scores["FID"])
    if scores["INP"] != "N/A":
        scores["INP"] = float(scores["INP"])

    return scores

def main():
    creds = get_credentials()
    service = build('sheets', 'v4', credentials=creds)
    date_str = str(datetime.datetime.now())

    for sheet_name, page_url in URLS.items():
        row_index = get_row_count(service, sheet_name) + 1

        # Fetch Desktop data
        desktop_data = fetch_page_speed_data(page_url, 'desktop')
        desktop_performance_score, desktop_best_practices_score = get_performance_scores(desktop_data)

        # Fetch Mobile data
        mobile_data = fetch_page_speed_data(page_url, 'mobile')
        mobile_performance_score, mobile_best_practices_score = get_performance_scores(mobile_data)

        # Process Desktop data
        desktop_thisurl_scores = process_data(desktop_data, "loadingExperience")
        desktop_origin_scores = process_data(desktop_data, "originLoadingExperience")

        # Process Mobile data
        mobile_thisurl_scores = process_data(mobile_data, "loadingExperience")
        mobile_origin_scores = process_data(mobile_data, "originLoadingExperience")

        # Prepare data for the sheet
        data = [
            [
                date_str, page_url, "ThisURL",
                desktop_performance_score, desktop_best_practices_score,
                desktop_thisurl_scores["CLS"], desktop_thisurl_scores["TTFB"], desktop_thisurl_scores["FCP"],
                desktop_thisurl_scores["FID"], desktop_thisurl_scores["INP"], desktop_thisurl_scores["LCP"],
                mobile_performance_score, mobile_best_practices_score,
                mobile_thisurl_scores["CLS"], mobile_thisurl_scores["TTFB"], mobile_thisurl_scores["FCP"],
                mobile_thisurl_scores["FID"], mobile_thisurl_scores["INP"], mobile_thisurl_scores["LCP"]
            ],
            [
                date_str, page_url, "Origin",
                desktop_performance_score, desktop_best_practices_score,
                desktop_origin_scores["CLS"], desktop_origin_scores["TTFB"], desktop_origin_scores["FCP"],
                desktop_origin_scores["FID"], desktop_origin_scores["INP"], desktop_origin_scores["LCP"],
                mobile_performance_score, mobile_best_practices_score,
                mobile_origin_scores["CLS"], mobile_origin_scores["TTFB"], mobile_origin_scores["FCP"],
                mobile_origin_scores["FID"], mobile_origin_scores["INP"], mobile_origin_scores["LCP"]
            ]
        ]

        range_name = f'{sheet_name}!A{row_index}:S{row_index + len(data) - 1}'
        set_values(service, range_name, data)
        
        # Sleep to respect rate limits
        time.sleep(DELAY_BETWEEN_CALLS)

if __name__ == '__main__':
    try:
        main()
        print("\n")
        print("Script Execution Completed")
        print(f"--- Time Elapsed: {time.time() - start_time} seconds ---")
    except HttpError as err:
        print(err)
