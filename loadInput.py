# Input： Long text bid requirement
# Return: Whole bid requirement text
import PyPDF2


def get_page_number(file_path):
    # 打开文件
    pdf_file_obj = open(file_path, 'rb')
    # 创建一个PDF阅读器对象
    pdf_reader = PyPDF2.PdfReader(pdf_file_obj)
    # 获取PDF文件的页数
    num_pages = len(pdf_reader.pages)
    return num_pages


def read_pdf_file(file_path, start_page, end_page):
    # 打开文件
    pdf_file_obj = open(file_path, 'rb')
    # 创建一个PDF阅读器对象
    pdf_reader = PyPDF2.PdfReader(pdf_file_obj)
    # 初始化一个空字符串，用于存储文本
    texts = ''
    # words_num = 0
    # 遍历每一页，获取文本
    for page in range(start_page, end_page):
        page_obj = pdf_reader.pages[page]
        # if page == 70:
        #     text = page_obj.extract_text() + "\n招标文本提供完毕"
        # else:
        #     text = page_obj.extract_text() + "\n招标要求文本还没有输入完毕，不需要回答"
        text = page_obj.extract_text()
        text = text[2:]
        # if len(text) > 850:
        #     text1 = text[0: len(text)//2]
        #     text2 = text[len(text)//2:]
        #     texts.append(text1)
        #     texts.append(text2)
        # else:
        #     texts.append(text)
        texts = texts + text
        # texts.append(text)
    # 关闭文件
    pdf_file_obj.close()
    return texts, len(texts)


def contruct_prompt(file_path, start_page, end_page):
    pdf_texts, words_num = read_pdf_file(file_path, start_page, end_page)
    # pdf_texts.insert(0, "请帮我缩短这段招标要求的文本的字数，但是不能丢失其中的技术细节信息，只需要输出缩短后的版本")
    return pdf_texts, words_num


# 测试功能
if __name__ == "__main__":
    file_path = "./招标文件.pdf"
    prompts, words_num = contruct_prompt(file_path)
    # print(prompts)
    # print(type(prompts))
    # # for prompt in prompts:
    # #     print(prompt)
    # print(words_num)



