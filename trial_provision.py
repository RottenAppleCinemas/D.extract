import json
import re

def extract_email_name(email):
    """Split an email into first and last name (best-effort)."""
    local_part = email.split('@')[0]
    parts = local_part.split('.')
    if len(parts) >= 2:
        first_name = parts[0].capitalize()
        last_name = parts[1].capitalize()
    else:
        first_name = parts[0].capitalize()
        last_name = ""
    return first_name, last_name

def parse_contract_email(file_path):
    data = {
        "contractAction": "NEW",  # Default to NEW for "Trial"
        "customerType": "",
        "geographicRegion": "",
        "accountName": "",
        "salesForceFullAccountId": "",
        "shipToEmailAddress": "",
        "shipToFirstName": "",
        "shipToLastName": "",
        "skus": [],
        "accountManagerEmail": "",
        "accountManagerName": "",
        "opportunity": "",
        "opportunityUrl": "",
        "quote": "",
        "quoteUrl": "",
        "comment": "TRIAL"
    }

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Normalize line endings
    content = content.replace('\r\n', '\n')

    # Regex pattern variants for each field (colon or hyphen)
    patterns = {
        "customerType": r"Customer Type[:\-]\s*(.+)",
        "geographicRegion": r"(?:Region|Geographic Region)[:\-]\s*(.+)",
        "accountName": r"Account Name[:\-]\s*(.+)",
        "salesForceFullAccountId": r"Salesforce Full Account ID[:\-]\s*(.+)",
        "shipToEmailAddress": r"Ship to Email Address[:\-]\s*(.+)",
        "accountManagerEmail": r"Account Manager Email[:\-]\s*(.+)",
        "accountManagerName": r"Account Manager Name[:\-]\s*(.+)",
        "contractAction": r"Contract Action[:\-]\s*(.+)"
    }

    for key, pattern in patterns.items():
        match = re.search(pattern, content, re.IGNORECASE)
        if match:
            data[key] = match.group(1).strip()

    # Extract first and last name if present separately
    first_name_match = re.search(r"Ship to First Name[:\-]\s*(.+)", content, re.IGNORECASE)
    last_name_match = re.search(r"Ship to Last Name[:\-]\s*(.+)", content, re.IGNORECASE)
    if first_name_match:
        data["shipToFirstName"] = first_name_match.group(1).strip()
    if last_name_match:
        data["shipToLastName"] = last_name_match.group(1).strip()

    # If names are not separate, try full name
    if not data["shipToFirstName"] or not data["shipToLastName"]:
        ship_to_name_match = re.search(r"Ship to Name[:\-]\s*(.+)", content, re.IGNORECASE)
        if ship_to_name_match:
            full_name = ship_to_name_match.group(1).strip()
            name_parts = full_name.split()
            if len(name_parts) >= 2:
                data["shipToFirstName"] = name_parts[0]
                data["shipToLastName"] = ' '.join(name_parts[1:])
            else:
                data["shipToFirstName"] = full_name
                data["shipToLastName"] = ""

    return data

# Example usage
output_data = parse_contract_email("contract_email.txt")
print(json.dumps(output_data, indent=4, ensure_ascii=False))
