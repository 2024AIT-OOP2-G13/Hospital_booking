from flask import Blueprint, render_template
import matplotlib
matplotlib.use('Agg') 
import matplotlib.pyplot as plt
from collections import Counter
from models import User
import os

# Blueprintの作成
graph_bp = Blueprint('graph', __name__)

@graph_bp.route('/')
def index():
    # 年齢データを取得
    ages = [user.age for user in User.select()]

    # 年齢を10代ごとに区分
    bins = range(0, 101, 10)
    age_groups = [(age // 10) * 10 for age in ages]

    # 年齢分布を集計
    age_counts = Counter(age_groups)

    # ラベルと値を生成
    labels = [f"{start}~{start+9}" for start in bins[:-1]]
    counts = [age_counts.get(start, 0) for start in bins[:-1]]

    # グラフの作成
    plt.figure()
    plt.bar(labels, counts, color="skyblue", edgecolor="black")
    plt.xlabel("Age")
    plt.ylabel("People")
    plt.title("Age distribution")
    plt.ylim(0, 10)
    plt.tight_layout()

    # グラフを画像としてファイルに保存
    static_dir = os.path.join(os.getcwd(), 'static')
    os.makedirs(static_dir, exist_ok=True)
    save_path = os.path.join(static_dir, 'age_distribution_chart.png')
    plt.savefig(save_path)
    plt.close()

    # 保存した画像のパスをテンプレートに渡す
    return render_template("index.html", graph_path=save_path)