import html
import random
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Hello World Motion Lab", layout="wide")
st.title("Hello World Motion Lab")
st.caption("Personalize your name and animate the scene.")

with st.sidebar:
    st.header("Controls")
    name = st.text_input("Enter your name", "Hello World")
    font = st.selectbox("Font type", ["Arial", "Courier New", "Georgia", "Times New Roman", "Verdana", "Trebuchet MS", "Impact"])
    size = st.slider("Font size (px)", 20, 100, 48)
    bg = st.selectbox("Background", ["Light", "Dark", "Sky", "Sunset", "Forest"])
    mode = st.selectbox("Name display mode", ["Centered", "Ticker Tape", "Repeated"])
    effect = st.selectbox("Dynamic action", ["None", "Rain", "Snow", "Hail", "Wind", "Confetti", "Tornado"])
    speed = st.slider("Animation speed", 1, 20, 8)
    amount = st.slider("Effect amount", 15, 140, 65)

colors = {
    "Light": ("#ffffff", "#171717"), "Dark": ("#10121b", "#ffffff"),
    "Sky": ("#dff4ff", "#123c5a"), "Sunset": ("#ffdfd2", "#542344"),
    "Forest": ("#173b2c", "#f0fff4")
}
background, foreground = colors[bg]
safe_name = html.escape(name or "Hello World")
symbols = {"Rain":"💧", "Snow":"❄", "Hail":"🧊", "Wind":"〰", "Confetti":"🎉", "Tornado":"🌪", "None":""}
symbol = symbols[effect]
rng = random.Random(f"{name}|{effect}|{amount}|{speed}")
particles = []
for _ in range(amount if effect != "None" else 0):
    left, delay = rng.randint(0,100), rng.uniform(-12,0)
    duration = rng.uniform(5,14) / (speed/8)
    size_px, drift = rng.randint(12,30), rng.randint(-120,120)
    particles.append(f'<span class="particle" style="left:{left}%;animation-delay:{delay:.2f}s;animation-duration:{duration:.2f}s;font-size:{size_px}px;--drift:{drift}px">{symbol}</span>')
particle_html = "".join(particles)

if mode == "Ticker Tape":
    name_html = f'<div class="ticker"><div class="track">{safe_name} ✦ {safe_name} ✦ {safe_name}</div></div>'
elif mode == "Repeated":
    name_html = '<div class="repeated">' + "<br>".join([safe_name]*6) + "</div>"
else:
    name_html = f'<div class="center-name">{safe_name}</div>'

doc = f"""<!doctype html><html><head><meta charset="utf-8"><style>
*{{box-sizing:border-box}} body{{margin:0;font-family:{font},sans-serif}}
.scene{{position:relative;height:620px;overflow:hidden;border-radius:18px;background:{background};color:{foreground};padding:36px}}
.effects{{position:absolute;inset:0;overflow:hidden;pointer-events:none}}
.particle{{position:absolute;top:-60px;opacity:.86;animation:fall linear infinite;filter:drop-shadow(0 1px 2px #0002)}}
@keyframes fall{{0%{{transform:translate3d(0,-8vh,0) rotate(0)}}100%{{transform:translate3d(var(--drift),115vh,0) rotate(720deg)}}}}
.center-name{{position:relative;z-index:2;text-align:center;font-weight:800;font-size:{size}px;overflow-wrap:anywhere;padding-top:190px}}
.repeated{{position:relative;z-index:2;text-align:center;font-weight:800;font-size:{size}px;line-height:1.25;overflow-wrap:anywhere}}
.ticker{{position:relative;z-index:2;margin-top:240px;overflow:hidden;white-space:nowrap;font-size:{size}px;font-weight:800}}
.track{{display:inline-block;padding-left:100%;animation:marquee {max(7,36-speed)}s linear infinite}}
@keyframes marquee{{from{{transform:translateX(0)}}to{{transform:translateX(-100%)}}}}
</style></head><body><div class="scene"><div class="effects">{particle_html}</div>{name_html}</div></body></html>"""
components.html(doc, height=640, scrolling=False)
st.info("The selected effect loops continuously in the preview.")
