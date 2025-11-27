# 🎥 YouTube Sentiment Analyzer  
**Analyse de sentiment des commentaires YouTube en temps réel**  
Projet MLOps complet – INDIA 2025/26  

---

## 📌 Description du projet
YouTube Sentiment Analyzer est une solution **MLOps** qui permet d’extraire, d’analyser et de visualiser automatiquement le **sentiment** (positif, neutre, négatif) des commentaires sous n’importe quelle vidéo YouTube.  
Le workflow complet est couvert : collecte de données, entraînement de modèle, API cloud, extension Chrome et déploiement Docker sur Hugging Face Spaces.

---

## 🏗️ Architecture technique

| Composant              | Technologie / Outil                                  | Rôle principal                                      |
|------------------------|------------------------------------------------------|-----------------------------------------------------|
| **Données**            | Dataset Reddit Sentiment (CSV)                      | Entraînement du modèle                              |
| **Pré-traitement**     | Python, pandas, regex, emoji                        | Nettoyage, suppression URLs, mentions, emojis…      |
| **Modèle ML**          | scikit-learn – TF-IDF + Logistic Regression         | Classification 3 classes (-1, 0, 1)                 |
| **API REST**           | FastAPI, Pydantic, Uvicorn                          | Endpoints `/health` & `/predict_batch`              |
| **Containerisation**   | Docker, python:3.10-slim                            | Image légère & reproductible                        |
| **Cloud**              | Hugging Face Spaces                                 | Hébergement gratuit + HTTPS                         |
| **Extension Chrome**   | Manifest V3, content-script, popup HTML/JS/CSS      | Injection dans page YouTube, appel API, stats temps réel |
| **Versioning**         | Git + GitHub                                        | CI/CD simple (push-to-deploy)                       |

**Flux de données simplifié :**
1. Extension Chrome → extraction des commentaires visibles  
2. Envoi batch à l’API HF Spaces  
3. Retour des prédictions + stats (%, répartition)  
4. Affichage dans popup avec filtres & dark-mode

---

## 🚀 Instructions d’installation et d’utilisation

### 0. Prérequis
- Python ≥ 3.10  
- Google Chrome (dernière version)  
- Compte [Hugging Face](https://huggingface.co/join)  
- Git installé

---

### 1. Cloner le repository
```bash
git clone https://github.com/Charbel491/youtube-sentiment-analyzer-2.git
cd youtube-sentiment-analyzer-2
```
---

### 2. Environnement Python
```bash
python -m venv venv
source venv/bin/activate        # Windows : venv\Scripts\activate
pip install -r requirements.txt # dev ou requirements-prod.txt
```

### 3. Tester l’API localement
```bash
uvicorn src.api.app:app --reload --port 8000
```
Visiter :
- [http://localhost:8000/health](http://localhost:8000/health)
- POST [http://localhost:8000/predict_batch](http://localhost:8000/predict_batch)  
  Body JSON :
  ```json
  {"comments": ["I love this video!", "Worst tutorial ever"]}
  ```

  ### 4. Installer l’extension Chrome
1. Ouvrir Chrome → `chrome://extensions/`  
2. Activer **Mode développeur**  
3. **Charger l’extension non empaquetée** → sélectionner le dossier `chrome-extension/`  
4. Ouvrir une vidéo YouTube → icône apparaît dans la barre d’outils  
5. Cliquer → **Analyse des sentiments** lancée automatiquement

---

## 📊 Performance
| Métrique          | Valeur |
|-------------------|--------|
| Accuracy          | 84 %   |
| F1-score macro    | 0.81   |
| Temps inférence 50 comments | ≈ 80 ms |

---

## 📄 Licence & crédits
Dataset : Reddit Sentiment (open-source)  
Icons : Heroicons  
Police : Inter  

---

**Made by Charbel – INDIA 2025/26**  
