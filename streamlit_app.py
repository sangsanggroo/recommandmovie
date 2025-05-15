
import streamlit as st
import pandas as pd
import plotly.express as px
import statsmodels.api as sm

# 데이터 불러오기
@st.cache_data
def load_data():
    df = pd.read_csv("movie_recommendations_500_full.csv")
    return df

df = load_data()

st.title("🎬 나만의 영화 추천 대시보드")
st.markdown("500편의 영화 데이터를 분석하여 다양한 시각화를 제공합니다.")

# 탭 구성
tab1, tab2, tab3 = st.tabs(["⭐ 평점별 영화 추천", "👦 어린이 추천 영화", "📊 장르별 상관관계 분석"])

# ⭐ 탭1: 평점별 영화 추천
with tab1:
    st.subheader("평점대별 인기 영화 보기")
    score_range = st.slider("평점 범위 선택", 9.0, 9.5, (9.2, 9.4), step=0.01)
    filtered = df[(df["평점"] >= score_range[0]) & (df["평점"] <= score_range[1])]
    st.write(f"🎞️ 총 {len(filtered)}편의 영화가 선택되었습니다.")
    st.dataframe(filtered[["영화제목", "평점", "장르", "국가", "러닝타임"]])

    fig = px.histogram(filtered, x="평점", nbins=10, title="선택한 범위 내 평점 분포")
    st.plotly_chart(fig, use_container_width=True)

# 👦 탭2: 어린이 추천 영화
with tab2:
    st.subheader("어린이를 위한 애니메이션 영화 추천")
    kids_movies = df[df["장르"].str.contains("애니메이션")]
    st.write(f"👶 총 {len(kids_movies)}편의 애니메이션 영화가 있습니다.")
    st.dataframe(kids_movies[["영화제목", "평점", "국가", "러닝타임"]].sort_values(by="평점", ascending=False).head(20))

    fig = px.bar(kids_movies.sort_values("평점", ascending=False).head(10),
                 x="평점", y="영화제목", orientation="h", color="국가",
                 title="어린이 추천 애니메이션 TOP 10")
    st.plotly_chart(fig, use_container_width=True)

# 📊 탭3: 장르별 상관관계 분석 (애니/드라마/코미디 비중과 평점)
with tab3:
    st.subheader("장르별 영화와 평점 관계 보기")

    def genre_flag(genre_str, keyword):
        return int(keyword in genre_str)

    df["is_애니메이션"] = df["장르"].apply(lambda x: genre_flag(x, "애니메이션"))
    df["is_드라마"] = df["장르"].apply(lambda x: genre_flag(x, "드라마"))
    df["is_코미디"] = df["장르"].apply(lambda x: genre_flag(x, "코미디"))

    genre_df = df[["평점", "is_애니메이션", "is_드라마", "is_코미디"]]

    st.write("🎯 선택 장르 여부와 평점 간의 관계:")
    st.dataframe(genre_df.corr())

    fig = px.scatter(df, x="is_코미디", y="평점", color="is_드라마",
                     title="드라마/코미디 여부에 따른 평점 분포")
    st.plotly_chart(fig, use_container_width=True)
