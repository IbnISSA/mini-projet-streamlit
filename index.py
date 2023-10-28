# Les imports
import streamlit as st
import plotly.express as px
import pandas as pd

################################################################
st.title(':bar_chart: Dashboard :bar_chart:')
@st.cache_data(ttl=3600, max_entries=100)
def load_data():
    df = pd.read_csv("donnees_ventes_etudiants.csv", low_memory=False,)
    return df
df = load_data()
# coord = pd.read_excel('coord.xlsx')

# Permettre à la colonne 'order_date' d'être converti en Date
df['order_date'] = pd.to_datetime(df['order_date'])

# On remplace la colonne country avec le bon nom
df.rename(columns={'County': 'Country'}, inplace=True)

# Création de la colonne State Complet
df['State Complet'] = df['State'].replace(
    {
        'AL': 'Alabama',
        'AK': 'Alaska',
        'AZ': 'Arizona',
        'AR': 'Arkansas',
        'CA': 'California',
        'CO': 'Colorado',
        'CT': 'Connecticut',
        'DC': 'District of Columbia',
        'DE': 'Delaware',
        'FL': 'Florida',
        'GA': 'Georgia',
        'HI': 'Hawaii',
        'ID': 'Idaho',
        'IL': 'Illinois',
        'IN': 'Indiana',
        'IA': 'Iowa',
        'KS': 'Kansas',
        'KY': 'Kentucky',
        'LA': 'Louisiana',
        'ME': 'Maine',
        'MD': 'Maryland',
        'MA': 'Massachusetts',
        'MI': 'Michigan',
        'MN': 'Minnesota',
        'MS': 'Mississippi',
        'MO': 'Missouri',
        'MT': 'Montana',
        'NE': 'Nebraska',
        'NV': 'Nevada',
        'NH': 'New Hampshire',
        'NJ': 'New Jersey',
        'NM': 'New Mexico',
        'NY': 'New York',
        'NC': 'North Carolina',
        'ND': 'North Dakota',
        'OH': 'Ohio',
        'OK': 'Oklahoma',
        'OR': 'Oregon',
        'PA': 'Pennsylvania',
        'RI': 'Rhode Island',
        'SC': 'South Carolina',
        'SD': 'South Dakota',
        'TN': 'Tennessee',
        'TX': 'Texas',
        'UT': 'Utah',
        'VT': 'Vermont',
        'VA': 'Virginia',
        'WA': 'Washington',
        'WV': 'West Virginia',
        'WI': 'Wisconsin',
        'WY': 'Wyoming',
    })

# Pour faciliter la tâche sur les dates
min_date = pd.to_datetime(df["order_date"]).min()
max_date = pd.to_datetime(df['order_date']).max()

# 1 : Le calendrier pour permettre à l’utilisateur le choix d’indiquer la période de vente choisie
col1, col2, col3 = st.columns(3)
with col1:
    start_date = pd.to_datetime(st.date_input(
        "Date de début : ", value=min_date, min_value=min_date, max_value=max_date))
with col2:
    end_date = pd.to_datetime(st.date_input(
        "Date de fin : ", value=max_date, min_value=min_date, max_value=max_date))
# On filtre les données en fonction des dates sélectionnées
df = df[(df['order_date'] >= start_date) & (df['order_date'] <= end_date)].copy()

# Les Filtres
st.sidebar.subheader('Choisissez votre filtre : ')

# Filtrage par Région
regions = df['Region'].sort_values().unique()
selected_region = st.sidebar.multiselect('Région', regions)
if not selected_region:
    regions = df.copy()
else:
    regions = df[df["Region"].isin(selected_region)]

# Filtrage par State en fonction de la Région sélectionnée
states = regions['State Complet'].sort_values().unique()
selected_state = st.sidebar.multiselect('État', states)
if not selected_state:
    states = regions.copy()
else:
    states = regions[regions['State Complet'].isin(selected_state)]

# Filtrage par Country
countries = states['Country'].sort_values().unique()
selected_country = st.sidebar.multiselect('Province', countries)
if not selected_country:
    countries = states.copy()
else:
    countries = states[states['Country'].isin(selected_country)]

# Filtrage par City
cities = countries['City'].sort_values().unique()
selected_city = st.sidebar.multiselect('Ville', cities)
if not selected_city:
    cities = countries.copy()
