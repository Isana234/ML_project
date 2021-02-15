from flask import Flask, flash, request, redirect, url_for,render_template
from werkzeug.utils import secure_filename
import os
import pandas as pd
from final_demo_project1 import hello
...
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def handle_data():
    if request.method == "POST":
        filess = request.files['file']
        filename = secure_filename(filess.filename)
        print(filename)
        filess.save(os.path.join("uploads",filename))
        
        hello(os.path.join("uploads",filename))
        x="static/yo.png"
        
        return render_template("result.html",y=x)
    return render_template("ProjectPredict.html")

if __name__ == '__main__':
    app.run(debug=True)

#hello("perrin-freres-monthly-champagne-.csv")
        #x="static/yo.png"