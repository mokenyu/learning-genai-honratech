import streamlit as st
import requests
import json
import time

# --- Page Configuration ---
st.set_page_config(
    page_title="FastAPI Route Dashboard",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.2rem;
        font-weight: 700;
        color: #1E88E5;
        margin-bottom: 0.2rem;
    }
    .sub-header {
        font-size: 1rem;
        color: #555;
        margin-bottom: 1.5rem;
    }
    .status-200 {
        color: #2e7d32;
        font-weight: bold;
    }
    .status-error {
        color: #c62828;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# --- Sidebar Configuration ---
with st.sidebar:
    st.title("⚙️ API Configuration")
    
    backend_url = st.text_input(
        "Backend Base URL",
        value="http://localhost:8000",
        help="Target FastAPI backend server URL"
    ).rstrip("/")
    
    st.markdown("---")
    
    # Backend Health Check Button
    st.subheader("🔌 Connection Status")
    if st.button("Check Backend Connection", use_container_width=True):
        try:
            start_time = time.time()
            resp = requests.get(f"{backend_url}/?action=health_check", timeout=3)
            elapsed = round((time.time() - start_time) * 1000, 2)
            if resp.status_code == 200:
                st.success(f"Connected! ({elapsed} ms)")
            else:
                st.warning(f"Backend responded with status code: {resp.status_code}")
        except Exception as e:
            st.error(f"Failed to connect: {str(e)}")

    st.markdown("---")
    st.subheader("📍 Route Navigation")
    navigation = st.radio(
        "Select Router / Category:",
        [
            "🏠 Root Endpoint (/)",
            "🛍️ Product Router (/product)",
            "👤 Profile Router (/profile)",
            "🧩 Miscellaneous Router (/multi)"
        ]
    )
    
    st.markdown("---")
    st.caption("🚀 FastAPI + Streamlit Interface")

# --- Helper Function for Request Execution ---
def execute_request(method, url, params=None, data=None, json_payload=None, files=None):
    """Executes HTTP request and displays formatted response metadata."""
    st.markdown(f"**Request:** `{method.upper()} {url}`")
    
    if params:
        st.caption(f"Query Params: `{params}`")
    if json_payload:
        st.caption("JSON Payload:")
        st.json(json_payload)
    if data:
        st.caption(f"Form Data: `{data}`")
    if files:
        st.caption(f"Files Uploaded: `{list(files.keys())}`")
        
    try:
        start_time = time.time()
        response = requests.request(
            method=method,
            url=url,
            params=params,
            data=data,
            json=json_payload,
            files=files,
            timeout=10
        )
        elapsed_ms = round((time.time() - start_time) * 1000, 2)
        
        # Display Status Code & Time
        col1, col2 = st.columns(2)
        with col1:
            if response.status_code == 200:
                st.markdown(f"Status Code: <span class='status-200'>{response.status_code} OK</span>", unsafe_allow_html=True)
            else:
                st.markdown(f"Status Code: <span class='status-error'>{response.status_code}</span>", unsafe_allow_html=True)
        with col2:
            st.markdown(f"⏱️ Response Time: **{elapsed_ms} ms**")
            
        # Display Body
        st.subheader("📥 Response Data")
        try:
            json_res = response.json()
            st.json(json_res)
        except Exception:
            st.code(response.text)
            
    except requests.exceptions.ConnectionError:
        st.error(f"❌ Could not connect to backend server at `{backend_url}`. Please ensure FastAPI is running (e.g. `uvicorn main:app --reload`).")
    except Exception as err:
        st.error(f"❌ Error executing request: {str(err)}")


# --- Main Application Header ---
st.markdown("<div class='main-header'>FastAPI Route Dashboard</div>", unsafe_allow_html=True)
st.markdown("<div class='sub-header'>Interactive UI for routes in <code>backend/main.py</code> and connected routers</div>", unsafe_allow_html=True)


# --- Section 1: Root Endpoint ---
if navigation == "🏠 Root Endpoint (/)":
    st.header("🏠 Root Endpoint")
    st.write("Endpoint defined in `backend/main.py` (`GET /`) requiring an `action` query parameter.")
    
    with st.form("root_form"):
        action_param = st.text_input("Action Parameter (`action`)", value="get_info", help="Action string passed to the root endpoint")
        submit_root = st.form_submit_button("Send GET Request 🚀")
        
    if submit_root:
        execute_request(
            method="GET",
            url=f"{backend_url}/",
            params={"action": action_param}
        )


# --- Section 2: Product Router ---
elif navigation == "🛍️ Product Router (/product)":
    st.header("🛍️ Product Router")
    st.caption("Endpoints defined in `backend/fastapi_advanced/app2.py` (Prefix: `/product`)")
    
    st.subheader("🔍 Search Product (`GET /product/search-product`)")
    st.write("Search product catalog by category, page number, and optional product ID.")
    
    with st.form("product_search_form"):
        col1, col2, col3 = st.columns(3)
        with col1:
            category = st.text_input("Category", value="electronics")
        with col2:
            page = st.number_input("Page Number", min_value=1, value=1, step=1)
        with col3:
            product_id_input = st.selectbox("Product ID (Optional)", options=["None", 1, 2, 3], index=1)
            
        submit_search = st.form_submit_button("Search Product 🔎")
        
    if submit_search:
        params = {
            "category": category,
            "page": int(page)
        }
        if product_id_input != "None":
            params["id"] = int(product_id_input)
            
        execute_request(
            method="GET",
            url=f"{backend_url}/product/search-product",
            params=params
        )


# --- Section 3: Profile Router ---
elif navigation == "👤 Profile Router (/profile)":
    st.header("👤 Profile Router")
    st.caption("Endpoints defined in `backend/fastapi_advanced/app.py` (Prefix: `/profile`)")
    
    st.subheader("📤 Profile Test Upload (`POST /profile/test`)")
    st.write("Upload a file alongside form data (`status`).")
    
    uploaded_file = st.file_uploader("Choose a file to upload", type=None)
    status_flag = st.checkbox("Status Flag (`status`)", value=True)
    
    if st.button("Upload & Test Profile Endpoint 📤"):
        if uploaded_file is None:
            st.warning("Please select a file to upload before submitting.")
        else:
            files_payload = {
                "file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type or "application/octet-stream")
            }
            data_payload = {
                "status": "true" if status_flag else "false"
            }
            execute_request(
                method="POST",
                url=f"{backend_url}/profile/test",
                data=data_payload,
                files=files_payload
            )


# --- Section 4: Miscellaneous Router ---
elif navigation == "🧩 Miscellaneous Router (/multi)":
    st.header("🧩 Miscellaneous Router")
    st.caption("Endpoints defined in `backend/first_app.py` (Prefix: `/multi`)")
    
    multi_tab1, multi_tab2, multi_tab3, multi_tab4, multi_tab5 = st.tabs([
        "👋 Hello & Default Sentiment",
        "💬 Dynamic Sentiment Analysis",
        "⚙️ Config Parameters",
        "📝 Post User Data",
        "🤖 Post AI Prompt"
    ])
    
    # Tab 1: Hello & Default Sentiment
    with multi_tab1:
        st.subheader("Simple GET Requests")
        col_a, col_b = st.columns(2)
        
        with col_a:
            st.markdown("#### `GET /multi/hello`")
            if st.button("Call `/multi/hello`"):
                execute_request(method="GET", url=f"{backend_url}/multi/hello")
                
        with col_b:
            st.markdown("#### `GET /multi/sentiment-analysis`")
            if st.button("Call `/multi/sentiment-analysis`"):
                execute_request(method="GET", url=f"{backend_url}/multi/sentiment-analysis")
                
    # Tab 2: Dynamic Sentiment Analysis
    with multi_tab2:
        st.subheader("💬 Sentiment Analysis by Text (`GET /multi/sentiment/{text}`)")
        st.write("Evaluates text input (e.g. keywords like *good*, *nice*, *great* vs others).")
        
        sample_text = st.text_input("Enter Text for Sentiment Analysis", value="great")
        if st.button("Analyze Sentiment"):
            execute_request(
                method="GET",
                url=f"{backend_url}/multi/sentiment/{sample_text.strip()}"
            )
            
    # Tab 3: Config Parameters
    with multi_tab3:
        st.subheader("⚙️ Config Endpoint (`GET /multi/get-config/{response}`)")
        config_param = st.text_input("Config Parameter / Temperature", value="0.7")
        if st.button("Fetch Config"):
            execute_request(
                method="GET",
                url=f"{backend_url}/multi/get-config/{config_param.strip()}"
            )
            
    # Tab 4: Post User Data
    with multi_tab4:
        st.subheader("📝 User Data Submission (`POST /multi/posting-data`)")
        with st.form("user_data_form"):
            user_name = st.text_input("Name", value="Alice")
            user_age = st.number_input("Age", min_value=1, max_value=120, value=25)
            user_fav_meal = st.text_input("Favorite Meal", value="Pizza")
            user_is_sleepy = st.checkbox("Is Sleepy?", value=False)
            
            submit_user_data = st.form_submit_button("Submit User Data 📤")
            
        if submit_user_data:
            user_payload = {
                "name": user_name,
                "age": int(user_age),
                "favMeal": user_fav_meal,
                "isSleepy": user_is_sleepy
            }
            execute_request(
                method="POST",
                url=f"{backend_url}/multi/posting-data",
                json_payload=user_payload
            )

    # Tab 5: Post AI Data
    with multi_tab5:
        st.subheader("🤖 AI Data Prompt (`POST /multi/ai-post`)")
        with st.form("ai_data_form"):
            ai_name = st.text_input("AI Model / Task Name", value="Summarizer")
            ai_prompt = st.text_area("Prompt", value="Explain FastAPI in three bullet points.")
            ai_id = st.number_input("ID", min_value=1, value=101)
            
            submit_ai_data = st.form_submit_button("Submit AI Prompt 🤖")
            
        if submit_ai_data:
            ai_payload = {
                "name": ai_name,
                "prompt": ai_prompt,
                "id": int(ai_id)
            }
            execute_request(
                method="POST",
                url=f"{backend_url}/multi/ai-post",
                json_payload=ai_payload
            )
