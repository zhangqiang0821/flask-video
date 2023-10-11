import hashlib
import os
from datetime import datetime
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import sqlalchemy as sa

# 创建拓展插件实例
db = SQLAlchemy()
# 创建应用程序 app
app = Flask(__name__)
# 配置 SQLite 数据库, 默认存放在 app instance 文件夹下
current_directory = os.path.dirname(os.path.abspath(__file__))
print(current_directory)
os.system("mkdir -p  static/upload/video")
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///{}/instance/flask-video.db".format(current_directory)


# app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///flask-video.db"
# 图片默认的上传地址
app.config["UPLOAD_FOLDER"] = 'static/upload/video'
# 将拓展插件对象绑定到程序实例
db.init_app(app)

class MovieORM(db.Model):
    __tablename__ = 'movie'
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    name = sa.Column(sa.String(255), nullable=False)
    url = sa.Column(sa.String(255), nullable=False)
    create_at = sa.Column(sa.DateTime, default=datetime.now)

@app.cli.command()
def create():
    print(123)
    # db.drop_all()
    # db.create_all()

    # mv = MovieORM()
    # mv.name = '默认演示电影'
    # mv.url = '/static/upload/video/7e245fc2483742414604ce7e67c13111.mp4'
    # db.session.add(mv)
    # db.session.commit()

@app.route('/')
def hello_world():
    q = db.select(MovieORM)
    movie_list = db.session.execute(q).scalars()
    return render_template('index.html', movie_list=movie_list)

@app.route('/video_view')
def video_view():
    url = request.args.get('url')
    return render_template('video_view.html', url=url)

@app.get('/upload_movie')
def upload_movie():
    return render_template('video_upload.html')

@app.post('/video_upload')
def upload_movie2():
    file = request.files['file']
    if file:
        filename = file.filename
        content = file.read()
        name = hashlib.md5(content).hexdigest()
        suffix = os.path.splitext(filename)[-1]
        new_filename = name + suffix
        new_path = os.path.join(app.config['UPLOAD_FOLDER'], new_filename)
        open(new_path, mode='wb').write(content)

        mv = MovieORM()
        mv.url = '/' + new_path
        mv.name = filename
        db.session.add(mv)
        db.session.commit()

    return {
        'code': 0, 'msg': '上传视频成功'
    }

app.run(debug=True)