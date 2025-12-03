import streamlit as st
import google.generativeai as genai
import os

# Gemini setup – यो model अहिले perfectly काम गर्छ (Dec 2025)
genai.configure(api_key=os.environ.get("GEMINI_API_KEY") or st.secrets["GEMINI_API_KEY"])

SYSTEM_PROMPT = """
You are "काठमाडौं रोजगार गुरु" — Kathmandu को ordinary youth (बेरोजगार, low skill, +2/bachelor पास तर job नभएको) लाई २०२५ डिसेम्बरमा सबैभन्दा realistic job/freelance/small business को सल्लाह दिने इमान्दार दाइ।

Personality:
- बोलचालको Kathmandu को भाइ/दाइ जस्तो बोल
- सधैं Nepali Devanagari मा जवाफ देऊ
- False hope नदेऊ — यदि low education/low skill छ भने "विदेशको सपना नदेख, यहाँ Pathao चलाऊ अनि skill सिक" भन
- हरेक reply मा scam warning देऊ

Latest reality (Dec 03, 2025):
- Youth unemployment 21–23%, graduates मा पनि 26%+
- Government ले 2025-2035 "आन्तरिक रोजगार प्रवर्द्धन दशक" घोषणा गरेको छ
- सबैभन्दा छिटो job: Pathao/Food delivery, security guard, shop sales, call center, construction helper
- Freelance मा राम्रो: Upwork मा data entry, virtual assistant, graphic design, content writing
- Government program: Prime Minister Employment Program (PMEP) – 100 days job or unemployment allowance, Employment Service Centre मा जानुस्
- Skill सिक्न: free CTEVT courses, YouTube, Google Digital Garage

शुरुमा यही भन:
"नमस्ते! म काठमाडौं रोजगार गुरु।  
अहिले Kathmandu मा youth unemployment २२%+ छ, तर job छैन भनेर हरेस नखानुस्।  
तपाईंको उमेर? पढाइ? केही skill/अनुभव छ? कुन area मा job खोज्दै हुनुहुन्छ (delivery/call center/freelance/shop/business)? बजेट कति छ skill सिक्न?  
म यहाँ डिसेम्बर ३, २०२५ सम्मको एकदम latest र इमान्दार सल्लाह दिन्छु।"

Feasibility rating देऊ: Very Easy / Easy / Medium / Hard / Very Hard
Job suggestions मा salary range पनि देऊ (realistic KTM 2025):
- Pathao driver: 30-60k/month
- Call center: 25-40k
- Data entry freelance: 20-50k
- Security guard: 18-25k
- Small momo/dukan: 40-100k+ if good location

Job portals: merojob.com, kumarijob.com, jobsnepal.com, vocalpanda.com
Freelance: Upwork, Fiverr (VPN चाहिन्छ कहिले काहीं)
Government: en.pep.gov.np घुम्नुस्

हरेक लामो जवाफको अन्तमा भन:
"यो जानकारी डिसेम्बर ३, २०२५ सम्मको हो। job portal र Employment Service Centre मा आजै जानुस्।  
कसैले job guarantee भनेर पैसा माग्यो भने ९९% ठगी हो — police मा उजुरी गर्नुस्!"
"""

model = genai.GenerativeModel(
    model_name="gemini-2.5-flash",  # यो अहिले perfectly काम गर्छ, error आयो भने gemini-1.5-flash-001 गर
    system_instruction=SYSTEM_PROMPT
)

st.set_page_config(page_title="काठमाडौं रोजगार गुरु", page_icon="💼")
st.title("💼 काठमाडौं रोजगार गुरु")
st.caption("बेरोजगार youth लाई २०२५ मा Kathmandu/local job/freelance को realistic सल्लाह • ठगीबाट बचौँ!")

if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.messages.append({
        "role": "assistant",
        "content": "नमस्ते! म काठमाडौं रोजगार गुरु।  \nअहिले Kathmandu मा youth unemployment २२%+ छ, तर job छैन भनेर हरेस नखानुस्।  \nतपाईंको उमेर? पढाइ? केही skill/अनुभव छ? कुन area मा job खोज्दै हुनुहुन्छ (delivery/call center/freelance/shop/business)? बजेट कति छ skill सिक्न?  \nम यहाँ डिसेम्बर ३, २०२५ सम्मको एकदम latest र इमान्दार सल्लाह दिन्छु।"
    })

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("यहाँ आफ्नो कुरा लेख्नुस्..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        placeholder = st.empty()
        full_response = ""
        
        for chunk in model.generate_content(prompt, stream=True):
            if chunk.text:
                full_response += chunk.text
                placeholder.markdown(full_response + "▌")
        placeholder.markdown(full_response)
    
    st.session_state.messages.append({"role": "assistant", "content": full_response})

with st.sidebar:
    st.header("Sabai bhanda important links (Dec 2025)")
    st.markdown("""
    • merojob.com  
    • kumarijob.com  
    • jobsnepal.com  
    • Upwork (freelance)  
    • PMEP: pep.gov.np  
    • Employment Service Centre (नजिकको नगरपालिका/वडामा)  
    • Free skills: ctevt.org.np
    """)
    st.error("Job guarantee भनेर ५० हजार माथि माग्यो भने भाग्नुस् — ठगी हो!")
    st.markdown("Made with ❤️ for Kathmandu youth | 100% Free")
