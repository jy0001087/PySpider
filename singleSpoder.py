from bs4 import BeautifulSoup
import requests

# 获取网页内容
url = "https://www.soymilk.eu.org/2023/09/727.html?zx=9dee3ba44198193a"
response = requests.get(url)
html_content = response.content

# 使用BeautifulSoup解析HTML内容
soup = BeautifulSoup(html_content, 'html.parser')

# 提取所有<p>元素中的正文部分
p_texts = [p.get_text() for p in soup.find_all('p')]

# 打印提取的正文内容
for text in p_texts:
    print(text)