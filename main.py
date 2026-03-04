import streamlit as st
from PIL import Image
import io
import numpy as np

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
            st.download_button("Download PNG", data=png_buffer,
                               file_name="converted.png", mime="image/png")

    with col2:
        if st.button("Convert to JPG"):
            jpg_buffer = io.BytesIO()
            image.convert("RGB").save(jpg_buffer, format="JPEG")
            jpg_buffer.seek(0)
            st.download_button("Download JPG", data=jpg_buffer,
                               file_name="converted.jpg", mime="image/jpeg")

    with col3:
        if st.button("Convert to SVG"):
            import potracer

            # Convert to 1-bit bitmap for tracing
            bw = image.convert("L").point(lambda x: 255 if x > 128 else 0, "1")
            bmp = potracer.Bitmap(np.array(bw, dtype=np.uint32))
            path = bmp.trace()

            svg_buffer = io.StringIO()
            w, h = bw.size
            svg_buffer.write(f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}">\n')
            for curve in path:
                svg_buffer.write('<path d="')
                start = curve.start_point
                svg_buffer.write(f"M {start.x},{h - start.y} ")
                for segment in curve.segments:
                    if segment.is_corner:
                        svg_buffer.write(f"L {segment.c.x},{h - segment.c.y} ")
                        svg_buffer.write(f"L {segment.end_point.x},{h - segment.end_point.y} ")
                    else:
                        svg_buffer.write(
                            f"C {segment.c1.x},{h - segment.c1.y} "
                            f"{segment.c2.x},{h - segment.c2.y} "
                            f"{segment.end_point.x},{h - segment.end_point.y} "
                        )
                svg_buffer.write('Z" fill="black"/>\n')
            svg_buffer.write("</svg>")

            st.download_button("Download SVG", data=svg_buffer.getvalue(),
                               file_name="converted.svg", mime="image/svg+xml")