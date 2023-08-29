import os.path
import streamlit as st
import openai
import loadInput
import loadWholeUserInput
import re

OPENAI_API_KEY = st.secrets["openai_api_key"]
openai.api_key = OPENAI_API_KEY


st.title("华鑫人工智能标书系统")
st.header("分项报价表检测功能")

target_start_page = 0
target_end_page = 0
answer_start_page = 0
answer_end_page = 0

target_path = ''
answer_path = ''

uploaded_file_1 = st.file_uploader("请上传招标文件", type='pdf')

if uploaded_file_1 is not None:
    path1 = os.path.join('.', uploaded_file_1.name)
    target_path = path1
    with open(path1, 'wb') as f:
        f.write(uploaded_file_1.getbuffer())

    st.write("上传完成")

    docs1, _ = loadInput.contruct_prompt(path1, 1, 10)

    if docs1 is not None:
        conversation = [{'role': 'user', 'content': "这是一个招标要求文件：" + "\n" + docs1},
                        {'role': 'assistant', 'content': "请问一些关于这个招标要求文件的问题"},
                        {'role': 'user', 'content': "招标公告在第几页到第几页，只需回答两个数字"},
                        {'role': 'assistant', 'content': "2, 3"},
                        {'role': 'user', 'content': "供货要求等技术细节在第几页到第几页，只需回答两个数字"}]
        response = openai.ChatCompletion.create(
            model='gpt-3.5-turbo-16k-0613',
            messages=conversation
        )
        answer = response.choices[0].message.content
        numbers = re.findall(r'\d+', answer)
        target_start_page = list(map(int, numbers))[0]
        target_end_page = list(map(int, numbers))[1]

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

if target_path != '' and answer_path != '':
    question1, _ = loadInput.contruct_prompt(target_path, target_start_page, target_end_page)
    question2, _ = loadWholeUserInput.contruct_prompt(answer_path, answer_start_page, answer_end_page)

    if question1 is not None and question2 is not None:
        conversation = [{'role': 'user', 'content': "这是招标要求中的供货要求等技术细节，我需要你根据这个供货要求等技术细节检查我的分项价目表是否有错误：" + "\n" + question1},
                        {'role': 'assistant', 'content': "好的，请提供投标文件中的分项价目表"},
                        {'role': 'user', 'content': "这是投标文件中的分项价目表，请根据招标供货要求，找到分项价目表中各设备型号不符合招标要求的地方" + "\n" + question2}]
        response = openai.ChatCompletion.create(
            model='gpt-4-32k',
            messages=conversation
        )
        answer = response.choices[0].message.content
        st.subheader("以下是分项报价表中可能有错误的地方：")
        st.write(answer)
