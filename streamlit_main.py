import streamlit as st
import pandas as pd


def barre_latérale() :
    #st.sidebar.markdown("---")
    # Selection du modèle
    st.sidebar.title("A - Sélection d'un modèle")
    model_selection = st.sidebar.radio("Modèles disponibles", ("Chat", "Doc", "Expert"))

    # Paramétrage
    st.sidebar.title("B - Paramétrage du modèle")

    st.sidebar.header( "Mémoire")
    memory = st.sidebar.checkbox("sauvegarde" , True, key = "memory")

    # Checkbox
    st.sidebar.header("Paramètre 1")
    params1 = st.sidebar.columns(3)
    i= 1
    params1_values = []
    for param in params1 :
        with param :
            params1_values.append( st.checkbox(f"choix{i}") )
            i += 1
            
    st.sidebar.header("Paramètre 2")
    params2 = st.sidebar.slider('selection', 0, 200, 10)
            
    st.sidebar.header("Paramètre 3")
    params3 = st.sidebar.slider("selection d'interval" , -100 , 100 , (-6,10))

    return model_selection


# Fonction pour charger et analyser les données
def load_and_analyze_data(file):
    # Charger le fichier CSV
    df = pd.read_csv(file)
    
    # Suppression du TimeStamp
    df.drop(["Timestamp"], axis = 1, inplace = True)
    
    # Nombre Total de réponses
    st.sidebar.subheader("2 - Nombre total de réponses au Questionaire")
    st.sidebar.write(df.shape[0])
    
    # Sélectionner une colonne pour analyse
    columns = df.columns.tolist()
    st.sidebar.subheader("3 - Sélectionnez une colonne pour analyser :")
    column = st.sidebar.selectbox("", columns)
    
    # Afficher un aperçu des données
    st.sidebar.subheader("4 - Aperçu des données")
    st.sidebar.write(df.head())

    if column:
        st.sidebar.subheader(f"Analyse de la colonne : {column}")

        # Afficher les valeurs uniques et leur fréquence
        # Calcul des valeurs uniques et des fréquences
        unique_values = df[column].value_counts()
        percentages = df[column].value_counts(normalize=True) * 100  # Normaliser pour obtenir les pourcentages

        # Créer un DataFrame avec les fréquences et les pourcentages
        result = pd.DataFrame({ 'Fréquence': unique_values,
                                'Pourcentage (%)': percentages
                              })

        # Afficher le tableau avec les fréquences et les pourcentages
        st.subheader("**Valeurs uniques, leur fréquence et pourcentage associé :**")
        st.write(result)

        # Si la colonne est numérique, afficher des statistiques descriptives
        if pd.api.types.is_numeric_dtype(df[column]):
            st.subheader("**Statistiques descriptives :**")
            st.write(df[column].describe())
        else:
            # Longueur moyenne des réponses textuelles si la colonne est textuelle
            avg_length = df[column].astype(str).apply(len).mean()
            st.subheader(f"**Longueur moyenne des réponses textuelles :** {avg_length:.2f} caractères")

        # Visualisation de la distribution des valeurs
        st.subheader("Visualisation des valeurs")
        st.bar_chart(unique_values)

# Interface utilisateur
st.title("Analyse des données du sondage 'Enquête légumes d'Afrique'")

# Permettre à l'utilisateur de télécharger un fichier CSV
st.sidebar.title("1 - Cliquer ici Pour charger le fichier à analyser : ")
uploaded_file = st.sidebar.file_uploader("", type=["csv"])

if uploaded_file:
    # Analyser les données une fois le fichier téléchargé
    load_and_analyze_data(uploaded_file)

