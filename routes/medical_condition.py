from flask import Blueprint, render_template, request, redirect, url_for
from models.medical_condition import MedicalCondition
from models.user import User
import numpy as np
import os
import matplotlib
matplotlib.use('Agg')  # GUIのバックエンドを無効化
import matplotlib.pyplot as plt

medical_condition_bp = Blueprint('medical_condition', __name__, url_prefix='/medical-conditions')

@medical_condition_bp.route('/')
def list():
    generate_condition_chart()  # 症状のグラフを生成する関数を呼び出す

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
        condition.fever = bool(request.form.get('fever'))
        condition.vomiting = bool(request.form.get('vomiting'))
        condition.headache = bool(request.form.get('headache'))
        condition.dizziness = bool(request.form.get('dizziness'))
        condition.other = bool(request.form.get('other'))
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

# 新しい関数：症状ごとのグラフ作成
def generate_condition_chart():
    # 症状ごとのカウント
    fever_counter = 0
    vomiting_counter = 0
    headache_counter = 0
    dizziness_counter = 0
    other_counter = 0

    # MedicalConditionからすべてのデータを取得
    conditions = MedicalCondition.select()

    # 各症状のカウントを行う
    for condition in conditions:
        if condition.fever:
            fever_counter += 1
        if condition.vomiting:
            vomiting_counter += 1
        if condition.headache:
            headache_counter += 1
        if condition.dizziness:
            dizziness_counter += 1
        if condition.other:
            other_counter += 1

    # 英語のラベルとカウント
    labels = ['fever', 'vomiting', 'headache', 'dizziness', 'other']
    counts = [fever_counter, vomiting_counter, headache_counter, dizziness_counter, other_counter]

    # カウントが全て0の場合、グラフを生成しない
    if not any(counts):  # もしカウントが0の場合
        return

    # グラフ作成
    plt.figure(figsize=(6, 6))
    plt.bar(labels, counts, color=['blue', 'green', 'red', 'purple', 'orange'])
    plt.title('Symptom Counts')
    plt.xlabel('Symptoms')
    plt.ylabel('Count')

    # X軸のラベルが重ならないように回転を加える
    plt.xticks(rotation=45, ha='right')

    # レイアウト調整（ラベルの重なり防止）
    plt.tight_layout()

    # staticフォルダに保存
    static_dir = os.path.join(os.getcwd(), 'static')
    os.makedirs(static_dir, exist_ok=True)
    save_path = os.path.join(static_dir, 'condition_chart.png')
    plt.savefig(save_path)
    plt.close()