
# AI-Based Network Intrusion Detection System (NIDS) - Enterprise Edition

## Project Abstract
This project presents an **Enterprise-Grade Network Intrusion Detection System (NIDS)** designed for modern Security Operations Centers (SOCs). Leveraging a Random Forest Classifier, the system provides real-time traffic analysis to identify malicious patterns with high precision. The application features a professional, high-contrast "Heads-Up Display" (HUD) dashboard built with Streamlit and Plotly. Key capabilities include interactive dynamic visualizations, feature importance analysis, confusion matrix heatmaps for model validation, and a live "Packet Inspector" simulation engine. This system demonstrates a scalable, production-ready approach to AI-driven network security.

## Technical Architecture
**Data Ingestion Layer:**
* **Source:** Simulated enterprise network traffic (TCP/UDP/ICMP protocols).
* **Features:** Destination Port, Flow Duration, Total Fwd/Bwd Packets, Packet Length Std, Protocol Type.

**Processing & Logic Layer:**
* **Data Handling:** `pandas` and `numpy` for high-performance data manipulation.
* **Machine Learning:** `scikit-learn` (Random Forest Classifier) with 85/15 benign-to-malicious class distribution.
* **Metrics:** Accuracy Score, Confusion Matrix, Feature Importance.

**Application Layer (UI):**
* **Dashboard:** `streamlit` web interface with a custom "Charcoal/Matte" enterprise theme.
* **Visualization:** `plotly` (Interactive Pie Charts, Bar Charts, and Heatmaps) for professional-grade analytics.

## User Manual
**Prerequisites:**
* Python 3.8 or higher.
* Required libraries: `pandas`, `numpy`, `scikit-learn`, `streamlit`, `plotly`.

**Installation Steps:**
1.  Navigate to the `AI_NIDS_Project` directory.
2.  Install dependencies:
    ```bash
    pip install pandas numpy scikit-learn streamlit plotly
    ```

**Execution:**
1.  Run the application:
    ```bash
    python -m streamlit run nids_main.py
    ```
2.  **Dashboard Controls:**
    * **Retrain Model:** Click to optimize the Random Forest model with new simulated data.
    * **Analytics View:** Explore Protocol Distribution and Feature Importance.
    * **Model Performance:** View the Confusion Matrix Heatmap.
    * **Live Packet Inspector:** Input raw packet data (Port, Duration, etc.) to test the system's detection logic in real-time.

## Future Scope
* **SIEM Integration:** Connect to Splunk or ELK Stack for log aggregation.
* **Deep Learning Models:** Implement LSTM for sequence-based anomaly detection.
* **Real-Time Sniffing:** Integrate `scapy` for live packet capture from network interfaces.
* **API Deployment:** Expose the model via FastAPI for external consumption.
