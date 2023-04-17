import base64
font = open("fonts/JetBrainsMono-Regular.ttf", "rb")
encoded_font = open("base64_encoded_font.txt", "wb")
encoded_font = base64.encode(font, output=encoded_font)