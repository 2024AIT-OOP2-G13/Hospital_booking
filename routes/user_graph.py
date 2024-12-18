from flask import Blueprint, Flask, render_template
import matplotlib
matplotlib.use('Agg') 
import matplotlib.pyplot as plt
import io
import base64
from collections import Counter
from models import User

app = Flask(__name__)

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

    # グラフをBase64形式でエンコード
    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)
    base64_img = base64.b64encode(buf.read()).decode('utf-8')
    buf.close()

    # Base64画像をHTMLに埋め込む
    graph_html = f'<img src="data:image/png;base64,{base64_img}" alt="Graph">'
    return render_template("index.html", graph=graph_html)