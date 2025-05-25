import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.decomposition import PCA
import os
import io
import base64

EDA_DATA_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "data", "eda", "final_dataset.csv")

def generate_eda_plot(new_data: dict):
    data = pd.read_csv(EDA_DATA_PATH)
    num_cols = data.select_dtypes(include=np.number).columns.tolist()

    le = LabelEncoder()
    y = le.fit_transform(data['NObeyesdad'])

    scaler = StandardScaler()
    pca = PCA(n_components=2)

    scaled = scaler.fit_transform(data[num_cols])
    pca_data = pca.fit_transform(scaled)

    # Insertar el nuevo punto
    new_point_scaled = scaler.transform([list(new_data.values())])
    new_point_pca = pca.transform(new_point_scaled)[0]

    df_plot = pd.DataFrame({
        "PC1": pca_data[:, 0],
        "PC2": pca_data[:, 1],
        "class": le.inverse_transform(y)
    })

    fig, ax = plt.subplots(figsize=(6, 5))
    sns.scatterplot(data=df_plot, x="PC1", y="PC2", hue="class", palette="tab10", alpha=0.6, ax=ax)
    ax.scatter(new_point_pca[0], new_point_pca[1], color="black", s=100, label="Paciente")
    ax.legend(bbox_to_anchor=(1, 1))
    ax.set_title("Proyección PCA - Grupos vs. Paciente")

    # Guardar en base64
    buf = io.BytesIO()
    plt.tight_layout()
    fig.savefig(buf, format="png")
    plt.close(fig)
    buf.seek(0)

    encoded = base64.b64encode(buf.read()).decode("utf-8")
    return f"data:image/png;base64,{encoded}"
