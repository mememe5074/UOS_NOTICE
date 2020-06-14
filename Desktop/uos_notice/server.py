from flask import Flask, render_template, request
import urllib.request
from bs4 import BeautifulSoup
import datetime

notice_list = []

def crwal2(url, keyword):

    soup = BeautifulSoup(urllib.request.urlopen(url).read(), "html.parser")

    title = soup.select(" ul.listType a")
    for link in title:
        if link.get('href').find('fnView') != -1:
            if link.text.find(keyword) != -1:
                notice_list.append(link.text)

        elif link.get('href').find('#') != -1:
            if link.text.find(keyword) != -1:
                notice_list.append(link.text)

app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def index():
    notice_list.clear()
    if request.method == 'GET':
        return render_template('index.html')
    if request.method == 'POST':
        keyword = str(request.form['keyword'])
        num_page = str(request.form['num_page'])
    for i in range(1, int(num_page)+1):
        crwal2("https://www.uos.ac.kr/korNotice/list.do?list_id=FA1&pageIndex=%d" % i, keyword)
        i = i + 1
    return render_template('index.html', notice_list = list(filter(None, notice_list)))

if __name__ == '__main__':
    app.run(debug=True)