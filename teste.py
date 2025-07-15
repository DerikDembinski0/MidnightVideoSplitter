from PIL import Image

img = Image.open("icone.png")
img.save("icone.ico", format='ICO')