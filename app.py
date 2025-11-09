import streamlit as st
import supabase

# === بيانات SUPABASE الخاصة بك (معدلة) ===
SUPABASE_URL = "https://vjgkytqzllbacdjqgkvs.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InZqZ2t5dHF6bGxiYWNkanFna3ZzIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjI2ODIyODQsImV4cCI6MjA3ODI1ODI4NH0.9-RfO9TVPG-X3v2JTT3BIldQV1ZEFi5BFZ4QDx29yiA"

supabase_client = supabase.Client(SUPABASE_URL, SUPABASE_KEY)

st.set_page_config(page_title="Social Micro", layout="wide")

if 'user' not in st.session_state:
    st.session_state.user = None

def login(email, password):
    try:
        response = supabase_client.auth.sign_in_with_password({"email": email, "password": password})
        st.session_state.user = response.user
        st.success("✅ دخول ناجح!")
        st.rerun()
    except Exception as e:
        st.error(f"خطأ: {e}")

def signup(email, password):
    try:
        response = supabase_client.auth.sign_up({"email": email, "password": password})
        st.success("✅ تم إنشاء الحساب! تحقق من بريدك")
    except Exception as e:
        st.error(f"خطأ: {e}")

if st.session_state.user is None:
    tab1, tab2 = st.tabs(["تسجيل دخول", "إنشاء حساب"])
    
    with tab1:
        email = st.text_input("البريد الإلكتروني")
        password = st.text_input("كلمة المرور", type="password")
        if st.button("دخول"):
            login(email, password)
    
    with tab2:
        email = st.text_input("بريد إلكتروني جديد")
        password = st.text_input("كلمة مرور جديدة", type="password")
        if st.button("إنشاء حساب"):
            signup(email, password)

else:
    st.sidebar.title(f"مرحباً {st.session_state.user.email[:8]}...")
    if st.sidebar.button("خروج"):
        supabase_client.auth.sign_out()
        st.session_state.user = None
        st.rerun()
    
    st.header("📝 منشور جديد")
    content = st.text_area("ماذا تفكر؟", max_chars=280)
    if st.button("نشر"):
        if content:
            supabase_client.table("posts").insert({
                "user_email": st.session_state.user.email,
                "content": content
            }).execute()
            st.success("✅ تم النشر!")
            st.rerun()
    
    st.header("📱 خلاصة الأخبار")
    posts = supabase_client.table("posts").select("*").order("created_at", desc=True).execute()
    
    for post in posts.data:
        col1, col2 = st.columns([5, 1])
        with col1:
            st.write(f"**{post['user_email'][:8]}...** - {post['content']}")
            st.caption(f"📅 {post['created_at'][:16]}")
        st.divider()
