# Docker 생성 시
## Docker 경로
### mkdir my-container

## Dockerfile 작성
### Dockerfile 내 vim / 등등 apt install 수행
### pip requirements 작성 및 멈춤
### 데이터 변화 감지 설정

## Docker 빌드 및 실행 m1 -> arm64 배포 고려 필요
### docker build -t streamlit-dashboard .
### docker build --platform linux/amd64 -t streamlit-dashboard .

### docker run -p 8501:8501 -v $(pwd):/app streamlit-dashboard
### docker run --platform linux/amd64 -p 8501:8501 -v $(pwd):/app streamlit-dashboard


###-------------------------------------------------------------------------
# Docker 배포 시
## Docker 이미지 파일 생성
### docker commit <컨테이너_ID> <이미지_이름>
### docker save -o <저장할_경로>/image.tar <이미지_이름>

## Docker 이미지 이동 & load
###scp ./my_image.tar <사용자명>@<오프라인_서버_IP>:<저장_경로>
###docker load -i <이미지_파일_경로>/image.tar

## Docker 실행
###docker run -p 8501:8501 -v $(pwd):/app streamlit-dashboard

## 폴더 설정
###
import streamlit as st
import pandas as pd
import os
import time
import csv
import json
import gtts


# 페이지 구성 레이아웃 설정
st.set_page_config(layout="wide", initial_sidebar_state="collapsed")

# 새로고침 간격 설정 (3초)
refresh_interval = 3

