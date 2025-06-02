import json
import os

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def prompt_user_to_fill(data):
    modified = False

    def is_missing(value):
        return value == "" or (isinstance(value, list) and not value)

    missing_fields = [
        key for key in data
        if key not in ["skus"] and is_missing(data[key])
    ]

    if "skus" in data and isinstance(data["skus"], list):
        for i, sku_entry in enumerate(data["skus"]):
            for k, v in sku_entry.items():
                if is_missing(v):
                    clear_screen()
                    print(json.dumps(data, indent=4, ensure_ascii=False))
                    user_input = input(f"\nEnter value for skus[{i}]['{k}']: ").strip()
                    if user_input:
                        data["skus"][i][k] = user_input
                        modified = True

    for field in missing_fields:
        clear_screen()
        print(json.dumps(data, indent=4, ensure_ascii=False))
        user_input = input(f"\nEnter value for '{field}': ").strip()
        if user_input:
            data[field] = user_input
            modified = True

    return data if modified else None

if __name__ == "__main__":
    input_file = "output_filled.json"

    if not os.path.exists(input_file):
        print(f"File '{input_file}' not found.")
        exit(1)

    with open(input_file, 'r', encoding='utf-8') as f:
        json_data = json.load(f)

    updated = prompt_user_to_fill(json_data)

    clear_screen()
    if updated:
        with open(input_file, 'w', encoding='utf-8') as f:
            json.dump(json_data, f, indent=4, ensure_ascii=False)

        print("Updated JSON:\n")
        print(json.dumps(json_data, indent=4, ensure_ascii=False))
        print("\nMissing fields updated and saved to 'output_filled.json'.")
    else:
        print("No missing fields or no updates made.")
