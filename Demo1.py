#encoding: utf-8
#from werkzeug import secure_filename
import os
#import sys
#print(sys.path)
from flask import g,Flask,render_template,request,session,redirect,url_for
from models import User,Submit_file
import config
from decorators import login_required
from exts import db

app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)




def mkdir(path):
    path = path.strip() # 去除首位空格
    #path = path.rstrip("\\")# 去除尾部 \ 符号
    isExists = os.path.exists(path)    # 判断路径是否存在,存在True,不存在False
    # 判断结果
    if not isExists:
        os.makedirs(path) # 如果不存在则创建目录# 创建目录操作函数
    return path

@app.route("/upload/", methods=['GET', 'POST'])
def upload():
    if request.method  == 'GET':
        return render_template('submit.html')
    user = g.user
    #print(user.username)#测试user
    UPLOAD_FOLDER = mkdir("Demo1\\"+user.teamname+"\\"+user.username+"\\")
    #print(UPLOAD_FOLDER)#测试路径是否正确
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    file = request.files.get("filename")
    file.save(os.path.join(UPLOAD_FOLDER, file.filename))


    #存入数据库
    filepath = UPLOAD_FOLDER+file.filename
    submit_file = Submit_file(filepath = filepath)
    submit_file.user = g.user
    db.session.add(submit_file)
    db.session.commit()
    return render_template('success.html')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login/',methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        stuID = request.form.get('stuID')
        password = request.form.get('password')
        user = User.query.filter(User.stuID == stuID,User.password == password).first()
        if user:
            session['user_id'] = user.id
            session.permanent = True
            return redirect(url_for('index'))
        else:
            return render_template('warning.html')
@app.route('/logout/')
@login_required
def logout():
    del session['user_id']
    return redirect(url_for('login'))

@app.route('/root/',methods=['GET','POST'])
@login_required
def root():
    page = request.args.get('page',1,type=int)
    submit_files = Submit_file.query.order_by(Submit_file.create_time.desc()).paginate(
        page=page ,per_page=12,error_out=False )
    posts = submit_files.items
    return render_template('root.html',posts=posts,submit_files=submit_files)



@app.route('/regist/',methods=['GET','POST'])
@login_required
def regist():
    if request.method == 'GET':
        return render_template('regist.html')
    else:
        teamname = request.form.get('teamname')
        username = request.form.get('username')
        stuID = request.form.get('stuID')
        proclass = request.form.get('proclass')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        #手机号码验证，如果被注册了，就不能再注册了
        user = User.query.filter(User.stuID == stuID).first()
        if user:
            return render_template('warning1.html')
        else:
            #password1 要和 password2 想等才可以
            if password1 != password2:
                return render_template('warning2.html')
            else:
                user = User(teamname=teamname,username=username,stuID = stuID,proclass = proclass,password=password1)
                db.session.add(user)
                db.session.commit()
                #如果注册成功
                print('111------------------')
                return render_template('success1.html')


@app.route('/root_login/',methods=['GET','POST'])
def root_login():
    if request.method == 'GET':
        return render_template('root_login.html')
    else:
        ID = request.form.get('ID')
        password = request.form.get('password')
        user = User.query.filter(User.stuID == ID,User.password == password).first()
        if user and user.stuID == '123456':
            session['user_id'] = user.id
            session.permanent = True
            return redirect(url_for('root'))
        else:
            return render_template('warning.html')



@app.route('/submit/',methods=['GET','POST'])
@login_required
def submit():
    if request.method == 'GET':
        return render_template('submit.html')
    else:
        return redirect(url_for('upload'))

@app.before_request
def my_before_request():
    user_id = session.get('user_id')
    if user_id:
        user = User.query.filter(User.id == user_id).first()
        if user:
            g.user = user
@app.context_processor
def my_context_processor():
    user_id = session.get('user_id')
    if user_id:
        user = User.query.filter(User.id ==user_id).first()
        if user:
            return {'user':user}
    return {}


if __name__ == '__main__':
    app.run()
