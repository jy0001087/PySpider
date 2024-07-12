from bs4 import BeautifulSoup
import requests
from opencc import OpenCC

# 初始化转换器
# s2t: Simplified Chinese to Traditional Chinese
# t2s: Traditional Chinese to Simplified Chinese
cc_t2s = OpenCC('t2s')

# 获取网页内容
url = "https://www.soymilk.eu.org/2023/09/727.html?zx=9dee3ba44198193a"
response = requests.get(url)
html_content = response.content

# 使用BeautifulSoup解析HTML内容
soup = BeautifulSoup(html_content, 'html.parser')

# 提取所有<p>元素中的正文部分
p_texts = [p.get_text() for p in soup.find_all('p')]

# 翻译文本为简体中文，并在每个翻译后的文本开头加两个中文空格
translated_texts = ['\u3000\u3000' + cc_t2s.convert(text) for text in p_texts]

# 将翻译后的文本输出到D盘根目录下的文件中
with open("D:/translated_texts.txt", "w", encoding='utf-8') as file:
    for text in translated_texts:
        file.write(text + '\n')

print("翻译完成，文件已保存到D盘根目录下。")