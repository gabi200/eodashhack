import cv2
import os
import json
import glob
import sys
from colorthief import ColorThief
from PIL import Image, ImageDraw

COLORS = (
    (31,48,57),
    (33,55,59),
    (69,70,71),
    (61,73,69),
    (83,72,77),
    (60,60,68),
    (118,97,93),
    (109,91,90),
    (255,255,255),
    (254,246,233) # todo finish
)

COLORS_HEX = ["#1f3039", "#21373b", "#454647", "#3d4945", "#53484d", "#3c3c44", "#76615d", "#6d5b5a",
             "#ffffff", "#fef6e9", "#78404b", "#5d5d60", "#72828a", "#203038", "#1a2a35"]

lista_patratele = []

def diff(h1, h2):
    def hexs_to_ints(s):
        return [int(s[i:i+2], 16) for i in range(1,7,2)]
    return sum(abs(i - j) for i, j in zip(*map(hexs_to_ints, (h1, h2))))

def get_closest_color(hex):
    results = []
    index = 0
    for item in COLORS_HEX:
        results.append(diff(hex, item))
    return COLORS_HEX[results.index(min(results))]

def rgb_to_hex(rgb):
    return '%02x%02x%02x' % rgb

def hex_to_rgb(hex):
    return tuple(int(hex[i:i+2], 16) for i in (0, 2, 4))

fisier = 'INPUT.png'
color = "black"
parts_folder = "out"
color_database = json.loads(open("culori.json").read())
reconstruct_image = False

img = cv2.imread(fisier)

if not os.path.exists(parts_folder):
    os.mkdir(parts_folder)

print("Welcome! Please select mode. (please run first mode, the run again the program and select the second mode.)")
print("The program will use the file named 'INPUT.png'")
print("1) Deconstruction and analysis")
print("2) Image reconstruction")
sel = input("Option: ")

if sel == "1":
    reconstruct_image = False
elif sel == "2":
    reconstruct_image = True
else:
    print("Invalid choice")
    sys.exit()

print("Processing, please wait... This might take a minute or two")

IMAGINE_FINALA_2 = Image.new('RGB', (1080,1080))

for r in range(0, img.shape[0], 30):
    for c in range(0, img.shape[1], 30):
        filename = "./out/img" + str(r) + "_" + str(c) + ".png"
        
        if reconstruct_image == False:
            cv2.imwrite(filename, img[r: r + 30, c: c + 30, :])

            color_thief = ColorThief(filename)
            dominant_color = color_thief.get_color(quality=1)
            color_hex = rgb_to_hex(dominant_color)

            for item in color_database:
                if type(color_database[item]) is list:
                    for i in color_database[item]:
                        current_hex = "#" + i
                        if get_closest_color(color_hex) == current_hex:
                            if item == "apa":
                                color = "blue"
                            if item == "teren_cultivat":
                                color = "purple"
                            if item == "teren_necultivat":
                                color = "brown"
                            if item == "grau":
                                color = "yellow"
                            if item == "cladire":
                                color = "red"
                            if item == "padure":
                                color = "green"

                            img_sec = Image.new('RGB',(30, 30), color)
                            img_sec = img_sec.save(filename)
                else:
                    if get_closest_color(color_hex) == color_database[item]:
                        if item == "nor":
                            color = "white"
                        if item == "pan_sol":
                            color = "cyan"

                    img_sec = Image.new('RGB',(30, 30), color)
                    img_sec = img_sec.save(filename)
        else:
            patratel = Image.open(filename)
            IMAGINE_FINALA_2.paste(patratel, (r, c))
            IMAGINE_FINALA_3 = IMAGINE_FINALA_2.save("OUTPUT.png")

if reconstruct_image == False:
    print("Stage 1 done. Run again and select option 2")
else:
    print("Stage 2 done. See OUTPUT.png")