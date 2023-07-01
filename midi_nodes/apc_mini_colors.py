import mathutils

apc_mini_color_palette = {
        "#000000" : 0,
        "#1E1E1E" : 1,
        "#7F7F7F" : 2,
        "#FFFFFF" : 3,
        "#FF4C4C" : 4,
        "#FF0000" : 5,
        "#590000" : 6,
        "#190000" : 7,
        "#FFBD6C" : 8,
        "#FF5400" : 9,
        "#591D00" : 10,
        "#271B00" : 11,
        "#FFFF4C" : 12,
        "#FFFF00" : 13,
        "#595900" : 14,
        "#191900" : 15,
        "#88FF4C" : 16,
        "#54FF00" : 17,
        "#1D5900" : 18,
        "#142B00" : 19,
        "#4CFF4C" : 20,
        "#00FF00" : 21,
        "#005900" : 22,
        "#001900" : 23,
        "#4CFF5E" : 24,
        "#00FF19" : 25,
        "#00590D" : 26,
        "#001902" : 27,
        "#4CFF88" : 28,
        "#00FF55" : 29,
        "#00591D" : 30,
        "#001F12" : 31,
        "#4CFFB7" : 32,
        "#00FF99" : 33,
        "#005935" : 34,
        "#001912" : 35,
        "#4CC3FF" : 36,
        "#00A9FF" : 37,
        "#004152" : 38,
        "#001019" : 39,
        "#4C88FF" : 40,
        "#0055FF" : 41,
        "#001D59" : 42,
        "#000819" : 43,
        "#4C4CFF" : 44,
        "#0000FF" : 45,
        "#000059" : 46,
        "#000019" : 47,
        "#874CFF" : 48,
        "#5400FF" : 49,
        "#190064" : 50,
        "#0F0030" : 51,
        "#FF4CFF" : 52,
        "#FF00FF" : 53,
        "#590059" : 54,
        "#190019" : 55,
        "#FF4C87" : 56,
        "#FF0054" : 57,
        "#59001D" : 58,
        "#220013" : 59,
        "#FF1500" : 60,
        "#993500" : 61,
        "#795100" : 62,
        "#436400" : 63,
        "#033900" : 64,
        "#005735" : 65,
        "#00547F" : 66,
        "#0000FF" : 67,
        "#00454F" : 68,
        "#2500CC" : 69,
        "#7F7F7F" : 70,
        "#202020" : 71,
        "#FF0000" : 72,
        "#BDFF2D" : 73,
        "#AFED06" : 74,
        "#64FF09" : 75,
        "#108B00" : 76,
        "#00FF87" : 77,
        "#00A9FF" : 78,
        "#002AFF" : 79,
        "#3F00FF" : 80,
        "#7A00FF" : 81,
        "#B21A7D" : 82,
        "#402100" : 83,
        "#FF4A00" : 84,
        "#88E106" : 85,
        "#72FF15" : 86,
        "#00FF00" : 87,
        "#3BFF26" : 88,
        "#59FF71" : 89,
        "#38FFCC" : 90,
        "#5B8AFF" : 91,
        "#3151C6" : 92,
        "#877FE9" : 93,
        "#D31DFF" : 94,
        "#FF005D" : 95,
        "#FF7F00" : 96,
        "#B9B000" : 97,
        "#90FF00" : 98,
        "#835D07" : 99,
        "#392b00" : 100,
        "#144C10" : 101,
        "#0D5038" : 102,
        "#15152A" : 103,
        "#16205A" : 104,
        "#693C1C" : 105,
        "#A8000A" : 106,
        "#DE513D" : 107,
        "#D86A1C" : 108,
        "#FFE126" : 109,
        "#9EE12F" : 110,
        "#67B50F" : 111,
        "#1E1E30" : 112,
        "#DCFF6B" : 113,
        "#80FFBD" : 114,
        "#9A99FF" : 115,
        "#8E66FF" : 116,
        "#404040" : 117,
        "#757575" : 118,
        "#E0FFFF" : 119,
        "#A00000" : 120,
        "#350000" : 121,
        "#1AD000" : 122,
        "#074200" : 123,
        "#B9B000" : 124,
        "#3F3100" : 125,
        "#B35F00" : 126,
        "#4B1502" : 127 }


def hexColorCodeToBlenderColor(hex_color):
    bcolor = mathutils.Color()
    bcolor.r = int(hex_color[1:3], 16) / 255.0
    bcolor.g = int(hex_color[3:5], 16) / 255.0
    bcolor.b = int(hex_color[5:7], 16) / 255.0
    return bcolor

def colorDistance(ca, cb):
    h_dist = abs(ca.h - cb.h)
    s_dist = abs(ca.s - cb.s)
    return h_dist + s_dist

def blenderColorToAPCMiniColor(target_color):
    min_dist = 10000.0
    min_col = 3
    for p_hex_col in apc_mini_color_palette:
        p_color = hexColorCodeToBlenderColor(p_hex_col)
        dist = colorDistance(target_color, p_color)
        if dist < min_dist:
            min_dist = dist
            min_col = apc_mini_color_palette[p_hex_col]
    return min_col





