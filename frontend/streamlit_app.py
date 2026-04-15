"""NagrikMitra â€” Streamlit Frontend.

Three-panel layout:
- Left Sidebar: Location, language, quick actions
- Center: Chat interface with voice support
- Right: Scheme cards, eligibility results, grievance tracker
"""

import streamlit as st
import requests
import json
import base64
import uuid
import os
from datetime import datetime

# â”€â”€â”€ PAGE CONFIG â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€

st.set_page_config(
    page_title="NagrikMitra â€” Citizen Service Assistant",
    page_icon="ðŸ›ï¸",
    layout="wide",
    initial_sidebar_state="expanded",
)

API_BASE = st.secrets.get(
    "API_BASE_URL",
    os.getenv("API_BASE_URL", "http://localhost:8000"),
).rstrip("/")

# â”€â”€â”€ CUSTOM CSS â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€

st.markdown("""
<style>
    /* Main theme colors - Government of India inspired */
    :root {
        --primary: #1a237e;
        --primary-light: #534bae;
        --accent: #ff6f00;
        --accent-light: #ffa040;
        --bg-light: #f5f5f5;
        --success: #2e7d32;
        --warning: #f57f17;
    }

    /* Header styling */
    .main-header {
        background: linear-gradient(135deg, #1a237e 0%, #283593 50%, #303f9f 100%);
        color: white;
        padding: 1.2rem 2rem;
        border-radius: 12px;
        margin-bottom: 1.5rem;
        text-align: center;
        box-shadow: 0 4px 15px rgba(26, 35, 126, 0.3);
    }
    .main-header h1 {
        margin: 0;
        font-size: 1.8rem;
        font-weight: 700;
    }
    .main-header p {
        margin: 0.3rem 0 0 0;
        opacity: 0.9;
        font-size: 0.95rem;
    }

    /* Chat message bubbles */
    .chat-user {
        background: linear-gradient(135deg, #e3f2fd, #bbdefb);
        border-left: 4px solid #1a237e;
        padding: 1rem 1.2rem;
        border-radius: 0 12px 12px 12px;
        margin: 0.8rem 0;
        max-width: 85%;
        margin-left: auto;
    }
    .chat-bot {
        background: linear-gradient(135deg, #fff3e0, #ffe0b2);
        border-left: 4px solid #ff6f00;
        padding: 1rem 1.2rem;
        border-radius: 12px 0 12px 12px;
        margin: 0.8rem 0;
        max-width: 85%;
    }

    /* Scheme cards */
    .scheme-card {
        background: white;
        border: 1px solid #e0e0e0;
        border-radius: 12px;
        padding: 1.2rem;
        margin: 0.8rem 0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        transition: transform 0.2s, box-shadow 0.2s;
    }
    .scheme-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }
    .scheme-card h4 {
        color: #1a237e;
        margin: 0 0 0.5rem 0;
    }
    .scheme-badge {
        display: inline-block;
        padding: 0.2rem 0.6rem;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 600;
        margin-right: 0.3rem;
    }
    .badge-category {
        background: #e8eaf6;
        color: #1a237e;
    }
    .badge-central {
        background: #e8f5e9;
        color: #2e7d32;
    }
    .badge-state {
        background: #fff3e0;
        color: #e65100;
    }

    /* Status indicators */
    .status-submitted { color: #1565c0; font-weight: 600; }
    .status-in_review { color: #f57f17; font-weight: 600; }
    .status-resolved { color: #2e7d32; font-weight: 600; }

    /* Quick action buttons */
    .stButton > button {
        border-radius: 8px !important;
        font-weight: 500 !important;
        transition: all 0.2s !important;
    }

    /* Pipeline info badge */
    .pipeline-info {
        display: flex;
        gap: 0.5rem;
        flex-wrap: wrap;
        margin-top: 0.5rem;
        font-size: 0.75rem;
    }
    .info-chip {
        display: inline-block;
        padding: 0.15rem 0.5rem;
        border-radius: 12px;
        background: #f5f5f5;
        color: #616161;
        border: 1px solid #e0e0e0;
    }

    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}

    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #f8f9ff 0%, #eef0ff 100%);
    }
</style>
""", unsafe_allow_html=True)

# â”€â”€â”€ SESSION STATE â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€

if "session_id" not in st.session_state:
    st.session_state.session_id = uuid.uuid4().hex[:16]
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "selected_schemes" not in st.session_state:
    st.session_state.selected_schemes = []

