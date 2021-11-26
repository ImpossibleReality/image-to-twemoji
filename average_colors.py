import json
from PIL import Image
from colorthief import ColorThief

import os

def get_average_color(image):

    colour_tuple = [None, None, None, None]
    for channel in range(4):

        # Get data for one channel at a time
        pixels = image.getdata(band=channel)
        values = []
        for pixel in pixels:
            values.append(pixel)

        colour_tuple[channel] = sum(values) / len(values)
    return tuple(colour_tuple)

def getUnicode(filename):
    char_codepoints = filename.split('.')[0].split('-')
    char_codes = []

    for char in char_codepoints:
        code = int(char, base=16)
        if (code < 65536):
            char_codes.append(code)
        else:
            code -= 65536
            char_codes.append(55296 + (code >> 10))
            char_codes.append(56320 + (code & 1023))

    b = bytes([x for c in char_codes for x in c.to_bytes(2, 'little')])

    return b.decode('utf-16')

emoji_data = []
for filename in os.listdir("./twemojis"):
    img = Image.open(os.path.join('./twemojis', filename)).convert("RGBA")

    average_color = get_average_color(img)
    if average_color[3] < 110:
        continue
    dominant_color = ColorThief(img).get_color()

    emoji_data.append({
        "color": (round((dominant_color[0]*2 + average_color[0])/3), round((dominant_color[1]*2 + average_color[1])/3),round((dominant_color[2]*2 + average_color[2])/3)),
        "name": getUnicode(filename),
        "filename": filename
    })
with open('./emoji_data.json', 'w+') as data_file:
    json.dump(emoji_data, data_file)