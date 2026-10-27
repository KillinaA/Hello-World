import html
import json
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Hello World Motion Lab", page_icon="✨", layout="wide")

st.title("✨ Hello World Motion Lab")
st.caption("A beginner-friendly app for experimenting with names, fonts, backgrounds, and looping animations.")

with st.sidebar:
    st.header("Controls")
    name = st.text_input("Enter your name", value="Hello World", max_chars=80)
    font_family = st.selectbox(
        "Font type",
        ["Arial", "Courier New", "Georgia", "Times New Roman", "Verdana", "Trebuchet MS", "Impact", "Comic Sans MS"],
    )
    font_size = st.slider("Font size (px)", min_value=20, max_value=100, value=48, step=2)
    background = st.selectbox(
        "Background",
        ["Light", "Dark", "Ocean", "Sunset", "Forest", "Lavender", "Midnight"],
    )
    name_mode = st.selectbox("Name display mode", ["Centered", "Ticker Tape", "Repeated"])
    effect = st.selectbox(
        "Dynamic action",
        ["None", "Rain", "Snow", "Hail", "Wind Gust", "Confetti", "Tornado"],
    )
    speed = st.slider("Animation speed", min_value=0.5, max_value=3.0, value=1.5, step=0.25,
                      help="Lower values move more slowly; higher values move more quickly.")

themes = {
    "Light": ("#f7f8fc", "#171923", "#dfe7f5"),
    "Dark": ("#101116", "#ffffff", "#282b38"),
    "Ocean": ("#063b5b", "#f0fcff", "#087eaa"),
    "Sunset": ("#4a1942", "#fff7ef", "#e76f51"),
    "Forest": ("#163a2b", "#f3fff5", "#397653"),
    "Lavender": ("#eee7ff", "#33205c", "#d5c5ff"),
    "Midnight": ("#090d2b", "#f7f4ff", "#242b61"),
}
bg, fg, accent = themes[background]

# Escape user-provided text before placing it in HTML.
safe_name = html.escape(name.strip() or "Hello World")
safe_font = json.dumps(font_family)
duration = max(0.65, 4.0 / speed)

# Create repeated content for display modes. CSS animation drives motion entirely
# inside the embedded component, avoiding frequent Streamlit reruns.
if name_mode == "Repeated":
    display_content = " &nbsp; ✦ &nbsp; ".join([safe_name] * 5)
elif name_mode == "Ticker Tape":
    display_content = f"{safe_name} &nbsp; ✦ &nbsp; {safe_name} &nbsp; ✦ &nbsp; {safe_name}"
else:
    display_content = safe_name

effect_markup = ""
if effect != "None":
    particles = {
        "Rain": ("💧", 34, "fall"),
        "Snow": ("❄", 30, "fall"),
        "Hail": ("🧊", 26, "fall"),
        "Wind Gust": ("〰", 22, "wind"),
        "Confetti": ("🎉", 32, "confetti"),
        "Tornado": ("🌪", 18, "spin"),
    }
    symbol, count, animation = particles[effect]
    particle_items = []
    for i in range(count):
        left = (i * 37 + 11) % 100
        delay = -((i * 13) % 40) / 10
        size = 12 + (i * 7 % 20)
        drift = ((i * 17) % 81) - 40
        particle_items.append(
            f'<span class="particle p{i}" style="left:{left}%;animation-delay:{delay}s;'
            f'font-size:{size}px;--drift:{drift}px">{symbol}</span>'
        )
    effect_markup = f'<div class="effects {animation}" aria-hidden="true">{"".join(particle_items)}</div>'

mode_class = {
    "Centered": "centered",
    "Ticker Tape": "ticker",
    "Repeated": "repeated",
}[name_mode]

html_doc = f"""<!doctype html>
<html>
<head>
<meta charset="utf-8">
<style>
* {{ box-sizing: border-box; }}
html, body {{ margin: 0; padding: 0; }}
.stage {{
  position: relative; height: 590px; width: 100%; overflow: hidden;
  border-radius: 18px; background: {bg}; color: {fg};
  font-family: {safe_font}, sans-serif;
  border: 1px solid {accent};
  isolation: isolate;
}}
.stage::before {{
  content: ""; position: absolute; inset: 0; pointer-events: none; z-index: 0;
  background: radial-gradient(ellipse at 50% 0%, {accent}66, transparent 65%);
}}
.name-wrap {{
  position: absolute; z-index: 3; top: 50%; width: 100%;
  transform: translateY(-50%); font-size: {font_size}px; font-weight: 700;
  line-height: 1.25; text-shadow: 0 2px 12px #0002;
}}
.centered {{ text-align: center; padding: 20px; overflow-wrap: anywhere; }}
.ticker {{ white-space: nowrap; width: max-content; animation: marquee {duration * 3}s linear infinite; }}
.ticker span {{ display: inline-block; padding-left: 100vw; }}
.repeated {{ text-align: center; padding: 20px; overflow-wrap: anywhere; line-height: 1.8; }}
.effects {{ position: absolute; z-index: 1; inset: 0; overflow: hidden; pointer-events: none; }}
.particle {{ position: absolute; top: -12%; opacity: .86; user-select: none; }}
.fall .particle {{ animation: fall {duration * 2.5}s linear infinite; }}
.wind .particle {{ top: calc(8% + (var(--index, 0) * 1%)); animation: wind {duration * 2}s ease-in-out infinite; }}
.spin .particle {{ animation: spin {duration * 2.6}s linear infinite; }}
.confetti .particle {{ animation: confetti {duration * 2.7}s linear infinite; }}
.fall .particle:nth-child(3n) {{ animation-duration: {duration * 1.8}s; }}
.fall .particle:nth-child(3n + 1) {{ animation-duration: {duration * 3.1}s; }}
.confetti .particle:nth-child(odd) {{ font-size: 22px; }}
@keyframes fall {{ from {{ transform: translate3d(0,-20px,0) rotate(0); }} to {{ transform: translate3d(var(--drift),680px,0) rotate(300deg); }} }}
@keyframes wind {{ 0% {{ transform: translate(-20vw,0) rotate(0); }} 50% {{ transform: translate(50vw,35px) rotate(20deg); }} 100% {{ transform: translate(120vw,-15px) rotate(0); }} }}
@keyframes spin {{ 0% {{ transform: translateY(650px) rotate(0deg); }} 100% {{ transform: translateY(-80px) rotate(720deg); }} }}
@keyframes confetti {{ 0% {{ transform: translateY(-40px) rotate(0deg); }} 100% {{ transform: translateY(680px) rotate(800deg); }} }}
@keyframes marquee {{ from {{ transform: translateX(0); }} to {{ transform: translateX(-50%); }} }}
.footer {{ position: absolute; bottom: 14px; left: 0; width: 100%; text-align: center; z-index: 4;
  color: {fg}; opacity: .58; font: 12px Arial, sans-serif; letter-spacing: .08em; }}
@media (prefers-reduced-motion: reduce) {{
  .particle, .ticker {{ animation-duration: 20s !important; }}
}}
</style>
</head>
<body>
<div class="stage">
  {effect_markup}
  <div class="name-wrap {mode_class}">
    {('<span>' + display_content + '</span>') if name_mode == 'Ticker Tape' else display_content}
  </div>
  <div class="footer">HELLO WORLD MOTION LAB · CSS ANIMATIONS</div>
</div>
</body>
</html>"""

components.html(html_doc, height=610, scrolling=False)

st.markdown(
    "Tip: Try **Ticker Tape** with a long name, then switch backgrounds and effects. "
    "The animations run in the browser, so the page does not need to rerun continuously."
)
