from fastapi import FastAPI, Response
from PIL import Image
from .convert import imgToByte

app = FastAPI()


# Class to return the image as raw bytes
class RawResponse(Response):
    media_type = "binary/octet-stream"

    def render(self, content: bytearray) -> bytearray:
        return content


@app.get("/status")
async def status():
    # ---------------------- Construct image

    # initalize the datatype to store the image as bytes (two bits per pixel)
    img = bytearray( int(( 296 * 128 ) / 4) )

    with Image.open("status-disp-idea.png") as im:
        print(im.format, im.size, im.mode)
        im.show()


    # ---------------------- Return image
    return RawResponse(img)