else:
    cities = countries[countries['City'].isin(selected_city)]

# Filtrage par Statut
status = cities['status'].sort_values().unique()
selected_status = st.sidebar.multiselect('Statut', status)
if not selected_status:
    status = cities.copy()
else:
    status = cities[cities['status'].isin(selected_status)]

# Filtrer les données en fonction des sélections
filtered_df = status[
    (status['Region'].isin(selected_region)) |
    (status['State Complet'].isin(selected_state)) |
    (status['Country'].isin(selected_country)) |
    (status['City'].isin(selected_city)) |
    (status['status'].isin(selected_status))
]

#Obtention des ventes par categories
category_df = filtered_df.groupby(by=["category"], as_index=False)[
    "total"].sum().round(2)
category_df0 = df.groupby(by=["category"], as_index=False)[
    "total"].sum().round(2)

# Indicateurs ou KPI sous format de valeur numérique:
# Nombre Total de Ventes
if not filtered_df.empty:
    total_sales = filtered_df['total'].sum().round(2)
    total_sales_df = df['total'].sum().round(2)
    delta = total_sales - total_sales_df
else:
    total_sales_df = df['total'].sum().round(2)
    delta = 0

# Nombre distincts de client
if not filtered_df.empty:
    cust_dist = filtered_df['cust_id'].nunique()
    cust_dist_df = df['cust_id'].nunique()
    delta_cust_dist = cust_dist - cust_dist_df
else:
    cust_dist_df = df['cust_id'].nunique()
    delta_cust_dist = 0

# Nombre Total de commandes
if not filtered_df.empty:
    total_orders = filtered_df['order_id'].nunique()
    total_orders_df = df['order_id'].nunique()
    delta_total_orders = total_orders - total_orders_df
else:
    total_orders_df = df['order_id'].nunique()
    delta_total_orders = 0

# Ajout des KPI avec st.metric
ntv, ndc, ntc = st.columns(3)
if not filtered_df.empty:
    with ntv:
        st.metric(
            label='Nombre Total de Ventes',
            value=total_sales,
            delta=delta.round(2),
        )
    with ndc:
        st.metric(
            label='Nombre distinct de Client',
            value=cust_dist,
            delta=delta_cust_dist,
        )
    with ntc:
        st.metric(
            label='Nombre Total de Commandes',
            value=total_orders,
            delta=delta_total_orders,
        )
else:
    with ntv:
        st.metric(
            label='Nombre Total de Ventes',
            value=total_sales_df,
        )
    with ndc:
        st.metric(
            label='Nombre distinct de Client',
            value=cust_dist_df,
        )
    with ntc:
        st.metric(
            label='Nombre Total de Commandes',
            value=total_orders_df,
        )
# Les diagrammes
db, dc = st.columns(2)
# Diagramme en barre qui calcule le nombre total de vente suivant la catégorie (Category)
with db:
    if not filtered_df.empty:
        st.subheader("Ventes par Catégories")
        fig1 = px.bar(category_df, x="category", y="total", text=['${:,.2f}'.format(x) for x in category_df["total"]],
                     template="seaborn")
        st.plotly_chart(fig1, height=200)
    else:
        st.subheader("Ventes par Catégories")
        fig1 = px.bar(category_df0, x="category", y="total", text=['${:,.2f}'.format(x) for x in category_df0["total"]],
                     template="seaborn")
        st.plotly_chart(fig1, height=200)
# Diagramme circulaire qui calcule le pourcentage du nombre total de vente suivant la Région
with dc:
    if not filtered_df.empty:
        st.subheader("Ventes par Régions")
        fig2 = px.pie(filtered_df, values="total", names="Region", hole=0.5)
        fig2.update_traces(text=filtered_df["Region"], textposition="inside")
        st.plotly_chart(fig2, height=200)
    else:
        st.subheader("Ventes par Régions")
        fig2 = px.pie(df, values="total", names="Region", hole=0.5)
        fig2.update_traces(text=df["Region"], textposition="inside")
        st.plotly_chart(fig2, height=200)

