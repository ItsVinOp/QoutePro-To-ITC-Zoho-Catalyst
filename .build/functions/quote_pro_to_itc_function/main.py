import json
import requests
import xml.etree.ElementTree as ET
from xml.dom import minidom
import zcatalyst_sdk
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def json_to_acord_xml(data):
    # Create the root element
    acord = ET.Element("ACORD")

    # SignonRs Section
    signon_rs = ET.SubElement(acord, "SignonRs")
    signon_transport = ET.SubElement(signon_rs, "SignonTransport")
    ET.SubElement(signon_transport, "SignonRoleCd").text = "Agent"
    cust_id = ET.SubElement(signon_transport, "CustId")
    ET.SubElement(cust_id, "SPName").text = "turborater.com"
    ET.SubElement(cust_id, "CustPermId").text = ""
    ET.SubElement(signon_rs, "ClientDt").text = "2025-06-20T18:08:00+05:30"  # 06:08 PM IST
    ET.SubElement(signon_rs, "CustLangPref").text = data["policy"]["native_language"]
    client_app = ET.SubElement(signon_rs, "ClientApp")
    ET.SubElement(client_app, "Org").text = "Insurance Technologies Corporation"
    ET.SubElement(client_app, "Name").text = ""
    ET.SubElement(client_app, "Version").text = ""

    # InsuranceSvcRs Section
    insurance_svc_rs = ET.SubElement(acord, "InsuranceSvcRs")
    ET.SubElement(insurance_svc_rs, "RsUID").text = ""
    ET.SubElement(insurance_svc_rs, "com.getitc_QuoteSourceName").text = data["policy"]["lead_source"]
    ET.SubElement(insurance_svc_rs, "com.getitc_QuoteSourceId").text = ""
    ET.SubElement(insurance_svc_rs, "com.getitc_Carrier").text = ""
    ET.SubElement(insurance_svc_rs, "com.getitc_TotalPremium").text = "0.00"
    ET.SubElement(insurance_svc_rs, "com.getitc_DownPayment").text = "0.00"
    ET.SubElement(insurance_svc_rs, "com.getitc_Payment").text = "0.00"
    ET.SubElement(insurance_svc_rs, "com.getitc_PaymentPlan").text = data["policy"]["payment_option"]

    # PersAutoPolicyQuoteInqRs Section
    pers_auto_policy = ET.SubElement(insurance_svc_rs, "PersAutoPolicyQuoteInqRs")
    ET.SubElement(pers_auto_policy, "RsUID").text = ""
    ET.SubElement(pers_auto_policy, "TransactionRequestDt").text = "2025-06-20T18:08:00+05:30"  # 06:08 PM IST
    ET.SubElement(pers_auto_policy, "TransactionEffectiveDt").text = data["policy"]["effective_date"]
    ET.SubElement(pers_auto_policy, "CurCd").text = "USD"

    # Producer Section
    producer = ET.SubElement(pers_auto_policy, "Producer")
    general_party_info = ET.SubElement(producer, "GeneralPartyInfo")
    name_info = ET.SubElement(general_party_info, "NameInfo", id=data["producer"]["id"])
    comml_name = ET.SubElement(name_info, "CommlName")
    ET.SubElement(comml_name, "CommercialName").text = ""
    person_name = ET.SubElement(name_info, "PersonName")
    producer_name = data["producer"]["name"].split()
    ET.SubElement(person_name, "Surname").text = producer_name[-1]
    ET.SubElement(person_name, "GivenName").text = " ".join(producer_name[:-1])
    ET.SubElement(person_name, "OtherGivenName").text = ""
    tax_identity = ET.SubElement(name_info, "TaxIdentity")
    ET.SubElement(tax_identity, "TaxIdTypeCd").text = "FEIN"
    ET.SubElement(tax_identity, "TaxId").text = ""
    addr = ET.SubElement(general_party_info, "Addr")
    ET.SubElement(addr, "AddrTypeCd").text = "StreetAddress"
    ET.SubElement(addr, "Addr1").text = data["producer"]["address"]["street"]
    ET.SubElement(addr, "Addr2").text = ""
    ET.SubElement(addr, "City").text = data["producer"]["address"]["city"]
    ET.SubElement(addr, "StateProvCd").text = data["producer"]["address"]["state"]
    ET.SubElement(addr, "PostalCode").text = data["producer"]["address"]["postal_code"]
    ET.SubElement(addr, "County").text = ""
    communications = ET.SubElement(general_party_info, "Communications")
    phone_info = ET.SubElement(communications, "PhoneInfo")
    ET.SubElement(phone_info, "PhoneTypeCd").text = "Phone"
    ET.SubElement(phone_info, "CommunicationUseCd").text = "Business"
    ET.SubElement(phone_info, "PhoneNumber").text = data["producer"]["phone"]
    item_id_info = ET.SubElement(producer, "ItemIdInfo")
    ET.SubElement(item_id_info, "AgencyId").text = ""
    producer_info = ET.SubElement(producer, "ProducerInfo")
    ET.SubElement(producer_info, "ContractNumber").text = ""
    ET.SubElement(producer_info, "PlacingOffice").text = data["producer"]["id"]

    # PersPolicy Section
    pers_policy = ET.SubElement(pers_auto_policy, "PersPolicy")
    ET.SubElement(pers_policy, "LOBCd").text = "AUTOP"
    pers_application_info = ET.SubElement(pers_policy, "PersApplicationInfo")
    insured_or_principal = ET.SubElement(pers_application_info, "InsuredOrPrincipal")
    general_party_info = ET.SubElement(insured_or_principal, "GeneralPartyInfo")
    name_info = ET.SubElement(general_party_info, "NameInfo")
    person_name = ET.SubElement(name_info, "PersonName")
    ET.SubElement(person_name, "Surname").text = data["insured"]["last_name"]
    ET.SubElement(person_name, "GivenName").text = data["insured"]["first_name"]
    ET.SubElement(person_name, "OtherGivenName").text = ""
    communications = ET.SubElement(general_party_info, "Communications")
    phone_info = ET.SubElement(communications, "PhoneInfo")
    ET.SubElement(phone_info, "PhoneTypeCd").text = "Phone"
    ET.SubElement(phone_info, "CommunicationUseCd").text = "Home"
    ET.SubElement(phone_info, "PhoneNumber").text = data["insured"]["phone"]
    email_info = ET.SubElement(communications, "EmailInfo")
    ET.SubElement(email_info, "CommunicationUseCd").text = "Day"
    ET.SubElement(email_info, "EmailAddr").text = data["insured"]["email"]
    addr = ET.SubElement(general_party_info, "Addr")
    ET.SubElement(addr, "AddrTypeCd").text = "StreetAddress"
    ET.SubElement(addr, "Addr1").text = data["insured"]["address"]["street"]
    ET.SubElement(addr, "Addr2").text = ""
    ET.SubElement(addr, "City").text = data["insured"]["address"]["city"]
    ET.SubElement(addr, "StateProvCd").text = data["insured"]["address"]["state"]
    ET.SubElement(addr, "PostalCode").text = data["insured"]["address"]["postal_code"]
    ET.SubElement(addr, "County").text = data["insured"]["address"]["county"]
    insured_info = ET.SubElement(insured_or_principal, "InsuredOrPrincipalInfo")
    ET.SubElement(insured_info, "InsuredOrPrincipalRoleCd").text = "Insured"
    person_info = ET.SubElement(insured_info, "PersonInfo")
    ET.SubElement(person_info, "BirthDt").text = data["insured"]["birth_date"]
    ET.SubElement(person_info, "GenderCd").text = data["insured"]["gender"]
    contract_term = ET.SubElement(pers_policy, "ContractTerm")
    duration_period = ET.SubElement(contract_term, "DurationPeriod")
    ET.SubElement(duration_period, "NumUnits").text = "6" if data["policy"]["policy_term"] == "Semi-Annual" else "12"
    ET.SubElement(duration_period, "UnitMeasurementCd").text = "MON"
    ET.SubElement(contract_term, "EffectiveDt").text = ""
    ET.SubElement(contract_term, "StartTime").text = ""
    ET.SubElement(contract_term, "ExpirationDt").text = ""
    ET.SubElement(contract_term, "EndTime").text = ""
    quote_info = ET.SubElement(pers_policy, "QuoteInfo")
    ET.SubElement(quote_info, "CompanysQuoteNumber").text = ""
    ET.SubElement(quote_info, "QuotePreparedDt").text = ""
    ET.SubElement(pers_policy, "OtherInsuranceWithCompanyCd").text = ""
    driver_veh = ET.SubElement(pers_policy, "DriverVeh", DriverRef="Drv1", VehRef="Veh1")
    ET.SubElement(driver_veh, "UsePct").text = "100"

    # PersAutoLineBusiness Section
    pers_auto_line = ET.SubElement(pers_auto_policy, "PersAutoLineBusiness")
    pers_driver = ET.SubElement(pers_auto_line, "PersDriver", id="Drv1")
    general_party_info = ET.SubElement(pers_driver, "GeneralPartyInfo")
    addr = ET.SubElement(general_party_info, "Addr")
    ET.SubElement(addr, "AddrTypeCd").text = "StreetAddress"
    ET.SubElement(addr, "Addr1").text = data["insured"]["address"]["street"]
    ET.SubElement(addr, "Addr2").text = ""
    ET.SubElement(addr, "City").text = data["insured"]["address"]["city"]
    ET.SubElement(addr, "StateProvCd").text = data["insured"]["address"]["state"]
    ET.SubElement(addr, "PostalCode").text = data["insured"]["address"]["postal_code"]
    ET.SubElement(addr, "County").text = data["insured"]["address"]["county"]
    name_info = ET.SubElement(general_party_info, "NameInfo")
    person_name = ET.SubElement(name_info, "PersonName")
    ET.SubElement(person_name, "Surname").text = data["insured"]["last_name"]
    ET.SubElement(person_name, "GivenName").text = data["insured"]["first_name"]
    ET.SubElement(person_name, "OtherGivenName").text = ""
    driver_info = ET.SubElement(pers_driver, "DriverInfo")
    person_info = ET.SubElement(driver_info, "PersonInfo")
    ET.SubElement(person_info, "GenderCd").text = data["insured"]["gender"]
    ET.SubElement(person_info, "BirthDt").text = data["insured"]["birth_date"]
    ET.SubElement(person_info, "MaritalStatusCd").text = "S" if data["driver"]["civil_union"] == "No" else "M"
    drivers_license = ET.SubElement(driver_info, "DriversLicense")
    ET.SubElement(drivers_license, "DriversLicenseNumber").text = "O63266070229"
    ET.SubElement(drivers_license, "LicenseClassCd").text = "Valid"
    ET.SubElement(drivers_license, "LicensedDt").text = "2022-06-17"  # 3 years licensed
    ET.SubElement(drivers_license, "StateProvCd").text = data["driver"]["licensed_state"]
    license = ET.SubElement(driver_info, "License")
    ET.SubElement(license, "LicenseTypeCd").text = "Driver"
    ET.SubElement(license, "LicenseStatusCd").text = "Active"
    ET.SubElement(license, "LicensedDt").text = "2022-06-17"
    ET.SubElement(license, "LicensePermitNumber").text = "O63266070229"
    ET.SubElement(license, "LicenseClassCd").text = "Valid"
    ET.SubElement(license, "StateProvCd").text = data["driver"]["licensed_state"]
    ET.SubElement(driver_info, "com.turborater_TemporaryVisitorLicense").text = "0"
    question_answer = ET.SubElement(driver_info, "QuestionAnswer")
    ET.SubElement(question_answer, "QuestionCd").text = "GENRL14"
    ET.SubElement(question_answer, "YesNoCd").text = "No" if data["driver"]["suspended_expired_license"] == "None" else "Yes"
    question_answer = ET.SubElement(driver_info, "QuestionAnswer")
    ET.SubElement(question_answer, "QuestionCd").text = "AUTOP05"
    ET.SubElement(question_answer, "YesNoCd").text = "No" if data["driver"]["sr22"] == "No" else "Yes"
    pers_driver_info = ET.SubElement(pers_driver, "PersDriverInfo", VehPrincipallyDrivenRef="Veh1")
    ET.SubElement(pers_driver_info, "DefensiveDriverCd").text = "Y" if data["driver"]["acc_prevention_course"] == "Yes" else "N"
    ET.SubElement(pers_driver_info, "DriverRelationshipToApplicantCd").text = "IN"
    ET.SubElement(pers_driver_info, "DriverTrainingInd").text = "1" if data["driver"]["drivers_training"] == "Yes" else "0"
    ET.SubElement(pers_driver_info, "GoodStudentCd").text = "Y" if data["driver"]["good_student"] == "Yes" else "N"
    ET.SubElement(pers_driver_info, "MatureDriverInd").text = "Y" if data["driver"]["senior_discount"] == "Yes" else "N"

    # PersVeh Section
    pers_veh = ET.SubElement(pers_auto_line, "PersVeh", id="Veh1", LocationRef="Gar1", RatedDriverRef="Drv1")
    estimated_annual_distance = ET.SubElement(pers_veh, "EstimatedAnnualDistance")
    ET.SubElement(estimated_annual_distance, "NumUnits").text = data["vehicle"]["annual_miles"]
    ET.SubElement(estimated_annual_distance, "UnitMeasurementCd").text = "SMI"
    ET.SubElement(pers_veh, "GaragingCd").text = "N"
    ET.SubElement(pers_veh, "Manufacturer").text = data["vehicle"]["manufacturer"]
    ET.SubElement(pers_veh, "Model").text = data["vehicle"]["model"]
    ET.SubElement(pers_veh, "ModelYear").text = str(data["vehicle"]["year"])
    ET.SubElement(pers_veh, "MultiCarDiscountInd").text = "0"
    ET.SubElement(pers_veh, "NumCylinders").text = "0"  # Non-owner
    ET.SubElement(pers_veh, "PrincipalOperatorInd").text = "1"
    ET.SubElement(pers_veh, "SeatBeltTypeCd").text = "PassBoth"
    ET.SubElement(pers_veh, "SeenCarInd").text = "0"
    ET.SubElement(pers_veh, "TerritoryCd").text = ""
    ET.SubElement(pers_veh, "VehIdentificationNumber").text = data["vehicle"]["vin"]
    ET.SubElement(pers_veh, "VehUseCd").text = data["vehicle"]["usage"]

    # Coverages
    # UM/UIM BI
    if data["policy"]["um_uim_bi"] != "No Coverage":
        limits = data["policy"]["um_uim_bi"].split("/")
        cov = ET.SubElement(pers_veh, "Coverage")
        ET.SubElement(cov, "CoverageCd").text = "UM"
        ET.SubElement(cov, "CoverageDesc").text = "Uninsured Motorist Liability"
        current_term_amt = ET.SubElement(cov, "CurrentTermAmt")
        ET.SubElement(current_term_amt, "Amt").text = "0"
        lim = ET.SubElement(cov, "Limit")
        ET.SubElement(lim, "FormatInteger").text = str(int(limits[0]) * 1000)
        ET.SubElement(lim, "LimitAppliesToCd").text = "PerPerson"
        lim = ET.SubElement(cov, "Limit")
        ET.SubElement(lim, "FormatInteger").text = str(int(limits[1]) * 1000)
        ET.SubElement(lim, "LimitAppliesToCd").text = "PerAccident"

    # Comprehensive
    if data["vehicle"]["comp"] != "No Coverage":
        cov = ET.SubElement(pers_veh, "Coverage")
        ET.SubElement(cov, "CoverageCd").text = "COMP"
        ET.SubElement(cov, "CoverageDesc").text = "Comprehensive Coverage"
        current_term_amt = ET.SubElement(cov, "CurrentTermAmt")
        ET.SubElement(current_term_amt, "Amt").text = "0"
        deductible = ET.SubElement(cov, "Deductible")
        ET.SubElement(deductible, "FormatInteger").text = data["vehicle"]["comp"]
        ET.SubElement(deductible, "DeductibleTypeCd").text = "CL"

    # Collision
    if data["vehicle"]["coll"] != "No Coverage":
        cov = ET.SubElement(pers_veh, "Coverage")
        ET.SubElement(cov, "CoverageCd").text = "COLL"
        ET.SubElement(cov, "CoverageDesc").text = "Collision"
        current_term_amt = ET.SubElement(cov, "CurrentTermAmt")
        ET.SubElement(current_term_amt, "Amt").text = "0"
        deductible = ET.SubElement(cov, "Deductible")
        ET.SubElement(deductible, "FormatInteger").text = data["vehicle"]["coll"]
        ET.SubElement(deductible, "DeductibleTypeCd").text = "CL"

    # Add Liability Coverage (BI/PD)
    if data["policy"]["liability"] != "":
        limits = data["policy"]["liability"].split("/")
        # Bodily Injury (BI) Limits
        cov = ET.SubElement(pers_veh, "Coverage")
        ET.SubElement(cov, "CoverageCd").text = "BI"
        ET.SubElement(cov, "CoverageDesc").text = "Bodily Injury Liability"
        current_term_amt = ET.SubElement(cov, "CurrentTermAmt")
        ET.SubElement(current_term_amt, "Amt").text = "0"
        lim = ET.SubElement(cov, "Limit")
        ET.SubElement(lim, "FormatInteger").text = str(int(limits[0]) * 1000)
        ET.SubElement(lim, "LimitAppliesToCd").text = "PerPerson"
        lim = ET.SubElement(cov, "Limit")
        ET.SubElement(lim, "FormatInteger").text = str(int(limits[1]) * 1000)
        ET.SubElement(lim, "LimitAppliesToCd").text = "PerAccident"
        # Property Damage (PD) Limit
        cov = ET.SubElement(pers_veh, "Coverage")
        ET.SubElement(cov, "CoverageCd").text = "PD"
        ET.SubElement(cov, "CoverageDesc").text = "Property Damage Liability"
        current_term_amt = ET.SubElement(cov, "CurrentTermAmt")
        ET.SubElement(current_term_amt, "Amt").text = "0"
        lim = ET.SubElement(cov, "Limit")
        ET.SubElement(lim, "FormatInteger").text = str(int(limits[2]) * 1000)
        ET.SubElement(lim, "LimitAppliesToCd").text = "PerAccident"

    question_answer = ET.SubElement(pers_veh, "QuestionAnswer")
    ET.SubElement(question_answer, "QuestionCd").text = "AUPMA12"
    ET.SubElement(question_answer, "YesNoCd").text = "No"

    # InsuredOrPrincipal Section
    insured_or_principal = ET.SubElement(pers_auto_policy, "InsuredOrPrincipal")
    general_party_info = ET.SubElement(insured_or_principal, "GeneralPartyInfo")
    name_info = ET.SubElement(general_party_info, "NameInfo")
    person_name = ET.SubElement(name_info, "PersonName")
    ET.SubElement(person_name, "Surname").text = data["insured"]["last_name"]
    ET.SubElement(person_name, "GivenName").text = data["insured"]["first_name"]
    ET.SubElement(person_name, "OtherGivenName").text = ""
    communications = ET.SubElement(general_party_info, "Communications")
    phone_info = ET.SubElement(communications, "PhoneInfo")
    ET.SubElement(phone_info, "PhoneTypeCd").text = "Phone"
    ET.SubElement(phone_info, "CommunicationUseCd").text = "Home"
    ET.SubElement(phone_info, "PhoneNumber").text = data["insured"]["phone"]
    email_info = ET.SubElement(communications, "EmailInfo")
    ET.SubElement(email_info, "CommunicationUseCd").text = "Day"
    ET.SubElement(email_info, "EmailAddr").text = data["insured"]["email"]
    addr = ET.SubElement(general_party_info, "Addr")
    ET.SubElement(addr, "AddrTypeCd").text = "StreetAddress"
    ET.SubElement(addr, "Addr1").text = data["insured"]["address"]["street"]
    ET.SubElement(addr, "Addr2").text = ""
    ET.SubElement(addr, "City").text = data["insured"]["address"]["city"]
    ET.SubElement(addr, "StateProvCd").text = data["insured"]["address"]["state"]
    ET.SubElement(addr, "PostalCode").text = data["insured"]["address"]["postal_code"]
    ET.SubElement(addr, "County").text = data["insured"]["address"]["county"]
    insured_info = ET.SubElement(insured_or_principal, "InsuredOrPrincipalInfo")
    ET.SubElement(insured_info, "InsuredOrPrincipalRoleCd").text = "Insured"
    person_info = ET.SubElement(insured_info, "PersonInfo")
    ET.SubElement(person_info, "BirthDt").text = data["insured"]["birth_date"]
    ET.SubElement(person_info, "GenderCd").text = data["insured"]["gender"]

    # Location Section
    location = ET.SubElement(pers_auto_policy, "Location", id="Gar1")
    ET.SubElement(location, "ItemIdInfo")
    addr = ET.SubElement(location, "Addr")
    ET.SubElement(addr, "AddrTypeCd").text = "GaragingAddress"
    ET.SubElement(addr, "Addr1").text = data["insured"]["address"]["street"]
    ET.SubElement(addr, "Addr2").text = ""
    ET.SubElement(addr, "City").text = data["insured"]["address"]["city"]
    ET.SubElement(addr, "StateProvCd").text = data["insured"]["address"]["state"]
    ET.SubElement(addr, "PostalCode").text = data["insured"]["address"]["postal_code"]
    ET.SubElement(addr, "County").text = data["insured"]["address"]["county"]

    # Convert to string
    rough_string = ET.tostring(acord, encoding='utf-8')
    reparsed = minidom.parseString(rough_string)
    xml_str = reparsed.toprettyxml(indent="    ", encoding="utf-8").decode('utf-8')
    xml_str = '<?xml version="1.0" encoding="utf-8"?>\n' + xml_str.split('\n', 1)[1]
    logger.info(f"Generated XML: {xml_str}")
    return xml_str

