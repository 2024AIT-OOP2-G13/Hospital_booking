from flask import Blueprint, render_template, request, redirect, url_for
from models.appointment import Appointment
from models.user import User
from datetime import datetime
import io
import base64
import matplotlib
matplotlib.use('Agg')  # バックエンドをAggに設定
import matplotlib.pyplot as plt
from collections import defaultdict
import matplotlib.ticker as ticker

# 日本語フォントを設定
plt.rcParams['font.family'] = 'Hiragino Sans' 

appointment_bp = Blueprint('appointment', __name__, url_prefix='/appointments')

@appointment_bp.route('/')
def list():
    appointments = (Appointment
                   .select()
                   .join(User)
                   .order_by(Appointment.appointment_datetime))
    
    for appointment in appointments:
        if isinstance(appointment.appointment_datetime, str):
            appointment.appointment_datetime = datetime.strptime(appointment.appointment_datetime, '%Y-%m-%dT%H:%M')
    
    # 予約データを日付ごとに集計
    date_counts = defaultdict(int)
    for appointment in appointments:
        date = appointment.appointment_datetime.date()
        date_counts[date] += 1

    # 日付でソート
    sorted_dates = sorted(date_counts.keys())
    counts = [date_counts[date] for date in sorted_dates]

    # グラフの作成
    plt.figure(figsize=(10, 5))
    plt.plot(sorted_dates, counts, marker='o')
    plt.title('日別予約数', color='black') 
    plt.xlabel('日付', color='black')           
    plt.ylabel('予約数', color='black')            
    plt.grid(True)
    plt.gca().yaxis.set_major_locator(ticker.MultipleLocator(1))
    plt.tight_layout()

    # グラフを画像としてバッファに保存
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    plt.close()

    # 画像をBase64エンコード
    image_base64 = base64.b64encode(buf.getvalue()).decode('utf-8')
    buf.close()

    return render_template('appointment_list.html', title='予約一覧', items=appointments, image_base64=image_base64)

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
