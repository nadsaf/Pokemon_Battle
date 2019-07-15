import pandas as pd
import numpy as np

pokemon = pd.read_csv('pokemon.csv')
pokemon = pokemon.drop(['Type 1', 'Type 2', 'Generation', 'Legendary'], axis=1)
pokemon = pokemon.rename(columns={'#' : 'id'})

combat = pd.read_csv('combats.csv')
print(combat)

merged1 = combat.merge(pokemon, how = "left", left_on = "First_pokemon", right_on = "id")
merged2 = combat.merge(pokemon, how = "left", left_on = "Second_pokemon", right_on = "id")

merged2.drop(["Winner","First_pokemon","Second_pokemon"], axis = 1, inplace = True)

for i in merged2.columns : 
    merged2.rename(columns = {i : i + "_2"}, inplace = True)

df_combat = pd.concat([merged1,merged2], axis = 1)
# print(df_combat)
df_combat['is_firstwin'] = 0
df_combat.loc[df_combat['Winner'] == df_combat['First_pokemon'], 'is_firstwin'] = 1
# print(df_combat)

#========================================================================================
X = df_combat.drop(['First_pokemon', 'Second_pokemon', 'Winner', 'id', 'id_2', 'Name', 'Name_2', 'is_firstwin'], axis=1)
Y = df_combat['is_firstwin']

#========================================================================================
from sklearn.ensemble import GradientBoostingClassifier
model = GradientBoostingClassifier()
model.fit(X, Y)
print(model.score(X,Y))
print(model.predict_proba(X.iloc[0].values.reshape(1,-1)))

#===========================================================
pokemon1 = 'pikachu'
pokemon2 = 'bulbasaur'

data1 = pokemon[pokemon['Name'] == pokemon1.capitalize()][['HP','Attack', 'Defense', 'Sp. Atk', 'Sp. Def', 'Speed']].values.tolist()
data2 = pokemon[pokemon['Name'] == pokemon2.capitalize()][['HP','Attack', 'Defense', 'Sp. Atk', 'Sp. Def', 'Speed']].values.tolist()

input_data = data1[0]
input_data.extend(data2[0])
print(data1[0])
print(data2[0])

print(input_data)
prediksi = model.predict([input_data])[0]
print(model.predict_proba([input_data])[0][0]*100)
print(prediksi)
# import joblib
# joblib.dump([pokemon, model], 'modelpokemon')

