import json
import sys

def scan_missing_fields(data, prefix=""):
    missing = []

    if isinstance(data, dict):
        for key, value in data.items():
            full_key = f"{prefix}{key}"
            if value is None or value == "" or (isinstance(value, list) and len(value) == 0):
                missing.append(full_key)
            elif isinstance(value, list):
                # Scan inside list items (like skus)
                for idx, item in enumerate(value):
                    missing.extend(scan_missing_fields(item, prefix=f"{full_key}[{idx}]."))
            elif isinstance(value, dict):
                missing.extend(scan_missing_fields(value, prefix=f"{full_key}."))
    else:
        # If not dict, just check if empty or None
        if data is None or data == "":
            missing.append(prefix.rstrip('.'))

    return missing

def main(json_file_path):
    try:
        with open(json_file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        print(f"Error loading JSON file: {e}")
        sys.exit(1)

    missing_fields = scan_missing_fields(data)

    if missing_fields:
        print("Missing or empty fields found:")
        for field in missing_fields:
            print(f" - {field}")
    else:
        print("No missing or empty fields detected.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python scan_missing_fields.py <json_file_path>")
        sys.exit(1)

    main(sys.argv[1])
