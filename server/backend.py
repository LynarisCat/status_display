from fastapi import FastAPI, Response
from PIL import Image, ImageFile, ImageDraw, ImageFont
from modules.convert import imgToByte
from modules.obsidian import getMonthData
import math
import os


current_dir = os.path.dirname(__file__)
font_path = os.path.join(current_dir, "assets", "slkscr.ttf")
font = ImageFont.truetype(font_path, 8)

app = FastAPI()


# Class to return the image as raw bytes
class RawResponse(Response):
    media_type = "binary/octet-stream"

    def render(self, content: bytearray) -> bytearray:
        return content



# functions for graphics ----------------------------------------------

def left(image: ImageFile):

    # TO-DO : move this definition and all spacings (px) to config
    start_offset_days = [5, 10]

    # TO-DO : CACHE DATA
    # create data from notes (new file)
    daily_data = getMonthData()
    #print(daily_data)

    # place day images and month names (./assets) from data
    img_days = []
    img_days.append( Image.open("assets/0_day.png") )
    img_days.append( Image.open("assets/1_day.png") )
    img_days.append( Image.open("assets/2_day.png") )
    img_days.append( Image.open("assets/3_day.png") )
   
    draw = ImageDraw.Draw(image)
    draw.fontmode = "1"

    for m in range(3):

        # 43px down every month
        start_offset_days[1] = 10 + 41 * m

        # place month names
        pos = (33, start_offset_days[1] - 8)
        draw.text(pos, daily_data[m][0][:3]+".", fill="black", font=font)

        # place day images
        for day, task_count in enumerate( reversed(daily_data[m][1]) ):

            

            # x: 7px per day; y: 7px per 7 days
            x = start_offset_days[0] + (7 * ( (day)%7 ))
            y = start_offset_days[1] + (7 * ( (day)//7 ))
            offset = ( x, y )


            # TO-DO : move this definition of bounderies to config
            # tc == 0 -> 0; tc <= 2 -> 1; tc <= 5 -> 2; tc >= 6 -> 3;
            match task_count:
                case 0:
                    img_d = img_days[0]
                case 1|2:
                    img_d = img_days[1]
                case 3|4|5:
                    img_d = img_days[2]
                case default:
                    img_d = img_days[3]

            #print(daily_data[m][0], day, task_count, offset)
            image.paste(img_d, box=offset)



            
            
            
    for img in img_days:
        img.close()



def middle(image: ImageFile):
    pass


def right(image: ImageFile):
    
    # get wheather data (temp + clouds/rain)

    # place temp

    # place wheather symbol (sun, cloud, rain, thunder)

    pass

# end of functions for graphics ----------------------------------------


@app.get("/status")
async def status():
    # ---------------------- Construct image
    img = bytearray()

    # load the template image
    with Image.open("assets/status-disp-template.png") as im:

        # section left: build task overview
        left(im)

        # section middle: 
        middle(im)

        # section right: todays and tomorrows wheather
        right(im)

        im = im.rotate(90, expand=True)

        pixels = im.load()

        s = im.size
        
    # convert to bitmap
    img = imgToByte(pixels, s)

    #im.show()


    # ---------------------- Return image
    return RawResponse(img)
