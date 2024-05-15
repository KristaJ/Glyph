import svgwrite
import random


# path editor:  https://yqnn.github.io/svg-path-editor/

class Petal():
    def __init__(self, dwg, region, color=None, filter=None, opacity=.8):    

        if color:
            self.path = dwg.path(
                d=("M",(0,0)),
                fill=color,
                opacity=opacity,
                stroke_width="0",
                filter=filter.get_funciri(),
                style="mix-blend-mode:multiply"
            )      
        else:
            self.path = dwg.path(
                d=("M",(0,0)),
                fill="none",
                stroke="black",
                stroke_width="2"
            )
        for edge in self.petal_path(region):
            self.path.push(edge[0],edge[1])
            
    def rotate(self,angle):
        self.path.rotate(angle)
        
    def get_svg(self):
        return self.path
    
    def petal_path(self, region):
        petals_path = dict(
            a=[("M",(0, 0)),
              ("Q",(-30, 70, 30, 100)),
              ("Q",(40, 20, 0, 0))],
            c=[("M",(0,0)),
               ("Q",(100, 0, 100, 90)), 
               ("Q",(70, 30, 50, 50)), 
               ("Q",(30, 70, 90, 100)), 
               ("Q",(0, 100, 0, 0))],
            z=[("M",(0,0)),
              ("C",(50,0,50,60,0,100)),
              ("C",(-50,60,-50,0,0,0))],
           r=[("M",(0,0)),
              ("C",(50,35,50,65,0,100)),
              ("C",(-50,65,-50,35,0,0))],
           j=[("M",(0,15)),
              ("C",(25,15,25,0,25,0)),
              ("C",(35,0,50,60,0,100)), 
              ("C",(-50,60,-35,0,-25,0)),
              ("C",(-25,0,-25,15,0,15))],
           k=[("M",(0,0)),
              ("C",(50,40,50,100,0,100)),
              ("C",(-50,100,-50,40,0,0))],
           b=[("C",(50,40,50,70,20,100)),
              ("L",(0,85)),
              ("L",(-20,100)),
              ("C",(-50,70,-50,40,0,0))],
           s=[("M",(0,0)),
              ("S",(-50, 50, 0, 90)),
              ("S",(0, 33.333, 0, 0))],
           d=[("M",(0,0)),
              ("Q",(-20, 90, 0, 100)), 
              ("Q",(20, 90, 0, 0))],
           m=[("M",(0, 0)),
              ("Q",(-60, 100, 0, 80)),
              ("Q",(60, 100, 0, 0))],
                       )
        return petals_path[region]

class Glyph():
    def __init__(self, height:int=700, 
                       width:int=700):

        self.dwg = svgwrite.Drawing("custom", size=(height, width))
        self.blur_filter = self.dwg.defs.add(self.dwg.filter(x="-40%",width="180%",y="-40%",height="180%"))
        self.blur_filter.feGaussianBlur(in_='SourceGraphic', stdDeviation=2)

    def make_glyph(self,
                   nb_petals: int = None,
                   shape: str = None,
                   cm: list = None,
                   opacity: float = None
                   ):
        shape_list = ['a', 'z', 'r', 'j', 'k', 'b', 's', 'd', 'm']
        if nb_petals==None:
            nb_petals = random.randint(3,12)
        if shape==None:
            shape=random.choice(shape_list)
        if not cm:
            cm=[]
            for i in range(3):
                cm.append("#%06x" % random.randint(0, 0xFFFFFF))
        if opacity == None:
            opacity=random.uniform(.1, 1)

        self.g = self.dwg.add(self.dwg.g(id='g', fill='none',style="mix-blend-mode:hard-light"))
        self.g.translate(350,350)
        for i in range(nb_petals):
            color = Petal(self.dwg, shape, cm[i%len(cm)], self.blur_filter, opacity=opacity)
            color.rotate(i*360/nb_petals+random.randint(-4, 4))
            petal = Petal(self.dwg, shape)
            petal.rotate(i*360/nb_petals)
            self.g.add(petal.get_svg()) 
            self.g.add(color.get_svg())
        rand_scale = random.uniform(.3, 3)

        self.g.scale(rand_scale,rand_scale)



    def complete(self):
        self.dwg.save() 

    def get_svg_string(self):
        return self.dwg.tostring() 
