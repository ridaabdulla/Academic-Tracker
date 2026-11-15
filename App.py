import streamlit as st

st.set_page_config(page_title="Academic Tracker", layout="centered")

# Minimal Aesthetic Styling
st.markdown("""
    <style>
    .main {
        background-color: #fafafa;
    }
    h1, h2, h3 {
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
        font-weight: 500;
        color: #111111;
        letter-spacing: -0.5px;
    }
    .stButton > button {
        border-radius: 6px;
        border: 1px solid #d0d0d0;
        background-color: #ffffff;
        color: #111111;
        font-weight: 500;
    }
    .stButton > button:hover {
        border-color: #111111;
        background-color: #f5f5f5;
    }
    </style>
""", unsafe_allow_html=True)

st.title("Academic & Attendance Tracker")
st.caption("KTU 2024 Scheme (40 Internal + 60 End-Sem)")

# Initialize session state
if "subjects" not in st.session_state:
    st.session_state.subjects = {}

# Sidebar navigation
menu = st.sidebar.radio("Navigation", ["Dashboard & Attendance", "Add / Update Subject", "Marks Predictor"])

if menu == "Add / Update Subject":
    st.subheader("Add or Update a Subject")
    with st.form("subject_form"):
        name = st.text_input("Subject Name (e.g., Algorithmic Thinking with Python)").strip()
        total = st.number_input("Total classes conducted so far", min_value=0, value=10, step=1)
        attended = st.number_input("Total classes attended", min_value=0, value=8, step=1)
        internal = st.number_input("Current internal marks (out of 40)", min_value=0.0, max_value=40.0, value=30.0, step=0.5)
        
        submitted = st.form_submit_button("Save Subject")
        if submitted:
            if not name:
                st.error("Subject name cannot be empty.")
            elif attended > total:
                st.error("Attended classes cannot exceed total classes.")
            else:
                st.session_state.subjects[name] = {
                    "total": total,
                    "attended": attended,
                    "internal": internal
                }
                st.success(f"Saved {name}.")

elif menu == "Dashboard & Attendance":
    st.subheader("Semester Dashboard")
    if not st.session_state.subjects:
        st.info("No subjects added yet. Go to 'Add / Update Subject' in the sidebar to begin.")
    else:
        for name, data in st.session_state.subjects.items():
            total = data["total"]
            attended = data["attended"]
            internal = data["internal"]
            pct = (attended / total * 100) if total > 0 else 0
            
            col1, col2, col3 = st.columns([2, 1.5, 1])
            with col1:
                st.markdown(f"**{name}**")
                st.caption(f"Attended: {attended}/{total}  |  Internals: {internal}/40")
            with col2:
                st.metric("Attendance", f"{pct:.1f}%")
            with col3:
                if pct >= 75:
                    st.success("Eligible")
                else:
                    st.warning("Shortage")
            
            st.progress(min(pct / 100.0, 1.0))
            st.markdown("---")

elif menu == "Marks Predictor":
    st.subheader("End-Sem Marks Predictor")
    if not st.session_state.subjects:
        st.info("No subjects found. Add your subjects first.")
    else:
        subject_list = list(st.session_state.subjects.keys())
        selected_subject = st.selectbox("Select Subject", subject_list)
        
        internal = st.session_state.subjects[selected_subject]["internal"]
        st.write(f"Current Internals for **{selected_subject}**: **{internal} / 40**")
        
        target_total = st.number_input("Target Total Marks (out of 100)", min_value=0.0, max_value=100.0, value=80.0, step=1.0)
        
        if st.button("Calculate Required End-Sem Marks"):
            # KTU 2024 Scheme: Total (100) = Internal (40) + End-Sem scaled to 60 (i.e., Exam_Score * 0.6)
            required_scaled = target_total - internal
            required_out_of_100 = (required_scaled / 60.0) * 100.0
            
            if required_out_of_100 <= 100:
                # Note: KTU minimum end-sem pass requirement is typically 40% (40/100)
                effective_required = max(required_out_of_100, 40.0)
                
                st.success(f"To reach {target_total}/100 total, you need **{required_out_of_100:.1f}/100** in the End-Sem exam (which scales to {required_scaled:.1f}/60).")
                
                if required_out_of_100 < 40.0:
                    st.info("Note: While your score target requires less, you still need a minimum of 40/100 in the End-Sem exam to pass as per KTU norms.")
                elif required_out_of_100 <= 55:
                    st.info("Comfortable target. Steady revision will get you there.")
                elif required_out_of_100 <= 75:
                    st.warning("Moderate target. Focus on previous year questions and core modules.")
                else:
                    st.error("High target. Requires thorough preparation across all modules.")
            else:
                max_possible = internal + 60.0
                st.error(f"Target exceeds maximum possible score. With {internal}/40 internals, your maximum possible total is {max_possible:.1f}/100.")
