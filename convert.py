#!/usr/bin/env python3
import asyncio
from pyppeteer import launch
import sys
import os
from PIL import Image


if len(sys.argv) != 3:
    print('Usage: ./convert.py <input.html> <output.xyz>')
    sys.exit(0)

_HTML = os.path.dirname(os.path.realpath(__file__)) + "/" + sys.argv[1]
_OUTFILE = sys.argv[2]
sourcepath = 'file://' + _HTML


async def generate_pdf():
    browser = await launch()
    page = await browser.newPage()
    await page.goto(sourcepath, {'waitUntil': 'networkidle2'})
    await page.pdf({
      'path': _OUTFILE,
      'format': 'A3',
      'printBackground': True,
      'margin': {
        'top': 0,
        'bottom': 0,
        'left': 0,
        'right': 0
      }
    })
    await browser.close()


async def generate_png():
    browser = await launch()
    page = await browser.newPage()
    await page.goto(sourcepath)
    await page.screenshot({'path': _OUTFILE, 'fullPage': True})
    await browser.close()


if ".pdf" in _OUTFILE:
    asyncio.get_event_loop().run_until_complete(generate_pdf())
elif ".png" in _OUTFILE or ".jpg" in _OUTFILE:
    asyncio.get_event_loop().run_until_complete(generate_png())

filepath = input("Input file name\n> ")
im = Image.open(filepath)
width, height = im.size
if width != height:
    if width > height:
        new_height = width
        result = Image.new(im.mode, (width, new_height), (255, 255, 255))
        print(im.size)
        result.paste(im)
        print(im.size)
        result.save("output.png")
    elif height > width:
        new_width = height
        result =  Image.new(im.mode, (new_width, height), (255, 255, 255))
        print(im.size)
        result.paste(im)
        print(im.size)
        result.save("output.png")
im = Image.open(filepath)
width = int(input("Input desired width of image file\n> "))
height = int(input("Input desired height of image file\n> "))
im = im.resize((width, height))
im.show()
print("Input desired crop sizes")
x1 = int(input("X1: "))
y1 = int(input("Y1: "))
x2 = int(input("X2: "))
y2 = int(input("Y2: "))
im = im.crop((x1, y1, x2, y2))
output_name = input("Input desired image name\n> ")
im.save(output_name + ".png")
