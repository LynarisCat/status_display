from fastapi import FastAPI, Response
from PIL import Image
from .convert import imgToByte

app = FastAPI()


# Class to return the image as raw bytes
class RawResponse(Response):
    media_type = "binary/octet-stream"

    def render(self, content: bytearray) -> bytearray:
        return content



# functions for graphics

def left(pixels: Image.core.PixelAccess):
    pass


def middle(pixels: Image.core.PixelAccess):
    pass


def right(pixels: Image.core.PixelAccess):
    pass




@app.get("/status")
async def status():
    # ---------------------- Construct image
    img = bytearray()

    # load the template image
    with Image.open("assets/status-disp-template.png") as im:
        
        pixels = im.load()
        s = im.size

    # section left: build task overview
    left(pixels)

    # section middle: 
    middle(pixels)

    # section right: todays and tomorrows wheather
    right(pixels)

        
    # convert to bitmap
    img = imgToByte(pixels, s)

    im.show()


    # ---------------------- Return image
    return RawResponse(img)
