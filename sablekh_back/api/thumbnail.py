import os
import sys
from PIL import Image
import subprocess
import mimetypes
from datetime import datetime
import binascii

def generate_thumbnail(choosen_file):
    file_type = mimetypes.MimeTypes().guess_type(choosen_file)[0]
    if file_type is not None:
        file_name = choosen_file.split("/")[-1]
        thumbnail_name = 'thumbnails/' +file_name.split(".")[0] + str(binascii.crc32(str(datetime.now()).encode())) + '.jpg'
        params = ['convert', choosen_file+'[0]', thumbnail_name]
        try:
            subprocess.check_call(params)
        except:
            return False
        return compress_image(thumbnail_name)
    else:
        return False
    
def compress_image(thumbnail_name):
    try:
        file_size = os.stat(thumbnail_name).st_size 
        if file_size/1024 > 50:
            picture = Image.open(thumbnail_name)
            picture.save(thumbnail_name,"JPEG",optimize=True,quality=60) 
    except:
        pass
    return thumbnail_name
    