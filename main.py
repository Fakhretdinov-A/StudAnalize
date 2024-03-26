import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from PIL import Image


def print_dependance_on_part_time_job():
    st.subheader('2. Средняя успеваемость в зависимости от наличия трудоустройства')
    employed_mean_mark = np.mean(dataframe[(dataframe['part_time_job'] == 1)]['mean_mark'])
    unemployed_mean_mark = np.mean(dataframe[(dataframe['part_time_job'] == 0)]['mean_mark'])
    df = pd.DataFrame({'Трудоустройство': ["Нет", "Да"],
                       'Средняя оценка': [unemployed_mean_mark, employed_mean_mark]})

    fig = px.bar(df, x='Трудоустройство', y='Средняя оценка')
    fig.update_yaxes(range=[75, 85])
    st.plotly_chart(fig)

    st.write("Анализируя данный график, можно сделать однозначный вывод,"
             "что успеваемость студентов с трудоустройством на порядок ниже, чем у тех, у кого её нет.")


def print_sootnoshenie_job():
    st.subheader('3. Соотношение трудоустроенных и безработных студентов')
    df = pd.DataFrame({'Трудоустройство': ["Нет", "Да"],
                       'Количество студентов': [len(dataframe[(dataframe['part_time_job'] == 0)]),
                                                len(dataframe[(dataframe['part_time_job'] == 1)])]})
    fig = px.pie(df, values='Количество студентов', names='Трудоустройство')
    st.plotly_chart(fig)
    st.write("Подавляющее большинство студентов не работает.")


def print_career_aspiration():
    st.subheader('4. Соотношение планируемых сфер деятельности')
    careers = dataframe['career_aspiration'].unique()
    nums = [len(dataframe[(dataframe['career_aspiration'] == i)]) for i in careers]

    df = pd.DataFrame({'Профессия': dataframe['career_aspiration'].unique(),
                       'Количество студентов': nums})
    fig = px.pie(df, values='Количество студентов', names='Профессия')
    st.plotly_chart(fig)
    st.write("Подавляющее большинство студентов планируют работать в сфере ИТ или открыть собственный бизнес")


def print_weekly_self_study_hours():
    st.subheader('5. График количества студентов и затрачиваемых ими часов на самообразование')

    bins = [0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50]
    labels = ['0-5', '5-10', '10-15', '15-20', '20-25', '25-30', '30-35', '35-40', '40-45', '45-50']
    dataframe['interval'] = pd.cut(dataframe['weekly_self_study_hours'], bins=bins, labels=labels, right=False)
    counts = dataframe['interval'].value_counts().sort_index()
    print(counts)
    fig = px.bar(x=counts.index, y=counts.values, labels={'x': 'Количество часов', 'y': 'Количество студентов'})
    st.plotly_chart(fig)


def print_dependance_on_sex():
    st.subheader('1. Средняя успеваемость по полу и отдельно взятым дициплинам')

    men_df = dataframe[(dataframe['gender'] == 'male')]
    men_mean_marks = {}
    for i in dict_subjects.values():
        men_mean_marks[i] = np.mean(men_df[i])

    women_df = dataframe[(dataframe['gender'] == 'female')]
    women_mean_marks = {}
    for i in dict_subjects.values():
        women_mean_marks[i] = np.mean(women_df[i])

    selection = st.multiselect("Выберете нужные дисциплины:",
                               ["Математика", "История", "Физика", "Химия", "Биология", "Английский язык", "География"])

    df = pd.DataFrame({'Дисциплина': selection * 2,
                       'Пол': ['Мужчины'] * len(selection) + ['Женщины'] * len(selection),
                       'Оценка': list(men_mean_marks[dict_subjects[i]] for i in selection) + list(
                           women_mean_marks[dict_subjects[i]] for i in selection)})

    fig = px.bar(df, x='Дисциплина', y='Оценка', color='Пол', barmode='group',
                 title='Средние оценки по предметам для мужчин и женщин')

    fig.update_yaxes(range=[75, 85])
    st.plotly_chart(fig)

    st.write("Анализируя данный график, можно сделать вывод,"
             " что в большинстве случаев успеваемость девушек выше успеваемости юношей,"
             " однако парни показывают лучшие результаты в точных науках.")


csv = pd.read_csv('student-scores.csv')
dataframe = pd.DataFrame(csv)

keys = csv.keys()
dict_subjects = {"Математика": 'math_score', "История": 'history_score', "Физика": 'physics_score',
                 "Химия": 'chemistry_score', "Биология": 'biology_score', "Английский язык": 'english_score',
                 "География": 'geography_score'}

dataframe['mean_mark'] = dataframe[dict_subjects.values()].mean(axis=1)

st.title("Анализ успеваемости студентов")

image = Image.open("data/image.jpeg")
st.image(image)

st.text('В решении используются следующие данные:')
st.dataframe(dataframe)


if st.button("Отобразить среднюю успеваемость по полу и отдельно взятым дициплинам"):
    print_dependance_on_sex()

if st.button("Отобразить среднюю успеваемость в зависимости от наличия трудоустройства"):
    print_dependance_on_part_time_job()

if st.button("Отобразить соотношение трудоустроенных и безработных студентов"):
    print_sootnoshenie_job()

if st.button("Отобразить соотношение планируемых сфер деятельности"):
    print_career_aspiration()

if st.button("Отобразить график количества студентов и затрачиваемых ими часов на самообразование"):
    print_weekly_self_study_hours()
