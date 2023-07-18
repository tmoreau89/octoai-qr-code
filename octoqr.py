import streamlit as st
from PIL import Image
import webuiapi
import qrcode
import random
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers.pil import RoundedModuleDrawer


api = webuiapi.WebUIApi(
    host="a1111-webui-api-4jkxk521l3v1.octoai.cloud", port=443, use_https=True
)

def transform_qr_code(url, food_type):
    qr = qrcode.QRCode(
        version=3,
        box_size=30,
        border=1,
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
    for i in range(0, 3):
        unit1 = webuiapi.ControlNetUnit(
            input_image=img,
            module="invert",
            weight=1.20,
            guidance_start=0.25,
            guidance_end=0.95,
            model="controlnetQRPatternQR_v2Sd15 [2d8d5750]"
        )
        res = api.txt2img(
            prompt=food_type+", RAW photo, <lora:foodphoto:0.8> foodphoto, dslr, soft lighting, high quality, film grain, Fujifilm XT",
            seed=seed+i,
            cfg_scale=7,
            steps=30,
            width=512,
            height=512,
            n_iter=1,
            sampler_name="Euler a",
            controlnet_units=[unit1],
            override_settings={"sd_model_checkpoint": "v1-5-pruned.safetensors"},
        )
        if i % 3 == 0:
            col1.image(res.images[0])
        elif i % 3 == 1:
            col2.image(res.images[0])
        elif i % 3 == 2:
            col3.image(res.images[0])

st.set_page_config(layout="wide", page_title="OctoAI QR Code Generator")

st.write("## QR Chef - Powered by OctoAI")

url = st.text_input("URL to your webpage!", "https://octoml.ai/")

food_type = st.text_input("Your favorite food!", "nachos")

col1, col2, col3 = st.columns(3)

if st.button('(re-)Generate QR code!'):
    transform_qr_code(url, food_type)