import streamlit as st
from PIL import Image
import io
import base64

st.set_page_config(page_title="Image Converter", layout="centered")

st.title("🖼️ Image Format Converter")
st.write("Convert your images to SVG, PNG, or JPG formats")

uploaded_file = st.file_uploader("Choose an image", type=["jpg", "jpeg", "png", "bmp", "gif"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Original Image", use_column_width=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("Convert to PNG"):
            buf = io.BytesIO()
            image.save(buf, format="PNG")
            buf.seek(0)
            st.download_button("Download PNG", data=buf,
                               file_name="converted.png", mime="image/png")

    with col2:
        if st.button("Convert to JPG"):
            buf = io.BytesIO()
            image.convert("RGB").save(buf, format="JPEG")
            buf.seek(0)
            st.download_button("Download JPG", data=buf,
                               file_name="converted.jpg", mime="image/jpeg")

    with col3:
        if st.button("Convert to SVG"):
            # Encode image as base64 PNG embedded in SVG
            png_buf = io.BytesIO()
            image.save(png_buf, format="PNG")
            png_buf.seek(0)
            b64 = base64.b64encode(png_buf.read()).decode("utf-8")

            w, h = image.size
            svg = f'''<svg xmlns="http://www.w3.org/2000/svg" 
                          xmlns:xlink="http://www.w3.org/1999/xlink"
                          width="{w}" height="{h}" viewBox="0 0 {w} {h}">
  <image href="data:image/png;base64,{b64}" width="{w}" height="{h}"/>
</svg>'''

            st.download_button("Download SVG", data=svg,
                               file_name="converted.svg", mime="image/svg+xml")