# Contract Email Parser and Provisioning

This Python script automates the extraction of contract details from email text files and generates a structured JSON output. It also integrates with related scripts to scan for missing fields and interactively fill them.

---

## Features

- Flexible label matching using a customizable field map (`field_map.json`)
- Supports multiple date formats and normalizes them to `MM/DD/YYYY`
- Extracts first and last names from full name fields
- Default handling of contract actions and geographic regions
- Detects trial contracts and runs a dedicated trial provisioning script
- Generates a JSON output file (`output_filled.json`)
- Integrates with auxiliary scripts to scan and fill missing fields

---

## Prerequisites

- Python 3.6+
- Dependencies: standard Python libraries (`json`, `re`, `datetime`, `subprocess`, `os`)

---

## Usage

1. Place the contract email text file as `contract_email.txt` in the script directory.

2. Customize your `field_map.json` file to map desired fields to possible labels in your emails.

3. Run the parser script:
   ```bash
   python parse_contract_email.py

# Simple Contract Email Parser

This Python script extracts essential contract and customer information from plain-text contract emails using regular expressions.

---

## Features

- Parses fields such as customer type, geographic region, account name, Salesforce ID, and contact emails
- Handles both separate and combined ship-to first and last names
- Defaults contract action to `"NEW"` for trial contracts
- Outputs parsed data as a JSON-formatted dictionary

---

## Prerequisites

- Python 3.x (no external dependencies required)

---

## Usage

1. Place your contract email text file as `contract_email.txt` in the same directory as the script.

2. Run the script:

   ```bash
   python simple_parse_contract_email.py

# JSON Missing Fields Scanner

This Python utility scans JSON files to identify missing or empty fields, including nested keys and list elements.

---

## Features

- Recursively checks all dictionary keys and list items
- Reports fields with empty strings, `None`, or empty lists
- Simple CLI interface accepting a JSON file path as input

---

## Prerequisites

- Python 3.x (no additional dependencies required)

---

## Usage

1. Run the script with the JSON file path as an argument:

   ```bash
   python scan_missing_fields.py output_filled.json

# Interactive JSON Missing Fields Filler

This Python script helps you interactively fill in missing or empty fields within a JSON file, including nested lists.

---

## Features

- Detects missing or empty string fields and empty lists
- Interactive CLI prompts for user input to update missing data
- Clears screen for cleaner user experience
- Saves updated JSON back to the original file

---

## Prerequisites

- Python 3.x (no external dependencies)

---

## Usage

1. Ensure your JSON file (default: `output_filled.json`) exists in the script’s directory.

2. Run the script:

   ```bash
   python fill_missing_fields.py