# â”€â”€â”€ LANGUAGE MAP â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€

LANGUAGES = {
    "Auto-Detect": "",
    "English": "en-IN",
    "Hindi (हिंदी)": "hi-IN",
    "Tamil (தமிழ்)": "ta-IN",
    "Telugu (తెలుగు)": "te-IN",
    "Bengali (বাংলা)": "bn-IN",
    "Marathi (मराठी)": "mr-IN",
    "Gujarati (ગુજરાતી)": "gu-IN",
    "Kannada (ಕನ್ನಡ)": "kn-IN",
    "Malayalam (മലയാളം)": "ml-IN",
    "Odia (ଓଡ଼ିଆ)": "od-IN",
    "Punjabi (ਪੰਜਾਬੀ)": "pa-IN",
}

WELCOME_MESSAGES = {
    "": "Namaste! I'm **NagrikMitra**, your AI-powered government services assistant.\n\nI can help you with:\n- Government scheme information\n- Eligibility checks\n\nAsk me anything in your preferred language!",
    "en-IN": "Hello! I'm **NagrikMitra**, your AI-powered government services assistant.\n\nI can help you with:\n- Government scheme information\n- Eligibility checks\n\nAsk me anything!",
    "hi-IN": "नमस्ते! मैं **नागरिकमित्र** हूँ, आपका AI-संचालित सरकारी सेवा सहायक।\n\nमैं आपकी मदद कर सकता हूँ:\n- सरकारी योजनाओं की जानकारी\n- पात्रता जांच\n\nअपनी भाषा में कुछ भी पूछें!",
    "ta-IN": "வணக்கம்! நான் **நாகரிக்மித்ரா**, உங்கள் AI அரசு சேவை உதவியாளர்.\n\nநான் உதவ முடியும்:\n- அரசு திட்ட தகவல்\n- தகுதி சரிபார்ப்பு\n\nஉங்கள் மொழியில் கேளுங்கள்!",
    "te-IN": "నమస్కారం! నేను **నాగరిక్‌మిత్ర**, మీ AI ప్రభుత్వ సేవల సహాయకుడు.\n\nనేను సహాయం చేయగలను:\n- ప్రభుత్వ పథకాల సమాచారం\n- అర్హత తనిఖీ\n\nమీ భాషలో అడగండి!",
    "bn-IN": "নমস্কার! আমি **নাগরিকমিত্র**, আপনার AI-চালিত সরকারি সেবা সহায়ক।\n\nআমি সাহায্য করতে পারি:\n- সরকারি প্রকল্পের তথ্য\n- যোগ্যতা যাচাই\n\nআপনার ভাষায় জিজ্ঞাসা করুন!",
    "mr-IN": "नमस्कार! मी **नागरिकमित्र**, तुमचा AI-संचालित सरकारी सेवा सहाय्यक.\n\nमी मदत करू शकतो:\n- सरकारी योजनांची माहिती\n- पात्रता तपासणी\n\nतुमच्या भाषेत विचारा!",
    "gu-IN": "નમસ્તે! હું **નાગરિકમિત્ર**, તમારો AI આધારિત સરકારી સેવા સહાયક.\n\nહું મદદ કરી શકું:\n- સરકારી યોજનાઓની માહિતી\n- પાત્રતા તપાસ\n\nતમારી ભાષામાં પૂછો!",
    "kn-IN": "ನಮಸ್ಕಾರ! ನಾನು **ನಾಗರಿಕಮಿತ್ರ**, ನಿಮ್ಮ AI ಚಾಲಿತ ಸರ್ಕಾರಿ ಸೇವಾ ಸಹಾಯಕ.\n\nನಾನು ಸಹಾಯ ಮಾಡಬಹುದು:\n- ಸರ್ಕಾರಿ ಯೋಜನೆಗಳ ಮಾಹಿತಿ\n- ಅರ್ಹತಾ ಪರಿಶೀಲನೆ\n\nನಿಮ್ಮ ಭಾಷೆಯಲ್ಲಿ ಕೇಳಿ!",
    "ml-IN": "നമസ്കാരം! ഞാൻ **നാഗരികമിത്ര**, നിങ്ങളുടെ AI സർക്കാർ സേവന സഹായി.\n\nഎനിക്ക് സഹായിക്കാം:\n- സർക്കാർ പദ്ധതികളുടെ വിവരം\n- അർഹത പരിശോധന\n\nനിങ്ങളുടെ ഭാഷയിൽ ചോദിക്കൂ!",
    "od-IN": "ନମସ୍କାର! ମୁଁ **ନାଗରିକମିତ୍ର**, ଆପଣଙ୍କ AI ଆଧାରିତ ସରକାରୀ ସେବା ସହାୟକ।\n\nମୁଁ ସାହାଯ୍ୟ କରିପାରିବି:\n- ସରକାରୀ ଯୋଜନା ସୂଚନା\n- ଯୋଗ୍ୟତା ଯାଞ୍ଚ\n\nଆପଣଙ୍କ ଭାଷାରେ ପଚାରନ୍ତୁ!",
    "pa-IN": "ਸਤ ਸ੍ਰੀ ਅਕਾਲ! ਮੈਂ **ਨਾਗਰਿਕਮਿਤ੍ਰ**, ਤੁਹਾਡਾ AI-ਚਾਲਿਤ ਸਰਕਾਰੀ ਸੇਵਾ ਸਹਾਇਕ ਹਾਂ।\n\nਮੈਂ ਮਦਦ ਕਰ ਸਕਦਾ ਹਾਂ:\n- ਸਰਕਾਰੀ ਯੋਜਨਾਵਾਂ ਦੀ ਜਾਣਕਾਰੀ\n- ਯੋਗਤਾ ਜਾਂਚ\n\nਆਪਣੀ ਭਾਸ਼ਾ ਵਿੱਚ ਪੁੱਛੋ!",
}
STATES = [
    "", "Andhra Pradesh", "Arunachal Pradesh", "Assam", "Bihar", "Chhattisgarh",
    "Delhi", "Goa", "Gujarat", "Haryana", "Himachal Pradesh", "Jharkhand",
    "Karnataka", "Kerala", "Madhya Pradesh", "Maharashtra", "Manipur",
    "Meghalaya", "Mizoram", "Nagaland", "Odisha", "Punjab", "Rajasthan",
    "Sikkim", "Tamil Nadu", "Telangana", "Tripura", "Uttar Pradesh",
    "Uttarakhand", "West Bengal",
]

