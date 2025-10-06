import streamlit as st

# -----------------------------------
# 🎨 APP CONFIGURATION
# -----------------------------------
st.set_page_config(page_title="Fashion Chatbot", page_icon="👗", layout="wide")

# -----------------------------------
# 🌟 HEADER
# -----------------------------------
st.title("👗 Fashion Chatbot & Recommendation System")
st.write("Welcome to your personal fashion assistant! 💬")
st.write("Upload a dress image to find similar styles or chat with the AI about fashion trends.")

# -----------------------------------
# 🧭 SIDEBAR NAVIGATION
# -----------------------------------
st.sidebar.title("🛍️ Navigation")
menu = st.sidebar.radio("Choose an option:", ["Home", "Image Recommendation", "Chatbot", "About"])

# -----------------------------------
# 🏠 HOME PAGE
# -----------------------------------
if menu == "Home":
    st.subheader("✨ What You Can Do Here")
    st.markdown("""
    - 🖼️ **Upload an image** and discover visually similar outfits  
    - 💬 **Chat** with your fashion assistant for style advice  
    - 🕶️ **Explore** color, trends, and seasonal wear ideas  
    """)
    st.image("https://cdn.pixabay.com/photo/2016/11/29/12/54/fashion-1866579_1280.jpg", width=600)
    st.info("Use the sidebar to switch between different sections.")

# -----------------------------------
# 🖼️ IMAGE RECOMMENDATION PAGE
# -----------------------------------
elif menu == "Image Recommendation":
    st.header("🖼️ Fashion Image Recommendation")
    st.write("Upload a dress image to find similar designs and styles.")

    uploaded_file = st.file_uploader("Upload an image (JPG/PNG):", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        st.image(uploaded_file, caption="Uploaded Image", width=250)
        st.button("🔍 Find Similar Dresses")

        st.markdown("---")
        st.subheader("👗 Similar Dresses Will Appear Here")
        cols = st.columns(5)
        for i in range(5):
            with cols[i]:
                st.image("https://cdn.pixabay.com/photo/2017/08/06/08/05/fashion-2597769_1280.jpg", caption=f"Result {i+1}", use_container_width=True)

# -----------------------------------
# 💬 CHATBOT PAGE
# -----------------------------------
elif menu == "Chatbot":
    st.header("💬 Fashion Assistant Chatbot")
    st.write("Ask your fashion assistant anything about outfits, trends, or colors!")

    chat_container = st.container()
    with chat_container:
        user_message = st.text_input("You:", placeholder="Type your question here...")
        if st.button("Send"):
            st.success(f"👗 Bot: This is where the AI’s reply will appear.")

    st.markdown("---")
    st.caption("💡 Example questions:")
    st.markdown("""
    - What should I wear for a summer party?  
    - Show me some trendy jackets  
    - Suggest some casual shoes  
    """)

# -----------------------------------
# ℹ️ ABOUT PAGE
# -----------------------------------
elif menu == "About":
    st.header("ℹ️ About This Project")
    st.markdown("""
    **Fashion Chatbot & Recommendation System**  
    Developed as a prototype to merge computer vision and NLP for personalized fashion assistance.  
    """)
    st.markdown("🧠 Built using **Streamlit**, **TensorFlow**, and **Natural Language Processing**.")
    st.markdown("👤 Created by: **Shyam**")
    st.markdown("📅 Version: 1.0")

# -----------------------------------
# FOOTER
# -----------------------------------
st.markdown("---")
st.caption("© 2025 Fashion AI Prototype by Shyam ✨")
