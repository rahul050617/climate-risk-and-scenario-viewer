from docx import Document
import json

def parse_docx_to_json(docx_path):
    doc = Document(docx_path)
    data = {}
    current_sector = None
    current_block = None

    for para in doc.paragraphs:
        style = para.style.name
        text = para.text.strip()

        # Debug line (optional)
        print(f"[{style}] {text}")

        # Heading 2: Sector
        if style == "Heading 2" and text:
            current_sector = text
            data[current_sector] = {}
            current_block = None  # Reset inner block

        # Heading 3: Scenario or Risk Category
        elif style == "Heading 3" and current_sector and text:
            current_block = text
            data[current_sector][current_block] = []

        # Normal: Bullet Points or Description
        elif style == "Normal" and current_sector and current_block and text:
            data[current_sector][current_block].append(text)

    return data

def save_json(data, output_path):
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

# Example usage
docx_file = "Climate risk research.docx"
json_file = "default_scenarios.json"
parsed_data = parse_docx_to_json(docx_file)
save_json(parsed_data, json_file)
