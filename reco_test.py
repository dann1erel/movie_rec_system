import sqlite3
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

class TwoStageRecommender:
    def __init__(self, db_path):
        self.conn = sqlite3.connect(db_path)
        self._load_data()
        self._prepare_content_matrix()

    def _load_data(self):
        # Load movies and genres
        self.movies = pd.read_sql_query(
            "SELECT id, title, rating, num_ratings, year, country, duration, description FROM movies",
            self.conn
        )
        genres = pd.read_sql_query(
            "SELECT movie_id, genre FROM movie_genres",
            self.conn
        )
        # Pivot genres to one-hot
        self.genre_matrix = genres.assign(value=1).pivot(index='movie_id', columns='genre', values='value').fillna(0)
        self.user_likes = pd.read_sql_query(
            "SELECT movie_id FROM user_likes",
            self.conn
        )
        self.user_fav_genres = pd.read_sql_query(
            "SELECT genre FROM user_favorite_genres",
            self.conn
        )['genre'].tolist()

    def _prepare_content_matrix(self):
        # TF-IDF on descriptions
        self.tfidf = TfidfVectorizer(stop_words='english', max_features=5000)
        self.desc_matrix = self.tfidf.fit_transform(self.movies['description'].fillna(''))

    def build_user_profile(self):
        # Profile based on liked movies' content and favorite genres
        liked_ids = self.user_likes['movie_id'].tolist()
        if not liked_ids:
            # cold start: use favorite genres only
            genre_profile = pd.Series(0, index=self.genre_matrix.columns)
            genre_profile[self.user_fav_genres] = 1
            self.user_profile_desc = None
            self.user_profile_genre = genre_profile
        else:
            # content profile
            liked_idx = self.movies[self.movies['id'].isin(liked_ids)].index
            self.user_profile_desc = self.desc_matrix[liked_idx].mean(axis=0)
            # genre profile: avg of liked
            liked_genres = self.genre_matrix.loc[liked_ids]
            self.user_profile_genre = liked_genres.mean()

    def retrieve_candidates(self, top_k=200):
        # Stage 1: similarity based retrieval
        # Combine desc and genre similarities
        # Desc sim
        if self.user_profile_desc is not None:
            desc_sim = linear_kernel(self.user_profile_desc, self.desc_matrix).flatten()
        else:
            desc_sim = 0
        # Genre sim
        genre_sim = self.genre_matrix.dot(self.user_profile_genre.values)
        # Total sim
        total_sim = desc_sim + genre_sim.values
        idx_sorted = total_sim.argsort()[::-1]
        candidates_idx = idx_sorted[:top_k]
        return self.movies.iloc[candidates_idx].copy()

    def rank_candidates(self, candidates, weight_rating=0.7, weight_popularity=0.3):
        # Stage 2: ranking by a simple score
        # Normalize rating and popularity
        candidates = candidates.copy()
        candidates['norm_rating'] = (candidates['rating'] - candidates['rating'].min()) / (candidates['rating'].max() - candidates['rating'].min())
        candidates['norm_pop'] = (candidates['num_ratings'] - candidates['num_ratings'].min()) / (candidates['num_ratings'].max() - candidates['num_ratings'].min())
        candidates['score'] = weight_rating * candidates['norm_rating'] + weight_popularity * candidates['norm_pop']
        return candidates.sort_values('score', ascending=False)

    def recommend(self, n=10):
        self.build_user_profile()
        candidates = self.retrieve_candidates()
        ranked = self.rank_candidates(candidates)
        return ranked[['id', 'title', 'score']].head(n)

if __name__ == '__main__':
    reco = TwoStageRecommender('movies.db')
    recommendations = reco.recommend(10)
    print(recommendations)
