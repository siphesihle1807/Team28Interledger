import qrcode
import json

# JSON data to encode
wallet_data = {
    "assetCode": "USD",
    "assetScale": 2,
    "authServer": "https://rafiki.money/auth",
    "balance": 100.0,
    "id": "https://rafiki.money/alice",
    "publicName": "Alice",
    "resourceServer": "https://rafiki.money/op"
}

# Convert JSON data to a string
json_data = json.dumps(wallet_data)

# Create a QR code from the JSON string
qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_L,
    box_size=10,
    border=4,
)
qr.add_data(json_data)
qr.make(fit=True)

# Generate the QR code image
img = qr.make_image(fill='black', back_color='white')

# Save the QR code as an image file
img.save("wallet_qr_code.png")

print("QR code generated and saved as wallet_qr_code.png")

