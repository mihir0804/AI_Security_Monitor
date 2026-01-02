import streamlit as st
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix
import plotly.express as px
import time

# -------------------------------------------------------------------------
# 1. PAGE CONFIGURATION
# -------------------------------------------------------------------------
st.set_page_config(
    page_title="NIDS | Enterprise Security Monitor",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
    <style>
    .stApp { background-color: #0E1117; color: #FAFAFA; }
    section[data-testid="stSidebar"] { background-color: #161B22; border-right: 1px solid #30363D; }
    div[data-testid="stMetric"] { background-color: #161B22; border: 1px solid #30363D; padding: 15px; border-radius: 6px; }
    div[data-testid="stMetricLabel"] { font-size: 0.8rem; color: #8B949E; }
    div[data-testid="stMetricValue"] { font-size: 1.8rem; color: #FAFAFA; }
    .stButton>button { background-color: #238636; color: white; border-radius: 6px; font-weight: 600; width: 100%; }
    .stButton>button:hover { background-color: #2EA043; }
    </style>
    """, unsafe_allow_html=True)

# -------------------------------------------------------------------------
# 2. DATA ENGINE (NO CACHE - FORCED GENERATION)
# -------------------------------------------------------------------------
def load_data():
    """Generates data where Attack patterns are OBVIOUS."""
    n_samples = 5000
    
    # 1. Generate benign (Safe) traffic
    safe_data = {
        'Destination_Port': np.random.randint(20, 1000, n_samples),
        'Flow_Duration': np.random.randint(50, 2000, n_samples),
        'Total_Fwd_Packets': np.random.randint(1, 20, n_samples),
        'Total_Bwd_Packets': np.random.randint(1, 20, n_samples),
        'Packet_Length_Std': np.random.uniform(0, 10, n_samples),
        'Protocol': np.random.choice([0, 1], size=n_samples), # TCP/UDP
        'Label': 0 # SAFE
    }
    
    # 2. Generate malicious (Attack) traffic
    attack_samples = 1000
    attack_data = {
        'Destination_Port': np.random.choice([8080, 4444, 6667], attack_samples),
        'Flow_Duration': np.random.randint(50000, 100000, attack_samples),
        'Total_Fwd_Packets': np.random.randint(100, 500, attack_samples),
        'Total_Bwd_Packets': np.random.randint(20, 100, attack_samples),
        'Packet_Length_Std': np.random.uniform(100, 300, attack_samples),
        'Protocol': np.random.choice([0, 2], size=attack_samples), # TCP/ICMP
        'Label': 1 # ATTACK
    }
    
    # Combine them
    df_safe = pd.DataFrame(safe_data)
    df_attack = pd.DataFrame(attack_data)
    df = pd.concat([df_safe, df_attack], ignore_index=True)
    return df.sample(frac=1).reset_index(drop=True)

def train_model(df):
    X = df.drop('Label', axis=1)
    y = df['Label']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = RandomForestClassifier(n_estimators=50, max_depth=10, random_state=42)
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    cm = confusion_matrix(y_test, y_pred)
    return model, accuracy, cm, X.columns

# -------------------------------------------------------------------------
# 3. DASHBOARD
# -------------------------------------------------------------------------
def main():
    if 'model' not in st.session_state:
        st.session_state['model'] = None

    c1, c2 = st.columns([3, 1])
    c1.title("Network Intrusion Detection System")
    c1.markdown("<div style='color: #8B949E; margin-top: -10px;'>Enterprise SOC Dashboard | v3.1 (Clean Build)</div>", unsafe_allow_html=True)
    c2.markdown("### ")
    c2.markdown("<div style='text-align: right; color: #238636; font-weight: bold;'>SYSTEM ONLINE</div>", unsafe_allow_html=True)
    st.markdown("---")

    st.sidebar.header("Configuration")
    
    # RESET Button
    if st.sidebar.button("RESET & RETRAIN MODEL"):
        with st.spinner("Flushing cache & Retraining..."):
            df = load_data()
            model, acc, cm, features = train_model(df)
            st.session_state['model'] = model
            st.session_state['accuracy'] = acc
            st.session_state['cm'] = cm
            st.session_state['features'] = features
            st.session_state['df'] = df
        st.sidebar.success(f"New Accuracy: {acc*100:.2f}%")
        time.sleep(1)
        st.rerun()

    # Auto-init if empty
    if st.session_state['model'] is None:
        df = load_data()
        model, acc, cm, features = train_model(df)
        st.session_state['model'] = model
        st.session_state['accuracy'] = acc
        st.session_state['cm'] = cm
        st.session_state['features'] = features
        st.session_state['df'] = df

    # Metrics
    df = st.session_state['df']
    kpi1, kpi2, kpi3, kpi4 = st.columns(4)
    kpi1.metric("Total Records", f"{len(df)}")
    kpi2.metric("Attacks Found", f"{len(df[df['Label']==1])}", delta_color="inverse")
    kpi3.metric("Avg Flow Duration", f"{int(df['Flow_Duration'].mean())} ms")
    kpi4.metric("Model Accuracy", f"{st.session_state['accuracy']*100:.2f}%")

    st.markdown("### ")
    
    # Charts
    tab1, tab2 = st.tabs(["Analytics", "Model Performance"])
    with tab1:
        c1, c2 = st.columns([2, 1])
        c1.plotly_chart(px.pie(df, names='Protocol', title="Protocol Distribution"), width="stretch")
        feat_imp = pd.Series(st.session_state['model'].feature_importances_, index=st.session_state['features']).sort_values()
        c2.plotly_chart(px.bar(x=feat_imp, y=feat_imp.index, orientation='h', title="Feature Importance"), width="stretch")
    with tab2:
        st.plotly_chart(px.imshow(st.session_state['cm'], text_auto=True, color_continuous_scale='Blues', title="Confusion Matrix"), width="stretch")

    # Simulator
    st.markdown("---")
    st.subheader("Live Packet Inspector")
    
    with st.container():
        c1, c2, c3, c4 = st.columns(4)
        dp = c1.number_input("Dest Port", 0, 65535, 8080)
        fd = c2.number_input("Flow Duration", 0, 100000, 90000)
        fp = c3.number_input("Fwd Packets", 0, 1000, 500)
        proto = c4.selectbox("Protocol", [0, 1, 2], format_func=lambda x: {0:'TCP', 1:'UDP', 2:'ICMP'}[x])
        
        with st.expander("Advanced"):
            bp = st.number_input("Bwd Packets", 0, 1000, 55)
            pls = st.number_input("Packet Length Std", 0.0, 500.0, 350.0)

        if st.button("Run Inference", width="stretch"):
            input_data = pd.DataFrame([[dp, fd, fp, bp, pls, proto]], columns=st.session_state['features'])
            pred = st.session_state['model'].predict(input_data)[0]
            prob = st.session_state['model'].predict_proba(input_data)[0]
            
            if pred == 1:
                st.error(f"**THREAT DETECTED** | Malicious Confidence: {prob[1]*100:.2f}% | Action: BLOCK")
            else:
                st.success(f"**TRAFFIC CLEAR** | Benign Confidence: {prob[0]*100:.2f}% | Action: ALLOW")

if __name__ == "__main__":
    main()