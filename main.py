from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, VARCHAR, Float, desc
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import requests


#My Modules
from test import MoviesApiDb
from pprint import pprint


app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap(app)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///movies.db"
db = SQLAlchemy(app)


#Movie Database
MB_API_KEY = "9149b2f73b90782e603b46258102edd0"
movie_db_api = MoviesApiDb()


class Movie(db.Model):

    id = Column(Integer, primary_key=True)
    title = Column(VARCHAR(50), nullable=False, unique=True)
    year = Column(Integer, nullable=False)
    description = Column(VARCHAR(250), unique=True, nullable=False)
    rating = Column(Float, unique=False, nullable=False)
    ranking = Column(Integer, unique=True, nullable=False)
    review = Column(VARCHAR(100), unique=True, nullable=False)
    img_url = Column(VARCHAR(50), unique=True, nullable=False)

    def __repr__(self):
        return f"{self.title} - {self.year} - {self.rating} - {self.ranking} - {self.review} - {self.img_url}"


class EditForms(FlaskForm):

    #edit
    edit_rating = StringField('You Rating Out Of 10 e.g 7.5', validators=[DataRequired()])
    edited_review = StringField('Your Review', validators=[DataRequired()])
    done_button = SubmitField('Done')


class AddForms(FlaskForm):

    #add
    add_movie = StringField('Movie Title', validators=[DataRequired()])
    done_button = SubmitField('Add Movie')


#Routing
@app.route("/")
def home():

    container = []
    data = Movie.query.order_by(Movie.rating.desc()).all()
    #print(data)

    rank = 0
    for item in data:
        data = []
        data.append(item)
        container.append(data)

        #index = container.index(data)
        #print(index)

        #rank += 1
        #movie_rank = Movie(ranking=rank)
        #db.session.add(movie_rank)
        #db.session.commit()
    index=0

    return render_template("index.html", m_data=container, index=index)


@app.route("/edit/<int:id>", methods=['POST', 'GET'])
def edit(id):

    #global mid
    #mid = id

    form = EditForms()
    m_id = id

    if form.validate_on_submit():
        book_id = m_id
        book_to_update = Movie.query.get(book_id)
        book_to_update.rating = form.edit_rating.data
        book_to_update.review = form.edited_review.data
        db.session.commit()
        return redirect(url_for('home'))


    return render_template("edit.html", form=form)


@app.route('/delete/<int:id>', methods=['POST', 'GET'])
def delete(id):

    if request.method == 'GET':
        book_id = id
        book_to_delete = Movie.query.get(book_id)
        db.session.delete(book_to_delete)
        db.session.commit()

    return redirect(url_for('home'))


@app.route('/add', methods=['POST', 'GET'])
def add():

    global info

    form = AddForms()

    movie_title = str(form.add_movie.data)
    data = movie_db_api.get_movie_info(movie_title)['results']
    info = data

    if request.method == 'POST':

        return render_template('select.html', data=info)

    return render_template('add.html', form=form)


@app.route('/send/<int:id>', methods=['POST', 'GET'])
def send(id):

    m_id = id
    print(m_id)

    if request.method == 'GET':

        m_info = movie_db_api.get_movie_details(m_id)   

        print(True)

        new_movie = Movie(

                            title=m_info['original_title'], 
                            img_url=str('https://image.tmdb.org/t/p/original')+m_info['poster_path'], 
                            year=m_info['release_date'],
                            description=m_info['overview'],
                            ranking=1,

                                )


        db.session.add(new_movie)
        db.session.commit()      

        mid = Movie.query.filter_by(title=m_info['original_title']).first().id

        return redirect(url_for('edit', id=mid))        

    



if __name__ == '__main__':
    app.run(debug=True)
