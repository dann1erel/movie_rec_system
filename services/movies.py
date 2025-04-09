import pandas as pd

class Movies:
    def __init__(self, name):
        if name == 'kp':
            self.PATH = './data/kp_new_genres.csv'
            self.index = 'movie_id'
        elif name == 'kion':
            self.PATH = './data/kion_with_descr.csv'
            self.index = 'item_id'
        elif name == 'kp_final':
            self.PATH = './data/kp_final.csv'
            self.index = 'movie_id'
        self.df = pd.read_csv(self.PATH, index_col=self.index)


    def get_genres(self):
        genres_raw = self.df['genres'].unique().tolist()
        genres = []
            
        for genre in genres_raw:
            if ', ' in genre:
                genres.extend(genre.split(', '))
            else:
                genres.append(genre)

        genres = set(genres)
        d = {genre: 0 for genre in genres}

        for item in self.df['genres']:
            for genre in genres:
                if genre in item:
                    d[genre] += 1
        d = list(dict(sorted(d.items(), key=lambda item: item[1], reverse=True)[:20]).keys())
        return d
    

    def get_data_one_row(self, i):
        row = self.df.iloc[i]
        row_dict = row.to_dict()
        row_dict['id'] = int(row.name)
        return row_dict
    

    def get_len(self):
        return self.df.shape[0]

    
if __name__ == '__main__':
    movies = Movies('kp_final')
    print(movies.get_data_one_row(0))



