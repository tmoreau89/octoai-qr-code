import streamlit as st
from PIL import Image
import webuiapi
import qrcode
import random
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers.pil import RoundedModuleDrawer


api = webuiapi.WebUIApi(
    host="octoai-qr-logo-demo-4jkxk521l3v1.octoai.cloud", port=443, use_https=True
)

def transform_qr_code(url, food_type):
    qr = qrcode.QRCode(
        version=3,
        box_size=10,
        border=3,
        error_correction=qrcode.ERROR_CORRECT_H)
    qr.add_data(url)
    qr.make(fit=True)
    qr_code = qr.make_image(
        fill='black',
        back_color='white',
        image_factory=StyledPilImage,
        module_drawer=RoundedModuleDrawer()
    )
    img = qr_code.convert('RGB')

    seed = random.randint(0,1000)
    unit1 = webuiapi.ControlNetUnit(
        input_image=img,
        module="invert",
        weight=1.25,
        guidance_start=0,
        guidance_end=0.90,
        model="control_v1p_sd15_qrcode_monster [5e5778cb]"
    )
    res = api.txt2img(
        prompt=food_type+", RAW photo, <lora:foodphoto:0.8> foodphoto, soft lighting, high quality, film grain, Fujifilm XT",
        seed=seed,
        cfg_scale=7,
        steps=20,
        width=768,
        height=768,
        n_iter=1,
        sampler_name="Euler a",
        controlnet_units=[unit1],
        override_settings={"sd_model_checkpoint": "realistic.safetensors"},
    )
    st.image(res.images[0])

st.set_page_config(layout="wide", page_title="QR Chef")

st.write("## QR Chef - Powered by OctoAI")

url = st.text_input("URL to your webpage!", "https://octoml.ai/")

food_type = st.text_input("Your favorite food!", "nachos")

if st.button('(re-)Generate QR code!'):
    transform_qr_code(url, food_type)