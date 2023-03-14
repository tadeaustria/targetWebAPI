from flask import Flask, flash, redirect, render_template, request, url_for, Response
from werkzeug.datastructures import Headers

from targetlib.target import Target

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/pic', methods=['GET'])
def picture():
    noOfSpecialargs = 0
    tenth = request.args.get('tenth', type=bool)
    if tenth == None:
        tenth = False
    else:
        noOfSpecialargs += 1

    withTable = request.args.get('withtable', type=bool)
    if withTable == None:
        withTable = True
    else:
        noOfSpecialargs += 1

    colorType = request.args.get('type', type=str)
    if colorType == None:
        colorType = 'b'
    else:
        noOfSpecialargs += 1

    headline = request.args.get('headline', type=str)
    if headline == None:
        headline = ''
    else:
        noOfSpecialargs += 1

    target = Target(2048, 2048, (len(request.args) - noOfSpecialargs) // 2  if withTable else 0 , colorType, headline)

    idx = 1
    while(True):
        try:
            x = request.args.get('x' + str(idx), type=int)
            y = request.args.get('y' + str(idx), type=int)
            if(x == None or y == None):
                break
            target.drawShotByCoordinates(x, y)
            idx += 1
        except ValueError:
            break

    if withTable:
        target.drawTable(tenth)
        target.drawCenter()

    d = Headers()
    d.add('Content-Disposition', 'inline', filename='foo.jpg')
    return Response(target.getJpg(), status=201, headers=d, mimetype='image/jpeg')