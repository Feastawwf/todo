import pymongo
from bson.objectid import ObjectId
from datetime import datetime
from flask import Flask,url_for,redirect,render_template,request


app = Flask(__name__)
# 数据库实例化
connect = pymongo.MongoClient('127.0.0.1',27017)
db = connect.todo
# mongo ToDo文档结构
class Todo(object):
    """
    一行待办事项，数据结构,添加。
    字段：事项内容，添加创建时间，状态（未完成/已完成），完成时间
    """
    def create_doc(self,content):
        return {
            'content':content,
            'create_time':datetime.now(),
            'status': 0,           # 0未完成 1已完成
            'finish_time': None
        }

@app.route('/')
def index():
    return redirect(url_for('get'))

@app.route('/get')
def get():
    """展示todo事项"""
    todo_list = db.todo.find()
    print(todo_list)
    return render_template('index.html',todo_list=todo_list)


@app.route('/add',methods=['POST'])
def add():
    """增加一条todo"""
    form = request.form
    content = form['content']
    print(content)
    if connect:
        affected_id = db.todo.insert_one({
            'content':content,
            'create_time':datetime.now(),
            'status': 0,           # 0未完成 1已完成
            'finish_time': None
        })
        print(affected_id)
        if affected_id:
            return redirect(url_for('index'))


@app.route('/finish')
def finish():
    """更新状态已完成"""
    args = request.args
    _id = args['_id']
    affect_id = db.todo.update(
        {"_id":ObjectId(_id)},
        {
            "$set":{
                "status": 1,
                "finish_time": datetime.now()
            }
         }
    )
    print(affect_id)
    return redirect(url_for('index'))


@app.route('/delete')
def delete():
    """删除无用的todo"""
    args = request.args
    _id =args['_id']
    print(_id)
    affect_db = db.todo.remove({
        '_id': ObjectId(_id)
    })
    print(affect_db)
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run()
