dfo = pd.read_csv("hol.csv")
df = pd.read_csv("prob.csv")
print(df)
df['prob'] = dfo['prob']
df['prob'] = df['prob'] / df['prob'].sum()
print(df.sum())
df.to_csv("normalized_prob_n.csv")