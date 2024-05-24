from flask import Flask, render_template
import sqlite3


app = Flask(__name__)


@app.route('/')
def hello():
    db_values = get_db_values()


    return render_template("landing.html", job_values=db_values)

def get_db_values():
    db_con = sqlite3.connect("") #Enter path to database
    db_cursor = db_con.cursor()
    db_cursor.execute("select * from jobs;")

    return_list = list()
    all_job_id = db_cursor.fetchall()

    for i in all_job_id:
        return_list.append((i[0], i[1], i[2]))

    db_cursor.close()

    return return_list


app.run(host="0.0.0.0", port=8080)