CATEGORIES = [
    "All", "Agriculture", "Education", "Health", "Housing", "Employment",
    "Women & Child", "Social Security", "Financial Inclusion",
    "Rural Development", "Skill Development",
]


# â”€â”€â”€ SIDEBAR â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€

with st.sidebar:
    st.markdown("### Settings")

    # Location
    selected_state = st.selectbox("Your State", STATES, index=0)
    district = st.text_input("District (optional)")

    # Language
    selected_language = st.selectbox("Language", list(LANGUAGES.keys()), index=0)

    st.markdown("---")
    st.markdown("### Quick Actions")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Browse Schemes", use_container_width=True):
            st.session_state.show_schemes = True
    with col2:
        if st.button("Check Eligibility", use_container_width=True):
            st.session_state.show_eligibility = True

    st.markdown("---")
    st.caption("NagrikMitra v1.0 | Powered by Sarvam AI")


# â”€â”€â”€ MAIN CONTENT â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€

# Header
st.markdown("""
<div class="main-header">
    <h1>NagrikMitra</h1>
    <p>AI-Powered Unified Multilingual Citizen Service Assistant</p>
    <p style="font-size: 0.8rem; opacity: 0.7;">Powered by Sarvam AI | 11 Indian Languages Supported</p>
</div>
""", unsafe_allow_html=True)

# Main layout: Chat (left) + Info Panel (right)
chat_col, info_col = st.columns([3, 2])

# â”€â”€â”€ CHAT INTERFACE â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€

