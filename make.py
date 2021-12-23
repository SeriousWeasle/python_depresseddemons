from PIL import Image
import random
import colorsys
from tqdm import tqdm
import time

def mix(val, mul):
    r = int(val[0] * mul[0][0])
    g = int(val[1] * mul[0][1])
    b = int(val[2] * mul[0][2])
    a = int(val[3] * mul[1])
    
    return (r, g, b, a)

def getRand(min, max):
    val = random.random()

    scalar = max - min

    return (val * scalar) + min

def make():
    clothes = Image.open("./layers/clothes.png").convert("RGBA")
    eyes = Image.open("./layers/eyes.png").convert("RGBA")
    hair = Image.open("./layers/hair.png").convert("RGBA")
    lips = Image.open("./layers/lips.png").convert("RGBA")
    skin = Image.open("./layers/skin.png").convert("RGBA")

    layers = [clothes, eyes, hair, lips, skin]

    total = Image.new("RGBA", (32, 32), (0, 0, 0, 255))
    totalpx = total.load()

    cc = (colorsys.hsv_to_rgb(random.random(), random.random(), random.random()), 1)
    ec = (colorsys.hsv_to_rgb(random.random(), getRand(0.75, 1), getRand(0.75, 1)), 1)
    hc = (colorsys.hsv_to_rgb(getRand(0, 0.125), getRand(0, 0.75), getRand(0, 0.5)), 1)
    lc = (colorsys.hsv_to_rgb(random.random(), getRand(0.5, 1), getRand(0.5, 1)), 1)
    sc = (colorsys.hsv_to_rgb(random.random(), getRand(0.5, 1), getRand(0.75, 1)), 1)

    muls = [cc, ec, hc, lc, sc]

    for idx, l in enumerate(layers):

        px = l.load()
        for x in range(total.width):
            for y in range(total.height):
                if (px[x, y][3] != 0):
                    totalpx[x, y] = mix(px[x, y], muls[idx])

    bc = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255), 255)
    for x in range(total.width):
        for y in range(total.height):
            if (totalpx[x, y] == (0, 0, 0, 255)):
                totalpx[x, y] = bc
    total = total.resize((320, 320), Image.NEAREST)
    return total


gridX = 4
gridY = 4

complete = Image.new("RGBA", (gridX * 320, gridY * 320), (0, 0, 0, 0))

for gx in tqdm(range(gridX), desc="generating pain and suffering in PNG format"):
    for gy in range(gridY):
        panel = make()
        complete.paste(panel, (gx * 320, gy * 320))

complete.show()
complete.save("./output_%s.png" % str(time.time()))