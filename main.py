from flask import render_template, Flask, Markup, url_for
import feedparser
import pyqrcode
import png
import os

app = Flask(__name__)
mainDir = os.getcwd()
qrCodesDir = mainDir+'/static/styles/images/qrcodes'

def createQRCode(link, index):
    url = pyqrcode.create(link)
    name = 'qrcode'+str(index)+'.png'
    os.chdir(qrCodesDir)
    url.png(name, scale=2)
    os.chdir(mainDir)

def deleteOldQRCodes():
    for file in os.listdir(qrCodesDir):
        file_path = os.path.join(qrCodesDir, file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        except Exception as e:
            print(e)

def getContent(url):
    deleteOldQRCodes()
    content = []
    feed = feedparser.parse(url)
    for index, entry in enumerate(feed.entries):
        data = {}
        data['title'] = entry.title
        data['content'] = Markup(entry.content[0].value)
        data['published'] = entry.published
        data['qrcode'] = "/static/styles/images/qrcodes/qrcode"+str(index)+".png"
        createQRCode(entry.link, index)
        content.append(data)
    return content

dict = getContent("https://sdtimes.com/feed") + getContent("http://feeds.feedburner.com/Techcrunch")

@app.route('/test')
def content():
    return render_template('rss_template.html', posts = dict)

if __name__ == "__main__":
    app.run(debug = True)

