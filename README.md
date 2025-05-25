
# 🧬 Keep In Shape: Multiclass Prediction of Obesity Risk 🩺

<div align="center">
    <img src="https://github.com/fergarcat/multiclass_prediction_obesity_risk/blob/main/client/assets/logo/Keep-caqui-full-256.png" alt="ObesityRiskML Logo" width="300">
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
7. [📊 About our model](#-about-our-model)
8. [👥 Development Team](#-development-team)
9. [🤝 Contributing](#-contributing)

## 🧠 Intelligence for Health

Check out the [demo](https://www.canva.com/design/DAGoNogViFQ/Yhy9vFsc4LH1tYbLRMXkWw/edit?utm_content=DAGoNogViFQ&utm_campaign=designshare&utm_medium=link2&utm_source=sharebutton)
 of our app

---

## 🔍 Project Background

Details about:
- Exploratory Data Analysis
- Algorithm experimentation XGBoost
- Model evaluation metrics
- Development of the web application
- Please visit our [technical report](https://github.com/fergarcat/multiclass_prediction_obesity_risk/blob/main/docs/informe-obesidad.docx) for a detailed overview of the project.


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

[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Dash](https://img.shields.io/badge/Dash-000000?style=for-the-badge&logo=plotly&logoColor=white)](https://dash.plotly.com/)
[![Pandas](https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white)](https://pandas.pydata.org/)
[![NumPy](https://img.shields.io/badge/NumPy-013243?style=for-the-badge&logo=numpy&logoColor=white)](https://numpy.org/)
[![scikit-learn](https://img.shields.io/badge/scikit--learn-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white)](https://scikit-learn.org/)
[![XGBoost](https://img.shields.io/badge/XGBoost-EC6B24?style=for-the-badge&logo=github&logoColor=white)](https://xgboost.readthedocs.io/)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-DB291F?style=for-the-badge&logo=sqlalchemy&logoColor=white)](https://www.sqlalchemy.org/)
[![Matplotlib](https://img.shields.io/badge/Matplotlib-11557C?style=for-the-badge&logo=plotly&logoColor=white)](https://matplotlib.org/)
[![Seaborn](https://img.shields.io/badge/Seaborn-4C8CBF?style=for-the-badge&logo=python&logoColor=white)](https://seaborn.pydata.org/)
[![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com/)

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

### 4️⃣ Set Up Environment Variables

Duplicate the `env_example` file, rename it to `.env`

### 5️⃣ Run the Dashboard

```bash
python run_client.py
```

### 6️⃣ 🚀 Deploy with Docker

Run the following command to build and start the containers:

```bash
docker-compose up --build
```

### 7️⃣ Run test

```bash
python -m unittest discover tests
```


## 📊 About our model

### We compared several models to determine which one performed best. You can see the results in this [notebook](https://github.com/fergarcat/multiclass_prediction_obesity_risk/blob/main/server/model/prediction_model.py).

|        Model        |      Accuracy      |     Precision      |       Recall       |      F1-Score      | Train Time (s) | Overfitting |
|---------------------|--------------------|--------------------|--------------------|--------------------|----------------|-------------|
|       XGBoost       | 0.9073             | 0.9070             | 0.9073             | 0.9071             |     2.4346     |   0.0769    |
|      CatBoost       | 0.9061             | 0.9056             | 0.9061             | 0.9058             |    35.4323     |   0.0483    |
|      LightGBM       | 0.9051             | 0.9048             | 0.9051             | 0.9049             |     4.7564     |   0.0711    |
|    Random Forest    | 0.9037             | 0.9030             | 0.9037             | 0.9031             |     3.8831     |   0.0962    |
|      SVM (RBF)      | 0.8832             | 0.8822             | 0.8832             | 0.8826             |     5.1034     |   0.0137    |
|    SVM (Linear)     | 0.8697             | 0.8684             | 0.8697             | 0.8688             |     5.1625     |  -0.0029    |
| Logistic Regression | 0.8639             | 0.8624             | 0.8639             | 0.8629             |     0.7557     |  -0.0013    |
|    Decision Tree    | 0.8408             | 0.8404             | 0.8408             | 0.8404             |     0.1659     |   0.1591    |
|         KNN         | 0.7936             | 0.7906             | 0.7936             | 0.7908             |     0.2451     |   0.0574    |
|     Naive Bayes     | 0.7755             | 0.7710             | 0.7755             | 0.7691             |     0.0260     |  -0.0024    |

----

### We identified these two models as optimal.

|             Model              |      Accuracy      |     Precision      |       Recall       |      F1-Score      | Train Time (s) | Overfitting |
|--------------------------------|--------------------|--------------------|--------------------|--------------------|----------------|-------------|
|       XGBoost (Adjusted)       | 0.9053             | 0.9048             | 0.9053             | 0.9050             |     5.4682     |   0.0097    |
| Logistic Regression (Adjusted) | 0.8639             | 0.8639             | 0.8639             | 0.8633             |     0.7708     |   0.0002    |


-----

### Finally, we retrained the fastest model to reduce overfitting.

|      Model       |     Accuracy      |     Precision     |      Recall       |      F1-Score      | Train Time (s) | Overfitting |
|------------------|-------------------|-------------------|-------------------|--------------------|----------------|-------------|
| XGBoost + Optuna | 0.9118            | 0.9117            | 0.9118            | 0.9116             |     4.1328     |   0.0185    |

------

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
