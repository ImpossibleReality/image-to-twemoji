import json
from PIL import Image, ImageEnhance
import requests
from io import BytesIO
from math import sqrt

with open('./emoji_data.json') as file:
    data = json.load(file)

raw_img = Image.open(BytesIO(requests.get(input("Please input url to hosted image")).content)).convert("RGBA")

enhancer = ImageEnhance.Contrast(raw_img)

img = enhancer.enhance(1)

result = img.resize((14, 14), resample=Image.BOX)

def closest_color(r, g, b):
    color_diffs = []
    for item in data:
        if item.get("name") == "🦱":
            continue
        cr, cg, cb = item.get("color")
        color_diff = sqrt(abs(r - cr)**2 + abs(g - cg)**2 + abs(b - cb)**2)
        color_diffs.append((color_diff, item.get("name")))
    return min(color_diffs)[1]

def get_emoji_text():
    output = ""
    for x in range(result.height):
        for y in range(result.width):
            if y == 0:
                output += "\n"
            rgb = result.getpixel((y, x))
            r = rgb[0]
            g = rgb[1]
            b = rgb[2]
            a = rgb[3]
            if a < 20:
                output += "⬛"
                continue
            closeset_color = closest_color(r, g, b)
            output += closeset_color
    return output.split('\n')

txt = get_emoji_text()

print("\n".join(txt))

""" For 19x19 image
print("\n".join(txt[0:10]))

print("\n\n" + "\n".join(txt[10:19]))

print("\n\n" + txt[19])
"""