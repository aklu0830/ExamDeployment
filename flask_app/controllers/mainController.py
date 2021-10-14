from flask import render_template, session, request, redirect, flash
from flask_app import app
from flask_app.models import user, painting, join


@app.route("/")
def mainpage():
    if ('loggedIN') in session:
        print("Key Exists")
    else:
        session['loggedIN'] = False
        session['user_id'] = ""
        session['first_name'] = ""
        session['editing'] = False
        session['painting_id'] = ''

    if session['loggedIN']:
        return redirect('/paintings')

    return render_template('login.html')


@app.route("/makeuser", methods=['GET', 'POST'])
def makeuser():
    data = {"first_name": request.form['first_name'], "last_name": request.form['last_name'],
            "email": request.form['email'], "password": request.form['password'],
            "confirm-password": request.form['confirm-password']}

    if not user.User.regvalidate(data):
        return redirect('/')
    else:
        user.User.createusr(data)
    return redirect('/')


@app.route('/login', methods=['POST', 'GET'])
def login():
    data = {"email": request.form['email'], "password": request.form['password']}

    if not user.User.loginvalidate(data):
        return redirect('/')

    elif not user.User.login(data):
        flash(u"Login has failed", 'login')
        return redirect('/')
    else:

        session['loggedIN'] = True
        return redirect('/paintings')


@app.route("/logout")
def logout():
    session['loggedIN'] = False
    session.clear()
    return redirect('/')


@app.route("/paintings")
def paintings():
    data = join.Join.get_all()
    session['editing'] = False

    if not session['loggedIN']:
        return render_template('404.html')
    else:
        return render_template('paintings.html', data=data)


@app.route('/paintings/new')
def newPaintingPage():
    return render_template('addpainting.html')


@app.route('/createpainting', methods=['GET', 'POST'])
def makepainting():
    data = {'name': request.form['painting_name'], 'description': request.form['description'],
            'price': request.form['price'],
            'user_id': session['user_id']}

    if not painting.Painting.validations(data):
        return redirect('/paintings/new')
    else:

        painting.Painting.createpainting(data)

    return redirect('/paintings')


@app.route('/show/<int:painting_id>')
def showpainting(painting_id):
    data = {'painting_id': painting_id}
    paint = join.Join.getPainting(data)


    return render_template('showpainting.html', paint=paint)


@app.route('/delete', methods=['GET', 'POST'])
def removePainting():
    data = {'painting_id': request.form['delete']}

    painting.Painting.droppainting(data)

    return redirect('/paintings')


@app.route('/toggleEdit', methods=['GET', 'POST'])
def toggleEditStatus():
    if not session['editing']:
        session['editing'] = True
        recid = request.form['edit']
        return redirect('/edit/' + recid)
    else:
        session['painting_id'] = ""
        session['editing'] = False
        return redirect('paintings')


@app.route('/edit')
def edit1():
    return redirect('/')


@app.route('/edit/')
def edit2():
    return redirect('/')


@app.route('/edit/<int:paintingid>', methods=['GET', 'POST'])
def editPainting(paintingid):
    if not session['editing']:
        return redirect('/paintings')

    data = {'painting_id': paintingid}
    session['painting_id'] = data['painting_id']

    paintin = painting.Painting.getpainting(data)

    return render_template('editpainting.html', paintin=paintin)


@app.route('/applychanges', methods=['POST', 'GET'])
def applychanges():
    data = {'name': request.form['painting_name'], 'description': request.form['description'],
            'price': request.form['price'],
            'user_id': session['user_id'], 'painting_id': session['painting_id']}
    paintID = data['painting_id']
    if not painting.Painting.validations(data):
        return redirect(f'/edit/{paintID}')
    else:
        painting.Painting.updatepainting(data)
        toggleEditStatus()

    return redirect('/paintings')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html')


if __name__ == '__main__':
    app.run()
