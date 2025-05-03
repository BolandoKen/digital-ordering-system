import PIL.Image
import PIL.ImageDraw
import PIL.ImageFont
from datetime import *;

def getImage_textBytes(myOrder = None, target_width = 384) :
    fontsize = 25
    font = "src/utils/CatPrinter/helvetica-255/Helvetica.ttf"
    fontbold = "src/utils/CatPrinter/helvetica-255/Helvetica-Bold.ttf"
    width = 400
    padded_width_end = 400 - 10
    padded_width_start = 5
    myOrder_orderid = myOrder["orderid"]
    myOrder_total = myOrder["total"]
    myOrder_itemsArr = myOrder["items"]
    myOrder_choice = myOrder["choice"]
    myOrder_name = myOrder["profile_name"]
    myOrder_date = myOrder["date"]

    starty = 15 # padding for top
    spacing = 7 # spacing of each row
    offset = 35 + starty - spacing # height of each row?

    footer_paddingbottom = 15

    height_orderid_header = 65 + offset
    list_height = offset * len(myOrder_itemsArr)
    # 15 is constant spacing for line header/footer
    height_totalchoice_footer = 65 + 15 + fontsize + footer_paddingbottom

    total_height = height_orderid_header + list_height + height_totalchoice_footer

    img = PIL.Image.new("RGBA", (width, total_height), (0xFF, 0xFF, 0xFF, 0xFF))
    draw = PIL.ImageDraw.Draw(img)

    draw.text((10, starty), f"{myOrder_name}", font=PIL.ImageFont.truetype(fontbold, fontsize), fill=(0x00, 0x00, 0x00))

    header_starty = starty + offset
    draw.line([(padded_width_start,header_starty), (padded_width_end, header_starty)], fill="black", width=3)
    draw.text((130, header_starty + 15), f"Order # {myOrder_orderid}", font=PIL.ImageFont.truetype(fontbold, fontsize), fill=(0x00, 0x00, 0x00))
    draw.line([(padded_width_start, header_starty + 50), (padded_width_end, header_starty + 50)], fill="black", width=3)
    # this header height is 65

    index = 3 # start list at 2 * offset 
    for itemTuple in myOrder_itemsArr :
        _, fname, oiquan, subtotal = itemTuple 
        y_coord = index * offset

        pricexfname = f"{oiquan}x {fname}"
        draw.text((10, y_coord), pricexfname, font=PIL.ImageFont.truetype(font, fontsize), fill=(0x00, 0x00, 0x00))
        draw.text((300, y_coord), f"₱{subtotal}", font=PIL.ImageFont.truetype(font, fontsize), fill=(0x00, 0x00, 0x00))
        index +=1
    finaly = index*offset
    draw.line([(padded_width_start, finaly), (padded_width_end, finaly)], fill="black", width=3)
    draw.text((10 , finaly + 15 ), f"Total amount ₱{myOrder_total}", font=PIL.ImageFont.truetype(fontbold, fontsize), fill=(0x00, 0x00, 0x00))
    draw.line([(padded_width_start,finaly + 50), (padded_width_end, finaly + 50)], fill="black", width=3)

    draw.text((10 , finaly + 50 +  15 ), f"{myOrder_choice}", font=PIL.ImageFont.truetype(fontbold, fontsize), fill=(0x00, 0x00, 0x00))
    draw.text((150, finaly + 50 +  15), f"{myOrder_date}", font=PIL.ImageFont.truetype(fontbold, fontsize), fill=(0x00, 0x00, 0x00))
    # should be 50 + font height of choice

    

    aspect_ratio = img.height / img.width
    target_height = int(target_width * aspect_ratio)
    img = img.resize((target_width, target_height))

# from werwolvs catprinter implementation : https://github.com/WerWolv/PythonCatPrinter/blob/master/text/print.py
    byte_rows = []
    for y in range(0, img.height): 
        bmp = []
        bit = 0
        # Turn RGBA8 line into 1bpp
        for x in range(0, img.width):
            if bit % 8 == 0:
                bmp += [0x00]
            r, g, b, a = img.getpixel((x, y))
            bmp[int(bit / 8)] >>= 1
            if (r < 0x80 and g < 0x80 and b < 0x80 and a > 0x80):
                bmp[int(bit / 8)] |= 0x80
            else:
                bmp[int(bit / 8)] |= 0
            bit += 1
        byte_rows.append(bytes(bmp))
    
    img.save("assets/temp/hi3.png") # for preview/debugging purposes
    return b"".join(byte_rows)


if __name__ == "__main__" :
    
    mock_obj = {'items': [(256, 'squid', 1, '35.00'), (256, 'Shrimp', 1, '45.00'), (256, 'crab', 1, '50.00'), (256, 'Clams', 1, '75.00'), (256, 'seaweed', 1, '123.00'), (256, 'seashells', 1, '99.00')], 'total': '427.00', 'orderid': 256, 'choice' : 'Dine in', "profile_name" : "Frieren's Bakeshop", "date" : datetime(2025, 5, 3, 14, 39, 38)}
    getImage_textBytes(mock_obj)