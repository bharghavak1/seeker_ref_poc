from flask import Flask, request, jsonify
import pytesseract
import cv2
import base64
import re

from PIL import Image
import tempfile
app = Flask(__name__)

#print("tesseract version",pytesseract.get_tesseract_version())
# print(pytesseract.get_tesseract_version()[0])
def preprocess_image(image_path):
    # Read the image
    image = cv2.imread(image_path)

    # Convert to grayscale
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Perform thresholding or other preprocessing steps as needed

    return gray_image

def extract_text_from_image(image_path):
    # Preprocess the image
    preprocessed_image = preprocess_image(image_path)

    # Use Pytesseract to extract text
    extracted_text = pytesseract.image_to_string(preprocessed_image)

    return extracted_text

def save_base64_image(image_base64):
    with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as temp:
        temp.write(base64.b64decode(image_base64))
        return temp.name

def extract_aadhar_details(text, type):
    data = {}
    # Define regular expressions for Aadhar number, name, address, etc.
    if type == 'pan':
        pan_number_pattern = r"[A-Z]{5}[0-9]{4}[A-Z]{1}"
        pan_dob_pattern = r"(\d{2})(\d{2})(\d{4})"  # PAN number pattern: 5 letters, 4 digits, 1 letter
        father_name_pattern = r"Father's Name[:\s]+(.+)"

        pan_number_match = re.search(pan_number_pattern, text)
        data["pan_number"] = pan_number_match.group() if pan_number_match else None

        # Extract father name
        father_name_match = re.search(father_name_pattern, text)
        data["father_name"] = father_name_match.group(1) if father_name_match else None

        # Extract date of birth
        pan_dob_match = re.search(pan_dob_pattern, text)
        data["pan_dob"] = "/".join(pan_dob_match.groups()[::-1]) if pan_dob_match else None

    elif type == 'aadhar':
        aadhar_number_pattern = r"\b\d{12}\b"  # Aadhar number pattern: exactly 12-digit number
        dob_pattern = r"(Date of Birth|DOB):?\s*(\d{2}/\d{2}/\d{4})"  # Date of birth pattern: Date of Birth: dd/mm/yyyy
        address_pattern = r"Address[:\s]+(.+)"
        gender_pattern = r"/\s*(Male|Female|Other)"  # Gender pattern: / Male, / Female, or / Other

        aadhar_number_match = re.search(aadhar_number_pattern, text)
        data['aadhar_number'] = aadhar_number_match.group(0) if aadhar_number_match else None

        dob_match = re.search(dob_pattern, text)
        data['dob'] = dob_match.group(2) if dob_match else None

        address_match = re.search(address_pattern, text)
        data['address'] = address_match.group(1) if address_match else None

        gender_match = re.search(gender_pattern, text)
        data['gender'] = gender_match.group(1) if gender_match else None

    name_pattern = r"Name[:\s]+(.+)"

    # Extract name
    name_match = re.search(name_pattern, text)
    data['name'] = name_match.group(1) if name_match else None

    # Extract address

    return data


@app.route('/extract-data', methods=['POST'])
def extract_data():
    try:
        data = request.json
        image_base64 = data.get("image")
        doc_type = data.get('doc_type')
        image_bytes = save_base64_image(image_base64)
        extracted_text = extract_text_from_image(image_bytes)
        extract_data = extract_aadhar_details(extracted_text, doc_type)
#         return jsonify({'name': name, 'add': address, 'dob': dob, 'gender': gender,
#          'aadhar_number': aadhar_number, 'pan_dob': pan_dob, 'pan_number': pan_number, 'father': father_name,
#
#           })
        return extract_data

    except Exception as e:
        print(e)
        return jsonify({"error": str(e)})

if __name__ == '__main__':
    app.run(debug=True)
