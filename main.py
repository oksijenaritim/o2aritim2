import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# --- 1. GÖRÜNÜM AYARLARI (MODERN SİYAH TEMA) ---
st.set_page_config(page_title="Arıtma Pro v2", layout="wide", page_icon="💧")

# Arayüzü Güzelleştiren Özel CSS (Butonları ve Kartları Şık Yapar)
st.markdown("""
    <style>
    .stButton>button { width: 100%; border-radius: 10px; height: 3em; font-weight: bold; }
    .stExpander { border: 1px solid #30363d; border-radius: 10px; background-color: #161b22; }
    </style>
    """, unsafe_allow_stdio=True)

# --- 2. VERİ VE GİRİŞ KONTROLÜ ---
if 'musteriler' not in st.session_state:
    st.session_state.musteriler = []
if 'giris_yapildi' not in st.session_state:
    st.session_state.giris_yapildi = False

# --- 3. GİRİŞ EKRANI (LOGIN) ---
if not st.session_state.giris_yapildi:
    st.title("🔐 ArıtmaPlus+ Giriş")
    kullanici = st.text_input("Kullanıcı Adı")
    sifre = st.text_input("Şifre", type="password")
    if st.button("Sisteme Giriş Yap"):
        if kullanici == "admin" and sifre == "1234":
            st.session_state.giris_yapildi = True
            st.rerun()
        else:
            st.error("Hatalı kullanıcı adı veya şifre!")
    st.stop()

# --- 4. ANA PANEL (Giriş Yapıldıktan Sonra) ---
st.title("💧 ArıtmaPlus+ Yönetim Paneli")

# Sekmeler (Görseldeki gibi düzenli)
tab1, tab2, tab3 = st.tabs(["➕ Yeni Kayıt", "🔧 Servis & Navigasyon", "📦 Stok Durumu"])

# --- TAB 1: YENİ KAYIT ---
with tab1:
    with st.form("kayit_formu"):
        c1, c2 = st.columns(2)
        with c1:
            ad = st.text_input("👤 Müşteri Ad Soyad")
            tel = st.text_input("📞 Telefon (5xx...)")
        with c2:
            cihaz = st.selectbox("🚰 Cihaz Tipi", ["5 Aşamalı Çelik", "6 Aşamalı Alkalin", "7 Aşamalı Mineral", "Endüstriyel"])
            adres = st.text_area("📍 Navigasyon Adresi (Mahalle, Sokak, İlçe)")
        
        if st.form_submit_button("💾 Müşteriyi Sisteme Kaydet"):
            if ad and tel and adres:
                yeni = {"ad": ad, "tel": tel, "adres": adres, "cihaz": cihaz, "tarih": datetime.now().strftime("%d-%m-%Y")}
                st.session_state.musteriler.append(yeni)
                st.success(f"{ad} başarıyla kaydedildi!")
            else:
                st.warning("Lütfen tüm alanları doldurun!")

# --- TAB 2: SERVİS & NAVİGASYON (Hatasız Butonlar) ---
with tab2:
    st.subheader("🛠️ Günlük Servis Programı")
    if not st.session_state.musteriler:
        st.info("Henüz kayıtlı müşteri yok.")
    else:
        for i, m in enumerate(st.session_state.musteriler):
            with st.expander(f"👤 {m['ad']} | 📅 {m['tarih']}"):
                st.write(f"📱 **Telefon:** {m['tel']}  |  🚰 **Cihaz:** {m['cihaz']}")
                st.write(f"📍 **Adres:** {m['adres']}")
                
                col1, col2 = st.columns(2)
                
                # NAVİGASYON (Hatasız Yöntem)
                maps_adres = m['adres'].replace(" ", "+")
                nav_link = f"https://google.com{maps_adres}"
                col1.link_button("📍 YOL TARİFİ AL", nav_url=nav_link)
                
                # WHATSAPP (Hatasız Yöntem)
                msg = f"Merhaba {m['ad']}, Su Arıtma servisiniz için yoldayız."
                wa_msg = msg.replace(" ", "%20")
                wa_tel = "".join(filter(str.isdigit, m['tel']))
                if wa_tel.startswith("0"): wa_tel = wa_tel[1:]
                
                wa_link = f"https://wa.me{wa_tel}?text={wa_msg}"
                col2.link_button("🟢 WHATSAPP MESAJ", wa_url=wa_link)

# --- TAB 3: STOK DURUMU ---
with tab3:
    st.subheader("📦 Depo Stok Takibi")
    st.info("Bu modül geliştirme aşamasındadır. Satış yaptıkça buradan düşecektir.")
    st.metric("5'li Filtre Seti", "42 Adet")
    st.metric("Membran Filtre", "15 Adet")
