import datetime
import json
from pathlib import Path
import random
import streamlit as st

from supabase import create_client, Client

# Supabase Connection Setup
SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# 1. Page Configuration (Sidebar hidden initially for clean look)
st.set_page_config(
    page_title="Nexus OS | Amrit Raj",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# 2. Professional Symmetric SaaS Custom CSS Styling
st.markdown(
    """
    <style>
        .main {
            background-color: #0b0f19;
            color: #f3f4f6;
        }
        
        /* Time Badge Header Widget */
        .time-badge {
            background: rgba(56, 189, 248, 0.12);
            border: 1px solid rgba(56, 189, 248, 0.3);
            color: #38bdf8;
            padding: 8px 16px;
            border-radius: 30px;
            font-size: 13px;
            font-weight: 600;
            text-align: right;
            display: inline-block;
        }

        /* Symmetric Module Card Styling */
        .module-card {
            background-color: #161b22;
            border-radius: 16px;
            padding: 22px;
            height: 220px;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            border: 1px solid rgba(255, 255, 255, 0.08);
            box-shadow: 0 8px 20px rgba(0,0,0,0.3);
            margin-bottom: 20px;
            transition: transform 0.2s ease, box-shadow 0.2s ease;
        }
        .module-card:hover {
            transform: translateY(-4px);
            box-shadow: 0 12px 28px rgba(0,0,0,0.5);
        }

        /* Distinct Card Left Border Accents */
        .card-todo { border-left: 6px solid #ec4899; background: linear-gradient(135deg, #161b22 0%, #2a1226 100%); }
        .card-assignment { border-left: 6px solid #3b82f6; background: linear-gradient(135deg, #161b22 0%, #10223b 100%); }
        .card-movies { border-left: 6px solid #f97316; background: linear-gradient(135deg, #161b22 0%, #381b10 100%); }
        .card-activity { border-left: 6px solid #10b981; background: linear-gradient(135deg, #161b22 0%, #0c3327 100%); }
        .card-thoughts { border-left: 6px solid #eab308; background: linear-gradient(135deg, #161b22 0%, #36280b 100%); }
        .card-games { border-left: 6px solid #8b5cf6; background: linear-gradient(135deg, #161b22 0%, #24163d 100%); }

        .card-title { font-size: 18px; font-weight: 700; margin: 0 0 6px 0; }
        .card-desc { color: #94a3b8; font-size: 13px; margin: 0; line-height: 1.4; }
        .card-status { font-size: 12px; font-weight: 600; color: #cbd5e1; }
        
        h1, h2, h3 { color: #38bdf8; }
    </style>
""",
    unsafe_allow_html=True,
)

# 3. Local Data Setup
DATA_FILE = Path("user_data.json")


def load_data():
  if DATA_FILE.exists():
    try:
      return json.loads(DATA_FILE.read_text(encoding="utf-8"))
    except:
      pass
  return {
      "movies": [],
      "assignments": [],
      "hobbies": [],
      "thoughts": [],
  }


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

# Fetch Supabase Tasks Count
try:
  res = supabase.table("tasks").select("*").execute()
  supabase_tasks = res.data
except Exception:
  supabase_tasks = []

# Quotes Generator (Changes on every refresh)
quotes_list = [
    "“The secret of getting ahead is getting started.” — Mark Twain",
    (
        "“Code is like humor. When you have to explain it, it’s bad.” — Cory"
        " House"
    ),
    (
        "“Fix the cause, not the symptom.” — Steve Maguire,"
        " Debugging-Expert"
    ),
    (
        "“Simplicity is prerequisite for reliability.” — Edsger W. Dijkstra"
    ),
    "“First, solve the problem. Then, write the code.” — John Johnson",
    (
        "“Experience is the name everyone gives to their mistakes.” — Oscar"
        " Wilde"
    ),
]
daily_quote = random.choice(quotes_list)

# Time & Greeting Setup
now = datetime.datetime.now()
current_time_str = now.strftime("%A, %b %d • %I:%M %p")
hour = now.hour
if hour < 12:
  greeting = "Good Morning 🌅"
elif hour < 17:
  greeting = "Good Afternoon ☀️"
else:
  greeting = "Good Evening 🌙"

# Initialize Session Navigation state if not present
if "active_menu" not in st.session_state:
  st.session_state["active_menu"] = "🏠 Welcome Dashboard"

# ---------------------------------------------------------
# SIDEBAR NAVIGATION
# ---------------------------------------------------------
st.sidebar.markdown(
    "<h3 style='color: #38bdf8;'>⚡ NEXUS OS</h3>", unsafe_allow_html=True
)
st.sidebar.caption("Personal Command Center v3.0")
st.sidebar.divider()

menu_options = [
    "🏠 Welcome Dashboard",
    "✅ To Do Matrix",
    "📚 Assignments",
    "🎬 Movies & Media",
    "⚽ Activity & Hobbies",
    "💡 Thoughts & Notes",
    "🎮 Online Games",
]

# Sync sidebar with session state
current_index = (
    menu_options.index(st.session_state["active_menu"])
    if st.session_state["active_menu"] in menu_options
    else 0
)
menu = st.sidebar.radio("Navigation", menu_options, index=current_index)
st.session_state["active_menu"] = menu

st.sidebar.divider()
if st.sidebar.button("🔒 Secure Lockout"):
  del st.session_state["password_correct"]
  st.rerun()

# ---------------------------------------------------------
# 1. WELCOME DASHBOARD
# ---------------------------------------------------------
if menu == "🏠 Welcome Dashboard":

  # TOP BANNER: Photo (Left) + Welcome & Quote (Center) + Time Badge Widget (Right)
  c_profile, c_welcome, c_widget = st.columns([1.2, 4.5, 2.3])

  with c_profile:
    img_path = Path("profile.jpg")
    if img_path.exists():
      st.image(str(img_path), width=100)
    else:
      st.markdown(
          """
                <div style="width: 100px; height: 100px; border-radius: 50%; background: linear-gradient(135deg, #38bdf8, #8b5cf6); display: flex; align-items: center; justify-content: center; font-size: 45px; box-shadow: 0 8px 20px rgba(56, 189, 248, 0.3);">
                    👦🏽
                </div>
            """,
          unsafe_allow_html=True,
      )

  with c_welcome:
    st.markdown(
        f"""
            <div style="padding-top: 5px;">
                <h1 style="margin: 0; color: #f8fafc; font-size: 30px;">{greeting}, Amrit Raj 🚀</h1>
                <p style="margin: 6px 0 0 0; color: #cbd5e1; font-size: 14px; font-style: italic;">
                    {daily_quote}
                </p>
            </div>
        """,
        unsafe_allow_html=True,
    )

  with c_widget:
    st.markdown(
        f"""
            <div style="text-align: right; padding-top: 8px;">
                <div class="time-badge">
                    ⏱️ {current_time_str}
                </div>
                <p style="margin: 6px 0 0 0; color: #10b981; font-size: 12px; font-weight: 600;">
                    🟢 All Systems Operational
                </p>
            </div>
        """,
        unsafe_allow_html=True,
    )

  st.divider()

  # LIVE METRICS BAR
  st.markdown("### 📊 Live System Metrics")
  m1, m2, m3, m4 = st.columns(4)
  m1.metric("To-Do Tasks", len(supabase_tasks))
  m2.metric("Assignments Due", len(user_data.get("assignments", [])))
  m3.metric("Watchlist", len(user_data.get("movies", [])))
  m4.metric("Saved Thoughts", len(user_data.get("thoughts", [])))

  st.divider()
  st.markdown("### 🎛️ Command Center Modules")

  # SYMMETRIC 6 CARDS GRID WITH CLICKABLE BUTTONS
  r1_c1, r1_c2 = st.columns(2)

  with r1_c1:
    st.markdown(
        f"""
            <div class="module-card card-todo">
                <div>
                    <div class="card-title" style="color: #ec4899;">✅ To Do Matrix (Imp)</div>
                    <p class="card-desc">Manage high-priority cloud tasks synced directly with Supabase database.</p>
                </div>
                <div class="card-status">PENDING: {len(supabase_tasks)} Items</div>
            </div>
        """,
        unsafe_allow_html=True,
    )
    if st.button("Open To Do Matrix", key="btn_todo", use_container_width=True):
      st.session_state["active_menu"] = "✅ To Do Matrix"
      st.rerun()

  with r1_c2:
    st.markdown(
        f"""
            <div class="module-card card-assignment">
                <div>
                    <div class="card-title" style="color: #3b82f6;">📚 Academic Assignments</div>
                    <p class="card-desc">Keep track of college lab submissions, BCA projects and deadlines.</p>
                </div>
                <div class="card-status">DEADLINES: {len(user_data.get('assignments', []))} Active</div>
            </div>
        """,
        unsafe_allow_html=True,
    )
    if st.button(
        "Open Assignments", key="btn_assign", use_container_width=True
    ):
      st.session_state["active_menu"] = "📚 Assignments"
      st.rerun()

  r2_c1, r2_c2 = st.columns(2)

  with r2_c1:
    st.markdown(
        f"""
            <div class="module-card card-movies">
                <div>
                    <div class="card-title" style="color: #f97316;">🎬 Entertainment Hub</div>
                    <p class="card-desc">Curated watchlist for movies, anime, and tech web series.</p>
                </div>
                <div class="card-status">WATCHLIST: {len(user_data.get('movies', []))} Shows</div>
            </div>
        """,
        unsafe_allow_html=True,
    )
    if st.button(
        "Open Entertainment Hub", key="btn_movies", use_container_width=True
    ):
      st.session_state["active_menu"] = "🎬 Movies & Media"
      st.rerun()

  with r2_c2:
    st.markdown(
        f"""
            <div class="module-card card-activity">
                <div>
                    <div class="card-title" style="color: #10b981;">⚽ Activities & Skills</div>
                    <p class="card-desc">Extracurricular milestones, Python tracks and self-growth goals.</p>
                </div>
                <div class="card-status">MILESTONES: {len(user_data.get('hobbies', []))} Active</div>
            </div>
        """,
        unsafe_allow_html=True,
    )
    if st.button(
        "Open Activity & Skills", key="btn_activity", use_container_width=True
    ):
      st.session_state["active_menu"] = "⚽ Activity & Hobbies"
      st.rerun()

  r3_c1, r3_c2 = st.columns(2)

  with r3_c1:
    st.markdown(
        f"""
            <div class="module-card card-thoughts">
                <div>
                    <div class="card-title" style="color: #eab308;">💡 Thoughts & Notes</div>
                    <p class="card-desc">Instant journal and quick code snippet ideas.</p>
                </div>
                <div class="card-status">RECORDED: {len(user_data.get('thoughts', []))} Notes</div>
            </div>
        """,
        unsafe_allow_html=True,
    )
    if st.button(
        "Open Thoughts & Notes", key="btn_thoughts", use_container_width=True
    ):
      st.session_state["active_menu"] = "💡 Thoughts & Notes"
      st.rerun()

  with r3_c2:
    st.markdown(
        """
            <div class="module-card card-games">
                <div>
                    <div class="card-title" style="color: #8b5cf6;">🎮 Online Game Zone</div>
                    <p class="card-desc">Quick interactive puzzle & arcade games for study breaks.</p>
                </div>
                <div class="card-status">STATUS: Ready to Play 🚀</div>
            </div>
        """,
        unsafe_allow_html=True,
    )
    if st.button("Open Game Zone", key="btn_games", use_container_width=True):
      st.session_state["active_menu"] = "🎮 Online Games"
      st.rerun()

# ---------------------------------------------------------
# 2. TO DO MATRIX (SUPABASE)
# ---------------------------------------------------------
elif menu == "✅ To Do Matrix":
  st.title("✅ To Do List & Productivity Matrix")

  with st.form("task_form", clear_on_submit=True):
    col_t1, col_t2 = st.columns([3, 1])
    with col_t1:
      new_task = st.text_input(
          "Task Description", placeholder="e.g., Complete Python script"
      )
    with col_t2:
      category = st.selectbox(
          "Priority Level", ["🔥 High", "⚡ Medium", "☕ Low"], index=0
      )

    submitted = st.form_submit_button("➕ Add Task to Cloud")
    if submitted and new_task.strip():
      supabase.table("tasks").insert({
          "task_name": new_task.strip(),
          "status": "Pending",
          "category": category,
      }).execute()
      st.success("Task logged successfully!")
      st.rerun()

  st.divider()
  st.subheader("Active Cloud Queue")

  if supabase_tasks:
    for index, t in enumerate(supabase_tasks):
      cols = st.columns([0.1, 2.5, 1, 0.8])
      cols[0].write("🔹")
      cols[1].write(f"**{t.get('task_name')}**")
      cols[2].write(f"Priority: {t.get('category')}")

      if cols[3].button(
          "🗑️ Complete", key=f"supabase_task_{t.get('id', index)}"
      ):
        supabase.table("tasks").delete().eq("id", t.get("id")).execute()
        st.success("Task finished!")
        st.rerun()
  else:
    st.success("🎉 All tasks completed! Cloud queue is clear.")

# ---------------------------------------------------------
# 3. ASSIGNMENTS
# ---------------------------------------------------------
elif menu == "📚 Assignments":
  st.title("📚 Academic Assignment Tracker")

  with st.form("assignment_form", clear_on_submit=True):
    col_a1, col_a2, col_a3 = st.columns(3)
    with col_a1:
      sub = st.text_input("Subject", placeholder="e.g., Data Structures")
    with col_a2:
      desc = st.text_input("Task Detail", placeholder="e.g., Practical Lab 3")
    with col_a3:
      date = st.date_input("Deadline")

    if st.form_submit_button("➕ Log Assignment") and sub.strip():
      user_data["assignments"].append(
          {"subject": sub.strip(), "desc": desc.strip(), "date": str(date)}
      )
      save_data(user_data)
      st.success("Assignment added!")
      st.rerun()

  st.divider()
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
    st.success("No upcoming assignments.")

# ---------------------------------------------------------
# 4. MOVIES
# ---------------------------------------------------------
elif menu == "🎬 Movies & Media":
  st.title("🎬 Entertainment Hub")

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
      st.success("Added to watchlist!")
      st.rerun()

  st.divider()
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
    st.info("Watchlist is empty.")

# ---------------------------------------------------------
# 5. ACTIVITY
# ---------------------------------------------------------
elif menu == "⚽ Activity & Hobbies":
  st.title("⚽ Activity & Skill Roadmap")

  with st.form("hobby_form", clear_on_submit=True):
    col_h1, col_h2 = st.columns(2)
    with col_h1:
      skill = st.text_input(
          "Skill / Goal", placeholder="e.g., Python Web Dev"
      )
    with col_h2:
      goal = st.text_input(
          "Target Outcome", placeholder="e.g., Build Portfolio App"
      )

    if st.form_submit_button("➕ Add Goal") and skill.strip():
      user_data["hobbies"].append({"skill": skill.strip(), "goal": goal.strip()})
      save_data(user_data)
      st.success("Goal added!")
      st.rerun()

  st.divider()
  if user_data["hobbies"]:
    for index, hobby in enumerate(user_data["hobbies"]):
      cols = st.columns([2, 1])
      cols[0].markdown(f"⚡ **{hobby['skill']}** ➔ *Goal: {hobby['goal']}*")
      if cols[1].button("🏆 Complete", key=f"hobby_{index}"):
        user_data["hobbies"].pop(index)
        save_data(user_data)
        st.rerun()
  else:
    st.info("No active milestones.")

# ---------------------------------------------------------
# 6. THOUGHTS & NOTES
# ---------------------------------------------------------
elif menu == "💡 Thoughts & Notes":
  st.title("💡 Personal Thoughts & Journal")

  new_thought = st.text_area(
      "Write a quick thought or idea:",
      placeholder="Type your notes here...",
  )
  if st.button("💾 Save Thought") and new_thought.strip():
    if "thoughts" not in user_data:
      user_data["thoughts"] = []
    user_data["thoughts"].append(new_thought.strip())
    save_data(user_data)
    st.success("Note saved!")
    st.rerun()

  st.divider()
  if user_data.get("thoughts"):
    for idx, t in enumerate(user_data["thoughts"]):
      cols = st.columns([3, 0.5])
      cols[0].info(t)
      if cols[1].button("🗑️", key=f"thought_{idx}"):
        user_data["thoughts"].pop(idx)
        save_data(user_data)
        st.rerun()
  else:
    st.caption("No notes saved yet.")

# ---------------------------------------------------------
# 7. ONLINE GAMES
# ---------------------------------------------------------
elif menu == "🎮 Online Games":
  st.title("🎮 Arcade & Study Break Zone")
  st.write(
      "Enjoy a quick puzzle game to refresh your mind before getting back to"
      " coding!"
  )

  tab1, tab2 = st.tabs(["⭕ Tic-Tac-Toe", "🧩 2048 Puzzle"])

  with tab1:
    st.components.v1.iframe(
        "https://playtictactoe.org/", height=520, scrolling=False
    )

  with tab2:
    st.components.v1.iframe(
        "https://play2048.co/", height=550, scrolling=False
    )
