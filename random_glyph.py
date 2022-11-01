from wsgiref.simple_server import WSGIRequestHandler
from assets.glyph import Petal
import svgwrite
import math
from cairosvg import svg2png
import random
import sys



shapes = ['a', 'b', 'c']#, 'z', 'r', 'j', 'k', 's', 'd', 'm']
colors = ['#EC7E66',
           '#E65C75',
           '#A1DAD4',
           '#567FBF',
           '#63A2D7',
           '#7DD2EF',
           '#9AD8E3',
           '#F7EFBA',
           '#EE9963',
           '#C4A2C2',
           '#B8DDB1',
           '#52489C',
           '#4062BB',
           '#59C3C3',
           '#EBEBEB',
           '#F45B69']
              




width=1000
height=1000 
dwg = svgwrite.Drawing("./images/rand_glyph.svg", size=(width, height))
# dwg.add(dwg.rect(insert=(0, 0), size=(width, height), fill="white"))
blur_filter = dwg.defs.add(dwg.filter(x="-40%",width="180%",y="-40%",height="180%"))
blur_filter.feGaussianBlur(in_='SourceGraphic', stdDeviation=4)

num_glyph=5
wiggle=0
max_size=1
for j in range(num_glyph):
    g = dwg.add(dwg.g(id='g', fill='none',style="mix-blend-mode:hard-light"))
    dw = (1/(num_glyph**.5+1))*width
    dh = (1/(num_glyph**.5+1))*height
    dwidth=dw + (dw*(j%num_glyph**.5))
    dheight=dh + (dh*(j//num_glyph**.5))
    # add 10% wiggle
    wrand=dw*random.randint(wiggle*-1,wiggle)*.01
    hrand=dh*random.randint(wiggle*-1,wiggle)*.01

    g.translate(dwidth+wrand, dheight+hrand)
    # g.translate(random.random()*width, random.random()*height)

    nb_petals = random.randint(3,15)
    flower_size = random.randint(1,max_size)
    cm=random.sample(colors,3)
    shape = random.choice(shapes)
    for i in range(nb_petals):
        color = Petal(dwg, shape, cm[i%3], blur_filter, opacity=.7)
        color.rotate(i*360/nb_petals+random.randint(-4, 4))
        petal = Petal(dwg, shape)
        petal.rotate(i*360/nb_petals)
        g.add(petal.get_svg()) 
        g.add(color.get_svg())
    g.scale((flower_size, flower_size))
# filename = "./images/rand.png"
dwg.save()
# svg2png(bytestring=dwg.tostring(),write_to=filename)


