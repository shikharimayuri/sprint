from flask import Flask, render_template, request, redirect, url_for , session
import mysql.connector
from dotenv import load_dotenv
import os
from werkzeug.security import generate_password_hash,check_password_hash

app = Flask(__name__)

load_dotenv()
app.secret_key=os.getenv("SECRET_KEY")

db=mysql.connector.connect(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_NAME")
)

cursor=db.cursor()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/signup", methods=["GET", "POST"])
def signup():

    message=""

    if request.method == "POST":

        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]

        cursor.execute(
        """
        select * from users
        where username=%s
        OR email=%s
        """,
        (username,email)
        )

        existing=cursor.fetchone()

        if existing:
            message="account already exists"

        else:

            hashed=generate_password_hash(password)

            cursor.execute(
            """
            insert into users
            (username,email,password_hash)
            values(%s,%s,%s)
            """,
            (username,email,hashed)
            )

            db.commit()

            return redirect(url_for("login"))

    return render_template("signup.html",message=message)

@app.route("/login",methods=["GET","POST"])
def login():
    message=""

    if request.method=="POST":
        
        username=request.form["username"]
        password=request.form["password"]

        cursor.execute(
        """
        select id,password_hash
        from users
        where username=%s
        """,
        (username,)
        )

        user=cursor.fetchone()

        if user:

            if check_password_hash(
                user[1],
                password
            ):
                
                session["user"]=username
                session["user_id"]=user[0]

                return redirect(
                    url_for("dashboard")
                )
            
            else:
                message="wrong password"

        else:
            message="create account first"
            return render_template("signup.html",message="create account first" )
    
    return render_template(
        "login.html",
        message=message
    )

@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect(
            url_for("login")
        )
    
    return render_template(
        "dashboard.html",
        user=session["user"]
    )

@app.route("/logout")
def logout():

    session.clear()

    return redirect(
        url_for("login")
    )

@app.route("/create_note", methods=["GET","POST"])
def create_note():

    if "user_id" not in session:
        return redirect(url_for("login"))

    message=""

    if request.method=="POST":

        title=request.form["title"]
        content=request.form["content"]

        cursor.execute(
        """
        INSERT INTO notes
        (title,content,user_id)
        VALUES(%s,%s,%s)
        """,
        (
            title,
            content,
            session["user_id"]
        )
        )

        db.commit()

        message="Note saved"

    return render_template(
        "create_note.html",
        message=message
    )
    
@app.route("/view_notes")
def view_notes():

    if "user_id" not in session:
        return redirect(url_for("login"))

    cursor.execute(
    """
    SELECT id,title
    FROM notes
    WHERE user_id=%s
    """,
    (session["user_id"],)
    )

    notes=cursor.fetchall()

    return render_template(
        "view_notes.html",
        notes=notes
    )

@app.route("/note/<int:id>")
def note(id):

    if "user_id" not in session:
        return redirect(url_for("login"))
    
    cursor.execute(
    """
    select title,content
    from notes
    where  id=%s
    """,
    (id,)
    )

    note=cursor.fetchone()

    return render_template(
        "note.html",
        note=note
    )

if __name__== "__main__":
    app.run(debug=True)
