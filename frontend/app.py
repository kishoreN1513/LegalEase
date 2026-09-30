import streamlit as st
import requests
from utils.exporters import make_txt, make_docx, make_pdf

st.set_page_config(
    page_title="LegalEase — Liquid Glass",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown(r'''
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
html, body, [class*="css"] { font-family: Inter, sans-serif; }
.stApp {
  background:
    radial-gradient(circle at 15% 10%, rgba(92,155,255,.22), transparent 28%),
    radial-gradient(circle at 85% 15%, rgba(174,93,255,.18), transparent 28%),
    radial-gradient(circle at 50% 90%, rgba(56,220,190,.10), transparent 32%),
    #070a12;
  color: #f5f7ff;
}
.stApp:before {
  content:""; position:fixed; inset:-20%; pointer-events:none;
  background:conic-gradient(from 90deg, transparent, rgba(255,255,255,.035), transparent 30%);
  animation:spin 18s linear infinite;
}
@keyframes spin { to { transform:rotate(360deg); } }
.hero {
  padding:34px; border:1px solid rgba(255,255,255,.13);
  border-radius:30px; background:rgba(255,255,255,.07);
  backdrop-filter:blur(28px); -webkit-backdrop-filter:blur(28px);
  box-shadow:0 25px 80px rgba(0,0,0,.35), inset 0 1px rgba(255,255,255,.12);
  margin-bottom:20px;
}
.logo { font-size:48px; font-weight:800; letter-spacing:-3px; }
.logo span { background:linear-gradient(100deg,#fff,#9ac5ff,#d8a7ff);
  -webkit-background-clip:text; color:transparent; }
.sub { color:#aeb7cc; font-size:15px; }
.glass {
  padding:22px; border-radius:24px; border:1px solid rgba(255,255,255,.11);
  background:rgba(255,255,255,.055); backdrop-filter:blur(22px);
  box-shadow:inset 0 1px rgba(255,255,255,.08),0 15px 50px rgba(0,0,0,.20);
}
.badge {display:inline-block;padding:7px 12px;border-radius:999px;
  background:rgba(110,170,255,.13);border:1px solid rgba(150,190,255,.18);
  color:#cfe2ff;font-size:12px;}
textarea, input {
  border-radius:16px !important; border:1px solid rgba(255,255,255,.12) !important;
  background:rgba(10,15,28,.65) !important; color:#fff !important;
}
.stButton > button, .stDownloadButton > button {
  border-radius:15px !important; border:1px solid rgba(255,255,255,.15) !important;
  background:linear-gradient(135deg,rgba(120,175,255,.26),rgba(180,105,255,.22)) !important;
  color:white !important; font-weight:700 !important;
  transition:.25s;
}
.stButton > button:hover, .stDownloadButton > button:hover {
  transform:translateY(-2px); box-shadow:0 12px 35px rgba(110,160,255,.25);
}
</style>
''', unsafe_allow_html=True)

st.markdown('''
<div class="hero">
  <div class="badge">AI DOCUMENT STUDIO · LIQUID GLASS</div>
  <div class="logo"><span>LegalEase</span> ✦</div>
  <div class="sub">Draft • Edit • Preview • Export — in one futuristic workspace.</div>
</div>
''', unsafe_allow_html=True)

left, right = st.columns([1, 1.15], gap="large")

with left:
    st.markdown('<div class="glass">', unsafe_allow_html=True)
    st.subheader("Create your document")
    document_type = st.text_input("Document type", "Freelance Work Contract")
    parties = st.text_area("Parties involved", "Jane Doe (Service Provider), TechNova Inc. (Client)", height=100)
    terms = st.text_area(
        "Terms & conditions",
        "Payment within 30 days; Provider delivers work by agreed deadline; Confidentiality must be maintained; Either party may terminate with 15 days notice",
        height=150
    )
    dates = st.text_input("Effective date", "September 30, 2026")
    api_url = st.text_input("Backend URL", "http://127.0.0.1:8000")
    generate = st.button("✦ Generate Document", use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with right:
    st.markdown('<div class="glass">', unsafe_allow_html=True)
    st.subheader("Live preview")
    if "document" not in st.session_state:
        st.session_state.document = ""
    if generate:
        payload = {"document_type": document_type, "parties": parties, "terms": terms, "dates": dates}
        try:
            r = requests.post(f"{api_url.rstrip('/')}/generate", json=payload, timeout=90)
            r.raise_for_status()
            st.session_state.document = r.json()["document"]
            st.success("Document generated.")
        except Exception as e:
            st.error(f"Backend connection failed: {e}")

    edited = st.text_area("Editable document", st.session_state.document, height=500, key="editor")
    st.session_state.document = edited

    if edited.strip():
        c1, c2, c3 = st.columns(3)
        with c1:
            st.download_button("TXT", make_txt(edited), "legalease_document.txt", "text/plain", use_container_width=True)
        with c2:
            st.download_button("DOCX", make_docx(edited, document_type), "legalease_document.docx",
                               "application/vnd.openxmlformats-officedocument.wordprocessingml.document", use_container_width=True)
        with c3:
            st.download_button("PDF", make_pdf(edited, document_type), "legalease_document.pdf",
                               "application/pdf", use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("---")
st.caption("LegalEase is a drafting assistant. Generated documents should be reviewed for the user's specific legal circumstances.")
