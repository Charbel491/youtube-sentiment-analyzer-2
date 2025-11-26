import pandas as pd
import re
import emoji

def clean_text(text):
    # Suppression des URLs
    text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
    # Suppression des mentions @user
    text = re.sub(r'@\w+', '', text)
    # Suppression des caractères spéciaux et chiffres
    text = re.sub(r'[^A-Za-z\s]', '', text)
    # Suppression des emojis
    text = emoji.replace_emoji(text, replace='')
    # Normalisation des espaces
    text = re.sub(r'\s+', ' ', text).strip()
    return text.lower()

def main():
    # Charger le dataset brut
    df = pd.read_csv('./data/raw/reddit.csv')

    # Renommer les colonnes si nécessaire
    df.columns = ['text', 'label']

    # Nettoyer les commentaires
    df['text'] = df['text'].astype(str).apply(clean_text)

    # Supprimer les lignes vides
    df = df[df['text'].str.len() > 0]

    # Sauvegarder le dataset nettoyé
    df.to_csv('./data/processed/reddit_clean.csv', index=False)
    print("✅ Dataset nettoyé sauvegardé dans data/processed/reddit_clean.csv")

if __name__ == '__main__':
    main()