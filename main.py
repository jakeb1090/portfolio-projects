from flask import Flask, request, render_template
import modulefinder
from model import MovieAPI
import model
import requests

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return render_template("home.html")

@app.route('/photo', methods=['GET', 'POST'])
def photo():
    if request.method == 'GET':
        message = 'Find a TV show title poster'
        return render_template("photo.html", message=message)
    else:
        title = request.form['title']
        m = MovieAPI()
        poster_url = m.build_imgurl(title)
        r = requests.get(poster_url)
        if r.status_code != 200:
            message = "No matching TV title"
            return render_template("photo.html", message=message) 
        return render_template("photo.html", image=poster_url)
    
    
@app.route('/korean', methods=['GET', 'POST'])
def kr():
    if request.method == 'GET':
        message = 'Find a K-drama title poster'
        return render_template("korean.html", message=message)
    else:
        title = request.form['title']
        m = MovieAPI()
        poster_url = m.build_imgurl_kor(title)
        word = model.number_word("384")
        r = requests.get(poster_url)
        if r.status_code != 200:
            message = 'No matching TV title'
            return render_template("korean.html", message=message)
        return render_template("korean.html", image=poster_url)
    
@app.route('/loops', methods=['GET'])   
def loops():
    return render_template("loops.html")
        
@app.route('/projects', methods=['GET'])   
def cover():
    return render_template("starter.html")
        
        

if __name__ == "__main__":
    app.run()