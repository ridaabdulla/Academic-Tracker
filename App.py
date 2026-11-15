import streamlit as st

st.set_page_config(page_title="Smart Academic Tracker", layout="centered")

# Custom Styling: Google Font (Plus Jakarta Sans), Soft Lavender Dashboard, Beige Sidebar, and Single Floating Blob
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap');

    /* Apply modern font globally */
    html, body, [class*="css"], .stApp, button, input, select, textarea {
        font-family: 'Plus Jakarta Sans', sans-serif !important;
    }

    h1, h2, h3 {
        font-weight: 700 !important;
        letter-spacing: -0.02em;
        color: #1f1b24;
    }

    /* Main app background - soft lavender */
    .stApp {
        background-color: #f3eef8;
    }
    
    /* Sidebar background - warm beige */
    [data-testid="stSidebar"] {
        background-color: #f5f2eb;
        color: #2b2b2b;
    }
    
    /* Make sidebar navigation labels bigger and darker for contrast */
    [data-testid="stSidebar"] .stRadio label p {
        font-size: 1.15rem !important;
        font-weight: 600 !important;
        color: #2b2b2b !important;
    }
    
    /* Subtle floating organic shape */
    @keyframes floatSlow {
        0% { transform: translateY(0px) rotate(0deg); opacity: 0.5; }
        50% { transform: translateY(-15px) rotate(180deg); opacity: 0.8; }
        100% { transform: translateY(0px) rotate(360deg); opacity: 0.5; }
    }
    
    .floating-shape-1 {
        position: fixed;
        top: 80px;
        right: 40px;
        width: 75px;
        height: 75px;
        background: rgba(205, 193, 225, 0.4);
        border-radius: 30% 70% 70% 30% / 30% 30% 70% 70%;
        animation: floatSlow 10s infinite ease-in-out;
        z-index: 1;
        pointer-events: none;
    }
    </style>
    
    <div class="floating-shape-1"></div>
""", unsafe_allow_html=True)

st.title("Smart Academic & Attendance Tracker")
st.write("Manage your semester attendance, track internal marks, and calculate your target finals score easily.")

# Initialize session state so data persists when clicking around
if "subjects" not in st.session_state:
    st.session_state.subjects = {}

# Sidebar navigation
menu = st.sidebar.radio("Navigation", ["Dashboard & Attendance", "Add / Update Subject", "Marks Predictor"])

if menu == "Add / Update Subject":
    st.subheader("Add or Update a Subject")
    with st.form("subject_form"):
        name = st.text_input("Subject Name (e.g., Data Structures)").strip()
        total = st.number_input("Total classes conducted so far", min_value=0, value=10, step=1)
        attended = st.number_input("Total classes you attended", min_value=0, value=8, step=1)
        internal = st.number_input("Current internal marks (out of 40)", min_value=0.0, max_value=40.0, value=35.0, step=0.5)
        
        submitted = st.form_submit_button("Save Subject")
        if submitted:
            if not name:
                st.error("Subject name cannot be empty!")
            elif attended > total:
                st.error("Attended classes cannot exceed total classes!")
            else:
                st.session_state.subjects[name] = {
                    "total": total,
                    "attended": attended,
                    "internal": internal
                }
                st.success(f"Successfully saved {name}!")

elif menu == "Dashboard & Attendance":
    st.subheader("Your Semester Dashboard")
    if not st.session_state.subjects:
        st.info("No subjects added yet! Go to 'Add / Update Subject' in the sidebar to start.")
    else:
        for name, data in st.session_state.subjects.items():
            total = data["total"]
            attended = data["attended"]
            pct = (attended / total * 100) if total > 0 else 0
            
            col1, col2, col3 = st.columns([2, 2, 1])
            with col1:
                st.markdown(f"**{name}**")
                st.write(f"Attended: {attended}/{total}")
            with col2:
                st.metric("Attendance", f"{pct:.1f}%")
            with col3:
                if pct >= 75:
                    st.success("Safe")
                else:
                    st.warning("Low")
            
            # Progress bar
            st.progress(min(pct / 100.0, 1.0))
            
            # Attendance Skip / Required Calculation
            target_pct = 75.0
            if pct >= target_pct:
                skippable = int((attended - (0.75 * total)) / 0.75)
                if skippable > 0:
                    st.info(f"You can safely skip up to **{skippable}** upcoming classes without dropping below 75%.")
                else:
                    st.write("You are right at the 75% edge. Do not skip any classes.")
            else:
                needed = int((3 * total - 4 * attended + 3) / 4)
                st.warning(f"You need to attend the next **{needed}** classes consecutively to reach 75%.")
            
            st.markdown("---")

elif menu == "Marks Predictor":
    st.subheader("End-Sem Marks Predictor")
    if not st.session_state.subjects:
        st.info("No subjects found! Add your subjects first.")
    else:
        subject_list = list(st.session_state.subjects.keys())
        selected_subject = st.selectbox("Select Subject", subject_list)
        
        internal = st.session_state.subjects[selected_subject]["internal"]
        st.write(f"Current Internals for **{selected_subject}**: **{internal}/40**")
        
        target_total = st.number_input("Enter your Target Total Marks out of 100", min_value=0.0, max_value=100.0, value=80.0, step=1.0)
        
        if st.button("Calculate Required End-Sem Marks"):
            required_end_sem = (target_total - internal) * 2
            if required_end_sem <= 100:
                st.success(f"To get {target_total}/100 total, you need at least **{required_end_sem:.1f}/100** in the End-Sem exam.")
                if required_end_sem <= 40:
                    st.info("Easy target! You're cruising.")
                elif required_end_sem <= 70:
                    st.warning("Moderate effort needed. Keep your notes ready.")
                else:
                    st.error("High target! Grind time for the finals.")
            else:
                st.error(f"Mathematical limit exceeded! Max possible total with current internals is {internal + 40:.1f}/100.")
