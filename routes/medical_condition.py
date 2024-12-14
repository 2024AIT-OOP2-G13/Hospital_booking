from flask import Blueprint, render_template, request, redirect, url_for
from models.medical_condition import MedicalCondition
from models.user import User
import numpy as np
import matplotlib  # matplotlibを先にインポート
matplotlib.use('Agg')  # GUIのバックエンドを無効化
import matplotlib.pyplot as plt
import os

medical_condition_bp = Blueprint('medical_condition', __name__, url_prefix='/medical-conditions')

@medical_condition_bp.route('/')
def list():
    users = User.select()
    conditions = MedicalCondition.select()

    conditions_dict = {}
    for condition in conditions:
        if condition.user.id not in conditions_dict:
            conditions_dict[condition.user.id] = []

        if condition.fever:
            conditions_dict[condition.user.id].append('fever')
        if condition.vomiting:
            conditions_dict[condition.user.id].append('vomiting')
        if condition.headache:
            conditions_dict[condition.user.id].append('headache')
        if condition.dizziness:
            conditions_dict[condition.user.id].append('dizziness')
        if condition.other:
            conditions_dict[condition.user.id].append('other')

    ##グラフ作成ここから

    # 症状カウンタ
    symptom_counters = {
        "発熱": 0,
        "嘔吐": 0,
        "頭痛": 0,
        "眩暈": 0,
        "その他": 0
    }

    # conditionsを利用して症状のカウントを行う
    for condition in conditions:
        if condition.fever:
            symptom_counters["発熱"] += 1
        if condition.vomiting:
            symptom_counters["嘔吐"] += 1
        if condition.headache:
            symptom_counters["頭痛"] += 1
        if condition.dizziness:
            symptom_counters["眩暈"] += 1
        if condition.other:
            symptom_counters["その他"] += 1

    # グラフの作成
    labels = list(symptom_counters.keys())
    counts = list(symptom_counters.values())
    plt.bar(labels, counts, align="center", color="skyblue")
    plt.xlabel("症状")
    plt.ylabel("件数")
    plt.title("症状の分布")

    #staticフォルダのパスを入手(これでするらしい)
    static_dir = os.path.join(os.getcwd(), 'static')

    # グラフを保存
    save_path = os.path.join(static_dir, 'condition_chart.png')
    plt.savefig(save_path, format='png')
    plt.close()

    ##グラフ作成ここまで


    return render_template('medical_condition_list.html', title='症状一覧', users=users, conditions=conditions_dict)

@medical_condition_bp.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        user_id = request.form['user_id']

        fever = bool(request.form.get('fever'))
        vomiting = bool(request.form.get('vomiting'))
        headache = bool(request.form.get('headache'))
        dizziness = bool(request.form.get('dizziness'))
        other = bool(request.form.get('other'))

        MedicalCondition.create(user=user_id, fever=fever, vomiting=vomiting, headache=headache, dizziness=dizziness, other=other)
        return redirect(url_for('medical_condition.list'))

    users = User.select()
    return render_template('medical_condition_add.html', users=users)

@medical_condition_bp.route('/edit/<int:condition_id>', methods=['GET', 'POST'])
def edit(condition_id):
    condition = MedicalCondition.get_or_none(MedicalCondition.id == condition_id)
    if not condition:
        return redirect(url_for('medical_condition.list'))

    if request.method == 'POST':
        user_id = request.form['user_id']
        condition.check = bool(request.form.get('fever'))
        condition.check = bool(request.form.get('vomiting'))
        condition.check = bool(request.form.get('headache'))
        condition.check = bool(request.form.get('dizziness'))
        condition.check = bool(request.form.get('other'))
        condition.save()
        return redirect(url_for('medical_condition.list'))

    condition_states = {
        'fever': condition.fever,
        'vomiting': condition.vomiting,
        'headache': condition.headache,
        'dizziness': condition.dizziness,
        'other': condition.other
    }

    users = User.select()
    return render_template(
        'medical_condition_edit.html',
        condition=condition,
        condition_states=condition_states,
        users=users
    )

    users = User.select() 
    return render_template('medical_condition_edit.html', condition=condition, users=users) 
