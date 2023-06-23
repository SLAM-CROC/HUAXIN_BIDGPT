import os.path
import streamlit as st
import openai
import loadInput
import loadWholeUserInput

OPENAI_API_KEY = st.secrets["openai_api_key"]
openai.api_key = OPENAI_API_KEY


st.title("BIDGPT招投标文件对比检测功能")

with st.container():
    input_requirement = ''
    user_input = ''
    uploaded_file = st.file_uploader("请上传招标文件", type='pdf')

    if uploaded_file is not None:
        path = os.path.join('.', uploaded_file.name)
        with open(path, 'wb') as f:
            f.write(uploaded_file.getbuffer())

        st.write("上传完成")
        page_number = loadInput.get_page_number(path)

        values = st.slider(
            '选择招标文件范围',
            0, page_number, (int(page_number/3), int(page_number*2/3)))
        start_page = values[0]
        end_page = values[1]
        st.write('所选范围：', start_page, '--', end_page, '页')

        docs, words_number = loadInput.contruct_prompt(path, start_page, end_page)
        input_requirement = docs

        uploaded_file2 = st.file_uploader("请上传投标文件", type='pdf')

        if uploaded_file2 is not None:
            path2 = os.path.join('.', uploaded_file2.name)
            with open(path2, 'wb') as f2:
                f2.write(uploaded_file2.getbuffer())

            st.write("上传完成")
            page_number2 = loadWholeUserInput.get_page_number(path2)

            values2 = st.slider(
                '选择投标文件范围',
                0, page_number2, (int(page_number2 / 3), int(page_number2 * 2 / 3)))
            start_page2 = values2[0]
            end_page2 = values2[1]
            st.write('所选范围：', start_page2, '--', end_page2, '页')

            if st.button('对比检测'):
                docs2, words_number2 = loadWholeUserInput.contruct_prompt(path2, start_page2, end_page2)
                user_input = docs2
                if input_requirement is not None and user_input is not None:
                    conversation = [{'role': 'user', 'content': "这是一个招标要求文件的一部分：" + "\n" + input_requirement},
                                    {'role': 'assistant', 'content': "好的，请输入您与这部分招标要求对应的投标部分"},
                                    {'role': 'user', 'content': "这是与之对应的投标部分：" + "\n" + user_input + "\n请根据招标要求，查找投标文件中的错误，重点查看设备型号是否符合招标要求中的型号，时间是否和招标要求时间一致，金额是否计算正确"}]
                    response = openai.ChatCompletion.create(
                        model='gpt-3.5-turbo-16k-0613',
                        messages=conversation
                    )
                    answer = response.choices[0].message.content
                    st.write(answer)


