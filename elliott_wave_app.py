
import streamlit as st
import pandas as pd

# 波の種類と方向
waves = ["第2波", "第3波", "第4波"]
directions = ["ロング", "ショート"]

st.title("エリオット波動トレード記録アプリ")

# 入力フォーム
with st.form("trade_form"):
    date = st.date_input("日付")
    wave = st.selectbox("波の種類", waves)
    direction = st.radio("エントリー方向", directions)
    entry = st.number_input("エントリー価格", step=0.1)
    exit = st.number_input("決済価格", step=0.1)
    submit = st.form_submit_button("記録する")

if submit:
    # 損益計算
    profit = (exit - entry) * (1 if direction == "ロング" else -1) * 100
    new_data = pd.DataFrame([[date, wave, direction, entry, exit, profit]],
                            columns=["日付", "波", "方向", "エントリー", "決済", "損益"])
    
    # 保存またはCSVに追記
    try:
        df = pd.read_csv("trades.csv")
        df = pd.concat([df, new_data], ignore_index=True)
    except FileNotFoundError:
        df = new_data

    df.to_csv("trades.csv", index=False)
    st.success("トレードを記録しました！")

# 統計集計
if st.button("統計を表示"):
    try:
        df = pd.read_csv("trades.csv")
        result = df.groupby("波").agg({
            "損益": ["count", lambda x: (x > 0).sum(), "mean", lambda x: x[x > 0].sum() / max(-x[x < 0].sum(), 1)]
        })
        result.columns = ["回数", "勝ち数", "平均損益", "PF"]
        result["勝率"] = (result["勝ち数"] / result["回数"] * 100).round(1)
        st.dataframe(result)
    except FileNotFoundError:
        st.warning("まだデータがありません。")
