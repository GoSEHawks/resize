import streamlit as st
import potrace   
from PIL import Image
import io
from pathlib import Path
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
            png_buffer = io.BytesIO()
            image.save(png_buffer, format="PNG")
            png_buffer.seek(0)
            st.download_button(
                label="Download PNG",
                data=png_buffer,
                file_name="converted.png",
                mime="image/png"
            )
    
    with col2:
        if st.button("Convert to JPG"):
            jpg_buffer = io.BytesIO()
            image.convert("RGB").save(jpg_buffer, format="JPEG")
            jpg_buffer.seek(0)
            st.download_button(
                label="Download JPG",
                data=jpg_buffer,
                file_name="converted.jpg",
                mime="image/jpeg"
            )
    
    with col3:
        if st.button("Convert to SVG"):
            st.info("Note: Use an online tool or 'potrace' library for true raster-to-vector conversion")
            st.caption("PIL cannot directly convert to SVG. Consider using 'potrace' or online converters.")

    # Example of using potrace to convert to SVG
    st.write("Example of using potrace to convert to SVG")
    im = Image.open(uploaded_file).convert('1')
    bitmap = potrace.Bitmap(im.tobytes(), im.size[0], im.size[1])
    path = bitmap.trace()
    svg = path.to_svg(scale=1.0)   # or iterate paths and build XML yourself

    with open('out.svg','w') as f:
        f.write(svg)