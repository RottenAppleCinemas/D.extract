import re

input_file = "contract_email.txt"
output_file = "contract_email_cleaned.txt"

# Keywords we want to split into new lines
field_labels = [
    "Account Name", "Customer Type", "Ship To", "Ship To Email", "Region", "Shipping Country",
    "SalesForce Full Account ID", "Opportunity", "Quote", "SKU", "Start Date", "End Date", "Quantity"
]

# Create a single regex to split them
split_pattern = re.compile(rf"({'|'.join(map(re.escape, field_labels))})\s*:")

with open(input_file, 'r', encoding='utf-8') as f:
    content = f.read()

# Ensure all fields begin on a new line
reformatted = split_pattern.sub(r"\n\1:", content)

# Remove extra newlines and leading/trailing whitespace
cleaned = "\n".join(line.strip() for line in reformatted.splitlines() if line.strip())

with open(output_file, 'w', encoding='utf-8') as f:
    f.write(cleaned)

print(f"Cleaned email saved to: {output_file}")
