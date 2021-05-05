from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://wmnfglqm:WoUvdTWDIgSWFkVxq6duOVf7DNJ6wsot@dumbo.db.elephantsql.com:5432/wmnfglqm'
db = SQLAlchemy(app)


class Song(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    duration = db.Column(db.Integer, nullable=False)
    uploaded_time = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Song %r>' % self.id

class Podcast(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    duration = db.Column(db.Integer, nullable=False)
    uploaded_time = db.Column(db.DateTime, default=datetime.utcnow)
    host = db.Column(db.String(100), nullable=False)
    participants = db.Column(db.ARRAY(db.String(100)))


    def __repr__(self):
        return '<Podcast %r>' % self.id

class Audiobook(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    narrator = db.Column(db.String(100), nullable=False)
    duration = db.Column(db.Integer, nullable=False)
    uploaded_time = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Audiobook %r>' % self.id


songs = {}
podcasts = {}
audiobooks = {}
categories = {
    "songs": songs,
    "podcasts": podcasts,
    "audiobooks": audiobooks
}
# db.create_all()


def query_db(audioType):
    songs = {}
    podcasts = {}
    audiobooks = {}

    if audioType == 'songs':
        audios = Song.query.all()
        for audio in audios:
            obj = {
                "name": audio.name,
                "duration": audio.duration,
                "uploaded_time": audio.uploaded_time,
            }
            songs[audio.id] = obj
        return songs

    elif audioType == 'podcasts':
        audios = Podcast.query.all()
        for audio in audios:
            obj = {
                "name": audio.name,
                "duration": audio.duration,
                "uploaded_time": audio.uploaded_time,
                "host": audio.host,
                "participants": audio.participants
            }
            podcasts[audio.id] = obj
        return podcasts

    elif audioType == 'audiobooks':
        audios = Audiobook.query.all()
        for audio in audios:
            obj = {
                "title": audio.title,
                "author": audio.author,
                "narrator": audio.narrator,
                "duration": audio.duration,
                "uploaded_time": audio.uploaded_time,
            }
            audiobooks[audio.id] = obj
        return audiobooks
    else:
        return 'The audio type is not available. Available audios: Songs, Podcasts, & Audiobooks', 400


@app.route('/audios/<string:audioType>', methods=['POST', 'GET'])
def audios(audioType):
    new_audio = None
    if request.method == 'POST':
        if audioType == 'songs':
            name = request.form['name']
            duration = request.form['duration']
            new_audio = Song(name=name, duration=duration)
        
        elif audioType == 'podcasts':
            name = request.form['name']
            duration = request.form['duration']
            host = request.form['host']
            participants = request.form['participants']
            new_audio = Podcast(name=name, duration=duration, host=host, participants=participants)

        elif audioType == 'audiobooks':
            title = request.form['title']
            author = request.form['author']
            narrator = request.form['narrator']
            duration = request.form['duration']
            new_audio = Audiobook(title=title, author=author, narrator=narrator, duration=duration)

        if new_audio:
            try:
                db.session.add(new_audio)
                db.session.commit()
                return query_db(audioType)
            except:
                return 'There was an issue adding your audio', 500
        else:
            return 'The audio type is not available. Available audios: Songs, Podcasts, & Audiobooks', 400

    else:
        return jsonify(query_db(audioType))


@app.route("/audios/<string:audioType>/<int:id>", methods=["GET", "PUT", "DELETE"])
def single_audio(audioType, id):
    
    if request.method == 'PUT':
        if audioType == 'songs':
            audio = Song.query.get_or_404(id)
            audio.name = request.form['name']
            audio.duration = request.form['duration']
            audio.uploaded_time = datetime.utcnow()
            try:
                db.session.commit()
                return query_db(audioType)[id]
            except:
                return 'There was an issue updating song', 500

        elif audioType == 'podcasts':
            audio = Podcast.query.get_or_404(id)
            audio.name = request.form['name']
            audio.duration = request.form['duration']
            audio.uploaded_time = datetime.utcnow()
            audio.host = request.form['host']
            audio.participants = request.form['participants']
            try:
                db.session.commit()
                return query_db(audioType)[id]
            except:
                return 'There was an issue updating podcast', 500

        elif audioType == 'audiobooks':
            audio = Audiobook.query.get_or_404(id)
            audio.title = request.form['title']
            audio.author = request.form['author']
            audio.narrator = request.form['narrator']
            audio.duration = request.form['duration']
            audio.uploaded_time = datetime.utcnow()
            try:
                db.session.commit()
                return query_db(audioType)[id]
            except:
                return 'There was an issue updating audiobook', 500

        else:
            return 'The audio type is not available. Available audios: Songs, Podcasts, & Audiobooks', 400

    elif request.method == 'DELETE':
        if audioType == 'songs': audio = Song.query.get_or_404(id)
        elif audioType == 'podcasts': audio = Podcast.query.get_or_404(id)
        elif audioType == 'audiobooks': audio = Audiobook.query.get_or_404(id)
        
        try:
            db.session.delete(audio)
            db.session.commit()
            return query_db(audioType)
        except:
            return 'Cannot delete'
    
    else:
        try:
            audio = query_db(audioType)[id]
            return jsonify(audio)
        except:
            return 'Audio not available', 400




if __name__ == "__main__":
    app.run(debug=True) #TODO