# Diagramme en barre permettant de savoir le TOP 10 des meilleurs clients en vous servant de la variable Full_name
with db:
    if not filtered_df.empty:
        st.subheader("TOP 10 des meilleurs clients")
        fig3 = px.bar(filtered_df.sort_values("total", ascending=False).head(
            10), x="full_name", y="total", template="seaborn")
        st.plotly_chart(fig3, height=200)
    else:
        st.subheader("TOP 10 des meilleurs clients")
        fig3 = px.bar(df.sort_values("total", ascending=False).head(
            10), x="full_name", y="total", template="seaborn")
        st.plotly_chart(fig3, height=200)


# Un histogramme qui donne la répartition de l’âge des clients :
with dc:
    if not filtered_df.empty:
        fig4 = px.histogram(
            filtered_df, x="age", title="Répartition de l'âge des clients", template="seaborn")
        st.plotly_chart(fig4, height=200)
    else:
        fig4 = px.histogram(
            df, x="age", title="Répartition de l'âge des clients", template="seaborn")
        st.plotly_chart(fig4, height=200)

# Diagramme en barre qui compte le nombre d’hommes (+pourcentage) et de femmes
filtered_df["Percentage"] = filtered_df["total"] / filtered_df["total"].sum() * 100
df["Percentage"] = df["total"] / df["total"].sum() * 100

if not filtered_df.empty:
    st.subheader("Nombre d'hommes et de femmes en pourcentage")
    fig5 = px.bar(filtered_df, x="Gender", y="Percentage", template="seaborn")
# Ajout d'un labelle "Percentage" au diagramme
    fig5.update_layout(yaxis_title="Percentage (%)")
    st.plotly_chart(fig5, height=200)
else:
    st.subheader("Nombre d'hommes et de femmes en pourcentage")
    fig5 = px.bar(df, x="Gender", y="Percentage", template="seaborn")
# Ajout d'un labelle "Percentage" au diagramme
    fig5.update_layout(yaxis_title="Percentage (%)")
    st.plotly_chart(fig5, height=200)

#Tracer la courbe qui donne le nombre total de Vente suivant le mois. Pour ce faire, il faudrait faire un group By par mois-année et calculer le nombre total de Vente par mois-année
if not filtered_df.empty:
    filtered_df["month_year"] = filtered_df["order_date"].dt.to_period("M")
    st.subheader('Courbe du nombre de ventes par mois')
    linechart = pd.DataFrame(filtered_df.groupby(filtered_df["month_year"].dt.strftime("%Y : %b"))["total"].sum()).reset_index()
    fig6 = px.line(linechart, x = "month_year", y="total", labels = {"Ventes": "Montant"},height=500, width = 1000,template="gridon")
    st.plotly_chart(fig6,use_container_width=True, height=200)
else:
    df["month_year"] = df["order_date"].dt.to_period("M")
    st.subheader('Courbe du nombre de ventes par mois')
    linechart = pd.DataFrame(df.groupby(df["month_year"].dt.strftime("%Y : %b"))["total"].sum()).reset_index()
    fig6 = px.line(linechart, x = "month_year", y="total", labels = {"Ventes": "Montant"},height=500, width = 1000,template="gridon")
    st.plotly_chart(fig6,use_container_width=True, height=200)

# #Calcul du nombre total de vente par State en mettant en place une carte
# if not filtered_df.empty:
#     filtered_df = filtered_df.merge(coord, how="left", left_on="State Complet", right_on="State Complet")
#     # Calcul du nombre de ventes par État
#     data_by_state = filtered_df.groupby("State Complet")["total"].sum()
    
#     data_by_state.rename(columns={"State Complet": "locations"}, inplace=True)
#     # Création de la carte
#     fig7 = px.choropleth(data_by_state, locations="State Complet", color="total", hover_data=["total"], color_continuous_scale="YlOrRd")
#     fig7.update_layout(margin=dict(l=0, r=0, t=0, b=0))
#     st.plotly_chart(fig7)
# else:
#     df = df.merge(coord, how="left", left_on="State Complet", right_on="State Complet")
#     # Calcul du nombre de ventes par État
#     data_by_state = df.groupby("State Complet")["total"].sum()
#     # Création de la carte
#     fig7 = px.choropleth(data_by_state, locations="State Complet", color="total", hover_data=["total"], color_continuous_scale="YlOrRd")
#     fig7.update_layout(margin=dict(l=0, r=0, t=0, b=0))
#     st.plotly_chart(fig7)