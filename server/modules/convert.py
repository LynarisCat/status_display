from PIL import Image


def imgToByte(pix: Image.core.PixelAccess, size: (int, int)) -> bytearray:
    by = bytearray()
    c = 0
    bit = ""

    for y in range(size[1]):
        for x in range(size[0]):
            
            if c >= 4:
                c = 1
                by += int(bit, 2).to_bytes(len(bit) // 8, byteorder='big')
                bit = ""

            else:
                c += 1
    
            match pix[x,y]:
                case 0:
                    bit += "00"

                case 64:
                    bit += "10"

                case 192:
                    bit += "01"
    
                case 255:
                    bit += "11"

                case default:
                    pass

    if bit:
        bit = bit.ljust(8, "0")
        by += int(bit, 2).to_bytes(1, byteorder='big')


    # print(len(by))

    return by

   
if __name__ == "__main__":

    with Image.open("status-disp-idea.png") as im:
        by = imgToByte(im.load(), im.size)

    with open("status-disp-idea.bytes", "wb") as f:
        f.write(by)