with chat_col:
    st.markdown("### Chat with NagrikMitra")

    # Play pending voice response audio
    if st.session_state.get("pending_audio"):
        st.audio(st.session_state.pending_audio, format="audio/wav", autoplay=True)
        st.session_state.pending_audio = None

    # Display chat history
    chat_container = st.container(height=450)
    with chat_container:
        if not st.session_state.chat_history:
            lang_code = LANGUAGES.get(selected_language, "")
            welcome = WELCOME_MESSAGES.get(lang_code, WELCOME_MESSAGES[""])
            with st.chat_message("assistant"):
                st.markdown(welcome)

        for msg_idx, msg in enumerate(st.session_state.chat_history):
            if msg["role"] == "user":
                with st.chat_message("user"):
                    st.markdown(msg["content"])
            else:
                with st.chat_message("assistant"):
                    st.markdown(msg["content"])

                    if msg.get("meta"):
                        meta = msg["meta"]
                        chips = []
                        if meta.get("detected_language"):
                            chips.append(f'<span class="info-chip">Lang: {meta["detected_language"]}</span>')
                        if meta.get("intent"):
                            chips.append(f'<span class="info-chip">Intent: {meta["intent"]}</span>')
                        if meta.get("from_cache"):
                            chips.append(f'<span class="info-chip">Cached</span>')
                        if meta.get("pii_detected"):
                            chips.append(f'<span class="info-chip">PII Masked</span>')
                        if chips:
                            st.markdown(f'<div class="pipeline-info">{"".join(chips)}</div>', unsafe_allow_html=True)

                # Listen button
                if st.button("Listen", key=f"listen_{msg_idx}"):
                    lang = msg.get("meta", {}).get("detected_language", "hi-IN") or "hi-IN"
                    import re
                    clean_text = msg["content"]
                    clean_text = re.sub(r'\*\*(.+?)\*\*', r'\1', clean_text)
                    clean_text = re.sub(r'\*(.+?)\*', r'\1', clean_text)
                    clean_text = re.sub(r'#{1,6}\s*', '', clean_text)
                    clean_text = re.sub(r'\[(.+?)\]\(.+?\)', r'\1', clean_text)
                    clean_text = re.sub(r'[`~]', '', clean_text)
                    try:
                        tts_resp = requests.post(
                            f"{API_BASE}/api/tts",
                            data={
                                "text": clean_text[:500],
                                "language_code": lang,
                            },
                            timeout=30,
                        )
                        if tts_resp.status_code == 200:
                            st.audio(tts_resp.content, format="audio/wav", autoplay=True)
                        else:
                            st.toast("TTS failed, please try again.")
                    except Exception:
                        st.toast("Could not connect to TTS service.")

    # Input area
    user_input = st.chat_input("Type your message... (in any Indian language)")

    # Voice input (supports both new and old Streamlit versions)
    audio_bytes = None
    audio_filename = "recording.wav"
    audio_mime = "audio/wav"

    if hasattr(st, "audio_input"):
        audio_input = st.audio_input("🎤 Record your voice")
        if audio_input:
            audio_bytes = audio_input.getvalue()
    else:
        st.caption("Voice recording isn't available in this Streamlit version. Upload audio instead.")
        uploaded_audio = st.file_uploader(
            "Upload voice file",
            type=["wav", "mp3", "m4a", "ogg"],
            key="voice_upload",
        )
        if uploaded_audio:
            audio_bytes = uploaded_audio.getvalue()
            audio_filename = uploaded_audio.name or audio_filename
            audio_mime = uploaded_audio.type or audio_mime

    if audio_bytes:
        audio_id = hash(audio_bytes)
        if audio_id != st.session_state.get("last_audio_id"):
            st.session_state.last_audio_id = audio_id
            with st.spinner("🎧 Processing voice..."):
                try:
                    files = {"audio": (audio_filename, audio_bytes, audio_mime)}
                    data = {
                        "session_id": st.session_state.session_id,
                        "state": selected_state or "",
                        "language_preference": LANGUAGES.get(selected_language, "hi-IN"),
                    }
                    response = requests.post(
                        f"{API_BASE}/api/voice",
                        files=files,
                        data=data,
                        timeout=60,
                    )
                    if response.status_code == 200:
                        result = response.json()
                        st.session_state.chat_history.append({
                            "role": "user",
                            "content": f"🎤 {result['transcribed_text']}",
                        })
                        st.session_state.chat_history.append({
                            "role": "assistant",
                            "content": result["response_text"],
                            "meta": {
                                "detected_language": result.get("detected_language", ""),
                                "intent": result.get("intent", ""),
                            },
                        })
                        if result.get("audio_base64"):
                            st.session_state.pending_audio = base64.b64decode(result["audio_base64"])
                        st.rerun()
                    else:
                        st.error(f"Voice processing failed: {response.text}")
                except requests.exceptions.ConnectionError:
                    st.error("Cannot connect to backend server.")
                except Exception as e:
                    st.error(f"Voice processing error: {e}")
    # Process text input
    if user_input:
        st.session_state.chat_history.append({"role": "user", "content": user_input})

        try:
            response = requests.post(
                f"{API_BASE}/api/chat",
                json={
                    "message": user_input,
                    "session_id": st.session_state.session_id,
                    "state": selected_state or None,
                    "district": district or None,
                    "language_preference": LANGUAGES.get(selected_language, ""),
                },
                timeout=30,
            )
            if response.status_code == 200:
                data = response.json()
                st.session_state.chat_history.append({
                    "role": "assistant",
                    "content": data["response"],
                    "meta": {
                        "detected_language": data.get("detected_language", ""),
                        "intent": data.get("intent", ""),
                        "from_cache": data.get("from_cache", False),
                        "pii_detected": data.get("pii_detected", False),
                        "schemes_referenced": data.get("schemes_referenced", []),
                    },
                })
                # Update scheme cards if schemes were referenced
                if data.get("schemes_referenced"):
                    st.session_state.selected_schemes = data["schemes_referenced"]
            else:
                st.session_state.chat_history.append({
                    "role": "assistant",
                    "content": "Sorry, I encountered an error. Please try again.",
                })
        except requests.exceptions.ConnectionError:
            st.session_state.chat_history.append({
                "role": "assistant",
                "content": "Cannot connect to the backend server. Please ensure it's running.",
            })
        except Exception as e:
            st.session_state.chat_history.append({
                "role": "assistant",
                "content": f"Error: {str(e)}",
            })
        st.rerun()


