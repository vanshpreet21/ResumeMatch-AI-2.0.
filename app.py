import html
from datetime import datetime

import plotly.graph_objects as go
import streamlit as st

from resume_parser import extract_text
from matcher import analyze_resume
from ats_checker import check_ats
from career_chatbot import coach_reply
from llm_chatbot import ask_llm
from career_roadmap import create_roadmap
from job_fit_finder import rank_job_roles
from interview_coach import make_questions, evaluate_answer
from resume_comparison import compare_resumes

st.set_page_config(page_title="ResumeMatch AI 2.0 | Career Dashboard", page_icon="🎯", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
<style>
:root {color-scheme:dark}
.stApp {background:#0b1120 !important;color:#f8fafc}
[data-testid="stHeader"] {background:#0b1120 !important}
.block-container {max-width:1280px !important;padding-top:1.5rem !important;padding-bottom:5rem !important}
[data-testid="stSidebar"] {background:#0e1930 !important;border-right:1px solid #273a5c}
[data-testid="stSidebar"] * {color:#e5edff !important}
.stApp h1,.stApp h2,.stApp h3 {color:#f8fafc !important;letter-spacing:-.03em}
.stApp h2 {font-size:1.65rem !important}
.stApp h3 {font-size:1.15rem !important}
.stApp p,.stApp label,.stApp li {color:#dce7fa}
.stApp small,[data-testid="stCaptionContainer"] * {color:#b4c5e2 !important}
[data-testid="stTextArea"] textarea,.stApp input {background:#17243a !important;color:#fff !important;border:1px solid #4b6181 !important}
.stApp textarea::placeholder,.stApp input::placeholder {color:#b3c3df !important;opacity:1}
[data-testid="stFileUploader"] section {background:#17243a !important;border:1px dashed #647b9e !important;border-radius:14px}
[data-testid="stFileUploader"] section * {color:#eaf0ff !important}
[data-testid="stFileUploader"] section button {background:#e8f0ff !important;color:#0b1120 !important}
.stButton>button[kind="primary"] {background:linear-gradient(90deg,#2563eb,#7c3aed) !important;color:#fff !important;border:0 !important;border-radius:12px !important;min-height:50px;font-weight:700}
.stButton>button[kind="primary"] * {color:#fff !important}
.stButton>button {border-radius:12px}
[data-testid="stMetric"] {background:linear-gradient(145deg,#1b304f,#17263f) !important;border:1px solid #30466a !important;border-radius:17px;padding:17px 20px;min-height:117px;box-shadow:0 12px 24px #02061740}
[data-testid="stMetricLabel"] * {color:#afc5e7 !important}
[data-testid="stMetricValue"] * {color:#fff !important;font-size:2rem !important;font-weight:800 !important}
.hero {background:linear-gradient(105deg,#1a3c63,#282049);border:1px solid #345780;border-radius:20px;padding:25px 29px;margin-bottom:14px}
.hero .eyebrow {color:#93c5fd;font-size:12px;letter-spacing:2px;font-weight:800}
.hero h1 {margin:7px 0 8px !important;font-size:2.05rem !important}
.hero p {color:#cbdaf1 !important;margin:0 !important}
.eyebrow {font-size:12px;color:#9abcfb;font-weight:800;letter-spacing:1.7px;margin:10px 0 5px}
.panel {background:#1a2c48;border:1px solid #2e4567;border-radius:18px;padding:20px 22px;margin:6px 0 12px;box-shadow:0 8px 25px #03071226}
.panel h3 {font-size:1.06rem !important;margin:0 0 9px !important}
.panel .muted {color:#afc3e0 !important;font-size:13px}
.tag {display:inline-block;padding:7px 12px;margin:3px 5px 3px 0;border-radius:999px;font-size:12px;font-weight:600}
.tag-ok {background:#145334;color:#bbf7d0;border:1px solid #257a53}
.tag-warn {background:#644015;color:#ffdf99;border:1px solid #986524}
.priority {display:flex;align-items:center;gap:12px;padding:10px 0;border-bottom:1px solid #314562}
.priority:last-child {border:0}
.priority .number {background:#263e60;color:#a5caff;padding:7px 11px;border-radius:9px;font-weight:700}
.priority .name {color:#edf4ff;font-weight:600}
[data-testid="stPlotlyChart"] {border:1px solid #30466a;border-radius:18px;overflow:hidden}
[data-testid="stExpander"] {background:#14243b;border:1px solid #30466a;border-radius:12px}
[data-testid="stDataFrame"] {border-radius:12px;overflow:hidden}
.st-key-floating_chat {position:fixed !important;right:24px !important;bottom:22px !important;z-index:999999 !important;width:82px !important;max-width:82px !important}
.st-key-floating_chat [data-testid="stPopover"],.st-key-floating_chat [data-testid="stPopover"]>div {width:82px !important}
.st-key-floating_chat button {width:78px !important;height:78px !important;min-width:78px !important;min-height:78px !important;max-width:78px !important;border-radius:50% !important;background:linear-gradient(135deg,#3b82f6,#7c3aed 75%) !important;color:white !important;border:3px solid #a5b4fc !important;padding:0 !important;font-size:34px !important;box-shadow:0 0 0 6px #6366f12e,0 12px 32px #4f46e588 !important}
.st-key-floating_chat button * {color:white !important;font-size:34px !important}
.st-key-floating_chat button:hover {transform:scale(1.06)}
[data-testid="stPopoverBody"] {min-width:min(390px,90vw) !important;max-width:430px !important;border:1px solid #6366f1 !important;border-radius:19px !important;background:#101e35 !important;box-shadow:0 20px 55px #0008 !important}
[data-testid="stPopoverBody"] * {color:#f8fafc}
[data-testid="stPopoverBody"] input,
[data-testid="stPopoverBody"] textarea,
[data-testid="stPopoverBody"] [data-baseweb="input"] input {
    background-color:#f8fafc !important;
    color:#0f172a !important;
    -webkit-text-fill-color:#0f172a !important;
    caret-color:#0f172a !important;
    border-radius:9px !important;
}
[data-testid="stPopoverBody"] input::placeholder,
[data-testid="stPopoverBody"] textarea::placeholder {
    color:#64748b !important;
    -webkit-text-fill-color:#64748b !important;
    opacity:1 !important;
}
[data-testid="stPopoverBody"] [data-testid="stChatMessage"] {
    background:#1e3050 !important;
    border:1px solid #385174 !important;
    border-radius:13px !important;
}
[data-testid="stPopoverBody"] [data-testid="stChatMessage"] p,
[data-testid="stPopoverBody"] [data-testid="stChatMessage"] span,
[data-testid="stPopoverBody"] [data-testid="stMarkdownContainer"] p,
[data-testid="stPopoverBody"] [data-testid="stMarkdownContainer"] li {
    color:#f8fafc !important;
    -webkit-text-fill-color:#f8fafc !important;
}
[data-testid="stPopoverBody"] [data-testid="stFormSubmitButton"] button {
    background:linear-gradient(90deg,#2563eb,#7c3aed) !important;
    color:white !important;
    -webkit-text-fill-color:white !important;
    min-height:38px !important;
    border:0 !important;
    border-radius:9px !important;
}
[data-testid="stPopoverBody"] [data-testid="stFormSubmitButton"] button * {
    color:white !important;
    -webkit-text-fill-color:white !important;
}

@media(max-width:750px) {.hero {padding:18px}.hero h1 {font-size:1.55rem !important}.st-key-floating_chat {right:12px !important;bottom:12px !important}}

/* Animated premium landing page; all motion respects reduced-motion settings. */
.rm-landing {position:relative;isolation:isolate;overflow:hidden;border:1px solid #344c78;border-radius:28px;padding:54px 48px 40px;background:radial-gradient(circle at 82% 22%,#293c87 0%,transparent 36%),linear-gradient(115deg,#111e38 10%,#101832 60%,#171439 100%);box-shadow:0 25px 70px #02061766;}
.rm-landing-grid {position:relative;z-index:2;display:grid;grid-template-columns:1.15fr .85fr;gap:25px;align-items:center;min-height:355px}
.rm-landing-copy {animation:rm-rise .85s ease-out both}
.rm-kicker {display:inline-flex;align-items:center;gap:10px;padding:9px 13px;border:1px solid #526ab1;border-radius:999px;background:#17294e9c;color:#c6d7ff;font-size:11px;font-weight:750;letter-spacing:1.5px}
.rm-live-dot {height:8px;width:8px;border-radius:50%;background:#6ee7b7;box-shadow:0 0 14px #34d399;animation:rm-pulse 2.1s ease-in-out infinite}
.rm-landing h1 {font-size:clamp(2.25rem,4.3vw,4.25rem)!important;line-height:1.12!important;letter-spacing:-.065em!important;font-weight:850!important;margin:24px 0 19px!important;color:#f8fafc!important}
.rm-gradient-text {background:linear-gradient(95deg,#93c5fd 5%,#c4b5fd 55%,#67e8f9 100%);background-size:200% 100%;-webkit-background-clip:text;background-clip:text;-webkit-text-fill-color:transparent;animation:rm-shimmer 8s linear infinite}
.rm-subtitle {color:#c3d2eb!important;font-size:1.05rem;line-height:1.8;max-width:570px}
.rm-chiprow {display:flex;flex-wrap:wrap;gap:9px;margin-top:24px}
.rm-chiprow span {color:#e2e8f0;background:#1e3152a8;border:1px solid #41587e;padding:7px 11px;border-radius:99px;font-size:12px}
.rm-orb {position:absolute;border-radius:50%;filter:blur(10px);pointer-events:none;z-index:0}
.rm-orb-a {width:270px;height:270px;background:#4f46e52b;right:-70px;top:-90px;animation:rm-orbit 9s ease-in-out infinite alternate}
.rm-orb-b {width:230px;height:230px;background:#0ea5e924;bottom:-135px;left:25%;animation:rm-orbit 12s ease-in-out infinite alternate-reverse}
.rm-visual-wrap {position:relative;min-height:340px;display:flex;align-items:center;justify-content:center;animation:rm-rise 1s .2s both}
.rm-glow-ring {position:absolute;width:295px;height:295px;border-radius:50%;border:1px solid #a5b4fc55;box-shadow:0 0 90px #6366f133,inset 0 0 45px #3b82f62a;animation:rm-rotate 25s linear infinite}
.rm-demo-card {position:relative;z-index:2;width:min(100%,290px);border:1px solid #6881b7aa;background:linear-gradient(150deg,#23385de8,#172442ef);border-radius:22px;padding:21px 22px;box-shadow:0 28px 55px #03071299;animation:rm-float 5.5s ease-in-out infinite}
.rm-card-top {display:flex;justify-content:space-between;color:#c6d7f7;font-size:10px;font-weight:800;letter-spacing:1.2px}
.rm-dot {display:inline-block;background:#34d399;width:7px;height:7px;border-radius:50%;margin-right:5px}
.rm-spark {font-size:23px;color:#c4b5fd}
.rm-score-circle {height:157px;width:157px;margin:14px auto;display:flex;align-items:center;justify-content:center;border-radius:50%;background:conic-gradient(#818cf8 0 56%,#38bdf8 56% 78%,#354767 78% 100%);box-shadow:0 0 30px #818cf82b}
.rm-score-inner {width:122px;height:122px;border-radius:50%;background:#1b2c4b;display:flex;align-items:center;justify-content:center;flex-direction:column}
.rm-score-inner strong {font-size:38px;color:#fff;line-height:1.1}
.rm-score-inner small {font-size:10px;color:#cbd5e1}
.rm-demo-label {display:flex;justify-content:space-between;gap:8px;color:#cbd5e1;font-size:10px;margin:8px 0}
.rm-demo-track {height:7px;background:#394966;border-radius:20px;overflow:hidden}
.rm-demo-track span {display:block;width:78%;height:100%;border-radius:20px;background:linear-gradient(90deg,#6366f1,#38bdf8);animation:rm-grow 1.8s ease-out both}
.rm-mini-stats {display:flex;justify-content:space-between;color:#a8c1eb;font-size:10px;margin-top:17px}
.rm-float-tag {position:absolute;z-index:3;color:#e0e7ff;background:#283c68ee;border:1px solid #657db2;border-radius:11px;padding:11px 13px;font-size:11px;font-weight:700;box-shadow:0 12px 24px #02061780;animation:rm-float 4.5s ease-in-out infinite}
.rm-tag-one {top:18%;right:-1%}.rm-tag-two {bottom:13%;left:-1%;animation-delay:-2.1s}
.rm-section-title {font-size:12px;letter-spacing:2px;font-weight:800;color:#93c5fd;margin:35px 0 16px}
.rm-features {display:grid;grid-template-columns:repeat(4,1fr);gap:15px}
.rm-feature {border:1px solid #304665;background:linear-gradient(155deg,#1b2b46,#131f34);border-radius:17px;padding:20px;transition:transform .25s ease,border-color .25s ease,box-shadow .25s ease;animation:rm-rise .7s both}
.rm-feature:nth-child(2){animation-delay:.1s}.rm-feature:nth-child(3){animation-delay:.2s}.rm-feature:nth-child(4){animation-delay:.3s}
.rm-feature:hover {transform:translateY(-6px);border-color:#818cf8;box-shadow:0 14px 32px #0a0d2688}
.rm-feature-icon {font-size:26px;display:block;margin-bottom:12px}
.rm-feature h3 {color:#f8fafc!important;font-size:16px!important;margin:0 0 9px!important}
.rm-feature p {font-size:13px!important;line-height:1.65;color:#b9cbe4!important;margin:0}
.rm-steps {display:flex;align-items:center;justify-content:center;flex-wrap:wrap;gap:20px;margin:27px 0;padding:18px;background:#17263e;border:1px solid #2c4263;border-radius:14px;color:#c4d7ff;font-size:12px;font-weight:800;letter-spacing:1.1px}
.rm-steps b {color:#818cf8;font-size:18px}
.rm-honesty {color:#9db0d0!important;font-size:12px!important;text-align:center}
@keyframes rm-rise {from {opacity:0;transform:translateY(20px)}to{opacity:1;transform:translateY(0)}}
@keyframes rm-float {0%,100%{transform:translateY(0)}50%{transform:translateY(-11px)}}
@keyframes rm-pulse {0%,100%{opacity:1;box-shadow:0 0 10px #34d399}50%{opacity:.55;box-shadow:0 0 20px #34d399}}
@keyframes rm-shimmer {0%{background-position:0% 50%}100%{background-position:200% 50%}}
@keyframes rm-orbit {from{transform:translate(0,0)}to{transform:translate(-25px,35px)}}
@keyframes rm-rotate {to{transform:rotate(360deg)}}
@keyframes rm-grow {from{width:0}to{width:78%}}
@media(max-width:950px){.rm-landing{padding:30px 22px}.rm-landing-grid{grid-template-columns:1fr}.rm-visual-wrap{min-height:320px}.rm-features{grid-template-columns:repeat(2,1fr)}}
@media(max-width:520px){.rm-features{grid-template-columns:1fr}.rm-landing h1{font-size:2.3rem!important}.rm-tag-one{right:0}.rm-tag-two{left:0}.rm-steps{gap:9px;font-size:10px}}
@media(prefers-reduced-motion:reduce){.rm-landing *, .rm-feature{animation:none!important;transition:none!important}}

</style>
""", unsafe_allow_html=True)

for key, default in {"result": None, "ats": None, "messages": [], "analyzed_at": "", "resume_text": "", "job_description": "", "interview_answers": {}, "roadmap_done": {}}.items():
    if key not in st.session_state:
        st.session_state[key] = default


def pct(value):
    try:
        n = float(value)
        if 0 <= n <= 1:
            n *= 100
        return round(max(0, min(100, n)), 1)
    except (TypeError, ValueError):
        return 0.0


def panel(title, description="", content=""):
    st.markdown(
        '<div class="panel"><h3>' + html.escape(title) + '</h3>'
        + (f'<p class="muted">{html.escape(description)}</p>' if description else "")
        + content + '</div>',
        unsafe_allow_html=True
    )


def tags(items, kind):
    if not items:
        return '<span class="muted">No recognized skills in this category</span>'
    return "".join(f'<span class="tag tag-{kind}">{html.escape(str(item).title())}</span>' for item in items)


def donut(value, title, color):
    fig = go.Figure(go.Pie(
        values=[value, 100-value], hole=.78,
        marker={"colors": [color, "#334155"], "line": {"width": 0}},
        sort=False, direction="clockwise", textinfo="none", hoverinfo="skip",
        showlegend=False
    ))
    fig.add_annotation(x=.5, y=.56, text=f"<b>{value:g}%</b>", showarrow=False,
                       font={"size": 32, "color": "#fff"})
    fig.add_annotation(x=.5, y=.36, text=title, showarrow=False,
                       font={"size": 13, "color": "#b7c8e7"})
    fig.update_layout(height=230, margin={"l": 25, "r": 25, "t": 12, "b": 12},
                      paper_bgcolor="#1a2c48", plot_bgcolor="#1a2c48")
    return fig



def radar_chart(match, ats_score, coverage, similarity):
    names = ["Job Match", "ATS Readiness", "Skill Coverage", "Text Similarity"]
    values = [match, ats_score, coverage, similarity]
    fig = go.Figure(go.Scatterpolar(
        r=values + [values[0]], theta=names + [names[0]],
        fill="toself", fillcolor="rgba(129,140,248,0.25)",
        line=dict(color="#818cf8", width=3),
        marker=dict(size=7, color="#c4b5fd"),
        hovertemplate="%{theta}: %{r:.1f}%<extra></extra>"
    ))
    fig.update_layout(
        polar=dict(
            bgcolor="#1a2c48",
            radialaxis=dict(range=[0, 100], tickvals=[25, 50, 75, 100],
                            gridcolor="#3b506e", tickfont=dict(color="#b4c5e2", size=10)),
            angularaxis=dict(gridcolor="#3b506e", tickfont=dict(color="#f8fafc", size=11))
        ),
        height=325, margin=dict(l=75, r=75, t=28, b=28),
        paper_bgcolor="#1a2c48", font=dict(color="#fff"), showlegend=False
    )
    return fig


def skill_distribution_chart(matched_count, missing_count):
    total = matched_count + missing_count
    if not total:
        return None
    fig = go.Figure(go.Pie(
        labels=["Matched", "To Develop"],
        values=[matched_count, missing_count],
        hole=.73, sort=False,
        marker=dict(colors=["#22c55e", "#f59e0b"], line=dict(width=0)),
        textinfo="none", hovertemplate="%{label}: %{value} skills<extra></extra>"
    ))
    fig.add_annotation(x=.5, y=.55, text=f"<b>{matched_count}/{total}</b>",
                       font=dict(color="white", size=27), showarrow=False)
    fig.add_annotation(x=.5, y=.38, text="skills matched",
                       font=dict(color="#b4c5e2", size=12), showarrow=False)
    fig.update_layout(
        height=325, margin=dict(l=20, r=20, t=15, b=48),
        paper_bgcolor="#1a2c48", font=dict(color="#fff"),
        legend=dict(orientation="h", x=.5, xanchor="center", y=-.12)
    )
    return fig


def readiness_chart(match, ats_score, coverage, similarity):
    names = ["Job Match", "ATS Readiness", "Skill Coverage", "Text Similarity"]
    values = [match, ats_score, coverage, similarity]
    fig = go.Figure(go.Bar(
        x=values, y=names, orientation="h",
        marker=dict(color=["#60a5fa", "#4ade80", "#a78bfa", "#fbbf24"]),
        text=[f"{v:.1f}%" for v in values], textposition="inside",
        insidetextanchor="end", textfont=dict(color="#081225", size=13),
        hovertemplate="%{y}: %{x:.1f}%<extra></extra>"
    ))
    fig.update_layout(
        height=270, margin=dict(l=20, r=25, t=15, b=20),
        paper_bgcolor="#1a2c48", plot_bgcolor="#1a2c48",
        font=dict(color="#e2e8f0"), bargap=.42, showlegend=False,
        xaxis=dict(range=[0, 105], ticksuffix="%", gridcolor="#334155", zeroline=False),
        yaxis=dict(autorange="reversed", showgrid=False)
    )
    return fig


def navigate_to(destination):
    """Run before sidebar radio is instantiated on the next rerun."""
    st.session_state["page"] = destination


with st.sidebar:
    st.markdown("## 🧠 ResumeMatch AI")
    st.caption("Career intelligence • Version 2.0")
    st.divider()
    st.markdown("### Workspace")
    page = st.radio(
        "Navigate",
        ["✨ Welcome", "📄 Resume Analyzer", "🏠 Overview", "📊 Career Dashboard", "🚀 Improvement Plan", "🎤 Mock Interview", "🧭 Career Roadmap", "💼 Job Fit Finder", "🔄 Resume Comparison"],
        label_visibility="collapsed",
        key="page"
    )
    st.divider()
    st.info("Your resume stays in this app session. Analyze it to unlock insights.")
    st.caption("Built with Streamlit • NLP • Machine Learning")

if page == "✨ Welcome":
    st.markdown("""
    <section class="rm-landing" aria-label="ResumeMatch introduction">
      <div class="rm-orb rm-orb-a"></div><div class="rm-orb rm-orb-b"></div>
      <div class="rm-landing-grid">
        <div class="rm-landing-copy">
          <div class="rm-kicker"><span class="rm-live-dot"></span> CAREER INTELLIGENCE PLATFORM · HACKATHON EDITION</div>
          <h1>Turn your resume into<br><span class="rm-gradient-text">your next opportunity.</span></h1>
          <p class="rm-subtitle">Discover how your skills align with a role, find the gaps, practice interviews, and track real improvements — all in one workspace.</p>
          <div class="rm-chiprow"><span>✦ Resume intelligence</span><span>✦ Skill-gap insights</span><span>✦ Career guidance</span></div>
        </div>
        <div class="rm-visual-wrap">
          <div class="rm-glow-ring"></div>
          <div class="rm-demo-card">
            <div class="rm-card-top"><span><i class="rm-dot"></i> LIVE ANALYSIS PREVIEW</span><span class="rm-spark">✧</span></div>
            <div class="rm-score-circle"><div class="rm-score-inner"><strong>78%</strong><small>Example match</small></div></div>
            <div class="rm-demo-label"><span>Python · SQL · ML</span><span>Matched skills</span></div>
            <div class="rm-demo-track"><span></span></div>
            <div class="rm-mini-stats"><span>◎ ATS insights</span><span>↗ Learning roadmap</span></div>
          </div>
          <div class="rm-float-tag rm-tag-one">✦ Skills identified</div>
          <div class="rm-float-tag rm-tag-two">↗ Career growth</div>
        </div>
      </div>
    </section>
    """, unsafe_allow_html=True)
    btn1, btn2, _ = st.columns([1.3, 1.3, 2.2], gap="medium")
    with btn1:
        st.button("🚀 Start Resume Analysis", type="primary", use_container_width=True,
                  key="welcome_start", on_click=navigate_to, args=("📄 Resume Analyzer",))
    with btn2:
        st.button("📊 Explore Dashboard", use_container_width=True,
                  key="welcome_dashboard", on_click=navigate_to, args=("📊 Career Dashboard",))
    st.markdown("<div class='rm-section-title'>BUILT FOR YOUR NEXT STEP</div>", unsafe_allow_html=True)
    st.markdown("""
    <div class="rm-features">
      <div class="rm-feature"><span class="rm-feature-icon">🎯</span><h3>Resume Analysis</h3><p>Compare your resume against the skills in a target job description.</p></div>
      <div class="rm-feature"><span class="rm-feature-icon">📈</span><h3>Growth Dashboard</h3><p>Visualize strengths, skill gaps, and before-and-after improvements.</p></div>
      <div class="rm-feature"><span class="rm-feature-icon">🎤</span><h3>Interview Practice</h3><p>Practice role-relevant questions with transparent offline feedback.</p></div>
      <div class="rm-feature"><span class="rm-feature-icon">🧭</span><h3>Career Roadmap</h3><p>Build a learning plan and explore matching career paths.</p></div>
    </div>
    <div class="rm-steps"><span>01 · UPLOAD</span><b>→</b><span>02 · ANALYZE</span><b>→</b><span>03 · IMPROVE</span><b>→</b><span>04 · PREPARE</span></div>
    <p class="rm-honesty">Illustrative preview only. Actual results are generated from your resume and job description. Scores are heuristic estimates, not hiring predictions.</p>
    """, unsafe_allow_html=True)
if page in ("🏠 Overview", "📄 Resume Analyzer"):
    st.markdown("## 📄 Resume Analyzer")
    st.caption("Upload your resume and paste a job description to see your results immediately below.")
    left, right = st.columns(2, gap="large")
    with left:
        uploaded = st.file_uploader("Upload your resume", type=["pdf", "docx", "txt"])
    with right:
        job = st.text_area("Job description", height=145,
                           placeholder="Paste the job requirements, responsibilities and skills here...")
    if st.button("✨ Analyze Resume", type="primary", use_container_width=True):
        if uploaded is None:
            st.warning("Upload a resume to continue.")
        elif not job.strip():
            st.warning("Paste a job description to continue.")
        else:
            try:
                with st.spinner("Analyzing resume and job description..."):
                    resume_text = extract_text(uploaded)
                    if not resume_text or not resume_text.strip():
                        raise ValueError("No readable resume text was found. Use a text-based PDF, DOCX or TXT.")
                    result = analyze_resume(resume_text, job)
                    ats = check_ats(resume_text)
                    st.session_state.resume_text = resume_text
                    st.session_state.job_description = job
                    st.session_state.interview_answers = {}
                    st.session_state.roadmap_done = {}
                    st.session_state.result = result
                    st.session_state.ats = ats
                    st.session_state.messages = []
                    st.session_state.analyzed_at = datetime.now().strftime("%d %b %Y • %I:%M %p")
                st.success("Analysis completed! Your results are displayed directly below.")
            except Exception as exc:
                st.error(f"Analysis failed: {exc}")

# Keep the Resume Analyzer at the top, followed by Career Overview.
if page == "🏠 Overview":
    st.markdown("""
    <div class="hero">
    <div class="eyebrow">YOUR AI-ASSISTED CAREER WORKSPACE</div>
    <h1>Career Overview</h1>
    <p>Understand your resume performance, identify skill gaps and prepare for your next opportunity.</p>
    </div>
    """, unsafe_allow_html=True)

result = st.session_state.result
ats = st.session_state.ats

if (result is None or ats is None) and page != "✨ Welcome":
    panel("Your dashboard is ready", "Upload a resume and paste a job description to unlock match scores, skills and personalized recommendations.")
elif result is not None and ats is not None:
    match = pct(result.get("match_score", 0))
    ats_score = pct(ats.get("ats_score", 0))
    similarity = pct(result.get("similarity", 0))
    matched = result.get("matched_skills", []) or []
    missing = result.get("missing_skills", []) or []
    checks = ats.get("checks", {}) or {}
    tips = ats.get("tips", []) or []
    total = len(matched) + len(missing)
    coverage = round(100 * len(matched) / total, 1) if total else 0

    if page in ("🏠 Overview", "📄 Resume Analyzer", "📊 Career Dashboard"):
        st.markdown('<div class="eyebrow">PERFORMANCE AT A GLANCE</div>', unsafe_allow_html=True)
        st.markdown("### 📊 Your Career Intelligence Dashboard")
        a, b, c = st.columns(3, gap="medium")
        a.metric("🎯 Job Match", f"{match:g}%")
        b.metric("🛡️ ATS Readiness", f"{ats_score:g}%")
        c.metric("🧠 Skill Coverage", f"{coverage:g}%")
        st.caption("These are algorithmic estimates, not official ATS results or hiring predictions.")
        st.markdown("### 📈 AI Analytics")
        graph_left, graph_right = st.columns(2, gap="large")
        with graph_left:
            st.markdown("#### 🎯 Resume Performance")
            st.plotly_chart(radar_chart(match, ats_score, coverage, similarity),
                            use_container_width=True, config={"displayModeBar": False})
        with graph_right:
            st.markdown("#### 🧠 Skill Match Distribution")
            skill_fig = skill_distribution_chart(len(matched), len(missing))
            if skill_fig is not None:
                st.plotly_chart(skill_fig, use_container_width=True,
                                config={"displayModeBar": False})
            else:
                panel("No skills detected", "Add more detailed technical requirements to the job description.")

        st.markdown("#### 📊 Career Readiness Breakdown")
        st.plotly_chart(readiness_chart(match, ats_score, coverage, similarity),
                        use_container_width=True, config={"displayModeBar": False})

        left, right = st.columns(2, gap="large")
        with left:
            priorities = "".join(
                f'<div class="priority"><span class="number">{i}</span><span class="name">{html.escape(str(skill).title())}</span></div>'
                for i, skill in enumerate(missing[:5], 1)
            )
            if not priorities:
                priorities = '<p class="muted">No missing dictionary skills detected.</p>'
            panel("Skills to Develop", "Prioritized missing skills from the job description.", priorities)
        with right:
            panel("Your Career Improvement Plan",
                  "Practical next steps based on the job requirements.",
                  "".join(f'<span class="tag tag-warn">{html.escape(str(skill).title())}</span>'
                          for skill in missing[:5])
                  if missing else '<span class="muted">No skill gaps detected by the current dictionary.</span>')

    if page in ("🏠 Overview", "📄 Resume Analyzer", "📊 Career Dashboard", "🚀 Improvement Plan"):
        st.markdown('<div class="eyebrow">SKILLS & DEVELOPMENT</div>', unsafe_allow_html=True)
        left, right = st.columns(2, gap="large")
        with left:
            panel("✅ Matched Skills", "Skills recognized in both the resume and job description.", tags(matched, "ok"))
        with right:
            panel("⚠️ Missing Skills", "Requirements to learn or demonstrate with real projects.", tags(missing, "warn"))

        with st.expander("🛡️ ATS checklist and improvement suggestions", expanded=(page == "🚀 Improvement Plan")):
            for label, passed in checks.items():
                st.write(f"{'✅' if passed else '⚠️'} {label}: {'Pass' if passed else 'Review'}")
            st.markdown("**Suggested improvements**")
            for tip in tips:
                st.write(f"• {tip}")
            if not tips:
                st.write("No major issues detected by the current checklist.")

        st.markdown("### 🚀 Your Personalized Learning Roadmap")
        if missing:
            for i, skill in enumerate(missing[:5], 1):
                with st.expander(f"Step {i} — {str(skill).title()}"):
                    st.write(f"Learn the fundamentals of {skill}, build a small practical project, and document your real experience.")
        else:
            st.success("No missing skills detected in the current skill dictionary.")

        with st.expander("🎤 Interview preparation"):
            for i, skill in enumerate(matched[:3], 1):
                st.write(f"**Q{i}.** Describe a project where you used {skill}.")
            st.write("**General:** Tell me about a challenging technical problem you solved.")

        report = [
            "RESUMEMATCH AI 2.0 — CAREER ANALYSIS",
            f"Analyzed: {st.session_state.analyzed_at}",
            f"Job Match: {match:g}%",
            f"ATS Readiness: {ats_score:g}%",
            f"Text Similarity: {similarity:g}%",
            f"Skill Coverage: {coverage:g}%",
            "Matched Skills: " + (", ".join(map(str, matched)) or "None"),
            "Missing Skills: " + (", ".join(map(str, missing)) or "None"),
            "",
            "ATS CHECKS",
            *[f"{k}: {'Pass' if v else 'Review'}" for k, v in checks.items()],
            "",
            "SUGGESTIONS",
            *[f"- {t}" for t in tips],
            "",
            "Scores are estimates and not hiring predictions."
        ]
        st.download_button("⬇️ Download Full Analysis Report", data="\n".join(report),
                           file_name="ResumeMatch_AI_Report.txt", mime="text/plain",
                           use_container_width=True)

# NEW MODULES: accessible as separate sidebar pages after analyzing a resume.
if page == "🎤 Mock Interview":
    st.markdown("## 🎤 AI Mock Interview Coach")
    st.caption("Text-based interview practice with transparent rule-based feedback. No microphone or API key required.")
    if not st.session_state.result:
        st.info("Analyze a resume and job description first.")
    else:
        data = st.session_state.result
        questions = make_questions(
            data.get("matched_skills", []) or [],
            data.get("missing_skills", []) or [],
            role="the target job"
        )
        st.progress(sum(bool(st.session_state.interview_answers.get(i, {}).get("answer")) for i in range(len(questions))) / len(questions))
        for i, item in enumerate(questions):
            with st.container(border=True):
                st.markdown(f"**Question {i + 1}:** {item['question']}")
                with st.form(f"interview_form_{i}"):
                    answer = st.text_area("Your answer", value=st.session_state.interview_answers.get(i, {}).get("answer", ""), key=f"interview_text_{i}", height=110)
                    submitted = st.form_submit_button("Evaluate my answer", type="primary")
                if submitted:
                    if not answer.strip():
                        st.warning("Write an answer before evaluating.")
                    else:
                        st.session_state.interview_answers[i] = {"answer": answer, "feedback": evaluate_answer(answer, item["keywords"])}
                saved = st.session_state.interview_answers.get(i)
                if saved:
                    feedback = saved["feedback"]
                    st.metric("Practice feedback score", f"{feedback['score']}/100")
                    for tip in feedback["tips"]:
                        st.write("•", tip)
                    st.caption(feedback["note"])
        completed = [x["feedback"]["score"] for x in st.session_state.interview_answers.values()]
        if completed:
            st.success(f"Questions completed: {len(completed)}/{len(questions)} · Average practice score: {sum(completed)/len(completed):.1f}/100")

elif page == "🧭 Career Roadmap":
    st.markdown("## 🧭 Personalized Career Roadmap")
    st.caption("Actionable study milestones based on detected missing skills.")
    if not st.session_state.result:
        st.info("Analyze a resume and job description first.")
    else:
        missing_skills = st.session_state.result.get("missing_skills", []) or []
        roadmap = create_roadmap(missing_skills)
        if not roadmap:
            st.success("No missing dictionary skills were detected. Try another job description to explore different goals.")
        else:
            completed = 0
            for i, step in enumerate(roadmap):
                with st.container(border=True):
                    checked = st.checkbox(
                        f"Week {step['week']} · {step['skill']}",
                        value=st.session_state.roadmap_done.get(step["skill"], False),
                        key=f"roadmap_{i}"
                    )
                    st.session_state.roadmap_done[step["skill"]] = checked
                    completed += int(checked)
                    st.write("**Learn:**", step["goal"])
                    st.write("**Build:**", step["project"])
                    st.write("**Show evidence:**", step["proof"])
                    st.caption(f"Suggested target: {step['target_date']}")
            st.progress(completed / len(roadmap), text=f"{completed}/{len(roadmap)} milestones completed")
            roadmap_report = "\\n".join(
                f"Week {x['week']}: {x['skill']}\\nGoal: {x['goal']}\\nProject: {x['project']}\\n"
                for x in roadmap
            )
            st.download_button("⬇️ Download Learning Roadmap", roadmap_report, "Career_Roadmap.txt", "text/plain")

elif page == "💼 Job Fit Finder":
    st.markdown("## 💼 Job Fit Finder")
    st.caption("Ranks eight example career roles by detected skill coverage. Not live vacancies or hiring probabilities.")
    if not st.session_state.resume_text:
        st.info("Analyze a resume first to discover matching career roles.")
    else:
        roles = rank_job_roles(st.session_state.resume_text)
        for rank, item in enumerate(roles, 1):
            with st.container(border=True):
                a, b = st.columns([3, 1])
                a.markdown(f"### {rank}. {item['role']}")
                b.metric("Skill coverage", f"{item['score']:.1f}%")
                st.progress(item["score"] / 100)
                st.write("**Detected:**", ", ".join(item["matched"]) or "None")
                st.write("**Skills to explore:**", ", ".join(item["missing"]) or "None")
        st.caption("Role recommendations use a curated dictionary; they are illustrative, not personalized job listings.")

if page == "🔄 Resume Comparison":
    st.markdown("## 🔄 Before vs. After Resume Comparison")
    st.caption("Compare two real resume versions against exactly the same job description. Scores are algorithmic estimates, not hiring predictions.")
    original, revised = st.columns(2, gap="large")
    with original:
        before_file = st.file_uploader("Original resume", type=["pdf", "docx", "txt"], key="comparison_before")
    with revised:
        after_file = st.file_uploader("Improved resume", type=["pdf", "docx", "txt"], key="comparison_after")
    jd_default = st.session_state.job_description or ""
    comparison_jd = st.text_area("Job description (same for both)", value=jd_default, height=160, key="comparison_jd")
    if st.button("🔍 Compare Resumes", type="primary", use_container_width=True):
        if not before_file or not after_file or not comparison_jd.strip():
            st.warning("Upload both resume versions and provide a job description.")
        else:
            try:
                with st.spinner("Comparing both versions against the same job..."):
                    before_text = extract_text(before_file)
                    after_text = extract_text(after_file)
                    if not before_text or not before_text.strip() or not after_text or not after_text.strip():
                        raise ValueError("A resume contained no readable text. Try a text-based PDF, DOCX or TXT file.")
                    st.session_state.comparison_results = compare_resumes(before_text, after_text, comparison_jd, analyze_resume, check_ats)
            except Exception as exc:
                st.error(f"Could not compare resumes: {exc}")
    comparison = st.session_state.get("comparison_results")
    if comparison:
        before, after = comparison["before"], comparison["after"]
        st.markdown("### 📊 Improvement Dashboard")
        c1, c2, c3 = st.columns(3)
        c1.metric("Job Match", f"{after['match_score']:.1f}%", f"{comparison['match_delta']:+.1f} points")
        c2.metric("ATS Checklist", f"{after['ats_score']:.1f}%", f"{comparison['ats_delta']:+.1f} points")
        c3.metric("Skill Coverage", f"{after['skill_score']:.1f}%", f"{comparison['skill_delta']:+.1f} points")
        names = ["Job Match", "ATS Checklist", "Skill Coverage", "Text Similarity"]
        fig = go.Figure()
        fig.add_trace(go.Bar(name="Before", x=names, y=[before['match_score'], before['ats_score'], before['skill_score'], before['similarity']], marker_color="#64748b"))
        fig.add_trace(go.Bar(name="After", x=names, y=[after['match_score'], after['ats_score'], after['skill_score'], after['similarity']], marker_color="#818cf8"))
        fig.update_layout(barmode="group", height=360, paper_bgcolor="#1a2c48", plot_bgcolor="#1a2c48", font=dict(color="#f8fafc"), yaxis=dict(range=[0, 105], ticksuffix="%", gridcolor="#334155"), legend=dict(orientation="h"), margin=dict(l=15, r=15, t=25, b=30))
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
        left, right = st.columns(2)
        with left:
            st.markdown("#### Original Resume")
            st.write("**Matched skills:**", ", ".join(before['matched_skills']) or "None detected")
            st.write("**Missing skills:**", ", ".join(before['missing_skills']) or "None detected")
        with right:
            st.markdown("#### Improved Resume")
            st.write("**Matched skills:**", ", ".join(after['matched_skills']) or "None detected")
            st.write("**Missing skills:**", ", ".join(after['missing_skills']) or "None detected")
        st.success("Newly detected job skills: " + (", ".join(comparison["new_skills"]) or "None"))
        if comparison["removed_skills"]:
            st.warning("Previously detected skills no longer present: " + ", ".join(comparison["removed_skills"]))
        st.info("A higher keyword match does not prove a better candidate. Only include skills and accomplishments you genuinely have.")
        lines = ["RESUMEMATCH AI — BEFORE / AFTER COMPARISON", "", "Metric | Before | After | Change"]
        for title, key in [("Job Match", "match_score"), ("ATS Checklist", "ats_score"), ("Skill Coverage", "skill_score"), ("Text Similarity", "similarity")]:
            lines.append(f"{title} | {before[key]:.1f}% | {after[key]:.1f}% | {after[key]-before[key]:+.1f} points")
        lines.append("Newly detected skills: " + (", ".join(comparison["new_skills"]) or "None"))
        st.download_button("⬇️ Download Comparison Report", data="\n".join(lines), file_name="Resume_Comparison.txt", mime="text/plain")

st.caption("ResumeMatch AI 2.0 • Hackathon prototype • Contextual career guidance")

# Native Streamlit popover — fixed circular launcher at bottom-right.
with st.container(key="floating_chat"):
    with st.popover("🤖", help="Open LLM Career Coach"):
        st.markdown("### 🧠 AI Career Assistant")
        st.caption("Gemini AI via cloud API • Rule-based fallback if unavailable")
        if st.session_state.result is None:
            st.info("Analyze a resume first to get personalized guidance. You can still ask general career questions.")
        with st.container(height=275):
            if not st.session_state.messages:
                st.info("Ask about your match score, missing skills, ATS readiness, or interview preparation.")
            for message in st.session_state.messages:
                with st.chat_message(message["role"]):
                    st.markdown(message["content"])
        with st.form("chat_form", clear_on_submit=True):
            question = st.text_input("Message", placeholder="Ask your AI career coach...", label_visibility="collapsed")
            send = st.form_submit_button("Send ➤", use_container_width=True)
        if st.session_state.get("llm_last_error"):
            st.error(st.session_state["llm_last_error"])
if send and question.strip():
    with st.spinner("AI is thinking..."):
        try:
            answer = ask_llm(
                question=question,
                resume_text=st.session_state.resume_text,
                job_description=st.session_state.job_description,
                analysis=st.session_state.result,
                ats=st.session_state.ats,
                history=st.session_state.messages,
            )

            st.session_state.chat_engine = "LLM"
            st.session_state.llm_last_error = None

        except Exception as error:
            import logging
            logging.exception("GEMINI CHATBOT FAILED")

            st.session_state.llm_last_error = (
                f"Gemini chatbot error: {type(error).__name__}. "
                "Check the Streamlit Cloud logs for details."
            )

            if st.session_state.result is not None:
                answer = coach_reply(
                    question,
                    st.session_state.result,
                    st.session_state.ats,
                    st.session_state.job_description,
                )
                answer = (
                    "⚠️ Online AI unavailable; showing rule-based guidance.\n\n"
                    + answer
                )
            else:
                answer = "Online AI is unavailable. Check the Gemini API configuration and try again."

            st.session_state.chat_engine = "Fallback"

    st.session_state.messages.append(
        {"role": "user", "content": question}
    )
    st.session_state.messages.append(
        {"role": "assistant", "content": answer}
    )
    st.rerun()