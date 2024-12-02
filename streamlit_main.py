###################################################################################################################
###################################################################################################################
import streamlit as st
import pandas as pd


###################################################################################################################
###################################################################################################################
# Fonction pour charger et analyser les données
def load_and_analyze_data( ):
    sheet_name = "Enquete_legumes_d_Afrique" # replace with your own sheet name
    sheet_id = '1tjN9K9KeY5Eb6G3J-IFJ5HUmZQuGjZh9ZvT-hZUMpF8' # replace with your sheet's ID
    url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}"

    # Charger le fichier CSV
    df = pd.read_csv(url)
    
    # Suppression du TimeStamp
    df.drop(["Timestamp"], axis = 1, inplace = True)
    
    # Nombre Total de réponses
    st.sidebar.subheader(f"2 -   Nombre total de réponses au Questionaire:   {df.shape[0]}")
    
    # Sélectionner une colonne pour analyse
    columns = df.columns.tolist()
    st.sidebar.subheader("3 -   Sélectionnez une colonne pour analyser :")
    column = st.sidebar.selectbox("", columns)
    
    # Afficher un aperçu des données
    st.sidebar.subheader("4 -   Aperçu des données")
    st.sidebar.dataframe(df.head())

    if column:
        st.subheader(f"I -   **Analyse de la colonne : {column}**")

        # Afficher les valeurs uniques et leur fréquence
        # Calcul des valeurs uniques et des fréquences
        unique_values = df[column].value_counts()
        percentages = df[column].value_counts(normalize=True) * 100  # Normaliser pour obtenir les pourcentages

        # Créer un DataFrame avec les fréquences et les pourcentages
        result = pd.DataFrame({ 'Fréquence': unique_values,
                                'Pourcentage (%)': percentages
                              })

        # Afficher le tableau avec les fréquences et les pourcentages
        st.subheader("II -   **Valeurs uniques, leur fréquence et pourcentage associé :**")
        st.dataframe(result)

        # Si la colonne est numérique, afficher des statistiques descriptives
        if pd.api.types.is_numeric_dtype(df[column]):
            st.subheader("III -   **Statistiques descriptives :**")
            st.write(df[column].describe())
        else:
            pass
            # Longueur moyenne des réponses textuelles si la colonne est textuelle
            #avg_length = df[column].astype(str).apply(len).mean()
            #st.subheader(f"III -   **Longueur moyenne des réponses textuelles :** {avg_length:.2f} caractères")

        # Visualisation de la distribution des valeurs
        st.subheader("III -  Visualisation des valeurs")
        st.bar_chart(unique_values )


###################################################################################################################
###################################################################################################################
# Interface utilisateur
st.title("Analyse des données du sondage 'Enquête légumes d'Afrique'")


# Permettre à l'utilisateur de télécharger un fichier CSV
st.sidebar.title("1 -   Le fichier Analalysé est directement chargé depuis GoogleSheet : ")
    
# Analyser les données une fois le fichier téléchargé
load_and_analyze_data( )

