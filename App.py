import streamlit as st

st.set_page_config(page_title="Smart Academic Tracker", page_icon="🎓", layout="centered")

# Custom Styling for Larger Purple Sidebar & Subtle Animated Shape
st.markdown("""
    <style>
    /* Sidebar purple gradient background */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #4c1d95 0%, #6d28d9 100%);
        color: #ffffff;
    }
    
    /* Make sidebar navigation radio options bigger and clearer */
    [data-testid="stSidebar"] .stRadio label p {
        font-size: 1.15rem !important;
        font-weight: 500 !important;
        color: #f3f4f6 !important;
    }
    
    /* Subtle animated background shape inside the sidebar */
    @keyframes floatShape {
        0% { transform: translateY(0px) scale(1); opacity: 0.4; }
        50% { transform: translateY(15px) scale(1.05); opacity: 0.7; }
        100% { transform: translateY(0px) scale(1); opacity: 0.4; }
    }
    [data-testid="stSidebar"]::before {
        content: "";
        position: absolute;
        bottom: 20px;
        right: -20px;
        width: 140px;
        height: 140px;
        background: rgba(255, 255, 255, 0.08);
        border-radius: 40% 60% 70% 30% / 40% 50% 60% 50%;
        animation: floatShape 8s infinite ease-in-out;
        pointer-events: none;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🎓 Smart Academic & Attendance Tracker")
st.write("Manage your semester attendance, track internal marks, and calculate your target finals score easily.")

# Initialize session state so data persists when clicking around
if "subjects" not in st.session_state:
    st.session_state.subjects = {}

# Sidebar navigation
menu = st.sidebar.radio("Navigation", ["📊 Dashboard & Attendance", "➕ Add / Update Subject", "🎯 Marks Predictor"])

if menu == "➕ Add / Update Subject":
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

elif menu == "📊 Dashboard & Attendance":
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
                    st.success("Safe ")
                else:
                    st.warning("Low ")
            
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

elif menu == "🎯 Marks Predictor":
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
                    st.error(" High target! Grind time for the finals.")
            else:
                st.error(f"❌ Mathematical limit exceeded! Max possible total with current internals is {internal + 40:.1f}/100.")
