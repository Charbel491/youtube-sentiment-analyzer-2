import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def main():
    df = pd.read_csv('./data/processed/reddit_clean.csv')

    # Distribution des classes
    print("Distribution des labels :")
    print(df['label'].value_counts())

    # Longueur des textes
    df['text_length'] = df['text'].str.len()
    print("Statistiques de longueur des textes :")
    print(df['text_length'].describe())

    # Visualisation
    sns.countplot(x='label', data=df)
    plt.title('Distribution des sentiments')
    plt.savefig('./label_distribution.png')
    plt.show()

if __name__ == '__main__':
    main()