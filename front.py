import streamlit as st
import requests


st.title('Student Performance')

api_url = 'http://127.0.0.1:8000/predict/'

gender = st.selectbox('Пол', ['male', 'female'])
race_ethnicity = st.selectbox('этническая группа', ['group B', 'group C', 'group D', 'group E'])
parental_level_of_education = st.selectbox('образования родителей', ["bachelor's degree", 'high school',
                                                                     "master's degree", 'some college', 'some high school'])
lunch = st.selectbox('обед', ['standard', 'free/reduced'])
test_preparation = st.selectbox('подготовка к тесту', ['none', 'completed'])
match_score = st.number_input('оценка по математики', min_value=0, max_value=100, step=1)
reading_score = st.number_input('оценка по чтению', min_value=0, max_value=100, step=1)

student_data = {
    "gender": gender,
    "race_ethnicity": race_ethnicity,
    "parental_level_of_education": parental_level_of_education,
    "lunch": lunch,
    "test_preparation": test_preparation,
    "match_score": match_score,
    "reading_score": reading_score,
}

if st.button('Проверка'):
    try:
        answer = requests.post(api_url, json=student_data, timeout=10)
        if answer.status_code == 200:
            result = answer.json()
            st.json(result)
        else:
            st.error(f'Ошибка: {answer.status_code}')
    except requests.exceptions.RequestException as e:
        st.error(f'Не удалось подключиться к API: {e}')