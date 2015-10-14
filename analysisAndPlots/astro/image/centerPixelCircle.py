#
from PIL import Image, ImageDraw
image = Image.open('DSC_0031_NEF_embedded.jpg')
draw = ImageDraw.Draw(image)
r = 18 
x = 1936
y = 1296
draw.ellipse((x-r, y-r, x+r, y+r))
image.show()
