"""
Flagship design system for the Business Analytics Dashboard.

Every visual primitive here relies on Streamlit's native CSS custom
properties (--primary-color, --background-color,
--secondary-background-color, --text-color) for base surfaces and text,
so the UI still adapts automatically to light/dark mode. Brand identity
(navy + gold, serif display type) is layered on top as fixed tokens so
the dashboard reads as a deliberate, formal product rather than a
default Streamlit theme.
"""

import streamlit as st

# ── Brand tokens ──────────────────────────────────────────────────────
NAVY = "#1B2E4B"
NAVY_SOFT = "#3D5A80"
GOLD = "#AD8A4E"
RISK = "#8C3B3B"
SUCCESS = "#3F6B4F"

CHART_COLORWAY = [
    NAVY, "#3D5A80", "#5B7A9E", "#8FA6BE",
    GOLD, "#7A6A53", "#4A6178", "#9CA3AF",
]
CHART_FONT_COLOR = "#8a919b"
CHART_GRID_COLOR = "rgba(128,128,128,0.14)"

DISPLAY_FONT = "'Source Serif 4', Georgia, serif"
BODY_FONT = "'Inter', sans-serif"


def load_css():
    st.markdown(
        f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Source+Serif+4:wght@600;700&family=Inter:wght@400;500;600;700;800&display=swap');
        @import url('https://cdn.jsdelivr.net/npm/@tabler/icons-webfont@latest/dist/tabler-icons.min.css');

        html, body, [class*="css"] {{ font-family: {BODY_FONT}; }}

        #MainMenu {{visibility: hidden;}}
        footer {{visibility: hidden;}}

        .block-container {{ padding-top: 4.5rem; padding-bottom: 3rem; max-width: 1200px; }}

        /* ---------- Eyebrow label ---------- */
        .db-eyebrow {{
            font-family: {BODY_FONT}; font-size: 0.82rem; font-weight: 600;
            letter-spacing: 0.08em; text-transform: uppercase;
            color: {GOLD}; opacity: 0.95; margin-bottom: 10px;
        }}

        /* ---------- Page Header (letterhead) ---------- */
        .db-header {{
            display: flex; align-items: center; gap: 16px;
            margin-bottom: 4px;
        }}
        .db-header .icon-badge {{
            width: 48px; height: 48px; border-radius: 8px;
            display: flex; align-items: center; justify-content: center;
            font-size: 22px; flex-shrink: 0; color: {GOLD};
            background: var(--secondary-background-color);
            border: 1px solid rgba(173, 138, 78, 0.45);
        }}
        .db-header h1 {{
            font-family: {DISPLAY_FONT}; font-size: 1.9rem; font-weight: 700;
            margin: 0; letter-spacing: -0.005em; color: var(--text-color);
        }}
        .db-header p {{
            margin: 4px 0 0 0; color: var(--text-color);
            opacity: 0.6; font-size: 0.95rem; font-family: {BODY_FONT};
        }}
        .db-header-rule {{ margin: 16px 0 26px 0; }}
        .db-header-rule .bar {{
            height: 3px; width: 42px; border-radius: 2px;
            background: {NAVY}; margin-bottom: 6px;
        }}
        .db-header-rule .hairline {{
            height: 1px; width: 100%;
            background: linear-gradient(90deg, {GOLD}, rgba(173,138,78,0));
            opacity: 0.55;
        }}

        /* ---------- Section Header ---------- */
        .db-section {{ display: flex; align-items: center; gap: 10px; margin: 6px 0 14px 0; }}
        .db-section .bar {{
            width: 3px; height: 18px; border-radius: 2px;
            background: {NAVY}; display: inline-block;
        }}
        .db-section h3 {{
            margin: 0; font-family: {DISPLAY_FONT}; font-size: 1.1rem;
            font-weight: 600; color: var(--text-color);
        }}
        .db-section h3 i {{ color: {NAVY_SOFT}; margin-right: 6px; font-size: 0.95rem; }}

        /* ---------- KPI Cards ---------- */
        .kpi-card {{
            background: var(--secondary-background-color);
            border: 1px solid rgba(128,128,128,0.16);
            border-top: 3px solid {NAVY};
            border-radius: 10px; padding: 20px 22px; height: 100%;
        }}
        .kpi-card .kpi-top {{ display: flex; align-items: center; justify-content: space-between; margin-bottom: 10px; }}
        .kpi-card .kpi-icon {{ font-size: 18px; opacity: 0.9; color: {GOLD}; }}
        .kpi-card .kpi-label {{
            font-size: 0.78rem; font-weight: 600; text-transform: uppercase;
            letter-spacing: 0.05em; color: var(--text-color); opacity: 0.6;
        }}
        .kpi-card .kpi-value {{
            font-family: {DISPLAY_FONT}; font-size: 1.6rem; font-weight: 700;
            color: var(--text-color); letter-spacing: -0.005em;
            line-height: 1.25; word-break: break-word;
        }}
        .kpi-card .kpi-delta {{ margin-top: 6px; font-size: 0.82rem; font-weight: 600; }}
        .kpi-delta.positive {{ color: {SUCCESS}; }}
        .kpi-delta.negative {{ color: {RISK}; }}
        .kpi-delta.neutral {{ color: var(--text-color); opacity: 0.5; }}

        /* ---------- Feature / nav cards (Home page) ---------- */
        .nav-card {{ margin-bottom: 16px; border-top: 3px solid {GOLD}; }}
        .nav-card .nav-icon {{ font-size: 1.3rem; margin-bottom: 8px; opacity: 0.95; color: {GOLD}; }}
        .nav-card .nav-title {{
            font-family: {DISPLAY_FONT}; font-weight: 600; font-size: 1.02rem;
            margin-bottom: 4px; color: var(--text-color);
        }}
        .nav-card .nav-desc {{ font-size: 0.85rem; color: var(--text-color); opacity: 0.6; }}

        /* ---------- Chart card wrapper ---------- */
        .chart-card {{
            background: var(--secondary-background-color);
            border: 1px solid rgba(128,128,128,0.16);
            border-radius: 10px; padding: 16px 18px 4px 18px; margin-bottom: 22px;
        }}

        /* ---------- Summary / insight card ---------- */
        .summary-card {{
            background: var(--secondary-background-color);
            border: 1px solid rgba(128,128,128,0.16);
            border-left: 3px solid {NAVY};
            border-radius: 8px; padding: 18px 22px;
            font-size: 0.95rem; line-height: 1.65;
            color: var(--text-color); white-space: pre-wrap;
        }}

        /* ---------- Signal cards (risk / priority / opportunity) ---------- */
        .signal-card {{
            background: var(--secondary-background-color);
            border: 1px solid rgba(128,128,128,0.16);
            border-radius: 8px; padding: 12px 16px; margin-bottom: 10px;
        }}
        .signal-card .signal-label {{
            display: block; font-size: 0.74rem; font-weight: 600;
            letter-spacing: 0.06em; text-transform: uppercase; margin-bottom: 5px;
        }}
        .signal-card .signal-label i {{ margin-right: 4px; font-size: 0.8rem; }}
        .signal-card .signal-body {{ font-size: 0.92rem; line-height: 1.55; color: var(--text-color); }}
        .signal-risk {{ border-left: 3px solid {RISK}; }}
        .signal-risk .signal-label {{ color: {RISK}; }}
        .signal-priority {{ border-left: 3px solid {NAVY_SOFT}; }}
        .signal-priority .signal-label {{ color: {NAVY_SOFT}; }}
        .signal-opportunity {{ border-left: 3px solid {GOLD}; }}
        .signal-opportunity .signal-label {{ color: {GOLD}; }}
        .signal-note {{
            font-size: 0.88rem; font-style: italic; opacity: 0.55;
            color: var(--text-color); padding: 10px 4px;
        }}

        /* ---------- Empty state ---------- */
        .empty-state {{
            text-align: center; padding: 40px 20px;
            border: 1px dashed rgba(173, 138, 78, 0.4);
            border-radius: 10px; color: var(--text-color);
        }}
        .empty-state .icon {{ font-size: 2rem; margin-bottom: 10px; opacity: 0.7; }}
        .empty-state .msg {{ font-weight: 600; opacity: 0.7; }}

        /* Divider */
        .db-divider {{ height: 1px; background: rgba(128,128,128,0.16); margin: 28px 0; border: none; }}

        /* Sidebar branding */
        .sidebar-brand {{ display: flex; align-items: center; gap: 10px; padding: 4px 0 20px 0; }}
        .sidebar-brand .badge {{
            width: 36px; height: 36px; border-radius: 8px;
            background: {NAVY}; color: #fff; font-size: 17px;
            display: flex; align-items: center; justify-content: center;
        }}
        .sidebar-brand .name {{
            font-family: {DISPLAY_FONT}; font-weight: 700; font-size: 1.0rem;
            color: var(--text-color); line-height: 1.2;
        }}
        .sidebar-brand .tag {{
            font-size: 0.74rem; letter-spacing: 0.05em; text-transform: uppercase;
            color: {GOLD}; opacity: 0.9;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )


def sidebar_brand():
    st.sidebar.markdown(
        """
        <div class="sidebar-brand">
            <div class="badge"><i class="ti ti-chart-infographic"></i></div>
            <div>
                <div class="name">Business Analytics</div>
                <div class="tag">Enterprise Intelligence</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def page_header(icon: str, title: str, subtitle: str = ""):
    st.markdown(
        f"""
        <div class="db-eyebrow">Business Intelligence</div>
        <div class="db-header">
            <div class="icon-badge">{icon}</div>
            <div>
                <h1>{title}</h1>
                {f'<p>{subtitle}</p>' if subtitle else ''}
            </div>
        </div>
        <div class="db-header-rule">
            <div class="bar"></div>
            <div class="hairline"></div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def section_header(title: str, icon: str = ""):
    st.markdown(
        f"""
        <div class="db-section">
            <span class="bar"></span>
            <h3>{(icon + '  ') if icon else ''}{title}</h3>
        </div>
        """,
        unsafe_allow_html=True,
    )


def divider():
    st.markdown('<hr class="db-divider">', unsafe_allow_html=True)


def _kpi_card_html(label, value, icon="", delta=None, delta_type="neutral"):
    delta_html = f'<div class="kpi-delta {delta_type}">{delta}</div>' if delta else ""
    return f"""
        <div class="kpi-card">
            <div class="kpi-top">
                <span class="kpi-label">{label}</span>
                <span class="kpi-icon">{icon}</span>
            </div>
            <div class="kpi-value">{value}</div>
            {delta_html}
        </div>
    """


def kpi_row(cards: list):
    """
    Render a responsive row of KPI cards.
    cards: list of dicts -> label, value, icon(optional), delta(optional), delta_type(optional: positive|negative|neutral)
    """
    cols = st.columns(len(cards))
    for col, card in zip(cols, cards):
        with col:
            st.markdown(
                _kpi_card_html(
                    card.get("label", ""),
                    card.get("value", ""),
                    card.get("icon", ""),
                    card.get("delta"),
                    card.get("delta_type", "neutral"),
                ),
                unsafe_allow_html=True,
            )


def chart_card_start():
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)


def chart_card_end():
    st.markdown("</div>", unsafe_allow_html=True)


def render_chart(fig, height: int = None):
    """Style a Plotly figure to blend with the current Streamlit theme, wrap it
    in a card, and render it — use this instead of a raw st.plotly_chart call."""
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter, sans-serif", color=CHART_FONT_COLOR, size=13),
        margin=dict(l=10, r=10, t=30, b=10),
        legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(color=CHART_FONT_COLOR)),
        colorway=CHART_COLORWAY,
    )
    fig.update_xaxes(gridcolor=CHART_GRID_COLOR, zerolinecolor=CHART_GRID_COLOR)
    fig.update_yaxes(gridcolor=CHART_GRID_COLOR, zerolinecolor=CHART_GRID_COLOR)
    if height:
        fig.update_layout(height=height)

    chart_card_start()
    st.plotly_chart(fig, use_container_width=True)
    chart_card_end()


