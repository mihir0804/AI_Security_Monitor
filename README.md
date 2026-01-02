# AI-Based Network Intrusion Detection System (NIDS) 

![Project Status](https://img.shields.io/badge/Status-Active-brightgreen)
![Python](https://img.shields.io/badge/Python-3.11-blue)
![Framework](https://img.shields.io/badge/Framework-Streamlit-red)

## Project Overview
The **Enterprise Security Monitor** is an AI-powered Network Intrusion Detection System (NIDS) designed to detect malicious network traffic in real-time. Unlike traditional firewalls that rely on static rules, this system uses **Machine Learning (Random Forest Classifier)** to identify complex attack patterns such as DDoS, Port Scanning, and Brute Force attacks.

The application features a professional **Heads-Up Display (HUD)** dashboard built with Streamlit, offering security analysts immediate visibility into network health and threat levels.

## Key Features
* **Real-Time Traffic Analysis:** Instantly classifies network packets as "Benign" or "Malicious."
* **Interactive Dashboard:** Visualizes protocol distribution (TCP/UDP/ICMP) and traffic volume.
* **Live Packet Inspector:** A simulation tool that lets users input raw packet data to test the model's response.
* **High Accuracy:** The underlying Random Forest model achieves **99%+ accuracy** on the validation dataset.
* **Explainable AI:** Displays "Feature Importance" charts to show which data points (e.g., Duration, Packet Count) contributed most to the decision.

## Technology Stack
* **Language:** Python 3.x
* **Machine Learning:** Scikit-Learn (Random Forest)
* **Dashboard/UI:** Streamlit
* **Data Processing:** Pandas, NumPy
* **Visualization:** Plotly Express

## Installation & Setup

### 1. Clone the Repository
```bash
git clone [https://github.com/mihir0804/AI_Security_Monitor.git](https://github.com/mihir0804/AI_Security_Monitor.git)
cd AI_Security_Monitor
