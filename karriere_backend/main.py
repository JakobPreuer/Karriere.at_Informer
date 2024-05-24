import datetime
import requests
from bs4 import BeautifulSoup
import sqlite3

import re
def get_job_info(url):

    job_id_and_name = dict()
    result = requests.get(url=url)
    content_as_str = str(result.content)

    regex_pattern = re.compile("[0-9]")

    soup = BeautifulSoup(content_as_str, 'html.parser')

    for a in soup.find_all("a",  href=True):
        #print(str(a.text.strip()).split("/")[-1])
        #print (str(a['href']).split("/")[-1])
        if a.text:
            if regex_pattern.match(str(a['href']).split("/")[-1]):
                job_id_and_name.update({str(a['href']).split("/")[-1]: a.text.strip()})
                # print("Found the URL:", str(a['href']).split("/")[-1])  # Gets all hrefs
                # print("Found the URL:", a.text.strip())

    return job_id_and_name

def write_to_file(job_id_and_name):
    with open("job_id" ,"a") as file:
        for job_ids in job_id_and_name:
            file.write(f"{job_ids}; {job_id_and_name.get(job_ids)}; \n")
    return

def create_db(db_connection):
    db_cursor = db_connection.cursor()
    db_cursor.execute("CREATE TABLE IF NOT EXISTS jobs (job_id INTEGER PRIMARY KEY, job_name TEXT, date DATETIME);")
    db_connection.commit()

    return

def write_to_db(db_connection, job_id_and_name):
    #Check if Dataset is in Database
    #If not write to DB
    db_cursor = db_connection.cursor()
    all_db_entries = get_all_db_entries(db_cursor)
    rows_to_insert = list()
    for key in job_id_and_name:
        print(job_id_and_name.get(key))
        if int(key) not in all_db_entries: #Entrie not in DB -> write to DB
            rows_to_insert.append((int(key), job_id_and_name.get(key), datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")))

    if len(rows_to_insert) > 0:
        db_cursor.executemany('INSERT INTO jobs values (?,?,?)', rows_to_insert)
        db_connection.commit()
    db_cursor.close()
    return

def get_all_db_entries(db_cursor):
    db_cursor.execute("select job_id from jobs")
    return_list = list()
    all_job_id = db_cursor.fetchall()

    for i in all_job_id:
        return_list.append(i[0])

    return return_list


if __name__ == "__main__":
    db_con = sqlite3.connect("karriere.db")

    job_id_and_name = get_job_info("https://www.karriere.at/jobs/ried-im-innkreis-bezirk?jobFields%5B%5D=2172")
    #write_to_file(job_id_and_name)

    create_db(db_con)
    write_to_db(db_con, job_id_and_name)
    exit(0)
