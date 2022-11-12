
from PIL import Image
import os

def register_user(form_data):
    data = form_data.to_dict()

    im = Image.open("data['image_in'].png")
    print("The size of the image before conversion : ", end = "")
    print(os.path.getsize("data['image_in'].png"))
    
    # converting to jpg
    rgb_im = im.convert("RGB")
    
    
    # exporting the image
    image_out = rgb_im.save("data['image_in'].jpg")
    print("The size of the image after conversion : ", end = "")
    print(os.path.getsize("data['image_in'].jpg"))
    
    return image_out