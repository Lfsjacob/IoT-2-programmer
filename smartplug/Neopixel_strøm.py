import board
import neopixel

n = 12
pixels = neopixel.NeoPixel(board.D18, n)
farver = {"rød" : (25, 0, 0),
          "grøn" : (0, 25, 0)}

def strøm_farve(farve, lader_med_sort_strøm):
    for i in range(n):
        pixels[i] = (0, 0, 0)
        if lader_med_sort_strøm == False:
            pixels[i] = farve
        elif lader_med_sort_strøm == True:
            if i % 2 == 0:
                pixels[i] = farve


strøm_farve(farver["rød"], True)