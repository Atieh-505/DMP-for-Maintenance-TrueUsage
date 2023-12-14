import pandas as pd



Sparepart_path = '../../Data/Processed/Sparepart.csv'
resultBoth_Path = '../../Data/Processed/results_Both.csv'

df = pd.read_csv(Sparepart_path, encoding='ISO-8859-1')
df_fahrzeugtyp= pd.read_csv(resultBoth_Path)



# Group data based on the "plate number" column and count the frequency of each value 
grouped_data = df.groupby('PNumber')['spare_part'].value_counts().reset_index(name='frequency')


#add fahrzeugtyp
grouped_data['fahrzeugtyp']=None

for i in grouped_data['PNumber'].unique():
    if i in df_fahrzeugtyp['plate'].values:
        fahrzeugtyp_value = df_fahrzeugtyp.loc[df_fahrzeugtyp['plate'] == i, 'fahrzeugtyp'].values
        if len(fahrzeugtyp_value) > 0:
            # Update the 'fahrzeugtyp' column in 'grouped_data' where 'PNumber' matches 'i'
            grouped_data.loc[grouped_data['PNumber'] == i, 'fahrzeugtyp'] = fahrzeugtyp_value[0]

#delete luft
grouped_data = grouped_data[(grouped_data["spare_part"] != "luft")]


print((grouped_data))


output_path1 = '../../Output/data/SP_freq_UNIMOG.csv'
grouped_data.to_csv(output_path1, index=False)


#data for first page(General dashboard) 10 most repeted
df_general = grouped_data.groupby(['fahrzeugtyp', 'spare_part'])['frequency'].sum().reset_index(name='frequency')

sorted_df = df_general.groupby("fahrzeugtyp").apply(lambda x: x.sort_values("frequency", ascending=False)).reset_index(drop=True)
print(sorted_df)


output_path2 = '../../Output/data/SP_freq_TGM.csv'
sorted_df.to_csv(output_path2, index=False)


#data for second page(PNumber dashboard) 5 most repeted
df_PN= grouped_data.groupby("PNumber").apply(lambda x: x.sort_values("frequency", ascending=False)).reset_index(drop=True)
df_PN_first_5 = df_PN.groupby("PNumber").apply(lambda x: x.head(5)).reset_index(drop=True)
print(df_PN_first_5)

output_path3 = '../../Output/data/SP_freq.csv'
df_PN_first_5.to_csv(output_path3, index=False)