# â”€â”€â”€ INFO PANEL â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€

with info_col:
    tab1, tab2 = st.tabs(["ðŸ“‹ Schemes", "âœ… Eligibility"])

    # â”€â”€ Schemes Tab â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
    with tab1:
        st.markdown("#### Government Schemes")

        scheme_cat = st.selectbox("Filter by category", CATEGORIES, key="scheme_cat")
        try:
            params = {}
            if selected_state:
                params["state"] = selected_state
            if scheme_cat and scheme_cat != "All":
                params["category"] = scheme_cat
            resp = requests.get(f"{API_BASE}/api/schemes", params=params, timeout=5)
            if resp.status_code == 200:
                schemes = resp.json()
                if not schemes:
                    st.info("No schemes found. Try changing filters.")
                for scheme in schemes[:10]:
                    badge_type = "badge-central" if scheme.get("is_central") else "badge-state"
                    badge_label = "Central" if scheme.get("is_central") else "State"
                    st.markdown(f"""
                    <div class="scheme-card">
                        <h4>{scheme['name_en']}</h4>
                        <p style="color: #666; font-size: 0.85rem;">{scheme.get('name_hi', '')}</p>
                        <span class="scheme-badge badge-category">{scheme.get('category', '')}</span>
                        <span class="scheme-badge {badge_type}">{badge_label}</span>
                        <p style="margin-top: 0.5rem; font-size: 0.9rem;">{scheme.get('description_en', '')[:150]}...</p>
                        <p style="color: #2e7d32; font-weight: 600;">ðŸ’° {scheme.get('benefits', '')[:100]}</p>
                    </div>
                    """, unsafe_allow_html=True)
        except Exception:
            st.info("Connect to backend to browse schemes")

    # â”€â”€ Eligibility Tab â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
    with tab2:
        st.markdown("#### Check Your Eligibility")

        with st.form("eligibility_form"):
            elig_age = st.number_input("Your Age", min_value=0, max_value=120, value=30)
            elig_income = st.number_input("Annual Income (â‚¹)", min_value=0, value=200000, step=50000)
            elig_gender = st.selectbox("Gender", ["male", "female"])
            elig_occupation = st.text_input("Occupation (e.g., farmer, student)")
            elig_state = st.selectbox("State", STATES[1:], key="elig_state")

            if st.form_submit_button("Check Eligibility", type="primary"):
                try:
                    resp = requests.post(
                        f"{API_BASE}/api/eligibility",
                        json={
                            "age": elig_age,
                            "income": elig_income,
                            "gender": elig_gender,
                            "state": elig_state,
                            "occupation": elig_occupation,
                        },
                        timeout=10,
                    )
                    if resp.status_code == 200:
                        results = resp.json()
                        if results:
                            st.success(f"Found {len(results)} matching schemes!")
                            for r in results:
                                icon = "âœ…" if r["eligible"] else "âŒ"
                                st.markdown(f"""
                                **{icon} {r['scheme_name']}**
                                - Match Score: {'â­' * int(r['match_score'] * 5)}
                                - {', '.join(r['reasons'][:3])}
                                """)
                                if r.get("missing_criteria"):
                                    st.caption(f"â„¹ï¸ Missing: {', '.join(r['missing_criteria'])}")
                        else:
                            st.warning("No matching schemes found with current criteria")
                except Exception as e:
                    st.error(f"Error: {e}")



