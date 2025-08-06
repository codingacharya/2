import streamlit as st
import cv2
from datetime import datetime
from utils.face_utils import identify_employee
from utils.body_utils import extract_body_vector
from utils.camera_health import check_camera
import pandas as pd
import os

# Constants
EMPLOYEE_DB = "employee_db/"
LOG_FILE = "logs/entries_log.csv"

# UI
st.set_page_config(layout="wide")
st.title("🛡️ Intelligent Office Access System")

tab1, tab2, tab3 = st.tabs(["📷 Live Access Control", "📊 Access Log", "🛠️ Camera Health"])

with tab1:
    st.header("🔐 Real-time Access Control")

    camera_index = 0
    cap = cv2.VideoCapture(camera_index)
    if not cap.isOpened():
        st.error("Camera not accessible!")
    else:
        ret, frame = cap.read()
        if ret:
            # Face Recognition
            emp_id, match_score = identify_employee(frame)
            
            # Body vector (not stored here, just example)
            body_vector = extract_body_vector(frame)
            
            # Tailgating (simplified check)
            person_count = 1  # TODO: Replace with object detection logic

            access_granted = emp_id is not None and person_count == 1

            # Save log
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            if not os.path.exists(LOG_FILE):
                with open(LOG_FILE, 'w') as f:
                    f.write("timestamp,employee_id,match_score,person_count,access_granted\n")

            with open(LOG_FILE, 'a') as f:
                f.write(f"{now},{emp_id},{match_score:.2f},{person_count},{access_granted}\n")

            # Display result
            st.image(frame, channels="BGR", caption="Camera Feed")
            st.success("✅ Access Granted!" if access_granted else "❌ Access Denied")
            st.write(f"👤 Employee ID: `{emp_id}`")
            st.write(f"📈 Match Score: `{match_score:.2f}`")
            st.write(f"🚶 People Detected: `{person_count}`")

        cap.release()

with tab2:
    st.header("📊 Access Logs")
    if os.path.exists(LOG_FILE):
        df = pd.read_csv(LOG_FILE)
        st.dataframe(df[::-1], use_container_width=True)
    else:
        st.info("No logs yet.")

with tab3:
    st.header("🛠️ Camera Health Monitor")
    status = check_camera(0)
    if status:
        st.success("Camera is working")
    else:
        st.error("Camera not working!")
