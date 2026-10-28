
import streamlit as st  # type: ignore

st.set_page_config(
    page_title="MedLabel",
    page_icon="💊",
    layout="centered"
)

st.title("MedLabel")
st.subheader("AI-Based Prescription Recognition")

st.write(
    "Upload prescription images to begin extracting "
    "medication information for review."
)

uploaded_files = st.file_uploader(
    "Upload prescription images",
    type=["png", "jpg", "jpeg"],
    accept_multiple_files=True
)

if uploaded_files:
    st.write(f"Uploaded {len(uploaded_files)} image(s).")

    for i, file in enumerate(uploaded_files, start=1):
        st.image(file, caption=f"Prescription {i}")

    st.info(
        "OCR and medication extraction will be implemented "
        "in a later development stage."
    )

st.caption(
    "Prototype only. Verify all medication instructions "
    "with a qualified healthcare professional."
)
