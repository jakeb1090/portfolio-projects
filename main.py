from flask import Flask, request, render_template
import model

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def bot():
    if request.method == 'GET':
        model.get_tweets()
        return {"status": "retweets okay"}
    else:
        title = request.form['title']
        m = MovieAPI()
        poster_url = m.build_imgurl(title)
        r = requests.get(poster_url)
        if r.status_code != 200:
            message = "No matching TV title"
            return render_template("photo.html", message=message) 
        return render_template("photo.html", image=poster_url)

        
        
                
        
if __name__ == "__main__":
    app.run()