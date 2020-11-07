from flask import Flask, request, render_template
import modulefinder
from model import MovieAPI
import model
import requests
import scraper
# from werkzeug import secure_filename

app = Flask(__name__)

# app.config['UPLOAD_FOLDER']
# app.config['MAX_CONTENT_PATH']

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
    return render_template("projects.html")

@app.route('/indeed_ca', methods=['GET', 'POST'])   
def indeed_ca():
    if request.method == 'POST':
        j_search = request.form['job_search']
        location = request.form['location']
        days_ago = request.form['days_ago']
        salary = request.form['salary']
        container_list = scraper.breakIntoContainers(j_search, location, salary, days_ago)
        all_data = scraper.scrapeData(container_list)
        if all_data == None:
            results_num = 0
        else:
            results_num = len(all_data)
        return render_template("indeed_ca.html", all_data=all_data, results_num=results_num)
    else:
        return render_template("indeed_ca.html")

# @app.route('/uploader', methods = ['GET', 'POST'])
# def upload_file():
#    if request.method == 'POST':
#       f = request.files['file']
#       f.save(secure_filename(f.filename))
#       return 'file uploaded successfully'


if __name__ == "__main__":
    app.run(debug=True)