import numpy as np
import os
import matplotlib.pyplot as plt

def generate_pie_chart():
    # 円グラフのデータ
    x = np.array([100, 200, 300, 400, 2500])
    labels = ['A', 'B', 'C', 'D', 'E']  # 各セクションのラベル

    # 円グラフを描画
    plt.pie(x, labels=labels, autopct='%1.1f%%')  # ラベルと割合を表示

    # staticフォルダのパスを取得
    static_dir = os.path.join(os.getcwd(), 'static')  # プロジェクト内のstaticフォルダ

    # staticフォルダが存在しない場合、作成する
    if not os.path.exists(static_dir):
        os.makedirs(static_dir)

    # staticフォルダ内に保存
    save_path = os.path.join(static_dir, 'pie_department_chart.png')
    plt.savefig(save_path)

