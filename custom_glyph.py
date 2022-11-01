from assets.glyph import Petal
import svgwrite
import math
from cairosvg import svg2png
import random
import argparse, sys


# path editor:  https://yqnn.github.io/svg-path-editor/

color_names =['#EC7E66',
           '#E65C75',
           '#A1DAD4',
           '#567FBF',
           '#63A2D7',
           '#7DD2EF',
           '#9AD8E3',
           '#F7EFBA',
           '#EE9963',
           '#C4A2C2',
           '#B8DDB1']


shape_list = ['a', 'z', 'r', 'j', 'k', 'b', 's', 'd', 'm']

def main(nb_petals = 5, shape="a", size=1, cm=['#9AD8E3', '#C4A2C2', '#EC7E66'], filename="custom.png", opacity=.8):
    dwg = svgwrite.Drawing("./images/custom.svg", size=(u'500', u'500'))
    blur_filter = dwg.defs.add(dwg.filter(x="-40%",width="180%",y="-40%",height="180%"))
    blur_filter.feGaussianBlur(in_='SourceGraphic', stdDeviation=2)
    g = dwg.add(dwg.g(id='g', fill='none',style="mix-blend-mode:hard-light"))

        #move the group to the next spot
    g.translate(250,250)

    for i in range(nb_petals):
        color = Petal(dwg, shape ,cm[i%len(cm)], blur_filter, opacity=opacity)
        color.rotate(i*360/nb_petals+random.randint(-4, 4))
        petal = Petal(dwg, shape)
        petal.rotate(i*360/nb_petals)
        g.add(petal.get_svg()) 
        g.add(color.get_svg())
    g.scale(size,size)

    dwg.save()
    # svg2png(bytestring=dwg.tostring(),write_to=f"./images/{filename}")

if __name__ == "__main__":
    parser=argparse.ArgumentParser()
    # nb_petals = 5, shape="a", size=1, cm=['#9AD8E3', '#C4A2C2', '#EC7E66'], filename="custom.png"
    parser.add_argument('--nb_petals', 
                        '-n', 
                        help="number of petals", 
                        type= int,
                        default=random.randint(3,20))
    parser.add_argument('--shape', '-s', help="letter corresponding to petal shape", type= str,
                        default = random.choice(shape_list))
    parser.add_argument('--size', '-z', help="scaler", type= float,
                        default=1 + random.random())
    parser.add_argument('--color_map', '-c', nargs="*", help="list of colors", type= str,
                         default=[])
    parser.add_argument('--filename', '-f', help="filename to save image to", type= str,
                        default="custom.png")
    parser.add_argument('--opacity', 
                        '-o', 
                        help="fill opacity", 
                        type= float,
                        default=random.randint(4,10)/10)

    args = parser.parse_args()

    if args.opacity > 1:
        print("ERROR: opacity can not be greater than 1.  Opacity set to default of 0.8")
        args.opacity = .8
    if args.nb_petals < 1:
        print("ERROR: number of petals must be greater than 0.  Number of petals set to default of 8")
        args.nb_petals=8
    
    if args.color_map==[]:
        for i in range(random.randint(2,3)):
            args.color_map.append("%06x" % random.randint(0, 0xFFFFFF))
        args.opacity = random.randint(4,10)/10
    args.color_map = [f"#{x}" for x in args.color_map]
    main(args.nb_petals, args.shape, args.size, args.color_map, args.filename, args.opacity)
