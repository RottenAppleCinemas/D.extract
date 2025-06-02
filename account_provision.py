import json
import re
import os
import subprocess
from datetime import datetime

def flexible_find(content, labels):
    lines = content.splitlines()
    for line in lines:
        for label in labels:
            pattern = rf"{label}\s*[:\-]\s*(.+)"
            match = re.match(pattern, line.strip(), re.IGNORECASE)
            if match:
                return match.group(1).strip()
    return ""

def parse_date(date_str):
    date_formats = ["%m/%d/%Y", "%m-%d-%Y", "%-m/%-d/%Y", "%-m-%-d-%Y", "%Y-%m-%d %H:%M:%S", "%Y-%m-%d"]
    for fmt in date_formats:
        try:
            dt = datetime.strptime(date_str, fmt)
            return dt.strftime("%m/%d/%Y")
        except Exception:
            continue
    return ""

def extract_first_last_name(full_name):
    parts = full_name.split()
    first = parts[0] if parts else ""
    last = " ".join(parts[1:]) if len(parts) > 1 else ""
    return first, last

def parse_email(file_path, field_map_path="field_map.json"):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    with open(field_map_path, 'r', encoding='utf-8') as map_file:
        field_map = json.load(map_file)

    data = {}
    for field, labels in field_map.items():
        data[field] = flexible_find(content, labels)

    # Handle contractAction default
    if not data.get("contractAction"):
        data["contractAction"] = "New"

    # Normalize geographic region
    if data.get("geographicRegion", "").strip().lower() in ["united states", "africa"]:
        data["geographicRegion"] = "Americas"

    # Extract first/last name from full name
    full_name = data.get("shipToName", "")
    first, last = extract_first_last_name(full_name)
    data["shipToFirstName"] = first
    data["shipToLastName"] = last

    # Dates
    today_str = datetime.now().strftime("%m/%d/%Y")
    start_date_str = today_str  # Fallback if no start date provided
    end_date_str = parse_date(data.get("rawEndDate", ""))
    if raw_start := data.get("rawStartDate"):
        parsed_start = parse_date(raw_start)
        if parsed_start:
            start_date_str = parsed_start

    # Quantity
    try:
        quantity = int(data.get("quantity", 0))
    except (ValueError, TypeError):
        quantity = 0

    # Build final JSON structure
    json_data = {
        "contractAction": data.get("contractAction", "New"),
        "customerType": data.get("customerType", ""),
        "geographicRegion": data.get("geographicRegion", ""),
        "accountName": data.get("accountName", ""),
        "salesForceFullAccountId": data.get("salesForceFullAccountId", ""),
        "shipToEmailAddress": data.get("shipToEmailAddress", ""),
        "shipToFirstName": data.get("shipToFirstName", ""),
        "shipToLastName": data.get("shipToLastName", ""),
        "skus": [
            {
                "sku": data.get("sku", ""),
                "startDate": start_date_str,
                "endDate": end_date_str,
                "quantity": quantity
            }
        ],
        "accountManagerEmail": data.get("accountManagerEmail", ""),
        "accountManagerName": data.get("accountManagerName", ""),
        "opportunity": data.get("opportunity", ""),
        "opportunityUrl": data.get("opportunity", ""),
        "quote": data.get("quote", ""),
        "quoteUrl": data.get("quote", "")
    }

    return json_data

if __name__ == "__main__":
    input_file = 'contract_email.txt'

    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()

    if re.search(r"Contract Action\s*[-:]?\s*Trial", content, re.IGNORECASE):
        print("Trial detected. Running trial_provision.py instead...")
        subprocess.run(["python", "trial_provision.py"], check=True)
        exit(0)

    if re.search(r"Trial Start Date|Trial End Date", content, re.IGNORECASE):
        print("Implicit trial detected. Running trial_provision.py instead...")
        subprocess.run(["python", "trial_provision.py"], check=True)
        exit(0)

    filled_data = parse_email(input_file)

    print(f"This '{filled_data['customerType']}' account name '{filled_data['accountName']}' has been successfully provisioned.\n")
    print(json.dumps(filled_data, indent=4))

    with open('output_filled.json', 'w', encoding='utf-8') as out_file:
        json.dump(filled_data, out_file, indent=4, ensure_ascii=False)

    print("\nRunning missing field scan...")
    try:
        subprocess.run(["python", "scan_missing_fields.py", 'output_filled.json'], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Missing field scanner failed with error: {e}")

print("\nJSON saved to: output_filled.json")

# Now run fill_missing_fields.py to interactively fill missing data
print("\nLaunching fill_missing_fields.py to update missing fields...")
try:
    subprocess.run(["python", "fill_missing_fields.py", "output_filled.json"], check=True)
except subprocess.CalledProcessError as e:
    print(f"fill_missing_fields.py failed with error: {e}")
