import cv2
import json
from pyzbar.pyzbar import decode

# Function to decode QR code
def decode_qr_code(image_path):
    # Read the image using OpenCV
    img = cv2.imread(image_path)
    
    # Decode the QR code using pyzbar
    qr_codes = decode(img)
    
    if not qr_codes:
        print("No QR code found in the image.")
        return None
    
    for qr_code in qr_codes:
        # Convert byte data to string and load the JSON object
        qr_data = qr_code.data.decode('utf-8')
        wallet_data = json.loads(qr_data)

        # Print the decoded wallet information
        print("Decoded QR Code Data:")
        print(json.dumps(wallet_data, indent=4))

        return wallet_data

# Path to the QR code image
qr_code_image_path = "wallet_qr_code.png"

# Call the function to decode the QR code
decoded_data = decode_qr_code(qr_code_image_path)
