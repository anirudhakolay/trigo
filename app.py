import streamlit as st
import math
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import random
import pandas as pd

# ============================================================
# PAGE CONFIGURATION
# ============================================================
st.set_page_config(
    page_title="Trigonometry Master",
    page_icon=None,
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# CUSTOM CSS
# ============================================================
st.markdown("""
<style>
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 5px 5px;
        font-weight: bold;
        font-size: 12px;
        transition: all 0.3s;
        width: 100%;
    }
    .stButton > button:hover {
        transform: scale(1.05);
        box-shadow: 0 5px 15px rgba(0,0,0,0.3);
    }
    .metric-card {
        background: white;
        border-radius: 15px;
        padding: 20px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        text-align: center;
    }
    .formula-box {
        background: #f8f9fa;
        border-left: 4px solid #667eea;
        padding: 15px;
        border-radius: 5px;
        margin: 10px 0;
    }
    /* Graph container styling */
    .graph-container {
        background: white;
        border-radius: 15px;
        padding: 20px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================
# TITLE
# ============================================================
st.title("TRIGONOMETRY MASTER")
st.markdown("### Complete Mathematical Trigonometry Tool with Interactive Graphs")
st.markdown("---")

# ============================================================
# SIDEBAR - INPUT
# ============================================================
def update_angle(val):
    st.session_state.angle_input = float(val)

def set_random_angle():
    st.session_state.angle_input = float(random.randint(0, 360))

with st.sidebar:
    st.header("CONTROL PANEL")
    st.markdown("---")

#     # Angle Input
#     st.subheader("Enter Angle")
#     # Initialize session state for angle if not present
#     if "angle_input" not in st.session_state:
#         st.session_state.angle_input = 45.0
#     # Use the session state value as the default for the number input
#     angle = st.number_input(
#         "Angle (Degrees):",
#         value=st.session_state.angle_input,
#         step=1.0,
#         format="%.1f"
#     )
#     # Keep session state in sync with the widget
#     st.session_state.angle_input = angle

    st.markdown("---")

    # Quick Angle Buttons
    st.subheader("Quick Angles")

    row1 = st.columns(4)
    row2 = st.columns(4)

    angles_row1 = [0, 30, 45, 60]
    angles_row2 = [90, 180, 270, 360]

    for col, ang in zip(row1, angles_row1):
        with col:
            st.button(f"{ang}°", key=f"q1_{ang}", use_container_width=True, on_click=update_angle, args=(ang,))

    for col, ang in zip(row2, angles_row2):
        with col:
            st.button(f"{ang}°", key=f"q2_{ang}", use_container_width=True, on_click=update_angle, args=(ang,))

    st.markdown("---")

    # Random Button
    st.button("Random Angle", use_container_width=True, on_click=set_random_angle)

    st.markdown("---")

    # Graph Toggles
    st.subheader("Display Options")
    show_unit_circle = st.checkbox("Unit Circle", True)
    show_graph_comparison = st.checkbox("Graph Comparison", True)
    show_astc = st.checkbox("ASTC Rule", True)
    show_bar_chart = st.checkbox("Bar Chart", True)
    show_angle_table = st.checkbox("Angle Table", True)
    show_identities = st.checkbox("Identities Checker", True)
    show_periodic = st.checkbox("Periodic Properties", True)
    show_formulas = st.checkbox("Formula Reference", True)
    show_converter = st.checkbox("Degree-Radian Converter", True)

# ============================================================
# CALCULATIONS
# ============================================================

rad = math.radians(angle)
sin_val = round(math.sin(rad), 4)
cos_val = round(math.cos(rad), 4)

# Handle undefined values
if abs(angle % 180 - 90) < 1e-9:
    tan_val = None
    cot_val = None
    sec_val = None
    cosec_val = round(1/sin_val, 4) if sin_val != 0 else None
elif abs(angle % 180) < 1e-9:
    tan_val = 0
    cot_val = None
    sec_val = round(1/cos_val, 4) if cos_val != 0 else None
    cosec_val = None
else:
    tan_val = round(math.tan(rad), 4)
    cot_val = round(1/math.tan(rad), 4) if math.tan(rad) != 0 else None
    sec_val = round(1/cos_val, 4) if cos_val != 0 else None
    cosec_val = round(1/sin_val, 4) if sin_val != 0 else None

# Quadrant Detection
a = angle % 360
if a == 0 or a == 360:
    quad = "Positive X-axis"
    astc_rule = "Boundary Point"
elif a == 90:
    quad = "Positive Y-axis"
    astc_rule = "Boundary Point"
elif a == 180:
    quad = "Negative X-axis"
    astc_rule = "Boundary Point"
elif a == 270:
    quad = "Negative Y-axis"
    astc_rule = "Boundary Point"
elif a < 90:
    quad = "Quadrant I (+,+)"
    astc_rule = "ALL Positive (Sin, Cos, Tan, Cot, Sec, Cosec)"
elif a < 180:
    quad = "Quadrant II (-,+)"
    astc_rule = "Only SIN & COSEC Positive"
elif a < 270:
    quad = "Quadrant III (-,-)"
    astc_rule = "Only TAN & COT Positive"
else:
    quad = "Quadrant IV (+,-)"
    astc_rule = "Only COS & SEC Positive"

# Radian Conversion
special_angles = {
    0: "0", 30: "π/6", 45: "π/4", 60: "π/3",
    90: "π/2", 120: "2π/3", 135: "3π/4",
    150: "5π/6", 180: "π", 210: "7π/6",
    225: "5π/4", 240: "4π/3", 270: "3π/2",
    300: "5π/3", 315: "7π/4", 330: "11π/6", 360: "2π"
}

if int(angle) in special_angles:
    rad_str = special_angles[int(angle)]
else:
    rad_str = f"{rad:.4f} rad"

# Identity Check
sin2_plus_cos2 = round(sin_val**2 + cos_val**2, 4)
identity_status = "Verified" if abs(sin2_plus_cos2 - 1) < 0.001 else "Failed"

# ============================================================
# FORMAT FUNCTION
# ============================================================
def format_val(val):
    if val is None:
        return "Undefined"
    return f"{val:.4f}"

# ============================================================
# 1. ALL 6 TRIG RATIOS
# ============================================================
st.markdown("## All 6 Trigonometric Ratios")

col1, col2, col3, col4, col5, col6 = st.columns(6)

with col1:
    st.metric("Sin θ", format_val(sin_val))
with col2:
    st.metric("Cos θ", format_val(cos_val))
with col3:
    st.metric("Tan θ", format_val(tan_val))
with col4:
    st.metric("Cot θ", format_val(cot_val))
with col5:
    st.metric("Sec θ", format_val(sec_val))
with col6:
    st.metric("Cosec θ", format_val(cosec_val))

# Info cards
col1, col2, col3 = st.columns(3)
with col1:
    st.info(f"**Angle:** {angle}°")
with col2:
    st.info(f"**Radian:** {rad_str}")
with col3:
    st.info(f"**Quadrant:** {quad}")

# Detailed table
st.markdown("### Detailed Ratio Table")
data = {
    'Function': ['Sin θ', 'Cos θ', 'Tan θ', 'Cot θ', 'Sec θ', 'Cosec θ'],
    'Value': [
        format_val(sin_val),
        format_val(cos_val),
        format_val(tan_val),
        format_val(cot_val),
        format_val(sec_val),
        format_val(cosec_val)
    ],
    'Formula': [
        'Opposite/Hypotenuse',
        'Adjacent/Hypotenuse',
        'Sin/Cos',
        'Cos/Sin',
        '1/Cos',
        '1/Sin'
    ],
    'Sign': [
        '+' if sin_val > 0 else '-' if sin_val < 0 else '0',
        '+' if cos_val > 0 else '-' if cos_val < 0 else '0',
        '+' if tan_val and tan_val > 0 else '-' if tan_val and tan_val < 0 else '0',
        '+' if cot_val and cot_val > 0 else '-' if cot_val and cot_val < 0 else '0',
        '+' if sec_val and sec_val > 0 else '-' if sec_val and sec_val < 0 else '0',
        '+' if cosec_val and cosec_val > 0 else '-' if cosec_val and cosec_val < 0 else '0'
    ]
}
df = pd.DataFrame(data)
st.table(df)

# ============================================================
# 2. DEGREE - RADIAN CONVERTER
# ============================================================
if show_converter:
    st.markdown("---")
    st.markdown("## Degree - Radian Converter")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Degrees to Radians")
        deg_input = st.number_input("Enter degrees:", value=45.0, key="deg_to_rad")
        if st.button("Convert to Radians", key="deg_to_rad_btn"):
            rad_output = math.radians(deg_input)
            st.metric("Radians", f"{rad_output:.6f}")
            st.write(f"**π form:** {rad_output/math.pi:.4f}π")

            # Show standard angle
            for d, r in special_angles.items():
                if d == int(deg_input):
                    st.success(f"Standard angle: {r}")

    with col2:
        st.subheader("Radians to Degrees")
        rad_input = st.number_input("Enter radians:", value=0.7854, key="rad_to_deg")
        if st.button("Convert to Degrees", key="rad_to_deg_btn"):
            deg_output = math.degrees(rad_input)
            st.metric("Degrees", f"{deg_output:.6f}°")

            # Show standard angle
            for d, r in special_angles.items():
                if abs(math.radians(d) - rad_input) < 0.01:
                    st.success(f"Standard angle: {d}° ({r})")

# ============================================================
# 3. GRAPH 1: UNIT CIRCLE (CLEAR VERSION)
# ============================================================
if show_unit_circle:
    st.markdown("---")
    st.markdown("## Interactive Unit Circle")

    fig = go.Figure()

    # Draw circle - thicker
    theta = np.linspace(0, 2*np.pi, 500)
    fig.add_trace(go.Scatter(
        x=np.cos(theta), y=np.sin(theta),
        mode='lines',
        line=dict(color='#2c3e50', width=3),
        name='Unit Circle (r = 1)'
    ))

    # Grid lines
    fig.update_xaxes(
        showgrid=True,
        gridwidth=1,
        gridcolor='lightgray',
        tickvals=[-1, -0.5, 0, 0.5, 1],
        ticktext=['-1', '-0.5', '0', '0.5', '1']
    )
    fig.update_yaxes(
        showgrid=True,
        gridwidth=1,
        gridcolor='lightgray',
        tickvals=[-1, -0.5, 0, 0.5, 1],
        ticktext=['-1', '-0.5', '0', '0.5', '1']
    )

    # Axes
    fig.add_hline(y=0, line_color='black', line_width=2)
    fig.add_vline(x=0, line_color='black', line_width=2)

    # Angle line
    x = [0, cos_val]
    y = [0, sin_val]
    fig.add_trace(go.Scatter(
        x=x, y=y,
        mode='lines+markers',
        line=dict(color='red', width=4),
        marker=dict(size=14, color='red', symbol='circle'),
        name=f'θ = {angle}°'
    ))

    # Sin projection
    fig.add_trace(go.Scatter(
        x=[cos_val, cos_val], y=[0, sin_val],
        mode='lines',
        line=dict(color='green', width=3, dash='dash'),
        name='Sin θ (Vertical)'
    ))

    # Cos projection
    fig.add_trace(go.Scatter(
        x=[0, cos_val], y=[0, 0],
        mode='lines',
        line=dict(color='blue', width=3, dash='dash'),
        name='Cos θ (Horizontal)'
    ))

    # Angle arc
    arc_theta = np.linspace(0, rad, 100)
    fig.add_trace(go.Scatter(
        x=0.4*np.cos(arc_theta), y=0.4*np.sin(arc_theta),
        mode='lines',
        line=dict(color='orange', width=3),
        name='Angle Arc'
    ))

    # Angle label inside arc
    mid_angle = rad/2
    fig.add_annotation(
        x=0.5*np.cos(mid_angle),
        y=0.5*np.sin(mid_angle),
        text=f"{angle}°",
        showarrow=False,
        font=dict(size=16, color='orange', weight='bold')
    )

    # Coordinate labels
    fig.add_annotation(
        x=cos_val, y=sin_val,
        text=f"<b>({cos_val:.3f}, {sin_val:.3f})</b>",
        showarrow=True,
        arrowhead=2,
        ax=30, ay=-40,
        font=dict(size=14, color='red')
    )

    # Quadrant labels
    fig.add_annotation(x=0.7, y=0.7, text="<b>I</b><br>All +", showarrow=False,
                       font=dict(size=14, color='green'), bgcolor='white', opacity=0.8)
    fig.add_annotation(x=-0.7, y=0.7, text="<b>II</b><br>Sin +", showarrow=False,
                       font=dict(size=14, color='blue'), bgcolor='white', opacity=0.8)
    fig.add_annotation(x=-0.7, y=-0.7, text="<b>III</b><br>Tan +", showarrow=False,
                       font=dict(size=14, color='orange'), bgcolor='white', opacity=0.8)
    fig.add_annotation(x=0.7, y=-0.7, text="<b>IV</b><br>Cos +", showarrow=False,
                       font=dict(size=14, color='purple'), bgcolor='white', opacity=0.8)

    fig.update_layout(
        height=600,
        xaxis=dict(range=[-1.3, 1.3], title='<b>Cos θ</b>', scaleanchor="y", scaleratio=1),
        yaxis=dict(range=[-1.3, 1.3], title='<b>Sin θ</b>'),
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="center",
            x=0.5,
            font=dict(size=12)
        ),
        plot_bgcolor='white'
    )

    st.plotly_chart(fig, use_container_width=True)

    # Explanation
    with st.expander("How to read this graph", expanded=True):
        st.markdown("""
        **Red Line** = Angle θ from origin to point on circle
        **Green Line** = Sin θ (vertical height from x-axis to point)
        **Blue Line** = Cos θ (horizontal distance from origin to point)
        **Orange Arc** = The angle θ in degrees
        **Point (cos θ, sin θ)** = Where the angle meets the circle
        """)

# ============================================================
# 4. GRAPH 2: GRAPH COMPARISON (CLEAR VERSION)
# ============================================================
if show_graph_comparison:
    st.markdown("---")
    st.markdown("## Graph Comparison (Sin, Cos, Tan)")

    x_wave = np.linspace(0, 360, 1000)

    fig = go.Figure()

    # Sin wave
    fig.add_trace(go.Scatter(
        x=x_wave, y=np.sin(np.radians(x_wave)),
        mode='lines',
        line=dict(color='#e74c3c', width=3),
        name='<b>Sin θ</b>',
        fill='tozeroy',
        fillcolor='rgba(231, 76, 60, 0.2)'
    ))

    # Cos wave
    fig.add_trace(go.Scatter(
        x=x_wave, y=np.cos(np.radians(x_wave)),
        mode='lines',
        line=dict(color='#2980b9', width=3),
        name='<b>Cos θ</b>',
        fill='tozeroy',
        fillcolor='rgba(41, 128, 185, 0.2)'
    ))

    # Tan wave (clipped)
    tan_wave = np.tan(np.radians(x_wave))
    tan_wave_clipped = np.clip(tan_wave, -3, 3)
    fig.add_trace(go.Scatter(
        x=x_wave, y=tan_wave_clipped,
        mode='lines',
        line=dict(color='#27ae60', width=2.5),
        name='<b>Tan θ</b>'
    ))

    # Current angle marker
    fig.add_vline(
        x=angle,
        line_dash='dash',
        line_color='#8e44ad',
        line_width=4,
        annotation_text=f'<b>{angle}°</b>',
        annotation_position='top',
        annotation_font_size=16
    )

    # Points at current angle
    fig.add_trace(go.Scatter(
        x=[angle], y=[sin_val],
        mode='markers',
        marker=dict(size=16, color='#e74c3c', symbol='circle', line=dict(width=2, color='white')),
        name=f'Sin({angle}°) = {sin_val:.4f}'
    ))
    fig.add_trace(go.Scatter(
        x=[angle], y=[cos_val],
        mode='markers',
        marker=dict(size=16, color='#2980b9', symbol='circle', line=dict(width=2, color='white')),
        name=f'Cos({angle}°) = {cos_val:.4f}'
    ))
    if tan_val is not None and abs(tan_val) <= 3:
        fig.add_trace(go.Scatter(
            x=[angle], y=[tan_val],
            mode='markers',
            marker=dict(size=16, color='#27ae60', symbol='circle', line=dict(width=2, color='white')),
            name=f'Tan({angle}°) = {tan_val:.4f}'
        ))

    # Asymptotes
    for deg in [90, 270]:
        fig.add_vline(
            x=deg,
            line_dash='dot',
            line_color='gray',
            line_width=2,
            annotation_text='∞',
            annotation_position='top'
        )

    fig.add_hline(y=0, line_color='black', line_width=1.5)

    fig.update_xaxes(
        showgrid=True,
        gridwidth=1,
        gridcolor='lightgray',
        tickvals=[0, 30, 60, 90, 120, 150, 180, 210, 240, 270, 300, 330, 360],
        ticktext=['0°', '30°', '60°', '90°', '120°', '150°', '180°', '210°', '240°', '270°', '300°', '330°', '360°']
    )

    fig.update_yaxes(
        showgrid=True,
        gridwidth=1,
        gridcolor='lightgray',
        tickvals=[-2, -1.5, -1, -0.5, 0, 0.5, 1, 1.5, 2],
        ticktext=['-2', '-1.5', '-1', '-0.5', '0', '0.5', '1', '1.5', '2']
    )

    fig.update_layout(
        height=500,
        xaxis_title='<b>Angle (Degrees)</b>',
        yaxis_title='<b>Value</b>',
        yaxis=dict(range=[-2.5, 2.5]),
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="center",
            x=0.5,
            font=dict(size=12)
        ),
        hovermode='x',
        plot_bgcolor='white'
    )

    st.plotly_chart(fig, use_container_width=True)

    # Values at current angle
    st.markdown("### Values at Current Angle")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Sin θ", format_val(sin_val))
    with col2:
        st.metric("Cos θ", format_val(cos_val))
    with col3:
        st.metric("Tan θ", format_val(tan_val))

# ============================================================
# 5. GRAPH 3: ASTC RULE (CLEAR VERSION)
# ============================================================
if show_astc:
    st.markdown("---")
    st.markdown("## ASTC Rule Visualizer")

    fig = go.Figure()

    quadrants = [
        {"name": "ALL", "sign": "All +", "color": "rgba(46, 204, 113, 0.4)", "x": 0.5, "y": 0.5},
        {"name": "SIN", "sign": "Sin +", "color": "rgba(52, 152, 219, 0.4)", "x": -0.5, "y": 0.5},
        {"name": "TAN", "sign": "Tan +", "color": "rgba(231, 76, 60, 0.4)", "x": -0.5, "y": -0.5},
        {"name": "COS", "sign": "Cos +", "color": "rgba(155, 89, 182, 0.4)", "x": 0.5, "y": -0.5}
    ]

    for i, q in enumerate(quadrants):
        x0 = 0 if i in [0, 3] else -1
        y0 = 0 if i in [0, 1] else -1
        x1 = 1 if i in [0, 3] else 0
        y1 = 1 if i in [0, 1] else 0

        fig.add_shape(
            type='rect',
            x0=x0, y0=y0, x1=x1, y1=y1,
            fillcolor=q['color'],
            line=dict(color='black', width=2),
            opacity=0.8
        )

        fig.add_annotation(
            x=(x0+x1)/2, y=(y0+y1)/2,
            text=f"<b>{q['name']}</b><br><span style='font-size:14px'>{q['sign']}</span>",
            showarrow=False,
            font=dict(size=20)
        )

    # Highlight current quadrant
    quadrant_map = {
        "Quadrant I (+,+)": 0,
        "Quadrant II (-,+)": 1,
        "Quadrant III (-,-)": 2,
        "Quadrant IV (+,-)": 3
    }

    if quad in quadrant_map:
        q = quadrant_map[quad]
        x0 = 0 if q in [0, 3] else -1
        y0 = 0 if q in [0, 1] else -1
        x1 = 1 if q in [0, 3] else 0
        y1 = 1 if q in [0, 1] else 0

        fig.add_shape(
            type='rect',
            x0=x0, y0=y0, x1=x1, y1=y1,
            line=dict(color='red', width=6, dash='dash')
        )

    # Axes
    fig.add_hline(y=0, line_color='black', line_width=2)
    fig.add_vline(x=0, line_color='black', line_width=2)

    # Axis labels
    fig.add_annotation(x=1.1, y=0, text="<b>Cos θ</b>", showarrow=False, font=dict(size=14))
    fig.add_annotation(x=0, y=1.1, text="<b>Sin θ</b>", showarrow=False, font=dict(size=14))

    fig.update_layout(
        height=450,
        xaxis=dict(range=[-1.4, 1.4], showgrid=False, zeroline=False),
        yaxis=dict(range=[-1.4, 1.4], showgrid=False, zeroline=False),
        showlegend=False
    )

    st.plotly_chart(fig, use_container_width=True)

    # Clear explanation
    col1, col2 = st.columns(2)
    with col1:
        st.success(f"""
        **Your Angle: {angle}°**
        **Quadrant: {quad}**
        **ASTC Rule: {astc_rule}**
        """)
    with col2:
        st.info("""
        **How to remember "ASTC":**

        **A**ll → Quadrant I (All positive)
        **S**in → Quadrant II (Sin positive)
        **T**an → Quadrant III (Tan positive)
        **C**os → Quadrant IV (Cos positive)
        """)

# ============================================================
# 6. GRAPH 4: BAR CHART (CLEAR VERSION)
# ============================================================
if show_bar_chart:
    st.markdown("---")
    st.markdown("## All 6 Ratios Bar Chart")

    ratios = ['Sin θ', 'Cos θ', 'Tan θ', 'Cot θ', 'Sec θ', 'Cosec θ']
    values = [
        sin_val,
        cos_val,
        tan_val if tan_val is not None else 0,
        cot_val if cot_val is not None else 0,
        sec_val if sec_val is not None else 0,
        cosec_val if cosec_val is not None else 0
    ]
    colors = ['#e74c3c', '#2980b9', '#2ecc71', '#e67e22', '#9b59b6', '#1abc9c']

    text_labels = []
    for i, v in enumerate(values):
        if i == 2 and tan_val is None:
            text_labels.append("∞")
        elif i == 3 and cot_val is None:
            text_labels.append("∞")
        elif i == 4 and sec_val is None:
            text_labels.append("∞")
        elif i == 5 and cosec_val is None:
            text_labels.append("∞")
        else:
            text_labels.append(f"{v:.3f}")

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=ratios,
        y=values,
        marker_color=colors,
        text=text_labels,
        textposition='outside',
        textfont=dict(size=16, color='black', family='Arial Black'),
        width=0.6,
        showlegend=False
    ))

    fig.add_hline(y=0, line_color="black", line_width=2)
    fig.add_hline(y=1, line_dash="dash", line_color="#2ecc71", line_width=2, opacity=0.5)
    fig.add_hline(y=-1, line_dash="dash", line_color="#e74c3c", line_width=2, opacity=0.5)

    fig.update_layout(
        height=450,
        yaxis_title="<b>Value</b>",
        xaxis_title="<b>Trigonometric Ratios</b>",
        yaxis=dict(range=[-1.5, 1.5], tickvals=[-1.5, -1, -0.5, 0, 0.5, 1, 1.5]),
        plot_bgcolor='white',
        bargap=0.2
    )

    st.plotly_chart(fig, use_container_width=True)

    st.info("""
    **Bar Chart Guide:**
    - **Green Line** = Value = 1
    - **Red Line** = Value = -1
    - **∞** = Undefined (division by zero)
    - Bar height shows the ratio value
    """)

# ============================================================
# 7. ANGLE TABLE
# ============================================================
if show_angle_table:
    st.markdown("---")
    st.markdown("## Complete Angle Table (0° - 360°)")

    standard_angles = [0, 30, 45, 60, 90, 120, 135, 150, 180,
                       210, 225, 240, 270, 300, 315, 330, 360]

    angle_data = []
    for ang in standard_angles:
        rad_ang = math.radians(ang)
        tan_ang = math.tan(rad_ang) if ang % 180 != 90 else '∞'

        # Quadrant
        if ang == 0 or ang == 360:
            q = "X-axis"
        elif ang == 90:
            q = "Y-axis"
        elif ang == 180:
            q = "X-axis"
        elif ang == 270:
            q = "Y-axis"
        elif ang < 90:
            q = "QI"
        elif ang < 180:
            q = "QII"
        elif ang < 270:
            q = "QIII"
        else:
            q = "QIV"

        angle_data.append({
            'Angle (°)': ang,
            'Radian': special_angles.get(ang, f"{rad_ang:.4f}"),
            'Sin': f"{math.sin(rad_ang):.4f}",
            'Cos': f"{math.cos(rad_ang):.4f}",
            'Tan': f"{tan_ang:.4f}" if isinstance(tan_ang, float) else '∞',
            'Quadrant': q
        })

    df = pd.DataFrame(angle_data)
    st.dataframe(df, use_container_width=True, height=400)

    if int(angle) in standard_angles:
        st.success(f"Current angle **{angle}°** is in the table above!")
    else:
        st.info(f"**{angle}°** is not a standard angle.")
        closest = min(standard_angles, key=lambda x: abs(x - angle))
        st.write(f"Closest standard angle: **{closest}°**")

# ============================================================
# 8. IDENTITIES CHECKER
# ============================================================
if show_identities:
    st.markdown("---")
    st.markdown("## Trig Identities Checker")

    identity1 = sin_val**2 + cos_val**2
    tan_float = tan_val if isinstance(tan_val, float) else 0
    identity2 = 1 + tan_float**2
    cot_float = cot_val if isinstance(cot_val, float) else 0
    identity3 = 1 + cot_float**2

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("### sin²θ + cos²θ")
        st.metric("= 1", f"{identity1:.4f}")
        if abs(identity1 - 1) < 0.001:
            st.success("Verified")

    with col2:
        st.markdown("### 1 + tan²θ")
        if sec_val is not None:
            sec_float = sec_val if isinstance(sec_val, float) else 0
            st.metric("= sec²θ", f"{identity2:.4f}")
            if abs(identity2 - sec_float**2) < 0.001:
                st.success("Verified")
        else:
            st.warning("Undefined for this angle")

    with col3:
        st.markdown("### 1 + cot²θ")
        if cosec_val is not None:
            cosec_float = cosec_val if isinstance(cosec_val, float) else 0
            st.metric("= csc²θ", f"{identity3:.4f}")
            if abs(identity3 - cosec_float**2) < 0.001:
                st.success("Verified")
        else:
            st.warning("Undefined for this angle")

# ============================================================
# 9. PERIODIC PROPERTIES
# ============================================================
if show_periodic:
    st.markdown("---")
    st.markdown("## Periodic Properties")

    col1, col2, col3 = st.columns(3)

    with col1:
        sin_360 = round(math.sin(math.radians(angle + 360)), 4)
        st.subheader("sin(θ + 360°)")
        st.write(f"sin({angle}° + 360°) = {sin_360:.4f}")
        st.write(f"sin({angle}°) = {sin_val:.4f}")
        if abs(sin_360 - sin_val) < 0.001:
            st.success("Period = 360°")

    with col2:
        sin_180 = round(math.sin(math.radians(180 - angle)), 4)
        st.subheader("sin(180° - θ)")
        st.write(f"sin(180° - {angle}°) = {sin_180:.4f}")
        if abs(sin_180 - sin_val) < 0.001:
            st.success("sin(180° - θ) = sin θ")

    with col3:
        cos_360 = round(math.cos(math.radians(angle + 360)), 4)
        st.subheader("cos(θ + 360°)")
        st.write(f"cos({angle}° + 360°) = {cos_360:.4f}")
        if abs(cos_360 - cos_val) < 0.001:
            st.success("Period = 360°")

# ============================================================
# 10. FORMULA REFERENCE
# ============================================================
if show_formulas:
    st.markdown("---")
    st.markdown("## Complete Formula Reference")

    with st.expander("Basic Ratios", expanded=False):
        st.markdown("""
        | Ratio | Formula |
        |-------|---------|
        | **Sin θ** | Opposite / Hypotenuse |
        | **Cos θ** | Adjacent / Hypotenuse |
        | **Tan θ** | Opposite / Adjacent = Sin/Cos |
        | **Cot θ** | Adjacent / Opposite = Cos/Sin = 1/Tan |
        | **Sec θ** | Hypotenuse / Adjacent = 1/Cos |
        | **Cosec θ** | Hypotenuse / Opposite = 1/Sin |
        """)

    with st.expander("Reciprocal Identities", expanded=False):
        st.markdown("""
        - csc θ = 1/sin θ
        - sec θ = 1/cos θ
        - cot θ = 1/tan θ
        - tan θ = sin θ/cos θ
        - cot θ = cos θ/sin θ
        """)

    with st.expander("Pythagorean Identities", expanded=False):
        st.markdown("""
        - **sin²θ + cos²θ = 1**
        - **1 + tan²θ = sec²θ**
        - **1 + cot²θ = csc²θ**
        """)

    with st.expander("Angle Sum & Difference", expanded=False):
        st.markdown("""
        - sin(A+B) = sinA cosB + cosA sinB
        - sin(A-B) = sinA cosB - cosA sinB
        - cos(A+B) = cosA cosB - sinA sinB
        - cos(A-B) = cosA cosB + sinA sinB
        - tan(A+B) = (tanA + tanB)/(1 - tanA tanB)
        - tan(A-B) = (tanA - tanB)/(1 + tanA tanB)
        """)

    with st.expander("Double Angle Formulas", expanded=False):
        st.markdown("""
        - sin(2θ) = 2sinθ cosθ
        - cos(2θ) = cos²θ - sin²θ = 2cos²θ - 1 = 1 - 2sin²θ
        - tan(2θ) = 2tanθ/(1 - tan²θ)
        """)

    with st.expander("Half Angle Formulas", expanded=False):
        st.markdown("""
        - sin(θ/2) = ±√((1-cosθ)/2)
        - cos(θ/2) = ±√((1+cosθ)/2)
        - tan(θ/2) = ±√((1-cosθ)/(1+cosθ))
        """)

# ============================================================
# FOOTER
# ============================================================
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; padding: 20px; color: #666;'>
        <h3>Trigonometry Master</h3>
        <p>Complete Mathematical Trigonometry Tool with Interactive Graphs</p>
        <p style='font-size: 12px;'>Made with using Streamlit & Plotly</p>
    </div>
    """,
    unsafe_allow_html=True
)