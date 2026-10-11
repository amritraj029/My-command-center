import json
from pathlib import Path
import streamlit as st

from supabase import create_client, Client

# Supabase Connection Setup
SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# 1. Page Configuration
st.set_page_config(
    page_title="Nexus | Personal Command Center",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# 2. Professional Custom CSS Styling (Giving it a SaaS / Notion-like feel)
st.markdown(
    """
    <style>
        /* Global Background & Font */
        .main {
            background-color: #0e1117;
            color: #fafafa;
        }
        /* Custom Card Container */
        .metric-card {
            background-color: #161b22;
            border: 1px solid #30363d;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }
        /* Button Styling */
        .stButton>button {
            border-radius: 6px;
            font-weight: 600;
            transition: all 0.3s ease;
        }
        /* Headers */
        h1, h2, h3 {
            color: #58a6ff;
        }
    </style>
""",
    unsafe_allow_html=True,
)

# 3. Secure Login System
DATA_FILE = Path("user_data.json")


def load_data():
  if DATA_FILE.exists():
    try:
      return json.loads(DATA_FILE.read_text(encoding="utf-8"))
    except:
      pass
  return {"tasks": [], "movies": [], "assignments": [], "hobbies": []}


def save_data(data):
  DATA_FILE.write_text(json.dumps(data, indent=4), encoding="utf-8")


def check_password():
  def password_entered():
    if st.session_state["password"] == "bca123":
      st.session_state["password_correct"] = True
      del st.session_state["password"]
    else:
      st.session_state["password_correct"] = False

  if "password_correct" not in st.session_state:
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
      st.markdown(
          "<h2 style='text-align: center;'>🔒 Restricted Access</h2>",
          unsafe_allow_html=True,
      )
      st.text_input(
          "Enter Master Password",
          type="password",
          on_change=password_entered,
          key="password",
      )
    return False
  elif not st.session_state["password_correct"]:
    st.text_input(
        "Enter Master Password",
        type="password",
        on_change=password_entered,
        key="password",
    )
    st.error("⚠️ Invalid Credentials. Access Denied.")
    return False
  else:
    return True


if not check_password():
  st.stop()

user_data = load_data()

# ---------------------------------------------------------
# PROFESSIONAL SIDEBAR NAVIGATION
# ---------------------------------------------------------
st.sidebar.markdown(
    "<h3 style='color: #58a6ff;'>⚡ NEXUS OS</h3>", unsafe_allow_html=True
)
st.sidebar.caption("Private Command Center v2.0")
st.sidebar.divider()

menu = st.sidebar.radio(
    "Navigation",
    [
        "📊 Executive Dashboard",
        "✅ Task Matrix",
        "🎬 Entertainment Hub",
        "📚 Academic Tracker",
        "🚀 Skill Roadmap",
    ],
)

st.sidebar.divider()
if st.sidebar.button("🔒 Secure Lockout"):
  del st.session_state["password_correct"]
  st.rerun()

# ---------------------------------------------------------
# 1. EXECUTIVE DASHBOARD
# ---------------------------------------------------------
if menu == "📊 Executive Dashboard":
  st.title("📊 Executive Dashboard")
  st.write(
      "Welcome back, Commander. Here is your real-time operational status."
  )
  st.divider()

  # Metrics Row
  col1, col2, col3, col4 = st.columns(4)
  with col1:
    st.metric(
        label="Pending Tasks", value=len(user_data.get("tasks", []))
    )
  with col2:
    st.metric(label="Watchlist Items", value=len(user_data.get("movies", [])))
  with col3:
    st.metric(
        label="Active Assignments", value=len(user_data.get("assignments", []))
    )
  with col4:
    st.metric(label="Skill Goals", value=len(user_data.get("hobbies", [])))

  st.markdown("---")
  st.subheader("💡 Quick System Status")
  st.info(
      "🟢 All systems operational. Database connected securely via JSON storage."
      " Use the sidebar to switch between modules."
  )

# ---------------------------------------------------------
# 2. TASK MATRIX (To-Do - Supabase Connected)
# ---------------------------------------------------------
elif menu == "✅ Task Matrix":
    st.title("✅ Task & Productivity Matrix")

    with st.form("task_form", clear_on_submit=True):
        col_t1, col_t2 = st.columns([3, 1])
        with col_t1:
            new_task = st.text_input(
                "Task Description", placeholder="e.g., Build API automation script"
            )
        with col_t2:
            category = st.selectbox(
                "Category / Priority", ["🔥 High", "⚡ Medium", "☕ Low"], index=1
            )

        submitted = st.form_submit_button("➕ Add Task to Matrix")
        if submitted and new_task.strip():
            # Supabase me task insert karne ka code
            supabase.table("tasks").insert({
                "task_name": new_task.strip(),
                "status": "Pending",
                "category": category
            }).execute()
            st.success("Task successfully logged to Cloud Database!")
            st.rerun()

    st.divider()
    st.subheader("Active Tasks Queue (Supabase Cloud)")

    # Supabase se tasks fetch (load) karne ka code
    try:
        response = supabase.table("tasks").select("*").execute()
        tasks_data = response.data
    except Exception as e:
        tasks_data = []
        st.error(f"Error loading tasks from database: {e}")

    if tasks_data:
        for index, t in enumerate(tasks_data):
            cols = st.columns([0.1, 2.5, 1, 0.8])
            cols[0].write("🔹")
            cols[1].write(f"**{t.get('task_name')}**")
            cols[2].write(f"Category: {t.get('category')}")
            
            # Delete/Complete button
            if cols[3].button("🗑️ Complete", key=f"supabase_task_{t.get('id', index)}"):
                # Supabase se task delete karne ka code
                supabase.table("tasks").delete().eq("id", t.get("id")).execute()
                st.success("Task completed & removed from cloud!")
                st.rerun()
    else:
        st.success("🎉 Zero pending tasks! Your cloud queue is completely clear.")
# ---------------------------------------------------------
# 3. ENTERTAINMENT HUB (Movies & Series)
# ---------------------------------------------------------
elif menu == "🎬 Entertainment Hub":
  st.title("🎬 Entertainment & Media Hub")

  with st.form("movie_form", clear_on_submit=True):
    col_m1, col_m2 = st.columns([2, 1])
    with col_m1:
      m_title = st.text_input("Title", placeholder="e.g., Interstellar")
    with col_m2:
      m_genre = st.selectbox(
          "Genre", ["Sci-Fi", "Anime", "Action", "Drama", "Tech / Docu"]
      )

    if st.form_submit_button("➕ Add to Watchlist") and m_title.strip():
      user_data["movies"].append(
          {"title": m_title.strip(), "genre": m_genre, "status": "To Watch"}
      )
      save_data(user_data)
      st.success(f"Added '{m_title}' to media queue!")
      st.rerun()

  st.divider()
  st.subheader("Media Watchlist")

  if user_data["movies"]:
    for index, movie in enumerate(user_data["movies"]):
      cols = st.columns([2, 1, 1])
      cols[0].markdown(f"🍿 **{movie['title']}**")
      cols[1].caption(f"Genre: {movie['genre']}")
      if cols[2].button("✔️ Watched", key=f"movie_{index}"):
        user_data["movies"].pop(index)
        save_data(user_data)
        st.rerun()
  else:
    st.info("Watchlist is currently empty.")

# ---------------------------------------------------------
# 4. ACADEMIC TRACKER (College Assignments)
# ---------------------------------------------------------
elif menu == "📚 Academic Tracker":
  st.title("📚 Academic Assignment Tracker")

  with st.form("assignment_form", clear_on_submit=True):
    col_a1, col_a2, col_a3 = st.columns(3)
    with col_a1:
      sub = st.text_input("Subject", placeholder="e.g., Data Structures")
    with col_a2:
      desc = st.text_input("Assignment Task", placeholder="e.g., Linked List Lab")
    with col_a3:
      date = st.date_input("Deadline")

    if st.form_submit_button("➕ Log Assignment") and sub.strip():
      user_data["assignments"].append(
          {"subject": sub.strip(), "desc": desc.strip(), "date": str(date)}
      )
      save_data(user_data)
      st.success("Assignment deadline tracked successfully!")
      st.rerun()

  st.divider()
  st.subheader("Pending Deadlines")

  if user_data["assignments"]:
    for index, assign in enumerate(user_data["assignments"]):
      cols = st.columns([2, 1.5, 1])
      cols[0].markdown(f"📖 **{assign['subject']}**: {assign['desc']}")
      cols[1].text(f"⏳ Due: {assign['date']}")
      if cols[2].button("✔️ Submit", key=f"assign_{index}"):
        user_data["assignments"].pop(index)
        save_data(user_data)
        st.rerun()
  else:
    st.success("No upcoming assignment deadlines.")

# ---------------------------------------------------------
# 5. SKILL ROADMAP (Hobbies & Extra Activities)
# ---------------------------------------------------------
elif menu == "🚀 Skill Roadmap":
  st.title("🚀 Skill & Venture Roadmap")
  st.write(
      "Track your extracurricular learning, AI automation tracks, and startup"
      " ideas."
  )

  with st.form("hobby_form", clear_on_submit=True):
    col_h1, col_h2 = st.columns(2)
    with col_h1:
      skill = st.text_input(
          "Skill / Project", placeholder="e.g., Python AI Agents"
      )
    with col_h2:
      goal = st.text_input("Target Outcome", placeholder="e.g., Build 3 mini-apps")

    if st.form_submit_button("➕ Add Roadmap Goal") and skill.strip():
      user_data["hobbies"].append({"skill": skill.strip(), "goal": goal.strip()})
      save_data(user_data)
      st.success("Roadmap milestone added!")
      st.rerun()

  st.divider()
  st.subheader("Active Learning Milestones")

  if user_data["hobbies"]:
    for index, hobby in enumerate(user_data["hobbies"]):
      cols = st.columns([2, 1])
      cols[0].markdown(f"⚡ **{hobby['skill']}** ➔ *Goal: {hobby['goal']}*")
      if cols[1].button("🏆 Complete", key=f"hobby_{index}"):
        user_data["hobbies"].pop(index)
        save_data(user_data)
        st.rerun()
  else:
    st.info("No active roadmap milestones recorded.")