def empty_state(message: str = "Please upload a dataset on the Home page first.", icon: str = '<i class="ti ti-paperclip"></i>'):
    st.markdown(
        f"""
        <div class="empty-state">
            <div class="icon">{icon}</div>
            <div class="msg">{message}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def summary_card(text: str):
    st.markdown(f'<div class="summary-card">{text}</div>', unsafe_allow_html=True)


def signal_card(text: str, kind: str = "risk"):
    """
    Formal replacement for st.error/st.info/st.success used in the AI
    intelligence sections. kind: "risk" | "priority" | "opportunity" | "note".
    "note" renders a quiet muted line (used for empty/neutral states).
    """
    labels = {
        "risk": ('<i class="ti ti-alert-triangle"></i> Risk'),
        "priority": ('<i class="ti ti-bulb"></i> Priority'),
        "opportunity": ('<i class="ti ti-star"></i> Opportunity'),
    }
    if kind in labels:
        st.markdown(
            f"""
            <div class="signal-card signal-{kind}">
                <span class="signal-label">{labels[kind]}</span>
                <div class="signal-body">{text}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        st.markdown(f'<div class="signal-note">{text}</div>', unsafe_allow_html=True)


def nav_card(icon: str, title: str, desc: str):
    st.markdown(
        f"""
        <div class="kpi-card nav-card">
            <div class="nav-icon">{icon}</div>
            <div class="nav-title">{title}</div>
            <div class="nav-desc">{desc}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
