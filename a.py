import os
from PIL import Image

lst = os.listdir("./JPEG")

for i in lst:
    if i.endswith(".jpg"):
        img = Image.open('./JPEG/'+i)
        img = img.resize((51,51),Image.ANTIALIAS)
        img.save('./JPEG/'+i)