# Function to refresh Zoho access token
def refresh_zoho_token(refresh_token, client_id, client_secret):
    url = "https://accounts.zoho.eu/oauth/v2/token"
    data = {
        "refresh_token": refresh_token,
        "client_id": client_id,
        "client_secret": client_secret,
        "grant_type": "refresh_token"
    }
    response = requests.post(url, data=data)
    response.raise_for_status()
    token_data = response.json()
    return token_data["access_token"]

def handler(request):
    app = zcatalyst_sdk.initialize()
    try:
        # Log the raw request body
        raw_body = getattr(request, 'data', b'').decode('utf-8') if hasattr(request, 'data') and hasattr(request.data, 'decode') else str(getattr(request, 'body', ''))
        logger.info(f"Raw request body: {raw_body}")
        # Attempt to parse JSON data
        quotepro_data = {}
        if raw_body:
            try:
                quotepro_data = json.loads(raw_body)
            except json.JSONDecodeError as e:
                logger.error(f"JSON decode error: {str(e)} with raw body: {raw_body}")
                return {
                    "status": 400,
                    "body": {
                        "status": "error",
                        "message": f"Invalid JSON payload: {str(e)}"
                    }
                }
        else:
            logger.error("No request body received")
            return {
                "status": 400,
                "body": {
                    "status": "error",
                    "message": "No request body received"
                }
            }
        logger.info(f"Parsed JSON data: {json.dumps(quotepro_data, indent=2)}")
        if not quotepro_data:
            raise ValueError("Empty or invalid JSON data received")
        xml_data = json_to_acord_xml(quotepro_data)
        url = "https://ratingqa.itcdataservices.com/webservices/imp/api/storage/savepolicy"
        headers = {
            "Content-Type": "application/json",
            "Accept-Encoding": "gzip, deflate"
        }
        auth = ("0443b34c-c7df-4239-a934-7c1f9c2f9989", "0443b34c-c7df-4239-a934-7c1f9c2f9989")
        body = {
            "InsuranceLine": "PA",
            "PolicyData": xml_data,
            "LockPolicyForUser": False,
            "OverrideExistingLock": True,
            "IncludeCompanyQuestions": False
        }
        logger.info(f"Sending to ITC with body: {json.dumps(body, indent=2)}")
        itc_response = requests.post(url, headers=headers, auth=auth, json=body)
        logger.info(f"ITC response status: {itc_response.status_code}")
        logger.info(f"ITC response headers: {dict(itc_response.headers)}")
        logger.info(f"ITC response text: {itc_response.text}")
        itc_response.raise_for_status()
        itc_response_data = itc_response.json()
        logger.info(f"ITC response data: {json.dumps(itc_response_data, indent=2)}")

        # Refresh Zoho access token
        client_id = "1000.W8GPUXOON80H4CRRM9X8205B19AWQY"
        client_secret = "a1e0ae4708cc94b62932cc6a3d9cd1a9ca2edeedab"
        refresh_token = "1000.5f6c3bf3d67eec16b4eb585cc1978a6e.77749487509425826b731e1fefc241e3"  # Your refresh token
        zoho_access_token = refresh_zoho_token(refresh_token, client_id, client_secret)

        # Store data in Zoho CRM QuotePro_Raw_Data module
        zoho_api_domain = "https://www.zohoapis.eu"
        zoho_module = "QuotePro_Raw_Data"
        zoho_url = f"{zoho_api_domain}/crm/v2/{zoho_module}"

        # Prepare data for Zoho CRM
        zoho_data = {
            "data": [
                {
                    "Quote_Pro_Data": json.dumps(quotepro_data, indent=2)  # Store raw JSON as Rich-Text
                }
            ]
        }
        zoho_headers = {
            "Authorization": f"Zoho-oauthtoken {zoho_access_token}",
            "Content-Type": "application/json"
        }
        logger.info(f"Sending to Zoho CRM with body: {json.dumps(zoho_data, indent=2)}")
        zoho_response = requests.post(zoho_url, headers=zoho_headers, json=zoho_data)
        logger.info(f"Zoho CRM response status: {zoho_response.status_code}")
        logger.info(f"Zoho CRM response text: {zoho_response.text}")
        zoho_response.raise_for_status()
        zoho_response_data = zoho_response.json()
        logger.info(f"Zoho CRM response data: {json.dumps(zoho_response_data, indent=2)}")

        return {
            "status": 200,
            "body": {
                "status": "success",
                "message": "Quote created successfully in ITC and stored in Zoho CRM",
                "itc_response": itc_response_data,
                "zoho_response": zoho_response_data
            }
        }
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        return {
            "status": 500,
            "body": {
                "status": "error",
                "message": f"Failed to process quote: {str(e)}"
            }
        }

if __name__ == "__main__":
    # For local testing
    quote_data = {
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
    xml_data = json_to_acord_xml(quote_data)
    url = "https://ratingqa.itcdataservices.com/webservices/imp/api/storage/savepolicy"
    headers = {
        "Content-Type": "application/json",
        "Accept-Encoding": "gzip, deflate"
    }
    auth = ("0443b34c-c7df-4239-a934-7c1f9c2f9989", "0443b34c-c7df-4239-a934-7c1f9c2f9989")
    body = {
        "InsuranceLine": "PA",
        "PolicyData": xml_data,
        "LockPolicyForUser": False,
        "OverrideExistingLock": True,
        "IncludeCompanyQuestions": False
    }
    try:
        response = requests.post(url, headers=headers, auth=auth, json=body)
        response.raise_for_status()
        print("Quote created successfully!")
        print("Response:", response.json())
    except requests.exceptions.RequestException as e:
        print("Failed to create quote:", str(e))
        if e.response is not None:
            print("Response:", e.response.text)