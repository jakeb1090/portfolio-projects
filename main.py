from flask import Flask, request, render_template
import modulefinder
from model import MovieAPI
import model
import requests

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'GET':
        message = 'Please enter a TV title'
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
        message = 'Please enter a KOREAN title'
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
        
        
        
        
        
        
           
        
if __name__ == "__main__":
    app.run()