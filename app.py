# -------------------------------
# IMPORTS
# -------------------------------
import streamlit as st
import random
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
import time

# -------------------------------
# PAGE CONFIG
# -------------------------------
st.set_page_config(page_title="Cyber Command Center", layout="wide")

# -------------------------------
# SESSION STATE
# -------------------------------
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "user_input" not in st.session_state:
    st.session_state.user_input = ""

if "report_status" not in st.session_state:
    st.session_state.report_status = None

if "status_time" not in st.session_state:
    st.session_state.status_time = None

if "alerts" not in st.session_state:
    st.session_state.alerts = []

# -------------------------------
# CSS
# -------------------------------
st.markdown("""
<style>
.stApp { background-color: #020617; color: #00ffff; font-family: monospace; }

/* RADAR */
@keyframes spin { from {transform:rotate(0);} to {transform:rotate(360deg);} }

.radar {
    width:260px;height:260px;border-radius:50%;
    border:2px solid #00ff00;
    position:relative;
    background:radial-gradient(circle,#001a00,black);
    overflow:hidden;margin:auto;
}

.sweep {
    position:absolute;width:100%;height:100%;
    border-radius:50%;
    background:conic-gradient(rgba(0,255,0,0.35),transparent);
    animation:spin 6s linear infinite;
}

.center {
    width:6px;height:6px;background:#00ff00;border-radius:50%;
    position:absolute;top:50%;left:50%;
    transform:translate(-50%,-50%);
}

.radar::before,.radar::after {
    content:"";position:absolute;background:rgba(0,255,0,0.25);
}
.radar::before {width:100%;height:1px;top:50%;}
.radar::after {width:1px;height:100%;left:50%;}

.ring {position:absolute;border:1px solid rgba(0,255,0,0.25);border-radius:50%;}
.ring1 {width:70px;height:70px;top:50%;left:50%;transform:translate(-50%,-50%);}
.ring2 {width:140px;height:140px;top:50%;left:50%;transform:translate(-50%,-50%);}
.ring3 {width:210px;height:210px;top:50%;left:50%;transform:translate(-50%,-50%);}

@keyframes orbit {
    from { transform: rotate(0deg) translateX(90px) rotate(0deg); }
    to { transform: rotate(360deg) translateX(90px) rotate(-360deg); }
}

.target1 {
    position:absolute;top:50%;left:50%;
    font-size:18px;
    animation:orbit 40s linear infinite;
}

.alert-box {
    padding:8px;margin-bottom:6px;border-radius:6px;background:#111;
}
</style>
""", unsafe_allow_html=True)

# -------------------------------
# HEADER
# -------------------------------
now = datetime.now()

st.markdown(f"<div style='text-align:right;'>📅 {now}</div>", unsafe_allow_html=True)

st.markdown("""
<marquee>
📰 LIVE NEWS: <a href="https://www.bbc.com/watch-live-news" target="_blank">▶ BBC Live</a>
| 🚨 Cyber Threat Level HIGH
</marquee>
""", unsafe_allow_html=True)

st.markdown("<h1 style='text-align:center;'>🛰️ CYBER COMMAND CENTER</h1>", unsafe_allow_html=True)

# -------------------------------
# DATA
# -------------------------------
countries = ["USA","China","Russia","India","Germany","UK"]
attacks = ["DDoS","Phishing","Malware"]

coords = {
    "USA": (37.09, -95.71),
    "India": (20.59, 78.96),
    "China": (35.86, 104.19),
    "Russia": (61.52, 105.31),
    "Germany": (51.16, 10.45),
    "UK": (55.37, -3.43)
}

def generate_attack():
    return {
        "source": random.choice(countries),
        "target": random.choice(countries),
        "attack": random.choice(attacks),
        "ip": f"192.168.{random.randint(1,255)}.{random.randint(1,255)}",
        "speed": random.randint(100,900)
    }

# INIT ALERTS
if not st.session_state.alerts:
    st.session_state.alerts = [generate_attack() for _ in range(5)]

data = [generate_attack() for _ in range(25)]
df = pd.DataFrame(data)

# 🎨 COLOR MAP
attack_colors = {
    "DDoS": "#ff0040",
    "Phishing": "#ffd700",
    "Malware": "#00ff9f"
}

# -------------------------------
# LAYOUT
# -------------------------------
col1, col2 = st.columns([3,1])

# ===============================
# MAP + RADAR
# ===============================
with col1:

    fig = go.Figure()

    for row in data:
        s = coords[row["source"]]
        t = coords[row["target"]]
        color = attack_colors[row["attack"]]

        fig.add_trace(go.Scattergeo(
            lon=[s[1], t[1]],
            lat=[s[0], t[0]],
            mode='lines',
            line=dict(width=3, color=color),
            opacity=0.9
        ))

        fig.add_trace(go.Scattergeo(
            lon=[s[1]], lat=[s[0]],
            mode='markers',
            marker=dict(size=7, color=color)
        ))

        fig.add_trace(go.Scattergeo(
            lon=[t[1]], lat=[t[0]],
            mode='markers',
            marker=dict(size=7, color="#00ffff")
        ))

    fig.update_layout(
        geo=dict(
            bgcolor='#020617',
            landcolor='#0a0a0a',
            showcountries=True,
            countrycolor='#00ffff'
        ),
        paper_bgcolor='#020617',
        height=450
    )

    st.plotly_chart(fig, use_container_width=True)

    st.subheader("🛰️ Satellite Scanner")

    st.markdown("""
    <div class="radar">
        <div class="sweep"></div>
        <div class="center"></div>
        <div class="ring ring1"></div>
        <div class="ring ring2"></div>
        <div class="ring ring3"></div>
        <div class="target1">🛰️</div>
    </div>
    """, unsafe_allow_html=True)

    st.subheader("📊 Attack Distribution")
    st.plotly_chart(px.pie(df, names="attack"), use_container_width=True)

# ===============================
# SIDE PANEL
# ===============================
with col2:

    st.subheader("⚠️ Live Alerts")

    for a in st.session_state.alerts:
        st.markdown(f"<div class='alert-box'>🚨 {a['attack']} {a['source']} → {a['target']}</div>", unsafe_allow_html=True)

    if st.button("🔁 Refresh Alerts"):
        st.session_state.alerts = [generate_attack() for _ in range(5)]
        st.rerun()

    # CHAT
    st.subheader("💬 Report Center")

    if st.session_state.chat_history:
        st.markdown(f"📨 {st.session_state.chat_history[0]['text']}")

    st.text_input("Enter message", key="user_input")
    file = st.file_uploader("Attach file")

    if st.button("📤 Send"):
        if st.session_state.user_input or file:

            st.session_state.chat_history = [{
                "text": st.session_state.user_input if st.session_state.user_input else "File uploaded"
            }]

            st.session_state.user_input = ""
            st.session_state.report_status = "processing"
            st.session_state.status_time = time.time()

            st.rerun()

    # STATUS FLOW
    if st.session_state.report_status:

        elapsed = time.time() - st.session_state.status_time

        if st.session_state.report_status == "processing":
            st.info("📡 Report received. Processing...")

            if elapsed > 2:
                st.session_state.report_status = "success"
                st.session_state.status_time = time.time()
                st.rerun()

        elif st.session_state.report_status == "success":
            st.success("✅ Report received successfully")

            if elapsed > 2:
                st.session_state.report_status = None
                st.session_state.chat_history = []
                st.rerun()

# -------------------------------
# REFRESH
# -------------------------------
if st.button("🔄 Refresh Page"):
    st.rerun()