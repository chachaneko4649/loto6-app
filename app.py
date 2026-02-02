import streamlit as st
import pandas as pd
import collections
import random
import os

st.set_page_config(page_title="LOTO6 予測くん", layout="centered")
st.title("🎰 KAZUさんのLOTO6予測・分析アプリ")

# --- 自動読み込み機能 ---
# GitHub上に一緒にアップロードした 'loto6.csv' ば探しに行くバイ
csv_file = 'loto6.csv'

if os.path.exists(csv_file):
    try:
        # 複数の文字コードば試す頑丈な読み込み
        df = None
        for enc in ['cp932', 'utf-8', 'utf-8-sig']:
            try:
                df = pd.read_csv(csv_file, encoding=enc)
                break
            except:
                continue
        
        if df is not None:
            st.success("最新データの読み込みに成功したバイ！")
            
            # --- 以下、分析と予測のロジック（前と同じ） ---
            target_cols = ['第1数字', '第2数字', '第3数字', '第4数字', '第5数字', '第6数字']
            
            # 最新結果の表示
            st.write("最新の抽選結果：")
            st.dataframe(df.head(3))

            # 分析
            all_numbers = df[target_cols].values.flatten()
            counts = collections.Counter(all_numbers)
            most_common_data = counts.most_common(43)
            
            st.subheader("📊 出現頻度グラフ")
            chart_data = pd.DataFrame(most_common_data, columns=['数字', '出現回数']).set_index('数字')
            st.bar_chart(chart_data)

            # 予測
            st.header("💡 推奨予測番号")
            budget = st.number_input("予算（円）", min_value=0, step=200, value=1000)
            if st.button("推奨番号ば生成！"):
                pool = [int(n[0]) for n in most_common_data]
                top_selection = pool[:15] if len(pool) >= 15 else pool
                for i in range(budget // 200):
                    selected = sorted(random.sample(top_selection, 6))
                    st.success(f"{i+1}口目： {selected}")

            # 統計フォーム
            st.header("📝 結果の記録")
            with st.form("result"):
                draw_num = int(df['開催回'].max()) + 1
                st.write(f"第{draw_num}回の記録")
                hit = st.slider("当たった数", 0, 6)
                if st.form_submit_button("記録する"):
                    st.balloons()
    except Exception as e:
        st.error(f"エラーが出たバイ：{e}")
else:
    st.error("CSVファイルが見つからんばい！GitHubに 'loto6.csv' ば上げたか確認してね。")