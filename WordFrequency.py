import os
import re
from collections import Counter
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from docx import Document

# 确保已经下载了nltk的数据
import nltk
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('stopwords')

# 初始化词形还原器
lemmatizer = WordNetLemmatizer()

# 指定Word文档所在的目录和输出日志文件的路径
word_dir = r'D:\Coding\WorkSpace\PythonWorkSpace\PySpider'
log_path = r'D:\Coding\WorkSpace\PythonWorkSpace\PySpider\result.log'

# 用于存储所有文档的单词频次
total_word_freq = Counter()

# 遍历目录中的所有Word文档
for filename in os.listdir(word_dir):
    if filename.endswith('.docx'):
        file_path = os.path.join(word_dir, filename)
        doc = Document(file_path)
        text = []

        # 读取文档内容
        for para in doc.paragraphs:
            # 移除标点符号并转换为小写
            clean_text = re.sub(r'[^\w\s]', '', para.text).lower()
            text.append(clean_text)

        # 合并所有段落的文本
        full_text = ' '.join(text)

        # 分词
        words = word_tokenize(full_text)

        # 词形还原
        lemmatized_words = [lemmatizer.lemmatize(word) for word in words]

        # 更新总的单词频次计数器
        total_word_freq.update(lemmatized_words)

# 将结果写入日志文件
with open(log_path, 'w', encoding='utf-8') as log_file:
    for word, freq in total_word_freq.most_common():
        log_file.write(f"{word}: {freq}\n")

print(f"Word frequency has been written to {log_path}")