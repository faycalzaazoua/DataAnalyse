import pandas as pa
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st

st.set_option('deprecation.showPyplotGlobalUse', False)

st.title('Quel est le facteur principal permettant la réussite des étudiants lors des examens ?')

st.header('Consignes :')
st.write('* Une problématique pertinente (c-a-d ou il est possible de répondre avec des données)')
st.write('* Au moins 1 diagramme avec données continues, type nuage de point ou histogramme')
st.write('* Au moins 2 diagrammes avec des données discrètes')
st.write('* 1 boîte à moustaches avec filtrage des données aberrantes sur le dataset (si il y en a)')
st.write('* 1 heat map avec matrice de corrélation (si pertinent)')
st.write('* Des commentaires clairs et pertinents pour chaque graphiques')

st.header('Les données')
a = pa.read_csv('exams.csv');
a=a.assign(Result=a.mean(axis=1,numeric_only=True))
describe = a.Result.describe()
tab = st.checkbox('Voir les données')
if tab:
    st.write(a)
    st.write('On affiche la moyenne des éleves et on vérifie ensuite lécart type pour voir si cette moyenne est fiable')
    st.write(describe)


st.header('La préparation')
bam1 = plt.figure(figsize=(7,5))
sns.boxplot(data=a, x="Result", y="test preparation course")
value = a.loc[(a['Result'] > 40)]
bam2 = plt.figure(figsize=(7,5))
sns.boxplot(data=value, x="Result", y="test preparation course")
option = st.selectbox(
    'Quel boite à moustache souhaitez-vous afficher ?',
    ('Avec les valeurs abérrantes', 'Sans les valeurs abérrantes'))
if option == 'Avec les valeurs abérrantes' :
    st.pyplot(bam1)
if option == 'Sans les valeurs abérrantes' : 
    st.pyplot(bam2)
st.write("Observation : les personnes ayant révisé sont en moyenne meilleurs sur exam que les personnes qui n'ont pas révisé et il ny a pas beaucoup de valeurs abérrantes")
fig = sns.catplot(data=value, y="Result", x="test preparation course")
st.pyplot(fig)
st.write("Il faudra ensuite étudier d'autre facteur qui pourraient influer sur ces résultat pour tirer une conclusion finale")

st.header('Les groupes ethniques')
a['race/ethnicity'] = a['race/ethnicity'].replace(to_replace=["group A","group B","group C","group D","group E"],
value=[1,2,3,4,5])
fig = sns.catplot(data=a, x="race/ethnicity", y="Result",height=7, kind='bar' )
st.pyplot(fig)
st.write('On observe que les groupes E ET D sont un peu plus performants que le reste')
st.write("Il pourrait etre interessant de voir quel groupe ethnique a le plus révisé pour ainsi mettre en relation nos deux hypotheses précedentes, si possible")

st.subheader('Groupe 5')
fig = plt.figure(figsize=(3,2))
tmp = a[a['race/ethnicity'] == 5] 
tmp['test preparation course'].value_counts()
x = [86, 45]
plt.pie(x, labels = ['Révision incomplète', 'Révision complète'], 
        normalize = True,
        autopct = lambda x: str(round(x, 2)) + '%')
st.pyplot(fig)
st.subheader('Groupe 2')
fig = plt.figure(figsize=(3,2))
tmp = a[a['race/ethnicity'] == 2] 
tmp['test preparation course'].value_counts()
x = [133, 72]
plt.pie(x, labels = ['Révision incomplète', 'Révision complète'], 
        normalize = True,
        autopct = lambda x: str(round(x, 2)) + '%')
st.pyplot(fig)
st.write("Grace à cette partie de l'étude nous pouvont voir les notes supérieurs du groupe 5 ne s'expliquent pas par le fait que le groupe révise plus que les autres")

st.header("Niveau d'études des parents")
fig = plt.figure(figsize=(10,10))
a.groupby('parental level of education').agg('mean').sort_values(by = 'Result').plot(kind='barh',figsize=(15,10))
plt.legend(bbox_to_anchor=(1.03, 1), loc = 2);
figg = fig.show(fig)
st.pyplot(figg)
st.write("On remarque effectivement que le niveau d'études des parents peut être un facteur de réussite comme le démontre le graphique ")
st.write("Cependant d'autres facteurs ne sont pas exclus, tel que le genre des étudiants ")

st.header("Le genre")
fig, ax = plt.subplots(1, 3, figsize = (20, 6))
ax1 = sns.histplot(x = a['math score'], hue = a['gender'], palette= 'plasma', ax= ax[0])
ax1 = sns.histplot(x = a['reading score'], hue = a['gender'], palette= 'plasma', ax= ax[1])
ax1 = sns.histplot(x = a['writing score'], hue = a['gender'] , palette= 'plasma', ax= ax[2])
figg=fig.show()
st.pyplot(figg)
st.write("On remarque que les hommes ont + de facilité en math et à l'inverse dans les matières")
st.write("Nous pourrions nous poser la question de savoir si les femmes révisent plus certaines matières que les hommes et inversement ?")

sns.lmplot(x='math score',y='writing score',hue='gender',data=a,markers=['x','o'],line_kws={'color': 'yellow'})
plt.xlabel('Note math')
plt.ylabel('Note écrit')
plt.title('Note math vs Note Écrit ')
with sns.axes_style('white'):
    plt.figure(figsize= (20, 8))
    sns.heatmap(a.corr(), annot = True, fmt = '.2f', linewidths= 0.8, cmap="YlGnBu")



plt.figure(figsize=(10,10))
sns.catplot(x="gender", y="math score",
                 hue="test preparation course",
                 data=a, kind="bar")

plt.title('préparatin examen - Genre & Note en Math')
fig = plt.show();
st.pyplot(fig)

plt.figure(figsize=(10,10))
sns.catplot(x="gender", y="writing score",
                 hue="test preparation course",
                 data=a, kind="bar")
plt.title('préparation examen - Genre & Note ecrit')
fig = plt.show()
st.pyplot(fig)
st.write("On peut observer que les femmes révisent plus les matières de langue que les hommes et à l'inverse les hommes révisent plus les mathématiques, on peut alors supposer que le genre peut influer sur les facilitées/préférences au niveau des matières")

st.header('Conclusion')
st.write("Après observation de nos nombreux graphiques mettant en relation nos différentes propriétés, nous pouvons répondre à notre problématique qui est : ")
st.write("Quels sont les principaux facteurs influant sur la réussite des examens des étudiants ?")

st.write("La préparation des étudiants à l’examen est donc un facteur majeur pour l’obtention de meilleurs résultat, cependant d’autres facteurs peuvent agir sur ces derniers (sans généralité) comme le genre : Pour une partie des hommes, ils ont plus de facilité ou sont plus intéressés par l’apprentissage des mathématiques à l’inverse d’une partie des femmes qui eux, sont plus performantes en matière de langues. Le niveaux d’études des parents influe aussi sur les résultats des élèves à l’inverse des groupes de population qui sont un facteur non (ou peu) influant sur la préparation et la réussite des examens pour les étudiants.")