from flask import Flask,render_template,request,session,flash,redirect,url_for , g        # g is use for global flask , # sesssion stores the client logs at server side
import model

app = Flask(__name__)
app.secret_key = "super secret key"  # for encrypting session data



@app.route('/',methods=['GET','POST']) #post method i.e we are getting info back

def home():
    if request.method == 'GET':
        return render_template('structure.html')
    else :
        session.pop('username',None)
        Username = request.form['Username']
        password = request.form['password']
        db_password = model.match_password(Username)
        if  password == db_password:
            session['username'] = Username
            return redirect(url_for('dashboard'))
        else:
            #error_message='Please enter correct password or username'
            flash('Please enter correct password or username')
            return render_template('structure.html')


@app.route('/signup',methods=['GET','POST'])

def signup():
    if request.method == 'GET':
        return render_template('signup.html')
    else :
        session.pop('username',None)
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        message = model.signup(username,password,email)
        return render_template('signup.html',message = message)

@app.route('/newlist',methods=['POST'])

def newlist():
    
    if request.method == 'POST':
        listName = request.form['listname']
        listitem = request.form['listitem']
        model.insert_listName(listName)
        model.insert_listItem(listitem,listName)
        return redirect(url_for('dashboard'))

@app.route('/newitem',methods=['POST'])

def newitem():
    
    if request.method == 'POST':
        listName = request.form['listname']
        listitem = request.form['listitem']
        model.insert_listItem(listitem,listName)
        return redirect(url_for('dashboard'))

@app.route('/deleteitem',methods=['POST'])

def deleteitem():
    
    if request.method == 'POST':
        listName = request.form['listname']
        listitem = request.form['listitem']
        model.delete_listItem(listitem,listName)
        return redirect(url_for('dashboard'))

@app.route('/deletelist',methods=['POST'])

def deletelist():
    if request.method == 'POST':
        listName = request.form['listname']
        model.delete_list(listName)
        return redirect(url_for('dashboard'))


@app.route('/updatelistname',methods=['POST'])

def updatelistname():
    if request.method == 'POST':
        OldlistName = request.form['Oldlistname']
        NewlistName = request.form['Newlistname']
        model.rename_list(OldlistName,NewlistName)
        return redirect(url_for('dashboard'))

@app.route('/logout',methods=['GET'])

def logout():
    session.pop('username',None)
    return redirect(url_for('home'))


@app.route('/dashboard',methods=['GET'])
def dashboard():
    user = session['username']
    list_dictionary = model.get_list(user)
    return render_template('dashboard.html',list_dictionary = list_dictionary)


if __name__ == '__main__':
    
    app.run(port=7000,debug=True) 