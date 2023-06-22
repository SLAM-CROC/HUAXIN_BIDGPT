# Input： Long text bid text which need to be checked
# Return: Segments list of long text bid text with prompt header and tail
import PyPDF2


def read_pdf_file(file_path):
    # 打开文件
    pdf_file_obj = open(file_path, 'rb')
    # 创建一个PDF阅读器对象
    pdf_reader = PyPDF2.PdfReader(pdf_file_obj)
    # 初始化一个空字符串，用于存储文本
    texts = []
    # 遍历每一页，获取文本
    for page in range(12, 31):
        page_obj = pdf_reader.pages[page]
        text = page_obj.extract_text()
        # 假设每页有100行，我们只想要第10到90行
        lines = text.split('\n')
        lines_without_header_and_footer = lines[3:-1]

        # 将结果重新组合成一个字符串
        result = '\n'.join(lines_without_header_and_footer)
        if page == 30:
            text = result + "\n投标文本提供完毕"
        else:
            text = result + "\n投标文本还没有输入完毕，不需要回答"
        texts.append(text)


    # 关闭文件
    pdf_file_obj.close()
    return texts


def contruct_prompt(file_path):
    pdf_texts = read_pdf_file(file_path)
    pdf_texts.insert(0, "我将分段为你提供投标文本，不需要回答，投标文本输入完毕时我会提示你，你需要在投标文本输入完毕时帮我总结我的投标文本")
    return pdf_texts


# 测试功能
if __name__ == "__main__":
    file_path = "./投标文件.pdf"
    prompts = contruct_prompt(file_path)
    print(len(prompts))
    for prompt in prompts:
        print(prompt)

