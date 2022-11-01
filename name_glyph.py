from assets.glyph import Petal
import svgwrite
import math
from cairosvg import svg2png
import random
import sys


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



def main(names):
    print(names)
    dwg = svgwrite.Drawing('_'.join(names.split()), size=(u'1000', u'500'))
    blur_filter = dwg.defs.add(dwg.filter(x="-40%",width="180%",y="-40%",height="180%"))
    blur_filter.feGaussianBlur(in_='SourceGraphic', stdDeviation=4)

    for j, name in enumerate(names.split()):
        g = dwg.add(dwg.g(id='g', fill='none',style="mix-blend-mode:hard-light"))

        #move the group to the next spot
        g.translate(120 + 220*(j%4), 120 + 220*(j//4))
        text = dwg.text(name, insert=(0,0),style = "font-size:17px; font-family:Arial")
        text.translate(120+(220*(j%4)) - (len(name)*10/2), 250 + 220*(j//4))
        dwg.add(text)

        nb_petals = 3+len(name)
        chunk_size = math.ceil(nb_petals/3)
        region = name[0].lower()
        flower_size = 0.5
        name_chunks = [name[i:i+chunk_size] for i in range(0, nb_petals, chunk_size)]
        colors = [sum([ord(y)for y in x]) for x in name_chunks]
        color_nums = []
        for num in colors:
            while len(str(num))>1:
                num = sum([int(x) for x in str(num)])
            color_nums.append(num)
        colors_pallette = [color_names[x] for x in color_nums]
    #     colors_pallette=["green", "blue", "pink"]

        for i in range(nb_petals):
            color = Petal(dwg, region,colors_pallette[i%len(colors_pallette)], blur_filter)
            color.rotate(i*360/nb_petals+random.randint(-4, 4))
            petal = Petal(dwg, region)
            petal.rotate(i*360/nb_petals)
            g.add(petal.get_svg()) 
            g.add(color.get_svg())
        g.scale((1+flower_size/6),(1+flower_size/6))

    filename = f"images/{'_'.join(names.split())}.png"
    svg2png(bytestring=dwg.tostring(),write_to=filename)

if __name__ == "__main__":
    main(sys.argv[1])
