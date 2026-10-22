import os
import sys
import time
import streamlit as st

# 🌟 استيراد الوكلاء الحالية من المنظومة دون تعديل أي ملف
from autonomous_sabil import run_fully_autonomous_pipeline
from community_agent import CommunityAgent
from auto_editor_agent import AutoEditorAgent

# ----------------------------------------------------
# 1️⃣ إعدادات الصفحة والهوية البصرية للتطبيق
# ----------------------------------------------------
st.set_page_config(
    page_title="تطبيق سَبِيلُ الرُّشْدِ الذكي",
    page_icon="🕌",
    layout="centered",
    initial_sidebar_state="expanded"
)

# تخصيص التصميم بالـ CSS لتبدو الشاشة كواجهة محادثة احترافية
st.markdown("""
    <style>
    .main {
        direction: rtl;
        text-align: right;
    }
    .stChatMessage {
        border-radius: 12px;
        padding: 10px;
    }
    .stButton>button {
        width: 100%;
        border-radius: 8px;
        background-color: #0F172A;
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🕌 تطبيق «سَبِيلُ الرُّشْدِ» - مركز التحكم الذكي")
st.caption("تطبيق تفاعلي مستقل للتحكم بالصوت والكتابة في تشغيل ونشر فيديوهات القناة ومنشورات المجتمع.")

# ----------------------------------------------------
# 2️⃣ إدارة ذاكرة المحادثة (Chat History)
# ----------------------------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "أهلاً بك يا محمد في منظومة «سَبِيلُ الرُّشْدِ»! 🌿\nكيف يمكنني مساعدتك اليوم؟ يمكنك كتابة أمرك أو التحدث معي بالصوت."}
    ]

# عرض سجل الرسائل السابق
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# ----------------------------------------------------
# 3️⃣ الشريط الجانبي (Sidebar) للتحكم المباشر
# ----------------------------------------------------
with st.sidebar:
    st.header("⚙️ إعدادات وتشغيل سريع")
    st.info("المنظومة متصلة بالوكلاء الذكية وجاهزة للتنفيذ.")
    
    if st.button("🚀 تشغيل دورة إنتاج كاملة (Auto-Pilot)"):
        with st.spinner("جاري تشغيل المنظومة تلقائياً..."):
            try:
                run_fully_autonomous_pipeline(publish_community=True, publish_short=True, publish_long=False)
                st.success("✅ تمت الدورة بنجاح!")
            except Exception as e:
                st.error(f"❌ حدث خطأ: {e}")

    st.markdown("---")
    st.subheader("🎙️ التسجيل الصوتي")
    audio_val = st.audio_input("اضغط للتحدث بالأمر الصوتي") if hasattr(st, "audio_input") else None

# ----------------------------------------------------
# 4️⃣ معالجة المدخلات (النصية أو الصوتية)
# ----------------------------------------------------
user_query = st.chat_input("اكتب أمرك هنا (مثلاً: أنشئ فيديو قصير جديد، ارفع منشور مجتمع...)...")

# إذا تحدث المستخدم بالصوت
if audio_val and "audio_processed" not in st.session_state:
    st.session_state.audio_processed = True
    user_query = "تم استلام أمر صوتي من الميكروفون، جاري معالجته..."

if user_query:
    st.session_state.messages.append({"role": "user", "content": user_query})
    with st.chat_message("user"):
        st.write(user_query)

    # 2. تحليل أمر المستخدم وتوجيهه للوكيل المناسب
    with st.chat_message("assistant"):
        response_placeholder = st.empty()
        
        if "منشور" in user_query or "مجتمع" in user_query or "منشورات" in user_query:
            response_placeholder.markdown("⏳ **[وكيل المنتدى]:** جاري صياغة وحفظ منشور جديد للمجتمع...")
            try:
                comm = CommunityAgent()
                post_text = comm.publish_community_post()
                res_msg = f"✅ **تم تجهيز منشور المجتمع بنجاح!**\n\n**المحتوى:**\n> {post_text}"
            except Exception as e:
                res_msg = f"⚠️ حدث خطأ أثناء تجهيز المنشور: {e}"

        elif "فيديو" in user_query or "شورت" in user_query or "short" in user_query or "إنتاج" in user_query:
            response_placeholder.markdown("🎬 **[المنظومة العامة]:** جاري بدء دورة إنتاج فيديو قصير متزامن...")
            try:
                run_fully_autonomous_pipeline(publish_community=False, publish_short=True, publish_long=False)
                res_msg = "🎉 **تم إنتاج وتجهيز الفيديو القصير بنجاح متكامل!**"
            except Exception as e:
                res_msg = f"⚠️ حدث خطأ أثناء إنتاج الفيديو: {e}"

        else:
            res_msg = f"أهلاً بك! استلمت طلبك: **'{user_query}'**.\nيمكنك أمري بـ:\n- **إنتاج فيديو قصير/طويل**\n- **تجهيز منشور مجتمع جديد**\n- **تشغيل الدورة الذاتية بالكامل**"

        response_placeholder.markdown(res_msg)
        st.session_state.messages.append({"role": "assistant", "content": res_msg})