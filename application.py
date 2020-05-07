#! /usr/bin/python
from flask import render_template, session

from datetime import datetime
from flask import request, redirect
from werkzeug.utils import secure_filename
from flask import Flask
import os
from bs4 import BeautifulSoup
from urllib.request import urlopen as uReq
import urllib
from http.cookiejar import CookieJar
from flask import jsonify
import multiprocessing
from flask_cors import CORS

application = Flask(__name__)
CORS(application)

cwd = os.getcwd()

print(cwd)



users = {
    "mitsuhiko": {
        "name": "Armin Ronacher",
        "bio": "Creatof of the Flask framework",
        "twitter_handle": "@mitsuhiko"
    },
    "gvanrossum": {
        "name": "Guido Van Rossum",
        "bio": "Creator of the Python programming language",
        "twitter_handle": "@gvanrossum"
    },
    "elonmusk": {
        "name": "Elon Musk",
        "bio": "technology entrepreneur, investor, and engineer",
        "twitter_handle": "@elonmusk"
    }
}



@application.route("/")
def index():
    return render_template("public/index.html")


@application.route("/about")
def about():
    return
    """
    <h1 style='color: red;'>I'm a red H1 heading!</h1>
    <p>This is a lovely little paragraph</p>
    <code>Flask is <em>awesome</em></code>
    """

@application.template_filter("clean_date")
def clean_date(dt):
    return dt.strftime("%d %b %Y")

date = datetime.utcnow()

@application.route("/jinja")
def jinja():
    # Strings
    my_name = "Julian"

    # Integers
    my_age = 30

    # Lists
    langs = ["Python", "JavaScript", "Bash", "Ruby", "C", "Rust"]

    # Dictionaries
    friends = {
        "Tony": 43,
        "Cody": 28,
        "Amy": 26,
        "Clarissa": 23,
        "Wendell": 39
    }

    # Tuples
    colors = ("Red", "Blue")

    # Booleans
    cool = True

    # Classes
    class GitRemote:
        def __init__(self, name, description, domain):
            self.name = name
            self.description = description
            self.domain = domain

        def clone(self, repo):
            return f"Cloning into {repo}"

    my_remote = GitRemote(
        name="Learning Flask",
        description="Learn the Flask web framework for Python",
        domain="https://github.com/Julian-Nash/learning-flask.git"
    )

    # Functions
    def repeat(x, qty=1):
        return x * qty

    return render_template(
        "public/jinja.html", my_name=my_name, my_age=my_age, langs=langs,
        friends=friends, colors=colors, cool=cool, GitRemote=GitRemote,
        my_remote=my_remote, repeat=repeat, date=date
    )

@application.route("/sign-up", methods=["GET", "POST"])
def signup():

    if request.method == "POST":

        req = request.form

        missing = list()
        for k, v in req.items():
            if k=="username":
                username=v
            if k=="password":
                password=v
            if v == "":
                missing.append(k)

        if missing:
            feedback = f"Missing fields for {', '.join(missing)}"
            return render_template("public/sign-up.html", feedback=feedback)

        return redirect("/profile?username=\(username)>&password=<password>")

    return render_template("public/sign-up.html")



@application.route("/profile/<username>")
def profile(username):
    args = request.args

    if "username" in args:
        username = args["username"]

    if "password" in args:
        password = args.get("password")

    user = None
    if username in users:
        user = users[username]
    return render_template("public/profile.html")


application.secret_key = 'super secret key'
cwd = os.getcwd()
directory=cwd+"/static/img/uploads"
application.config["IMAGE_UPLOADS"] = directory
@application.route("/upload", methods=["GET", "POST"])
def upload():
    if request.method == "POST":
        if request.files:
            if "filesize" in request.cookies:
                if not allowed_image_filesize(request.cookies["filesize"]):
                    print("Filesize exceeded maximum limit")
                    return redirect(request.url)

            file = request.files["textFile"]

            if file.filename == "":
                print("No filename")
                return redirect(request.url)

            if allowed_image(file.filename):
                filename = file.filename
                print(filename)
                print(os.path.join(application.config["IMAGE_UPLOADS"], filename))
                session['file']=file.filename
                file.save(os.path.join(application.config["IMAGE_UPLOADS"], filename))
                print("Image saved")

                return redirect("/analyze")

            else:
                print("That file extension is not allowed")
                return redirect(request.url)

            print("File saved")

            return redirect("/analyze")

    return render_template("public/upload.html")

