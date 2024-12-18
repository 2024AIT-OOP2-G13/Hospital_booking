from flask import Blueprint, render_template, request, redirect, url_for
from models import Jibyou, User

# Blueprintの作成
jibyou_bp = Blueprint('jibyou', __name__, url_prefix='/jibyou')


@jibyou_bp.route('/')
def list():
    jibyou = Jibyou.select()

    return render_template('jibyou_list.html', title='持病一覧', items=jibyou)


@jibyou_bp.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':  
        user_id = request.form['user_id']

        check = request.form.get('condition')  # 探しているものがなければエラーが出ないようにデフォルトの値を返す

        Jibyou.create(user=user_id,check=bool(check))
        return redirect(url_for('jibyou.list'))
    
    users = User.select()
    return render_template('jibyou_add.html', users=users)



@jibyou_bp.route('/edit/<int:jibyou_id>', methods=['GET', 'POST'])
def edit(jibyou_id):
    jibyou = Jibyou.get_or_none(Jibyou.id == jibyou_id)
    if not jibyou:
        return redirect(url_for('jibyou.list'))

    if request.method == 'POST':
        jibyou.user = request.form['user_id']
        jibyou.check = bool(request.form.get('condition'))
        jibyou.save()
        return redirect(url_for('jibyou.list'))

    users = User.select()
    return render_template('jibyou_edit.html', jibyou=jibyou, users=users)
