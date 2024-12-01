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
    st.sidebar.subheader("Nombre total de réponses au Questionaire")
    st.sidebar.write(df.shape[0])
    
    # Afficher un aperçu des données
    st.sidebar.subheader("Aperçu des données")
    st.sidebar.write(df.head())

    # Sélectionner une colonne pour analyse
    columns = df.columns.tolist()
    column = st.sidebar.selectbox("Sélectionnez une colonne pour analyser :", columns)

    if column:
        st.subheader(f"Analyse de la colonne : {column}")

        # Afficher les valeurs uniques et leur fréquence
        unique_values = df[column].value_counts()
        st.write("**Valeurs uniques et leur fréquence :**")
        st.write(unique_values)

        # Si la colonne est numérique, afficher des statistiques descriptives
        if pd.api.types.is_numeric_dtype(df[column]):
            st.write("**Statistiques descriptives :**")
            st.write(df[column].describe())
        else:
            # Longueur moyenne des réponses textuelles si la colonne est textuelle
            avg_length = df[column].astype(str).apply(len).mean()
            st.write(f"**Longueur moyenne des réponses textuelles :** {avg_length:.2f} caractères")

        # Visualisation de la distribution des valeurs
        st.subheader("Visualisation des valeurs")
        st.bar_chart(unique_values)

# Interface utilisateur
st.title("Analyse des données du sondage")

# Permettre à l'utilisateur de télécharger un fichier CSV
uploaded_file = st.sidebar.file_uploader("Téléchargez un fichier CSV", type=["csv"])

if uploaded_file:
    # Analyser les données une fois le fichier téléchargé
    load_and_analyze_data(uploaded_file)

