import pandas as pd

class Movies:
    def __init__(self, name):
        if name == 'kp':
            self.PATH = './data/kp_new_genres.csv'
            self.index = 'movie_id'
        elif name == 'kion':
            self.PATH = './data/kion_with_descr.csv'
            self.index = 'item_id'


    def get_genres(self):
        df = pd.read_csv(self.PATH, index_col=self.index)
        genres_raw = df['genres'].unique().tolist()
        genres = []
            
        for genre in genres_raw:
            if ', ' in genre:
                genres.extend(genre.split(', '))
            else:
                genres.append(genre)

        genres = set(genres)
        i = 0
        d = {genre: 0 for genre in genres}

        for item in df['genres']:
            for genre in genres:
                if genre in item:
                    d[genre] += 1
        d = list(dict(sorted(d.items(), key=lambda item: item[1], reverse=True)[:20]).keys())
        return d
    
if __name__ == '__main__':
    movies = Movies('kp')
    print(movies.get_genres())


