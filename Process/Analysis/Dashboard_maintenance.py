import pandas as pd



AnlassTyp_path = '../../Data/Processed/4.2_Arbeitsaufträge.csv'
resultBoth_Path = '../../Data/Processed/results_Both.csv'

df_AnlassTyp = pd.read_csv(AnlassTyp_path, encoding='latin1')
df= pd.read_csv(resultBoth_Path)

new_df = df[['fahrzeugtyp', 'plate', 'lifetime', 'costs', 'year']]
#new_df.loc[:, 'Paragraph57'] = None
#new_df.loc[:, 'Korrektiv'] = None
#new_df.loc[:, 'Präventiv'] = None


#delete sub maintenance tasks
df_AnlassTyp["Year"] = pd.to_datetime(df_AnlassTyp["Erstell-datum"], format="%m/%d/%Y").dt.year
df_AnlassTyp = df_AnlassTyp[df_AnlassTyp["GFNr"].str[-4:] == df_AnlassTyp["Year"].astype(str)]

#frequency
grouped_data = df_AnlassTyp.groupby(['Los/IDMK', 'Year'])['AnlassTyp'].value_counts().reset_index(name='frequency')

grouped_data = grouped_data[
    (grouped_data["AnlassTyp"] == "korrektiv") |
    (grouped_data["AnlassTyp"] == "UNFALL") |
    (grouped_data["AnlassTyp"] == "Jahresservice & §57a") |
    (grouped_data["AnlassTyp"] == "präventiv") |
    (grouped_data["AnlassTyp"] == "Jahresservice") |
    (grouped_data["AnlassTyp"] == "KFG§57A")
]

# Change categories to 3 korrektiv, Jahresservice, präventiv
grouped_data["AnlassTyp"] = grouped_data["AnlassTyp"].replace({
    "KFG§57A": "Jahresservice",
    "Jahresservice & §57a": "Jahresservice",
    "UNFALL": "korrektiv"
})


df_new = grouped_data.groupby(['Los/IDMK', 'Year', 'AnlassTyp'])['frequency'].sum().reset_index(name='frequency')


print(df_new )




# Pivot the table to create separate columns for "korrektiv," "Jahresservice," and "Preventive"
pivot_table = df_new.pivot_table(
    index=["Los/IDMK", "Year"],
    columns="AnlassTyp",
    values="frequency",
    fill_value=0
).reset_index()

# Rename the columns
pivot_table.columns.name = None
pivot_table = pivot_table.rename(columns={
    "korrektiv": "korrektiv",
    "Jahresservice": "Jahresservice",
    "präventiv": "präventiv"
})


print(pivot_table)

output_path = '../../Output/data/AnlassTyp_freq.csv'
pivot_table .to_csv(output_path, index=False)
