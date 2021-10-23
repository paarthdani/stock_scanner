from flask import Flask, make_response
import requests
from bs4 import BeautifulSoup as bs
import sys
import PyQt5.QtWebEngineWidgets
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QUrl


result_list = []
app = Flask(__name__)


class Page(PyQt5.QtWebEngineWidgets.QWebEnginePage):
    def __init__(self, url):
        self.app = QApplication(sys.argv)
        PyQt5.QtWebEngineWidgets.QWebEnginePage.__init__(self)
        self.html = ''
        self.loadFinished.connect(self._on_load_finished)
        self.load(QUrl(url))
        self.app.exec_()

    def _on_load_finished(self):
        self.html = self.toHtml(self.Callable)
        # print('Load finished')

    def Callable(self, html_str):
        self.html = html_str
        self.app.quit()


@app.route('/')
def get_my_ip():
    page = Page('https://chartink.com/screener/profit-jump-by-200')
    soup = bs(page.html, 'html.parser')
    js_test = soup.find('table', class_='table table-striped scan_results_table dataTable no-footer')
    columns = []

    for tr in js_test.find_all('tr'):
        columns.append([td.text for td in tr.find_all("td")])

    del columns[0]
    for item in columns:
        result_list.append(item[2])

    message = ''
    for item in result_list:
        message = message + str(item).replace("&", "-") + ' \n'

    print(message)

    telegram_url = 'https://api.telegram.org/botxxxxxxxxxxxx/sendMessage?chat_id=xxxxxxxxx&text=' + message
    requests.post(telegram_url)
    del soup
    del page

    headers = {'Content-Type': 'text/html'}
    return make_response("It works", 200, headers)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8088)
