#Written by Thomas Norell
import PIL.Image
import random
import time
import math
import cmath
import imp
import datetime

def mapcolor(j,iterations,bandlength,shift=0):
    #(define col (/ (+ (sin (+ (* 4 3.1415 (- (+ (car val) 1) (/ (log (/ (/ (log (square_abs (cdr val))) 2) (log 2))) (log 2))) (/ 1 256) ) 512)) 1) 2))


    velocity = iterations - math.log(math.log(abs(j)+1)/math.log(2), 2)
    return int((math.sin(velocity*3.141592/32 + shift)+1)*256)


def iterate(f, coord, depth, count = 0 ):

    evaluation = f(coord)
    if not depth:
        return True, coord, count
    if abs(evaluation) >= 2:
        return False, coord, count
    return iterate(f, evaluation, depth - 1, count + 1)


def render_image(min_real, max_real, min_imag, max_imag, image_dim_imag, image_dim_real, depth, band_length, file_name, c):
    import sys
    sys.setrecursionlimit(depth * 1000)
    area = 0

    image = PIL.Image.new("RGB", (image_dim_real, image_dim_imag))
    for real_pixel in range(image_dim_real):
        real_coord = real_pixel * (max_real - min_real)/(image_dim_real-1)+min_real
        for imag_pixel in range(image_dim_imag):
            image_coord = imag_pixel * (max_imag - min_imag)/(image_dim_imag-1)+min_imag
            determination, j, count = iterate(lambda z: z*z + c, complex(real_coord, image_coord), depth)
            if determination:
                area += 1
                image.putpixel((real_pixel,imag_pixel),(0,0,0))
            else:

                #j = j + 1 - cmath.log(cmath.log(cmath.sqrt(real_coord ** 2 + image_coord ** 2))/cmath.log(2))
                #image.putpixel((real_pixel,imag_pixel),(255,255,255))
                image.putpixel((real_pixel, imag_pixel), (int(mapcolor(j,count,band_length)/2), int(mapcolor(j,count,band_length,3.1415/2)/2), mapcolor(j,count,band_length, 3.1415)))


    image.save(file_name,"GIF")
    print(area)
    return image



def make_animation():
    import imageio
    from numpy import array
    images = []


    for i in range(0,200):
        #print(i)

        #c = .7885*complex(math.cos(2*3.141592/800*i), math.sin(2*3.141592/800*i))
        #c = complex(math.cos(5/300*i*2*3.1415+3.141592/2), math.sin(4/300*i*2*3.141592))
        c = complex((2*math.cos(2*3.141592/200*i)-math.cos(2*2*3.141592/200*i))/4, (2*math.sin(2*3.141592/200*i)-math.sin(2*2*3.141592/200*i))/4)
        #c = complex(math.cos(2*3.141592/100*i)/4-1, math.sin(2*3.141592/100*i)/4)
        images.append(array(render_image(-2,2,-2,2,512,512,100,10,'test.gif',c)))

    imageio.mimsave('animation_cardiod.gif', images)
