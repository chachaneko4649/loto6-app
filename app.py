import streamlit as st
import pandas as pd
import collections
import random

# ページの設定
st.set_page_config(page_title="LOTO6 予測くん", layout="centered")

st.title("🎰 KAZUさんのLOTO6予測・分析アプリ")

# --- 1. CSV読み込み機能 ---
st.header("📂 1. 過去データの読み込み")
uploaded_file = st.file_uploader("お手元の 'loto6.csv' ば選んでね", type="csv")

if uploaded_file:
    df = None
    for enc in ['cp932', 'utf-8', 'utf-8-sig']:
        try:
            uploaded_file.seek(0)
            df = pd.read_csv(uploaded_file, encoding=enc)
            if df is not None:
                break
        except Exception:
            continue

    if df is not None:
        st.success("データの読み込みに成功したバイ！")
        
        target_cols = ['第1数字', '第2数字', '第3数字', '第4数字', '第5数字', '第6数字']
        
        if not set(target_cols).issubset(df.columns):
            st.error("CSVの列名が合わんばい。")
            st.write(f"今の列名: {list(df.columns)}")
        else:
            st.write("最新の抽選結果：")
            st.dataframe(df.head(3))

            # --- 2. 分析機能 ---
            all_numbers = df[target_cols].values.flatten()
            counts = collections.Counter(all_numbers)
            most_common_data = counts.most_common(43)
            
            st.subheader("📊 出現頻度グラフ")
            chart_data = pd.DataFrame(most_common_data, columns=['数字', '出現回数']).set_index('数字')
            st.bar_chart(chart_data)

            # --- 3. 推奨番号の作成 ---
            st.header("💡 3. 推奨予測番号の作成")
            budget = st.number_input("予算（円）", min_value=0, step=200, value=1000)
            num_tickets = budget // 200
            
            if st.button("推奨番号ば生成する！"):
                st.subheader("🎯 せーさんの推奨組み合わせ")
                # ここで数字ば普通の整数(int)に変換してリストにする
                pool = [int(n[0]) for n in most_common_data]
                top_selection = pool[:15] if len(pool) >= 15 else pool
                
                for i in range(num_tickets):
                    # 選ばれた数字もスッキリ表示
                    selected = sorted(random.sample(top_selection, 6))
                    st.success(f"{i+1}口目： {selected}")
                st.info("※よく出とる数字の上位15個から選んだバイ！")

            # --- 4. 結果の記録 ---
            st.header("📝 4. 購入結果の記録")
            with st.form("result_form"):
                last_draw = int(df['開催回'].max()) if '開催回' in df.columns else 0
                target_draw = st.number_input("今回の開催回", value=last_draw + 1)
                hit_count = st.select_slider("当たった数字の数", options=[0, 1, 2, 3, 4, 5, 6])
                prize = st.number_input("当選金額", value=0)
                if st.form_submit_button("結果ば記録する"):
                    st.balloons()
                    st.info(f"第{target_draw}回の結果ば記録したバイ！当たるとよかねぇ！")
    else:
        st.error("ファイルがうまく読み込めんばい。")
else:
    st.info("まずはCSVば読み込ませてみてね。")