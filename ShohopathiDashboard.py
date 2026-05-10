import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# --- PAGE SETUP ---
st.set_page_config(page_title="Shohopathi Dashboard", page_icon="📈", layout="wide", initial_sidebar_state="collapsed")

# --- CSS FOR CLEAN LOOK & PERFECT CENTERED BALANCED METRICS ---
st.markdown("""
    <style>
    /* একদম উপরের ফাঁকা জায়গা মুছে ফেলার জন্য */
    .block-container { 
        padding-top: 3rem !important; 
        padding-bottom: 2rem !important; 
        margin-top: -5rem !important; 
    }

    header[data-testid="stHeader"] {
        display: none;
    }

    /* সাইডবার ওপেন করার ছোট তীর (>) চিহ্নটি একদম গায়েব করার জন্য */
    [data-testid="collapsedControl"] {
        display: none;
    }

    .stApp { background-color: #f4f6f9; }

    /* Perfect Center Alignment & GLOSSY 3D Look for KPI Cards */
    [data-testid="stMetric"] {
        background: linear-gradient(145deg, #ffffff 0%, #e6e9f0 100%); 
        padding: 15px;
        border-radius: 12px;
        box-shadow: 0 8px 15px rgba(0,0,0,0.08), inset 0 2px 2px rgba(255, 255, 255, 1); 
        border: 1px solid #d2d6dd;
        display: flex;
        flex-direction: column;
        align-items: center; 
        justify-content: center; 
    }

    /* Balanced Bold for Label Text & Icon */
    [data-testid="stMetricLabel"] { 
        width: 100%;
        display: flex;
        justify-content: center;
    }
    [data-testid="stMetricLabel"] > div {
        display: flex;
        justify-content: center;
        align-items: center;
        width: 100%;
    }
    [data-testid="stMetricLabel"] p, 
    [data-testid="stMetricLabel"] span, 
    [data-testid="stMetricLabel"] div {
        font-size: 1.05rem !important; 
        font-weight: 600 !important; 
        color: #495057 !important; 
        text-align: center;
    }

    /* Balanced Bold for Value (Number) */
    [data-testid="stMetricValue"] {
        width: 100%;
        display: flex;
        justify-content: center;
        margin-top: 5px;
    }
    [data-testid="stMetricValue"] > div {
        display: flex;
        justify-content: center;
        align-items: center;
        font-size: 1.8rem !important; 
        font-weight: 700 !important; 
        color: #0E5E6F !important;
        white-space: nowrap;
        overflow: visible;
        width: 100%;
        text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

# --- CONFIGURATION ---
SHEET_ID = "1WO-Rs4wL7D2mIaFHmc3TXuVzfIENZIMreJwibyjCMkc"
GID = "1277367234"  # "test" tab er GID
SHEET_CSV_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid={GID}"

@st.cache_data(ttl=60)
def load_data():
    try:
        df = pd.read_csv(SHEET_CSV_URL)
        num_cols = ['Official Target', 'Sales', 'Actual Sales', 'Remain']
        for col in num_cols:
            df[col] = df[col].astype(str).str.replace(',', '').str.replace('৳', '').str.strip()
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)

        df = df.dropna(subset=['Name', 'Team'])
        df['Progress'] = df.apply(lambda x: (x['Sales'] / x['Official Target'] * 100) if x['Official Target'] > 0 else 0, axis=1)
        df['Progress'] = df['Progress'].apply(lambda x: min(x, 100))
        return df
    except Exception as e:
        return pd.DataFrame()

df = load_data()

if not df.empty:

    # ১. মেইন টাইটেল দেখানোর জন্য প্লেসহোল্ডার
    title_placeholder = st.empty()

    # ২. ফিল্টার এবং রিফ্রেশ বাটন (টপ বার)
    c1, c2, c3, c4 = st.columns([2.5, 1.5, 1.5, 2.5]) 

    with c2:
        team_list = ["All Teams"] + list(df['Team'].dropna().unique())
        selected_team = st.selectbox("Select Team", team_list, label_visibility="collapsed")

    with c3:
        if st.button("🔄 Refresh Data", use_container_width=True):
            st.cache_data.clear()
            st.rerun()

    # ৩. ডেটা ফিল্টার করা
    if selected_team != "All Teams":
        display_df = df[df['Team'] == selected_team]
        header_title = f"Live Dashboard - {selected_team}"
    else:
        display_df = df
        header_title = "Shohopathi Sales Dashboard"


   # ৪. টাইটেলটি সেট করা (Base64 লোগো সহ)

    logo_base64 = "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"

    title_html = f"""
    <div style="display: flex; justify-content: center; align-items: center; gap: 15px; margin-bottom: 0px; padding-bottom: 10px;">
        <img src="data:image/jpeg;base64,{logo_base64}" width="55" style="border-radius: 8px; box-shadow: 0 4px 8px rgba(0,0,0,0.1);">
        <h2 style='color: #0E5E6F; font-weight: bold; margin: 0;'>{header_title}</h2>
    </div>
    """
    title_placeholder.markdown(title_html, unsafe_allow_html=True)

    # --- 1, 3, 6: KPI CARDS ---
    total_target = display_df['Official Target'].sum()
    total_sales = display_df['Sales'].sum()
    total_remain = display_df['Remain'].sum()
    achievement_pct = (total_sales / total_target * 100) if total_target > 0 else 0

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("🎯 Total Target", f"৳ {total_target:,.0f}")
    m2.metric("📈 Total Sales", f"৳ {total_sales:,.0f}")
    m3.metric("📉 Remaining Amount", f"৳ {total_remain:,.0f}")
    m4.metric("🏆 Achievement %", f"{achievement_pct:.1f}%")

    # --- ROW 1: TARGET VS SALES & GAUGE CHART ---
    row1_col1, row1_col2 = st.columns([2, 1])

    with row1_col1:
        st.markdown("<h5 style='text-align: center; margin-top: 10px;'>📊 Target vs Sales Overview</h5>", unsafe_allow_html=True)
        team_agg = display_df.groupby('Team')[['Official Target', 'Sales']].sum().reset_index()

        vibrant_bar_colors = ['#3F51B5', '#D500F9'] 

        fig_bar = px.bar(team_agg, x='Team', y=['Official Target', 'Sales'], barmode='group',
                         color_discrete_sequence=vibrant_bar_colors)

        fig_bar.update_layout(
            height=320, 
            margin=dict(l=0, r=0, t=20, b=0), 
            plot_bgcolor="white", 
            legend_title_text="",
            legend=dict(
                font=dict(color="black", size=14, family="Arial Black"), 
                yanchor="top", y=1, xanchor="right", x=1
            )
        )

        fig_bar.update_yaxes(
            showgrid=True, gridcolor='#f0f0f0', 
            tickformat=",.0f", 
            tickfont=dict(color='black', size=13, family="Arial Black"),
            title=""
        )

        fig_bar.update_xaxes(
            tickfont=dict(color='black', size=14, family="Arial Black"),
            title=""
        )

        fig_bar.update_traces(
            hovertemplate="<b>%{data.name}</b><br><b>Team: %{x}</b><br><b>Value: %{y:,.0f}</b>",
            hoverlabel=dict(bgcolor="white", font=dict(color="black", size=14))
        )

        st.plotly_chart(fig_bar, use_container_width=True)

    with row1_col2:
        st.markdown("<h5 style='text-align: center; margin-top: 10px;'>⏱️ Overall Achievement Gauge</h5>", unsafe_allow_html=True)
        fig_gauge = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = achievement_pct,
            number = {'suffix': "%", 'font': {'color': '#0E5E6F', 'size': 40}},
            gauge = {
                'axis': {'range': [0, 100], 'tickwidth': 1, 'tickcolor': "black"},
                'bar': {'color': "#14082B", 'thickness': 0.70}, 
                'bgcolor': "white",
                'borderwidth': 2,
                'bordercolor': "#e0e0e0",
                'steps': [
                    {'range': [0, 30], 'color': "#FF4B4B"},   
                    {'range': [30, 70], 'color': "#FFC300"},  
                    {'range': [70, 100], 'color': "#00CC66"}  
                ],
            }
        ))
        fig_gauge.update_layout(height=320, margin=dict(l=20, r=20, t=30, b=20))
        st.plotly_chart(fig_gauge, use_container_width=True)

    # --- ROW 2: TEAM WISE PIE & TOP PERFORMER ---
    row2_col1, row2_col2 = st.columns(2)

    with row2_col1:
        if selected_team == "All Teams":
            st.markdown("<h5 style='text-align: center;'>🍩 Team Wise Sales Contribution</h5>", unsafe_allow_html=True)
            pie_data = display_df.groupby('Team')['Sales'].sum().reset_index()
            pie_names = 'Team'
        else:
            st.markdown(f"<h5 style='text-align: center;'>🍩 Member Wise Contribution ({selected_team})</h5>", unsafe_allow_html=True)
            pie_data = display_df.groupby('Name')['Sales'].sum().reset_index() 
            pie_names = 'Name'

        vibrant_colors = ['#1A73E8', '#FF7A00', '#34A853', '#A142F4', '#FBBC04', '#00BCD4']

        fig_pie = px.pie(
            pie_data, 
            values='Sales', 
            names=pie_names, 
            hole=0.45,
            color_discrete_sequence=vibrant_colors
        )

        fig_pie.update_layout(
            height=350, 
            margin=dict(l=20, r=20, t=20, b=20),
            showlegend=True
        )

        fig_pie.update_traces(
            textposition='inside', 
            texttemplate='<b>%{label}</b><br><b>%{percent}</b>',
            insidetextfont=dict(color='white', size=14),
            marker=dict(line=dict(color='#FFFFFF', width=3)),
            hovertemplate="<b>%{label}</b><br><b>Sales: %{value:,.0f}</b>",
            hoverlabel=dict(bgcolor="white", font=dict(color="black", size=14))
        )
        st.plotly_chart(fig_pie, use_container_width=True)

    with row2_col2:
        st.markdown("<h5 style='text-align: center;'>🚀 Top Performers Leaderboard</h5>", unsafe_allow_html=True)

        top_5 = display_df.sort_values(by='Sales', ascending=False).head(5).copy()
        ranks = ['1st 🏆', '2nd 🥈', '3rd 🥉', '4th 🏅', '5th 🏅']

        top_5['Rank'] = ranks[:len(top_5)]

        vibrant_colors = ['#1A73E8', '#FF7A00', '#34A853', '#A142F4', '#FBBC04']

        fig_leader = px.bar(
            top_5, 
            x='Sales', 
            y='Name', 
            orientation='h', 
            color='Name', 
            text='Sales', 
            color_discrete_sequence=vibrant_colors
        )

        max_sales = top_5['Sales'].max()

        fig_leader.update_layout(
            height=350, 
            margin=dict(l=0, r=40, t=20, b=0), 
            yaxis={'categoryorder':'total ascending', 'title': ''}, 
            xaxis={'title': '', 'range': [0, max_sales * 1.2 if pd.notnull(max_sales) else 100]}, 
            plot_bgcolor="white",
            showlegend=False
        )

        fig_leader.update_xaxes(showgrid=True, gridcolor='#f0f0f0', tickformat=",.0f", tickfont=dict(color='black', size=13))
        fig_leader.update_yaxes(tickfont=dict(color='black', size=14, family="Arial Black"))

        fig_leader.update_traces(
            texttemplate='<b>৳ %{x:,.0f}</b>', 
            textposition='inside',
            insidetextfont=dict(color='white', size=15), 
            hovertemplate="<b>%{y}</b><br><b>Sales: %{x:,.0f}</b>",
            hoverlabel=dict(bgcolor="white", font=dict(color="black", size=14))
        )

        for index, row in top_5.iterrows():
            fig_leader.add_annotation(
                x=row['Sales'], 
                y=row['Name'],
                text=f"<b> {row['Rank']}</b>",
                showarrow=False,
                xanchor='left',
                xshift=8,
                font=dict(color="black", size=15)
            )

        st.plotly_chart(fig_leader, use_container_width=True)

    # --- HEAT MAP TABLE ---
    st.markdown("##### 🔥 Heat Map Table (Details)")
    st.markdown("গাঢ় নীল মানে বেশি সেলস, গাঢ় লাল মানে বেশি টার্গেট বাকি আছে, এবং প্রোগ্রেস বারে টার্গেট পূরণের হার দেখানো হয়েছে।")

    styled_df = display_df[['Team', 'Name', 'Official Target', 'Sales', 'Remain', 'Progress']].style\
        .background_gradient(cmap='Blues', subset=['Sales'])\
        .background_gradient(cmap='Reds', subset=['Remain'])\
        .bar(subset=['Progress'], color='#34A853', vmin=0, vmax=100) \
        .format({
            'Official Target': '৳ {:,.0f}',
            'Sales': '৳ {:,.0f}',
            'Remain': '৳ {:,.0f}',
            'Progress': '{:.1f}%'
        })\
        .set_properties(**{
            'text-align': 'center', 
            'font-weight': '600',
            'font-size': '15px'
        })\
        .set_table_styles([
            {'selector': 'th', 'props': [('text-align', 'center'), ('font-size', '16px'), ('color', '#0E5E6F')]}
        ])

    st.dataframe(styled_df, use_container_width=True, hide_index=True, height=450)

else:
    st.error("Data load failed. Please check the connection.")
