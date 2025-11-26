import pandas as pd
from sklearn.model_selection import train_test_split

def main():
    # Charger le dataset nettoyé
    df = pd.read_csv('./data/processed/reddit_clean.csv')

    # Scinder en train/test avec stratification (équilibrage des classes)
    train_df, test_df = train_test_split(
        df,
        test_size=0.25,
        random_state=42,
        stratify=df['label']
    )

    # Sauvegarder les fichiers
    train_df.to_csv('./data/processed/train.csv', index=False)
    test_df.to_csv('./data/processed/test.csv', index=False)

    print(f"✅ Train/Test split terminé :")
    print(f"   - Train : {len(train_df)} lignes")
    print(f"   - Test  : {len(test_df)} lignes")

if __name__ == '__main__':
    main()