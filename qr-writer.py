import qrcode

# URL to encode
wallet_data = "https://ilp.interledger-test.dev/cedeee60"

# Create a QR code from the URL
qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_L,
    box_size=10,
    border=4,
)
qr.add_data(wallet_data)  # Directly add the URL
qr.make(fit=True)

# Generate the QR code image
img = qr.make_image(fill='black', back_color='white')

# Save the QR code as an image file
img.save("wallet_qr_code.png")

print("QR code generated and saved as wallet_qr_code.png")
