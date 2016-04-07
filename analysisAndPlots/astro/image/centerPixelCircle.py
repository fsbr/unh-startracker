#
from PIL import Image, ImageDraw
image = Image.open('figimage.jpg')
draw = ImageDraw.Draw(image)

# change this when the calibration vs. when you're making hte thesis figure
r = 1450/2
x = 1936
y = 1296
draw.ellipse((x-r, y-r, x+r, y+r))
image.save('maxradius.png')
image.show()
