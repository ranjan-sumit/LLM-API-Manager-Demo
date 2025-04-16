# # app.py
# import streamlit as st
# from openai import OpenAI  # New style client
# from datetime import datetime

# # Configuration (could move to secrets.toml for production)
# USERS = {
#     "admin": {"password": "adminpass", "role": "admin", "tokens": 10000},
#     "user1": {"password": "user1pass", "role": "user", "tokens": 1000},
#     "guest": {"password": "", "role": "guest", "tokens": 100}
# }

# # Initialize session state
# def init_session():
#     if 'user' not in st.session_state:
#         st.session_state.update({
#             'user': None,
#             'role': 'guest',
#             'usage': {user: USERS[user]['tokens'] for user in USERS},
#             'max_tokens': 500,
#             'openai_key': None
#         })

# # Authentication system
# def authenticate(username, password):
#     user = USERS.get(username)
#     if user and (user['password'] == password or username == 'guest'):
#         st.session_state.user = username
#         st.session_state.role = user['role']
#         return True
#     return False

# # Admin panel
# def admin_panel():
#     st.subheader("🚀 Admin Dashboard")
#     st.write("### API Usage")
#     st.write(st.session_state.usage)
    
#     st.session_state.openai_key = st.text_input(
#         "🔑 OpenAI API Key", 
#         value=st.session_state.openai_key,
#         type="password"
#     )
    
#     st.session_state.max_tokens = st.slider(
#         "🎚 Max Tokens per Request",
#         100, 2000, st.session_state.max_tokens
#     )

# # Chat interface for users/guests
# def chat_interface():
#     st.subheader("💬 Chat Interface")
#     prompt = st.text_area("Enter your prompt:", height=100)
    
#     if st.button("🚀 Submit") and prompt:
#         if st.session_state.usage[st.session_state.user] <= 0:
#             st.error("❌ You've exceeded your token quota!")
#             return
        
#         if not st.session_state.openai_key:
#             st.error("❌ Please enter a valid OpenAI API key in the admin panel.")
#             return

#         try:
#             # Initialize OpenAI client with current session key
#             client = OpenAI(api_key=st.session_state.openai_key)

#             response = client.chat.completions.create(
#                 model="gpt-3.5-turbo",
#                 messages=[{"role": "user", "content": prompt}],
#                 max_tokens=st.session_state.max_tokens
#             )
            
#             # Deduct token usage
#             used_tokens = response.usage.total_tokens
#             st.session_state.usage[st.session_state.user] -= used_tokens

#             st.write("📝 Response:")
#             st.write(response.choices[0].message.content)
            
#             st.success(f"🔋 Tokens remaining: {st.session_state.usage[st.session_state.user]}")
        
#         except Exception as e:
#             st.error(f"API Error: {str(e)}")

# # Main application flow
# def main():
#     st.title("🔒 OpenAI API Manager")
#     init_session()
    
#     if not st.session_state.user:
#         st.subheader("🔑 Login")
#         username = st.text_input("Username")
#         password = st.text_input("Password", type="password")
        
#         if st.button("Login"):
#             if authenticate(username, password):
#                 st.success(f"✅ Logged in as {username}!")
#                 st.rerun()
#             else:
#                 st.error("❌ Invalid credentials")
#     else:
#         st.sidebar.header("Account Info")
#         st.sidebar.write(f"👤 User: {st.session_state.user}")
#         st.sidebar.write(f"🎚 Role: {st.session_state.role}")
#         st.sidebar.write(f"🔋 Remaining tokens: {st.session_state.usage[st.session_state.user]}")
        
#         if st.sidebar.button("🚪 Logout"):
#             st.session_state.user = None
#             st.rerun()
        
#         if st.session_state.role == 'admin':
#             admin_panel()
#         else:
#             if st.session_state.role == 'guest':
#                 st.warning("⚠️ Guest access - limited functionality")
#             chat_interface()

# if __name__ == "__main__":
#     main()


# app.py
import streamlit as st
from mistralai import Mistral
from datetime import datetime

# Configuration (could move to secrets.toml for production)
USERS = {
    "admin": {"password": "adminpass", "role": "admin", "tokens": 10000},
    "user1": {"password": "user1pass", "role": "user", "tokens": 1000},
    "guest": {"password": "", "role": "guest", "tokens": 100}
}

# Initialize session state safely
def init_session():
    if 'user' not in st.session_state:
        st.session_state['user'] = None
    if 'role' not in st.session_state:
        st.session_state['role'] = 'guest'
    if 'usage' not in st.session_state:
        st.session_state['usage'] = {user: USERS[user]['tokens'] for user in USERS}
    if 'max_tokens' not in st.session_state:
        st.session_state['max_tokens'] = 500
    if 'mistral_key' not in st.session_state:
        st.session_state['mistral_key'] = None

# Authentication system
def authenticate(username, password):
    user = USERS.get(username)
    if user and (user['password'] == password or username == 'guest'):
        st.session_state.user = username
        st.session_state.role = user['role']
        return True
    return False

# Admin panel
def admin_panel():
    st.subheader("🚀 Admin Dashboard")
    st.write("### API Usage")
    st.write(st.session_state.usage)

    st.session_state.mistral_key = st.text_input(
        "🔑 Mistral API Key",
        value=st.session_state.mistral_key or "",
        type="password"
    )

    st.session_state.max_tokens = st.slider(
        "🎚 Max Tokens per Request",
        100, 2000, st.session_state.max_tokens
    )

# Chat interface for users/guests
def chat_interface():
    st.subheader("💬 Chat with Mistral")
    prompt = st.text_area("Enter your prompt:", height=100)

    if st.button("🚀 Submit") and prompt:
        if st.session_state.usage[st.session_state.user] <= 0:
            st.error("❌ You've exceeded your token quota!")
            return

        if not st.session_state.mistral_key:
            st.error("❌ Please enter a valid Mistral API key.")
            return

        try:
            client = Mistral(api_key=st.session_state.mistral_key)
            response = client.chat.complete(
                model="mistral-large-latest",
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )

            # Approximate token usage if actual usage is not returned
            response_text = response.choices[0].message.content
            used_tokens = len(prompt.split()) + len(response_text.split())
            st.session_state.usage[st.session_state.user] -= used_tokens

            st.write("📝 Response:")
            st.write(response_text)

            st.success(f"🔋 Tokens remaining: {st.session_state.usage[st.session_state.user]}")
        
        except Exception as e:
            st.error(f"API Error: {str(e)}")

# Main application flow
def main():
    st.title("🔒 Mistral API Manager")
    init_session()

    if not st.session_state.user:
        st.subheader("🔑 Login")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button("Login"):
            if authenticate(username, password):
                st.success(f"✅ Logged in as {username}!")
                st.rerun()
            else:
                st.error("❌ Invalid credentials")
    else:
        st.sidebar.header("Account Info")
        st.sidebar.write(f"👤 User: {st.session_state.user}")
        st.sidebar.write(f"🎚 Role: {st.session_state.role}")
        st.sidebar.write(f"🔋 Remaining tokens: {st.session_state.usage[st.session_state.user]}")

        if st.sidebar.button("🚪 Logout"):
            st.session_state.user = None
            st.rerun()

        if st.session_state.role == 'admin':
            admin_panel()
        else:
            if st.session_state.role == 'guest':
                st.warning("⚠️ Guest access - limited functionality")
            chat_interface()

if __name__ == "__main__":
    main()
