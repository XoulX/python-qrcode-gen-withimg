import pyqrcode
from PIL import Image
import os

# Change the URL to the one you want to generate a QR code for
qrobj = pyqrcode.create('https://stackoverflow.com')
with open('test.png', 'wb') as f:
    qrobj.png(f, scale=100)


img = Image.open('test.png').convert('RGBA')
width, height = img.size
logo = Image.open('logo2.png').convert('RGBA')
logo_size = min(width, height) // 5 
xmin = (width - logo_size) // 2
ymin = (height - logo_size) // 2
logo = logo.resize((logo_size, logo_size))

# Change RGB value to appropriate background colour you want
background = Image.new('RGBA', (logo_size, logo_size), (255, 255, 255, 230))
img.paste(background, (xmin, ymin), background)
img.paste(logo, (xmin, ymin), logo)

# Save and show the result
os.remove("test.png")
img.save('qr.png')
img.show()