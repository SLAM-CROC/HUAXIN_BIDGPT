# Input： Long text bid text which need to be checked
# Return: Whole user bid text input
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
    # 获取PDF文件的页数
    num_pages = len(pdf_reader.pages)
    # 初始化一个空字符串，用于存储文本
    texts = ''
    # 遍历每一页，获取文本
    for page in range(start_page, end_page):
        page_obj = pdf_reader.pages[page]
        text = page_obj.extract_text()
        # 假设每页有100行，我们只想要第10到90行
        lines = text.split('\n')
        lines_without_header_and_footer = lines[3:-1]

        # 将结果重新组合成一个字符串
        result = '\n'.join(lines_without_header_and_footer)
        # if page == 30:
        #     text = result + "\n投标文本提供完毕"
        # else:
        #     text = result + "\n投标文本还没有输入完毕，不需要回答"
        texts = texts + result

    # 关闭文件
    pdf_file_obj.close()
    return texts, len(texts)


def contruct_prompt(file_path, start_page, end_page):
    pdf_texts, words_number = read_pdf_file(file_path, start_page, end_page)
    # pdf_texts.insert(0, "我将分段为你提供投标文本，不需要回答，投标文本输入完毕时我会提示你，你需要在投标文本输入完毕时帮我总结我的投标文本")
    return pdf_texts, words_number


# 测试功能
if __name__ == "__main__":
    file_path = "./投标文件.pdf"
    prompts, words_number = contruct_prompt(file_path)
    print(prompts)
    print(words_number)
    # for prompt in prompts:
    #     print(prompt)