# 사이드바에 레이아웃 고정 여부 선택 옵션 추가
st.sidebar.title("Layout Selector")
layout_option = st.sidebar.selectbox(
    "Choose a layout to fix or let it toggle:",
    ("Auto toggle", "Layout 1", "Layout 2")
)
st.markdown("""
    <style>
    .title-container {
        display: flex;
        align-items: center;
        justify-content: center;
        margin-bottom: 20px;
    }
    .title-image {
        width: 50px;
        height: 50px;
        margin-right: 10px;
    }
    .title-text {
        font-size: 48px;
        font-weight: bold;
        color: #A9A9A9;
        text-shadow: 2px 2px 5px black;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("""
    <style>
    .title {
        font-size: 48px;
        font-weight: bold;
        color: ##F5D0A9;
        text-shadow: 2px 2px 5px black;
        text-align: center;
    }
    .section {
        background-color: #1E1E1E;
        border-radius: 10px;
        padding: 20px;
        box-shadow: 2px 2px 12px rgba(0, 0, 0, 0.5);
        margin-bottom: 20px;
    }
    .card {
        background-color: #262626;
        border-radius: 10px;
        padding: 3px;
        box-shadow: 3px 3px 8px rgba(0, 0, 0, 0.7);
        overflow-x: auto;
        overflow-y: auto;
    }
    .main-title {
        font-size: 48px;
        font-weight: bold;
        color: #A9A9A9;
        text-align: center;
    }
    .ai {
        color: #A9A9A9;
    }
    .anomaly {
        color: #00A9E0;
    }
    .special-o {
        display: inline-block;
        color: #00A9E0;
        font-size: 0.9em;
        border: 4px solid #00A9E0;
        border-radius: 50%;
        width: 1em;
        height: 1em;
        text-align: center;
        line-height: 0.9em;
        font-weight: bold;
        position: relative;
        top: 0.1em;
    }
    .subtitle {
        font-size: 20px;
        color: #00A9E0;
        text-align: center;
        margin-top: -5px;
        margin-bottom: 50px;
    }
    .joke {
        font-size: 14px;
        font-style: italic;
        color: #FFD700;
        text-align: center;
        margin-top: -5px;
    }
    </style>
""", unsafe_allow_html=True)

# 메인 타이틀 출력
st.markdown('<div class="main-title"><span class="ai">AI</span> <span class="anomaly">An<span class="special-o">O</span>maly Dashboard</span></div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">By 무선망 AI Analytics 연구팀 </div>', unsafe_allow_html=True)

# 스타일링 추가 (CSS)

# 데이터프레임 로드 함수 (Report 데이터를 로드할 때 사용)
# 데이터프레임 로드 함수 (Report 데이터를 로드할 때 사용)
#@st.cache_data(ttl=refresh_interval)
def load_dataframe():
    file_path = './data/dataframe/your_dataframe.csv'
    if os.path.exists(file_path):
        try:
            with open(file_path, mode='r', encoding='utf-8', errors='replace') as f:
                reader = csv.reader(f)
                data = list(reader)
            columns = data[0]
            df = pd.DataFrame(data[1:], columns=columns)
            return df
        except Exception as e:
            st.error(f"파일을 읽는 중에 오류가 발생했습니다: {e}")
            return pd.DataFrame()  # 오류 발생 시 빈 데이터프레임 반환
    else:
        st.error("데이터 파일이 존재하지 않습니다.")
        return pd.DataFrame({'Column 1': [], 'Column 2': []})

# HTML 파일 로드 함수
#@st.cache_data(ttl=refresh_interval)
def load_report_html_file(file_path):
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    return "<p>File not found</p>"

# HTML 파일 로드 함수
#@st.cache_data(ttl=refresh_interval)
def load_html_file(file_path):
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    return "<p>File not found</p>"

# 시계열 HTML 파일 로드 함수
#@st.cache_data(ttl=refresh_interval)
def load_timeseries_html():
    time_series_dir = './data/timeseries'
    if os.path.exists(time_series_dir):
        return [f for f in os.listdir(time_series_dir) if f.endswith('.html')]
    return []

## History 파일 로드 함수
#def load_history_files():
#    history_path = './history'
#    if not os.path.exists(history_path):
#        os.makedirs(history_path)
#    folders = [f for f in os.listdir(history_path) if os.path.isdir(os.path.join(history_path, f))]
#
#    if folders:
#        selected_folder = st.sidebar.selectbox("Select a folder", folders)
#        if selected_folder:
#            folder_path = os.path.join(history_path, selected_folder)
#            html_files = [f for f in os.listdir(folder_path) if f.endswith('.html')]
#
#            if html_files:
#                selected_file = st.sidebar.selectbox("Select an HTML file", html_files)
#
#                if st.sidebar.button("Show HTML File"):
#                    st.session_state['show_html'] = True
#                    st.session_state['selected_file'] = os.path.join(folder_path, selected_file)
#
#                if 'show_html' in st.session_state and st.session_state['show_html']:
#                    if st.sidebar.button("Close HTML File"):
#                        st.session_state['show_html'] = False
#                    with open(st.session_state['selected_file'], 'r', encoding='utf-8') as file:
#                        html_content = file.read()
#                    st.components.v1.html(html_content, height=600, scrolling=True)
#
#                    # 사용자 평가 입력
#                    st.subheader("Report Ratings")
#
#                    rating = st.slider("별점 (1-5)", 1, 5, 3)
#                    comment = st.text_area("코멘트를 입력하세요")
#
#                    # 평가 저장 기능
#                    if st.button("평가 저장"):
#                        rating_data = {
#                            "rating": rating,
#                            "comment": comment
#                        }
#                        save_path = os.path.join(folder_path, 'ratings.json')
#
#                        # 기존 평가가 있다면 불러오기
#                        if os.path.exists(save_path):
#                            with open(save_path, 'r', encoding='utf-8') as f:
#                                existing_data = json.load(f)
#                        else:
#                            existing_data = {}
#
#                        # 현재 HTML 파일에 대한 평가 추가
#                        existing_data[os.path.basename(st.session_state['selected_file'])] = rating_data
#
#                        # 평가 내용을 JSON 파일로 저장
#                        with open(save_path, 'w', encoding='utf-8') as f:
#                            json.dump(existing_data, f, ensure_ascii=False, indent=4)
#
#                        st.success("평가가 저장되었습니다.")
## 저장된 평가를 확인하는 함수
#def show_all_ratings_by_folder():
#    history_path = './history'
#    all_ratings = {}
#    
#    # history 경로 내의 모든 폴더 탐색
#    for root, dirs, files in os.walk(history_path):
#        for dir in dirs:
#            folder_path = os.path.join(root, dir)
#            rating_file_path = os.path.join(folder_path, 'ratings.json')
#            
#            if os.path.exists(rating_file_path):
#                with open(rating_file_path, 'r', encoding='utf-8') as f:
#                    ratings_data = json.load(f)
#                    all_ratings[dir] = ratings_data
#
#    # 폴더별로 평가를 표시
#    if all_ratings:
#        st.header("Saved Ratings & Comments by Folder")
#        for folder, ratings in all_ratings.items():
#            st.subheader(f"Folder: {folder}")
#            for html_file, rating_info in ratings.items():
#                st.markdown(f"**HTML File:** {html_file}")
#                st.write(f"**Rating:** {rating_info['rating']}")
#                st.write(f"**Comment:** {rating_info['comment']}")
#                st.markdown("---")
#    else:
#        st.write("No ratings found.")
# History 파일 로드 및 평가 입력/저장 함수
# History 파일 로드 및 평가 입력/저장 함수
def load_history_files():
    history_path = './history'
    
    # history 경로가 존재하지 않으면 생성
    if not os.path.exists(history_path):
        os.makedirs(history_path)
    
    # HTML 파일 리스트 가져오기 (파일명이 날짜 형식으로 되어 있음)
    html_files = [f for f in os.listdir(history_path) if f.endswith('_report.html')]
    
    if html_files:
        # 날짜별 파일 선택 (파일명에서 날짜를 추출)
        selected_file = st.sidebar.selectbox("Select a report file", html_files)
        file_date = selected_file.split('_report.html')[0]
        
        if selected_file:
            file_path = os.path.join(history_path, selected_file)
            rating_file_path = os.path.join(history_path, f'{file_date}_rating.json')
            
            # HTML 파일을 열어서 표시
            if st.sidebar.button("Show HTML File"):
                st.session_state['show_html'] = True
                st.session_state['selected_file'] = file_path

            if 'show_html' in st.session_state and st.session_state['show_html']:
                if st.sidebar.button("Close HTML File"):
                    st.session_state['show_html'] = False

                with open(st.session_state['selected_file'], 'r', encoding='utf-8') as file:
                    html_content = file.read()
                st.components.v1.html(html_content, height=600, scrolling=True)

                # 기존에 저장된 평가가 있다면 표시
                st.subheader(f"Report Ratings for {file_date}")
                existing_data = {}
                if os.path.exists(rating_file_path):
                    with open(rating_file_path, 'r', encoding='utf-8') as f:
                        existing_data = json.load(f)

                # 기존 평가 보여주기
                existing_rating = existing_data.get("rating", "No rating yet")
                existing_comment = existing_data.get("comment", "No comment yet")
                st.write(f"**Existing Rating:** {existing_rating}")
                st.write(f"**Existing Comment:** {existing_comment}")
                st.markdown("---")

                # 사용자 평가 입력
                rating = st.slider("별점 (1-5)", 1, 5, 3)
                comment = st.text_area("코멘트를 입력하세요")

                # 평가 저장 기능
                if st.button("평가 저장"):
                    rating_data = {
                        "rating": rating,
                        "comment": comment
                    }

                    # 현재 HTML 파일에 대한 평가 추가
                    with open(rating_file_path, 'w', encoding='utf-8') as f:
                        json.dump(rating_data, f, ensure_ascii=False, indent=4)

                    st.success(f"평가가 {file_date} 파일에 저장되었습니다.")
    else:
        st.sidebar.write("No HTML files found in history path.")


# 모든 저장된 평가를 한 번에 확인하는 함수
def show_all_ratings_by_folder():
    history_path = './history'
    all_ratings = {}
    
    # history 경로 내의 모든 rating.json 파일 탐색
    for file in os.listdir(history_path):
        if file.endswith('_rating.json'):
            rating_file_path = os.path.join(history_path, file)
            date_key = file.split('_rating.json')[0]

            # rating.json 파일이 있으면 데이터를 읽어옴
            if os.path.exists(rating_file_path):
                with open(rating_file_path, 'r', encoding='utf-8') as f:
                    ratings_data = json.load(f)
                    all_ratings[date_key] = ratings_data

    # 날짜별로 평가를 표시
    if all_ratings:
        st.header("Saved Ratings & Comments by Date")
        for report_date, rating_info in all_ratings.items():
            st.subheader(f"Report Date: {report_date}")
            rating_value = rating_info.get('rating', "No rating available")
            comment_value = rating_info.get('comment', "No comment available")
            st.write(f"**Rating:** {rating_value}")
            st.write(f"**Comment:** {comment_value}")
            st.markdown("---")
    else:
        st.write("No ratings found.")
# 레이아웃 함수 예시 (이 부분은 유지하되 레이아웃 변경 생략)
def layout_1(placeholder):
    # 모든 요소를 새로 그리기 전에 비워줍니다.
#    placeholder.empty()
    
#    with placeholder.container():
    left, right = st.columns([1, 1.33])

    with left:
        st.header("Anomaly Node")
        html_content = load_html_file('./data/main_graph/main_graph.html')
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.components.v1.html(html_content, height=500, scrolling=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with right:
        st.header("Sum of Abnormal Node")
        time_series_files = load_timeseries_html()
        if len(time_series_files) == 0:
            st.write("시계열 그래프가 없습니다.")
        else:
            for ts_file in time_series_files:
                file_path = f'./data/timeseries/{ts_file}'
                ts_html = load_html_file(file_path)
                st.markdown('<div class="card">', unsafe_allow_html=True)
                st.components.v1.html(ts_html, height=200, scrolling=True)
                st.markdown('</div>', unsafe_allow_html=True)

# 레이아웃 2: Report와 Anomaly Node 표시
def layout_2(placeholder):
    
#    with placeholder.container():
    left, right = st.columns([1, 1.33])
    with left:
        st.header("Anomaly Node")
        html_content = load_html_file('./data/main_graph/main_graph.html')
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.components.v1.html(html_content, height=500, scrolling=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
#    with right:
#        st.header("Report")
#        df = load_dataframe()
#        st.markdown('<div class="card">', unsafe_allow_html=True)
#        st.dataframe(df, height=500)
#        st.markdown('</div>', unsafe_allow_html=True)
## load_report_html_file

    with right:
        st.header("Report")
        html_content = load_html_file('./data/main_graph/main_graph.html')
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.components.v1.html(html_content, height=500*1.3, scrolling=True)
        st.markdown('</div>', unsafe_allow_html=True)
# Auto toggle 모드에서 레이아웃을 교차적으로 보여줌
def auto_toggle(placeholder):
    while True:
        current_time = int(time.time())  # 현재 시간을 초 단위로 가져옴
        layout_version = current_time % 2  # 짝수/홀수에 따라 레이아웃 선택

        # 레이아웃 전환
        if layout_version == 0:
            layout_1(placeholder)
        else:
            layout_2(placeholder)

        # 주기적으로 갱신
        time.sleep(refresh_interval)
        st.rerun()

# 메인 부분의 콘텐츠를 초기화할 수 있는 placeholder 생성
placeholder = st.empty()

# 주기적으로 두 레이아웃을 번갈아 보여주거나, 사용자가 선택한 레이아웃 고정
if layout_option == "Auto toggle":
    auto_toggle(placeholder)  # Auto toggle 모드에서 주기적으로 레이아웃 변경
elif layout_option == "Layout 1":
    layout_1(placeholder)
elif layout_option == "Layout 2":
    layout_2(placeholder)

# 사이드바에 History 탭 추가
st.sidebar.title("History")
load_history_files()

# 저장된 평가를 한 번에 확인할 수 있는 옵션 추가
if st.sidebar.checkbox("Show All Ratings"):
    show_all_ratings_by_folder()
