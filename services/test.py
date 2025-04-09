import pandas as pd

df = pd.read_csv('./app/static/clips/kp_cut.csv', index_col='movie_id')
print(df.head())
