import qrcode
from PIL import Image
import os

# Change the URL to the one you want to generate a QR code for
img = qrcode.make('https://www.youtube.com/channel/UCVHFbqXqoYvEWM1Ddxl0QDg')
type(img)

img = img.convert('RGBA')
width, height = img.size
logo = Image.open('logo.jpg').convert('RGBA')
logo_size = min(width, height) // 5 
xmin = (width - logo_size) // 2
ymin = (height - logo_size) // 2
logo = logo.resize((logo_size, logo_size))

# Change RGB value to appropriate background colour you want
background = Image.new('RGBA', (logo_size, logo_size), (255, 255, 255, 230))
img.paste(background, (xmin, ymin), background)
img.paste(logo, (xmin, ymin), logo)

# Save and show the result
img.save('qr.png')
img.show()