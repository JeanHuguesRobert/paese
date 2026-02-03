import streamlit as st
import pandas as pd

st.set_page_config(page_title="Pacte Voltaire", layout="wide")

# --- STYLE CSS ---
st.markdown("""<style> .main { background-color: #f8f9fa; } .stMetric { background-color: #ffffff; padding: 20px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); } </style>""", unsafe_allow_html=True)

st.title("🏛️ Pacte Voltaire : Reprenez le contrôle")

# --- ENTRÉES ---
with st.sidebar:
    st.header("📍 Ma situation actuelle")
    valeur_maison = st.number_input("Valeur de la maison visée (€)", value=200000)
    loyer_ville = st.slider("Loyer/Crédit ville actuel (€)", 0, 2000, 900)
    taxe_village = st.number_input("Taxe Résidence Secondaire (Annuel €)", value=1200)
    factures = st.slider("Électricité + Carburant mensuel (€)", 0, 600, 350)

# --- CALCULS ---
# 1. Gain mensuel
cout_actuel = loyer_ville + (taxe_village / 12) + factures
cout_voltaire = loyer_ville * 0.2  # Le touriste paie 80% du loyer urbain
gain_mensuel = cout_actuel - cout_voltaire

# 2. Gain à l'achat (BRS)
prix_achat_voltaire = valeur_maison * 0.7

# --- AFFICHAGE ---
tab1, tab2 = st.tabs(["📊 Mon Budget", "📈 Ma Revente"])

with tab1:
    st.subheader("Bilan du Pouvoir d'Achat")
    c1, c2, c3 = st.columns(3)
    c1.metric("Budget Actuel", f"{int(cout_actuel)} €")
    c2.metric("Budget Voltaire", f"{int(cout_voltaire)} €", f"-{int(gain_mensuel)} €")
    c3.metric("Gain Annuel", f"{int(gain_mensuel * 12)} €", "Net d'impôts")

    # Graphique
    chart_data = pd.DataFrame({
        "Statut": ["Actuel", "Voltaire"],
        "Logement": [loyer_ville, cout_voltaire],
        "Énergie/Taxes": [(taxe_village/12) + factures, 0]
    })
    st.bar_chart(chart_data.set_index("Statut"), color=["#FF4B4B", "#2E7D32"])

with tab2:
    st.subheader("Simulation de Revente (Clause Anti-Spéculation)")
    hausse_marche = st.slider("Hausse du marché sur 10 ans (%)", 0, 50, 20)
    
    valeur_future_marche = valeur_maison * (1 + hausse_marche/100)
    plus_value_brute = valeur_future_marche - prix_achat_voltaire
    part_famille = prix_achat_voltaire + (plus_value_brute * 0.7)
    part_scic = plus_value_brute * 0.3
    
    col_a, col_b = st.columns(2)
    col_a.write(f"**Prix d'achat (BRS -30%) :** {int(prix_achat_voltaire)} €")
    col_a.write(f"**Prix de revente Voltaire :** {int(part_famille)} €")
    col_b.info(f"Le village récupère **{int(part_scic)} €** pour aider la prochaine famille à s'installer.")

st.success(f"En devenant Résident Voltaire, vous vivez avec **{int(gain_mensuel)} €** de plus par mois tout en protégeant le patrimoine du village.")
