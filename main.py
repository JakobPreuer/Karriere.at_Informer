import requests
from bs4 import BeautifulSoup
import re
def get_job_info(url):

    job_id_and_name = dict()
    result = requests.get(url=url)
    content_as_str = str(result.content)

    regex_pattern = re.compile("[0-9]")

    soup = BeautifulSoup(content_as_str, 'html.parser')

    for a in soup.findAll("a",  href=True):
        #print(str(a.text.strip()).split("/")[-1])
        print (str(a['href']).split("/")[-1])
        if a.text:
            if regex_pattern.match(str(a['href']).split("/")[-1]):
                job_id_and_name.update({str(a['href']).split("/")[-1]: a.text.strip()})
                # print("Found the URL:", str(a['href']).split("/")[-1])  # Gets all hrefs
                # print("Found the URL:", a.text.strip())

    return job_id_and_name




if __name__ == "__main__":
    job_id_and_name = get_job_info("https://www.karriere.at/jobs/ried-im-innkreis-bezirk?jobFields%5B%5D=2172")

    print(job_id_and_name)
