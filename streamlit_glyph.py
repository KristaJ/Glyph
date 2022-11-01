import streamlit as st
import base64
from assets import glyph

def render_svg(svg):
    b64 = base64.b64encode(svg.encode("utf-8")).decode("utf-8")
    html = r'<img src="data:image/svg+xml;base64,%s"/>' % b64
    return html

st.title('Glyph')
disable_download = False
svg_string = ""
# random_color = st.sidebar.checkbox("random color?", value=True)
# color=st.sidebar.color_picker("Choose the color for your blob", disabled=random_color)
# if random_color:
#     color=None
random_petals = st.sidebar.checkbox("random number of petals?", value=True)
number_petals = st.sidebar.slider("number of petals", min_value=2, max_value=12, disabled=random_petals)
if random_petals:
    number_petals=None

random_opacity = st.sidebar.checkbox("random opacity?", value=True)
opacity = st.sidebar.slider("Opacity?", min_value=0.0, max_value=1.0, disabled=random_opacity)
if random_opacity:
    opacity=None

random_colors = st.sidebar.checkbox("random colors?", value=True)
colors = st.sidebar.multiselect(
     'What are your favorite colors',
     ['green', 'yellow', 'red', 'blue', 'pink', 'aqua'],
     [],
     disabled=random_colors)
if random_colors:
    colors=None

random_shape = st.sidebar.checkbox("random petal shape?", value=True)
shape = st.sidebar.selectbox(
     'petal shape?',
     ('a', 'z', 'r', 'j', 'k', 'b', 's', 'd', 'm'),
     disabled=random_shape)
if random_shape:
    shape=None



if st.button("Make Glyph!"):
    g = glyph.Glyph(nb_petals=number_petals, opacity=opacity, cm=colors, shape=shape) 
    g.make_glyph()
    svg_string=g.get_svg_string()
    gly = render_svg(svg_string)
    st.write(gly, unsafe_allow_html=True)
    st.sidebar.download_button(
        label="Download Glyph",
        data=svg_string,
        file_name='glyph.svg',
        disabled = False
    )

