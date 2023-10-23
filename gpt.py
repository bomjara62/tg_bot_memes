

from PIL import Image, ImageDraw, ImageFont
img1 = Image.new('RGB', (512, 512), (255, 255, 255))
img2 = Image.open('4.png')
img3 = Image.open('cloudd.png')
res = img2.resize((350,400))
res.save('4.png')
img2 = Image.open('4.png')
img1.putalpha(0)
res = img3.resize((200,100))
res.save('cloudd.png')
img3 = Image.open('cloudd.png')
draw = ImageDraw.Draw(img3)
font = ImageFont.truetype("ofont.ru_Zametka Parletter.ttf", 18)
txt = str(input())
if len(txt) > 13:
    txt = txt[:13] + '...'
draw.text((10,30), f'{txt}', fill='black', font=font)
img1.paste(img2,(0, 100), mask=img2.convert('RGBA'))
img1.paste(img3,(300, 80), mask=img3.convert('RGBA'))
img1.show()
img1.save('draw-ellipse-rectangle-line.png')