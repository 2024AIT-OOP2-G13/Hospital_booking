from flask import Blueprint, render_template, request, redirect, url_for
from models.appointment import Appointment
from models.user import User
from datetime import datetime
import numpy as np
import os

import matplotlib  # matplotlibを先にインポート
matplotlib.use('Agg')  # GUIのバックエンドを無効化
import matplotlib.pyplot as plt

appointment_bp = Blueprint('appointment', __name__, url_prefix='/appointments')

@appointment_bp.route('/')
def list():
    generate_department_pie_chart() #診療科のグラフを作る(画像保存まで行う)
    appointments = (Appointment
                   .select()
                   .join(User)
                   .order_by(Appointment.appointment_datetime))
    
    for appointment in appointments:
        if isinstance(appointment.appointment_datetime, str):
            appointment.appointment_datetime = datetime.strptime(appointment.appointment_datetime, '%Y-%m-%dT%H:%M')
    return render_template('appointment_list.html', title='予約一覧', items=appointments)

@appointment_bp.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        Appointment.create(
            user=request.form['user_id'],
            appointment_datetime=request.form['appointment_datetime'],
            department=request.form['department']
        )
        return redirect(url_for('appointment.list'))

    users = User.select()
    return render_template('appointment_add.html', users=users)

@appointment_bp.route('/edit/<int:appointment_id>', methods=['GET', 'POST'])
def edit(appointment_id):
    appointment = Appointment.get_or_none(Appointment.id == appointment_id)
    if not appointment:
        return redirect(url_for('appointment.list'))

    if isinstance(appointment.appointment_datetime, str):
        appointment.appointment_datetime = datetime.strptime(appointment.appointment_datetime, '%Y-%m-%dT%H:%M')

    if request.method == 'POST':
        appointment.user = request.form['user_id']
        appointment.appointment_datetime = request.form['appointment_datetime']
        appointment.department = request.form['department']
        appointment.save()
        return redirect(url_for('appointment.list'))

    users = User.select()
    appointment_datetime_str = appointment.appointment_datetime.strftime('%Y-%m-%dT%H:%M') if appointment.appointment_datetime else ''
    return render_template('appointment_edit.html', appointment=appointment, users=users, appointment_datetime_str=appointment_datetime_str)


def generate_department_pie_chart():
    from peewee import fn  #Peeweeが集計してくれるのでインポート

    #データベースを基に診療科ごとの予約数を集計
    department_counts = (Appointment
                         .select(Appointment.department, fn.COUNT(Appointment.id).alias('count'))
                         .group_by(Appointment.department))

    #診療科名と予約数をリストに分割
    labels = []
    counts = []
    for entry in department_counts:
        labels.append(entry.department)
        counts.append(entry.count)

    # グラフを描画
    plt.figure(figsize=(6, 6))
    plt.pie(counts, labels=labels, autopct='%1.1f%%')  # ラベルと割合をグラフに添える

    #staticフォルダのパスを入手(これでするらしい)
    static_dir = os.path.join(os.getcwd(), 'static')  

    #staticフォルダ内に保存
    save_path = os.path.join(static_dir, 'pie_department_chart.png')
    plt.savefig(save_path)
    plt.close() 
