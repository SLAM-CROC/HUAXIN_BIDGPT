import os.path
import streamlit as st
import openai
import loadWholeUserInput

OPENAI_API_KEY = st.secrets["openai_api_key"]
openai.api_key = OPENAI_API_KEY


st.title("BIDGPT投标文件检查功能")

with st.container():
    uploaded_file = st.file_uploader("选择您想要检查的投标文件", type='pdf')

    if uploaded_file is not None:
        path = os.path.join('.', uploaded_file.name)
        with open(path, 'wb') as f:
            f.write(uploaded_file.getbuffer())

        st.write("上传完成")
        # docs = load_pdf(path)
        page_number = loadWholeUserInput.get_page_number(path)

        values = st.slider(
            '选择想要查询的招标文件范围',
            0, page_number, (int(page_number/3), int(page_number*2/3)))
        start_page = values[0]
        end_page = values[1]
        st.write('所选范围：', start_page, '--', end_page, '页')

        docs, words_number = loadWholeUserInput.contruct_prompt(path, start_page, end_page)

        question = st.text_input("输入问题：")
        if docs is not None and question is not None and question != '':
            conversation = [{'role': 'user', 'content': "这是一个投标文件：" + "\n" + docs},
                            {'role': 'assistant', 'content': "请输入您想要检查的内容"},
                            {'role': 'user', 'content': question}]
            response = openai.ChatCompletion.create(
                model='gpt-3.5-turbo-16k-0613',
                messages=conversation
            )
            answer = response.choices[0].message.content
            st.write(answer)


