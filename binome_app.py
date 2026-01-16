import streamlit as st
import os
import random
import time
from PIL import Image
import base64

# ---------------- CONFIG ----------------
IMAGE_FOLDER = "images"
SOUND_FILE = "sounds/shuffle.wav"
PLACEHOLDER_FOLDER = os.path.join("placeholders")
ANIMATION_LOOPS = 18
ANIMATION_DELAY = 0.1

st.set_page_config(
    page_title="Logiciel de Binômage",
    layout="centered"
)

# ---------------- NOMS DES PERSONNES ----------------
if not os.path.exists(IMAGE_FOLDER):
    st.error("❌ Dossier 'images' introuvable")
    st.stop()

NAMES = {}
for filename in os.listdir(IMAGE_FOLDER):
    if filename.lower().endswith((".jpg", ".png")):
        # Supprime l'extension et remplace les underscores par des espaces
        name = os.path.splitext(filename)[0].replace("_", " ")
        NAMES[filename] = name


# ---------------- FUNCTIONS ----------------
def play_sound():
    try:
        with open(SOUND_FILE, "rb") as f:
            b64 = base64.b64encode(f.read()).decode()
        st.markdown(
            f"""
            <audio autoplay>
                <source src="data:audio/mp3;base64,{b64}">
            </audio>
            """,
            unsafe_allow_html=True
        )
    except FileNotFoundError:
        st.warning("🔊 Son introuvable")


# ---------------- SESSION STATE ----------------
if "available_images" not in st.session_state:
    st.session_state.available_images = os.listdir(IMAGE_FOLDER)

if "selected_pairs" not in st.session_state:
    st.session_state.selected_pairs = []

if "current_pair" not in st.session_state:
    st.session_state.current_pair = None

# ---------------- UI ----------------
st.title("🎯 Logiciel de Binômage")
st.divider()
btn_start, btn_reset = st.columns([3, 1])
# ---------------- START BUTTON ----------------
if btn_start.button("▶️ START"):
    # ================= FIN DES BINÔMES =================
    if len(st.session_state.available_images) < 2:
        @st.dialog("ℹ️ Information")
        def show_info():
            st.success("Tous les binômes ont été formés ✅")
            st.markdown("Cliquez sur **RESET** pour recommencer.")


        show_info()
    else:

        # disabled=len(st.session_state.available_images) <= 2
        # play_sound()
        placeholders = st.empty()

        # Animation dynamique
        for _ in range(ANIMATION_LOOPS):
            a, b = random.sample(st.session_state.available_images, 2)
            placeholders.empty()  # Efface l'ancien affichage
            cols = placeholders.columns(2)
            for i, img in enumerate([a, b]):
                with cols[i]:
                    st.image(Image.open(os.path.join(IMAGE_FOLDER, img)), width=220)
                    st.markdown(f"### {NAMES.get(img, img)}")
            time.sleep(ANIMATION_DELAY)
 
        # Sélection finale
        final_pair = random.sample(st.session_state.available_images, 2)
        st.session_state.selected_pairs.append(final_pair)

        for img in final_pair:
            st.session_state.available_images.remove(img)

        st.session_state.current_pair = final_pair
        placeholders.empty()

# ---------------- FINAL DISPLAY ----------------
if st.session_state.current_pair:
    st.subheader("✅ Binôme sélectionné")
    cols = st.columns(2)
    for i, img in enumerate(st.session_state.current_pair):
        with cols[i]:
            st.image(Image.open(os.path.join(IMAGE_FOLDER, img)), width=190)
            st.markdown(f"### {NAMES.get(img, img)}")

st.divider()

# ================= CADRE INITIAL =================
if st.session_state.current_pair is None:
    st.subheader("🎞️ Zone de tirage")
    with st.container():
        st.markdown('<div class="frame">', unsafe_allow_html=True)
        cols = st.columns(2)

        placeholders = os.listdir(PLACEHOLDER_FOLDER)
        for i in range(2):
            with cols[i]:
                img = placeholders[i % len(placeholders)]
                st.image(
                    Image.open(os.path.join(PLACEHOLDER_FOLDER, img)),
                    width=220
                )

        st.markdown('</div>', unsafe_allow_html=True)

# Affichage des binômes déjà formés
if st.session_state.selected_pairs:
    st.subheader("📌 Binômes déjà formés")
    for pair in st.session_state.selected_pairs:
        cols = st.columns(2)
        for i, img in enumerate(pair):
            with cols[i]:
                st.image(Image.open(os.path.join(IMAGE_FOLDER, img)), width=140)
                # st.caption(NAMES.get(img, img))

# ---------------- RESET ----------------
if btn_reset.button("🔄 RESET"):
    st.session_state.available_images = os.listdir(IMAGE_FOLDER)
    st.session_state.selected_pairs = []
    st.session_state.current_pair = None
    st.rerun()
