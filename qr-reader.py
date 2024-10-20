import cv2
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
        # Convert byte data to string
        qr_data = qr_code.data.decode('utf-8')

        # Print the decoded data
        print("Decoded QR Code Data:")
        print(qr_data)  # This is the URL string

        return qr_data  # Return the string directly

# Path to the QR code image
qr_code_image_path = "wallet_qr_code.png"

# Call the function to decode the QR code
decoded_data = decode_qr_code(qr_code_image_path)

# Print the result
if decoded_data:
    print("Decoded Data:", decoded_data)
