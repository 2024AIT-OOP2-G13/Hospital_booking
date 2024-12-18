from flask import Blueprint, render_template, request, redirect, url_for
from models import User

# Blueprintの作成
user_bp = Blueprint('user', __name__, url_prefix='/users')


@user_bp.route('/')
def list():
    
    # データ取得
    users = User.select()

    return render_template('user_listPersonInfo.html', title='ユーザー一覧', items=users)


@user_bp.route('/add', methods=['GET', 'POST'])
def add():
    
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        contact = request.form['contact']
        User.create(name=name, age=age, contact=contact)
        return redirect(url_for('user.list'))
    
    return render_template('user_add.html')


@user_bp.route('/edit/<int:user_id,contact_id>', methods=['GET', 'POST'])
def edit(user_id,contact_id):
    user = User.get_or_none(User.id == user_id)
    contactInfo = User.get_or_none(User.id == contact_id)
    if not user:
        return redirect(url_for('user.list'))
    if not contactInfo:
        return redirect(url_for('user.list'))

    if request.method == 'POST':
        user.name = request.form['name']
        user.age = request.form['age']
        user.contact = request.form['contact']
        user.save()
        return redirect(url_for('user.list'))

    return render_template('user_edit.html', user=user, contactInfo=contactInfo)