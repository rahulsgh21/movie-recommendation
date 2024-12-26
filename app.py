from flask import Flask, request, render_template
import pickle

app = Flask(__name__)

movies = pickle.load(open('model/movie_list.pkl', 'rb'))
similarity = pickle.load(open('model/similarity.pkl', 'rb'))

def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    for i in distances[1:6]:
        recommended_movie_names.append(movies.iloc[i[0]].title)
    return recommended_movie_names

@app.route('/', methods=['GET', 'POST'])
def home():
    recommendations = None
    selected_movie = None
    if request.method == 'POST':
        selected_movie = request.form['movie']
        recommendations = recommend(selected_movie)
    return render_template('index.html', movie_list=movies['title'].values, recommendations=recommendations, selected_movie=selected_movie)

if __name__ == '__main__':
    app.run(debug=True)
