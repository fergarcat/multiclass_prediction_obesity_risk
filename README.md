# 🧬 Keep In Shape: Multiclass Prediction of Obesity Risk 🩺

<div align="center">
    <img src="client/media/obesity_logo.png" alt="ObesityRiskML Logo" width="300">
    <br><br>
    <img src="https://img.shields.io/badge/Salud-IA%20Predictiva-4ECDC4?style=for-the-badge&logo=python&logoColor=white" alt="Salud IA Predictiva">
    <img src="https://img.shields.io/badge/Clasificación-Multiclase-orange?style=for-the-badge&logo=scikit-learn&logoColor=white" alt="Clasificación Multiclase">
</div>

> *Behind every piece of data, a type of obesity. Behind the model, a real solution.*

Welcome to **Keep In Shape**, an application that uses multiclass ML techniques to predict people's obesity risk based on lifestyle and eating habits data. This tool is designed to help healthcare professionals and users interested in monitoring and managing obesity-related risks.
## DeepWiki
[![Ask DeepWiki](https://deepwiki.com/badge.svg)](https://deepwiki.com/fergarcat/multiclass_prediction_obesity_risk)

## 📚 table of contents

1. [🧠 Intelligence for Health](#-intelligence-for-health)
2. [🔍 Project Background](#-project-background)
3. [💻 Key Features](#-key-features)
4. [⚙️ Tech Stack](#️-tech-stack)
5. [📁 Project Structure](#-project-structure)
6. [🚀 Installation & Usage](#-installation--usage)
7. [📊 Application Overview](#-application-overview)
8. [👥 Development Team](#-development-team)
9. [🤝 Contributing](#-contributing)

## 🧠 Intelligence for Health

Short summary of what the app does using AI to assess health risks and provide actionable feedback.

Check out the [demo](https://www.canva.com/design/DAGoNogViFQ/Yhy9vFsc4LH1tYbLRMXkWw/edit?utm_content=DAGoNogViFQ&utm_campaign=designshare&utm_medium=link2&utm_source=sharebutton)
 of our app

---

## 🔍 Project Background

Details about:
- Exploratory Data Analysis
- Algorithm experimentation XGBoost
- Model evaluation metrics
- Development of the web application

---

## 💻 Key Features

- Interactive dashboard
- User scenario simulator
- Personalized health recommendations
- Persistent prediction history (supabase)
- Intuitive user interface
- Dockerized deployment

---

## ⚙️ Tech Stack

Badges or list including: Python, Streamlit, Pandas, NumPy, scikit-learn, XGBoost, SQLAlchemy, Matplotlib, Seaborn, Docker.

---

## Project structure

```
multiclass_prediction_obesity_risk/
├── client/                      # User interface
│   └── media/                   # Static assets (images, etc.)
├── data/                        # Project data
│   ├── raw/                     # Original dataset
│   └── processed/               # Processed dataset
├── docs/                        # Project documentation
├── server/                      # Backend and model logic
│   ├── model/                   # Trained models and utilities
│   └── utils/                   # Helper functions
├── tests/                       # Automated tests
├── .gitignore                   # Files ignored by Git
├── pyproject.toml               # Project configuration
├── requirements.txt             # Project dependencies
├── README.md                    # Main documentation
└── Dockerfile                   # Containerization setup

```
----

## 🚀 Installation & Usage

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/fergarcat/multiclass_prediction_obesity_risk.git
cd multiclass_prediction_obesity_risk
```

### 2️⃣ Create and Activate a Virtual Environment

```bash
python3 -m venv .venv
```

**macOS/Linux:**

```bash
source .venv/bin/activate
```

**Windows:**

```bash
.venv\Scripts\activate
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

> 💡 **TIP:**  
> Use `pip list` to see all installed dependencies.

### 4️⃣ Run the Dashboard

```bash
python run_client.py
```

### 5️⃣ Run test

```bash
python -m unittest discover tests
```


## 📊 Application Overview
Dashboard – View obesity-related metrics and predictions.

Simulator – Test different lifestyle configurations.

History – Review and analyze past predictions.

## 👥 Development Team

| **Name**         | **GitHub**                          |  
|--------------------|-------------------------------------|  
| Fernando García Catalán    | [fergarcat](https://github.com/fergarcat) |   
| Anca Bacria        | [a-bac-0](https://github.com/a-bac-0) |  
| Omar Lengua          | [Omarlsant](https://github.com/Omarlsant) | 
| Abigail Masapanta        | [abbyenredes](https://github.com/abbyenredes) | 


## 🤝 Contributing

Contributions are welcome! To contribute:

1. Fork this repository.

2. Create a new branch:

   ```bash
   git checkout -b feature/new-feature
   ```

3. Make your changes and commit them:

   ```bash
   git commit -m "Add new feature"
   ```

4. Submit a pull request 🚀

---

## 🚀 Thank You for Using Keep In Shape!

If you have any questions, feel free to open an issue in the repository or contact us.


