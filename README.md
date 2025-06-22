# Quote to ITC Webhook Function

This repository contains a Python-based webhook function designed to process insurance quote data and send it to the Insurance Technologies Corporation (ITC) API via Zoho Catalyst. The function transforms JSON input into ACORD XML format and handles the API interaction.

## Overview

- **Purpose**: Convert insurance quote data (JSON) into ACORD XML and submit it to the ITC API for processing.
- **Platform**: Built and deployed using Zoho Catalyst serverless functions.
- **Language**: Python
- **Dependencies**: `zcatalyst-sdk`, `requests`

## Prerequisites

- Zoho Catalyst CLI installed (`npm install -g @zohocatalyst/cli`).
- Python environment with required packages (`pip install -r requirements.txt`).
- GitHub account for version control.

## Installation

1. Clone the repository:
   
Install dependencies:

pip install -r requirements.txt
Configure Catalyst:
Log in to Catalyst: catalyst auth login.
Initialize the project if not already done: catalyst init.

Start the local server: catalyst serve

Test the endpoint (e.g., http://localhost:3000/server/quote_pro_to_itc_function/quote-to-itc-webhook) using a tool like Postman with a POST request and the sample JSON payload.

Deploy the function to Catalyst: catalyst deploy
Use the deployed endpoint (e.g., https://quoteprotoitc-60041822215.development.catalystserverless.in/quote-to-itc-webhook) for production testing.


Sample JSON Payload
json

{
  "rating_state": "Illinois",
  "template_name": "Quote Template Name",
  "insured": {
    "first_name": "Pablo",
    "last_name": "Ortiz Hernandez",
    "birth_date": "1970-08-12",
    "gender": "M",
    "phone": "773-673-6911",
    "email": "BERTHA9530@GMAIL.COM",
    "address": {
      "street": "1320 Harder Ct",
      "city": "ROCKFORD",
      "state": "IL",
      "postal_code": "61103",
      "county": "WINNEBAGO"
    },
    "time_at_residence": {
      "years": 0,
      "months": 0
    }
  },
  "producer": {
    "name": "InsuranceNavy Desktop",
    "id": "0443b34c-c7df-4239-a934-7c1f9c2f9989",
    "address": {
      "street": "1234 Old Rd",
      "city": "Dallas",
      "state": "TX",
      "postal_code": "75007"
    },
    "phone": "+1-235-5656969"
  },
  "policy": {
    "effective_date": "2025-06-06",
    "policy_term": "Annual",
    "payment_option": "Installments",
    "non_owner": "Yes",
    "liability": "25/50/25",
    "medical_payments": "No Coverage",
    "um_uim_bi": "25/50",
    "uninsured_pd": "No Coverage",
    "accidental_death": "No Coverage",
    "legal_expense": "No",
    "contact_method": "None",
    "primary_contact": "Email",
    "lead_source": "",
    "marketing_number": "",
    "quote_description": "",
    "endorsement": "",
    "native_language": "English",
    "paperless_discount": "No"
  },
  "driver": {
    "prior_insurance": "",
    "reason_for_no_insurance": "",
    "prior_in_agency": "No",
    "prior_insurance_carrier": "",
    "prior_liability_limits": "",
    "prior_transfer_level": "No Prior Transfer",
    "time_with_prior_insurance": "",
    "parents_policy": "No",
    "time_licensed_us": {
      "years": 3,
      "months": 0
    },
    "licensed_state": "Illinois",
    "time_licensed_state": {
      "years": 3,
      "months": 0
    },
    "mvr_experience": {
      "years": 3,
      "months": 0
    },
    "foreign_licensed": "None",
    "sr22": "Yes",
    "sr22_state": "Illinois",
    "sr22_reason_filing": "No Insurance",
    "suspended_expired_license": "None",
    "acc_prevention_course": "No",
    "acc_prevention_course_date": "",
    "civil_union": "No",
    "time_since_suspension": {
      "years": 0,
      "months": 0
    },
    "residence_status": "Rent",
    "residence_type": "Apartment",
    "property_insurance": "No",
    "companion_home": "No",
    "industry_occupation": "LABORER",
    "time_employed": {
      "years": 0,
      "months": 0
    },
    "education_level": "",
    "good_student": "No",
    "distant_student": "None",
    "drivers_training": "No",
    "foreign_license_experience": "",
    "senior_discount": "No",
    "senior_driver_course_date": ""
  },
  "vehicle": {
    "manufacturer": "NONOWNER",
    "model": "NONOWNER",
    "year": 2025,
    "vin": "NON OWNER",
    "comp": "No Coverage",
    "coll": "No Coverage",
    "towing": "No Coverage",
    "rental": "No Coverage",
    "custom_equipment": "",
    "gap": "No",
    "purchase_type": "New",
    "license_plate_number": "",
    "telematics": "No",
    "percent_to_work": "",
    "leased": "No",
    "annual_miles": "0",
    "salvaged": "No",
    "miles_driven_to_work": "",
    "usage": "Pleasure",
    "ride_share": "No",
    "anti_theft": "No Anti-Theft",
    "grey_market": "No",
    "odometer": "",
    "purchase_price": "",
    "msrp": "",
    "acv": "",
    "purchase_date": {
      "years": 0,
      "months": 0
    }
  },
  "notes": []
}


Configuration
ITC API Endpoint: https://ratingqa.itcdataservices.com/webservices/imp/api/storage/savepolicy
Authentication: Uses a hardcoded username and password (0443b34c-c7df-4239-a934-7c1f9c2f9989). Update with secure credentials in production.
Catalyst Endpoint: Deployed at https://quoteprotoitc-60041822215.development.catalystserverless.in/quote-to-itc-webhook.


