import streamlit as st

# --- SAYFA AYARLARI ---
st.set_page_config(page_title="AritmaPlus+", layout="centered")

# --- VERİ SAKLAMA ---
if 'musteriler' not in st.session_state:
    st.session_state.musteriler = []

st.title("💧 ArıtmaPlus+ Takip")

# --- SEKMELER ---
tab1, tab2 = st.tabs(["➕ Yeni Kayıt", "🔧 Servis Listesi"])

with tab1:
    with st.form("kayit"):
        ad = st.text_input("Müşteri Adı")
        tel = st.text_input("Telefon (Örn: 5321112233)")
        adres = st.text_area("Adres (Navigasyon için)")
        if st.form_submit_button("KAYDET"):
            if ad and tel:
                st.session_state.musteriler.append({"ad": ad, "tel": tel, "adres": adres})
                st.success("Kayıt Başarılı!")

with tab2:
    if not st.session_state.musteriler:
        st.info("Kayıtlı müşteri yok.")
    else:
        for m in st.session_state.musteriler:
            with st.expander(f"👤 {m['ad']}"):
                st.write(f"📞 Tel: {m['tel']}")
                st.write(f"📍 Adres: {m['adres']}")
                
                # --- NAVİGASYON ---
                # En basit Google Maps linki
                maps_link = f"https://google.com{m['adres']}".replace(" ", "+")
                st.link_button("📍 YOL TARİFİ", maps_link)
                
                # --- WHATSAPP ---
                # En basit WhatsApp linki
                wa_link = f"https://wa.me{m['tel']}"
                st.link_button("🟢 WHATSAPP", wa_link)
