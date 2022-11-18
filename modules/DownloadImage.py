from PIL import Image
import requests
from io import BytesIO

def DownloadImage(url,name):
    response = requests.get(url)
    img = Image.open(BytesIO(response.content))
#    img.save(f"emote2/{name}.png")
