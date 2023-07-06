import os.path
import streamlit as st
import openai
import loadInput
import loadWholeUserInput
import re

OPENAI_API_KEY = st.secrets["openai_api_key"]
openai.api_key = OPENAI_API_KEY


st.title("华鑫人工智能标书系统")
st.header("价格计算检查功能")

answer_start_page = 0
answer_end_page = 0

answer_path = ''

uploaded_file_2 = st.file_uploader("请上传投标文件", type='pdf')

if uploaded_file_2 is not None:
    path2 = os.path.join('.', uploaded_file_2.name)
    answer_path = path2
    with open(path2, 'wb') as f:
        f.write(uploaded_file_2.getbuffer())

    st.write("上传完成")

    docs2, _ = loadWholeUserInput.contruct_prompt(path2, 1, 10)

    if docs2 is not None:
        conversation = [{'role': 'user', 'content': "这是一个投标文件：" + "\n" + docs2},
                        {'role': 'assistant', 'content': "请问一些关于这个投标文件的问题"},
                        {'role': 'user', 'content': "投标函在第几页到第几页，只需回答两个数字"},
                        {'role': 'assistant', 'content': "6, 7"},
                        {'role': 'user', 'content': "分项价目表在第几页到第几页，只需回答两个数字"}]
        response = openai.ChatCompletion.create(
            model='gpt-3.5-turbo-16k-0613',
            messages=conversation
        )
        answer = response.choices[0].message.content
        numbers = re.findall(r'\d+', answer)
        answer_start_page = list(map(int, numbers))[0]
        answer_end_page = list(map(int, numbers))[1]
        print(answer_start_page, answer_end_page)

if answer_path != '':
    question2, _ = loadWholeUserInput.contruct_prompt(answer_path, answer_start_page, answer_end_page)
    print(question2)
    if question2 is not None:
        conversation = [{'role': 'user', 'content': "这是我的投标文件中的分项价目表的部分，请找到帮我检查其中是否有金额或者总计计算错误的地方：" + "\n" + question2}]
        response = openai.ChatCompletion.create(
            model='gpt-3.5-turbo-16k-0613',
            messages=conversation
        )
        answer = response.choices[0].message.content
        st.subheader("以下是分项报价表中金额计算可能有错误的地方：")
        st.write(answer)
