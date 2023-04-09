from flask import Flask, render_template, request
import pickle
import pandas as pd
import numpy

# popular_df= pickle.load(open('popular.pkl','rb'))
popular_df= pd.read_pickle('popular.pkl')
books= pd.read_pickle('books.pkl')
pt= pd.read_pickle('pt.pkl')
similarity_scores= pd.read_pickle('similarity_scores.pkl')
app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html',
                           book_name= list(popular_df['Book-Title'].values),
                           author= list(popular_df['Book-Author'].values),
                           image= list(popular_df['Image-URL-M'].values),
                           votes= list(popular_df['num_ratings'].values),
                           rating= list(numpy.rint(popular_df['avg_ratings'].values)),
                           Publisher= list(popular_df['Publisher'].values),
                           Year_Of_Publication= list(popular_df['Year-Of-Publication'].values)
                           )

@app.route('/recommend')
def recommend_ui():
    return render_template('recommend.html')

@app.route('/recommend_books',methods=['post'])
def recommend():
    user_input = request.form.get('user_input')
    index = numpy.where(pt.index == user_input)[0][0]
    similar_items = sorted(list(enumerate(similarity_scores[index])), key=lambda x: x[1], reverse=True)[1:5]

    data = []
    for i in similar_items:
        item = []
        temp_df = books[books['Book-Title'] == pt.index[i[0]]]
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))

        data.append(item)

    print(data)

    return render_template('recommend.html',data=data)

if __name__ == '__main__':
    app.run(debug=True)