application.config["ALLOWED_IMAGE_EXTENSIONS"]=["TXT"]
application.config["MAX_IMAGE_FILESIZE"] = 100 * 1024 * 1024
def allowed_image(filename):

    # We only want files with a . in the filename
    if not "." in filename:
        return False

    # Split the extension from the filename
    ext = filename.rsplit(".", 1)[1]

    # Check if the extension is in ALLOWED_IMAGE_EXTENSIONS
    if ext.upper() in application.config["ALLOWED_IMAGE_EXTENSIONS"]:
        return True
    else:
        return False

def allowed_image_filesize(filesize):

    if int(filesize) <= application.config["MAX_IMAGE_FILESIZE"]:
        return True
    else:
        return False




from model.main import *


@application.route("/analyze")
def analyze():
    theFile = session.get('file')
    reset()
    result = get_data(theFile)
    promos = browsefunc()
    if not promos:
        promos["None used for the time period entered"]="Empty"
    df1 = result[0]
    df2 = result[1]
    df3 = result[2]
    breakdown=create_pie()
    asinSum  = breakdown[0]
    asin1    = breakdown[1]
    asin2    = breakdown[2]
    asin3    = breakdown[3]
    asin4    = breakdown[4]
    asin5 = breakdown[5]
    asins=[]
    for element in range(0, len(asin2)):
        asins.append([asin2[element], asin1[element], asin3[element], str(round(asin4[element], 2)), asin5[element]])
    print(asins)
    print("wtf")
    return render_template("public/analyze.html", promos = promos, df1=df1, df2=df2, df3=df3, asinSum=asinSum, asins=asins)


@application.route("/admin/dashboard")
def admin():
    return render_template("admin/dashboard.html")

courseList={}

@application.route("/courses", methods=['GET'])
def courses():
    username = request.args.get('username')
    print(username)
    course = request.args.get('course')
    print(course)
    results="kk"
    try:
        toInteger = int(course)
        if toInteger in range(0, 80000):
            if course in courseList:
                return jsonify(results=courseList[course])
            else:
                results = getClasses(course)
                courseList[course] = results
    except:
        print("error")
    return jsonify(results=results)
    #return "<h1 style='color: red;'>" + results + "</h1>"

def getClasses(courseNum):


    url = "https://webapp4.asu.edu/catalog/coursedetails?r=" + courseNum
    req = urllib.request.Request(url)
    cj = CookieJar()
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))

    while(True):
        response = opener.open(req)
        page_html = response.read()
        soup = BeautifulSoup(page_html, 'html.parser')
        all_a = soup.find_all('span', {'class':'icontip'})
        try:
            for item in all_a:
                if item['rel'] == "#tt_seats-open":
                    print("Class is Open")
                    p1 = multiprocessing.Process(target=keepClasses, args=(courseNum,))
                    p1.start()
                    return ("Class is Open")
                if item['rel'] == "#tt_seats-closed":
                    print("Class is closed")
                    p1 = multiprocessing.Process(target=keepClasses, args=(courseNum,))
                    p1.start()
                    return ("Class is closed")
        except:
            print("Error")

def keepClasses(courseNum):


    url = "https://webapp4.asu.edu/catalog/coursedetails?r=" + courseNum
    req = urllib.request.Request(url)
    cj = CookieJar()
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))

    while(True):
        response = opener.open(req)
        page_html = response.read()
        soup = BeautifulSoup(page_html, 'html.parser')
        all_a = soup.find_all('span', {'class':'icontip'})
        try:
            for item in all_a:
                if item['rel'] == "#tt_seats-open":
                    courseList[courseNum] = "Class is Open"
                if item['rel'] == "#tt_seats-closed":
                    courseList[courseNum] = "Class is closed"


        except:
            print("Error")



if __name__ == "__main__":
    application.debug = True
    application.run()
