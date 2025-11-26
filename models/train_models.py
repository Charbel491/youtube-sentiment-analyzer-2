import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score, f1_score
from sklearn.model_selection import GridSearchCV
import joblib
import seaborn as sns
import matplotlib.pyplot as plt

def load_data():
    train_df = pd.read_csv('data/processed/train.csv')
    test_df = pd.read_csv('data/processed/test.csv')
    return train_df['text'], train_df['label'], test_df['text'], test_df['label']

def train_model():
    X_train, y_train, X_test, y_test = load_data()

    # 🔧 Nettoyage des valeurs manquantes
    X_train = X_train.dropna()
    y_train = y_train.loc[X_train.index]
    X_test = X_test.dropna()
    y_test = y_test.loc[X_test.index]


    # Vectorisation TF-IDF
    tfidf = TfidfVectorizer(max_features=10000, ngram_range=(1,2), stop_words='english')
    X_train_tfidf = tfidf.fit_transform(X_train)
    X_test_tfidf = tfidf.transform(X_test)

    # Recherche d'hyperparamètres
    param_grid = {
        'C': [0.1, 1, 10],
        'penalty': ['l2'],
        'solver': ['liblinear']
    }
    model = LogisticRegression(max_iter=1000)
    grid = GridSearchCV(model, param_grid, cv=5, scoring='f1_macro', n_jobs=-1)
    grid.fit(X_train_tfidf, y_train)

    best_model = grid.best_estimator_
    y_pred = best_model.predict(X_test_tfidf)

    # Évaluation
    print("✅ Meilleurs paramètres :", grid.best_params_)
    print("Accuracy :", accuracy_score(y_test, y_pred))
    print("F1-score macro :", f1_score(y_test, y_pred, average='macro'))
    print("\nRapport de classification :\n", classification_report(y_test, y_pred))

    # Matrice de confusion
    cm = confusion_matrix(y_test, y_pred)
    plt.figure(figsize=(6, 4))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=['-1', '0', '1'], yticklabels=['-1', '0', '1'])
    plt.title("Matrice de confusion")
    plt.xlabel("Prédit")
    plt.ylabel("Réel")
    plt.savefig('./confusion_matrix.png')
    plt.show()

    # Sauvegarde
    joblib.dump(tfidf, './src/models/tfidf_vectorizer.joblib')
    joblib.dump(best_model, './src/models/logistic_model.joblib')
    print("✅ Modèle et vectoriseur sauvegardés dans `models/`")

if __name__ == '__main__':
    train_model()