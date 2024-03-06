### 简介

本代码可以自动连接OpenAI的API并翻译、润色英文文献。适用于Latex格式的文献文本。方便将自己已发表的论文翻译为学位论文。

### 环境要求

1. 根据requirements.txt配置python环境。
2. 注册一个OpenAI账号，并申请API密钥。保证自己有使用额度。
3. 国内用户需要开启代理，并设置代理软件打开代理端口。

### 使用

1. 在main.py文件中填写OpenAI API密钥和代理地址。

   ```python
   os.environ["OPENAI_API_KEY"] = "****" # 星号是自己的API密钥; 将密钥加入至环境变量
   os.environ["http_proxy"] = "http://127.0.0.1:7890"
   os.environ["https_proxy"] ="http://127.0.0.1:7890"
   ```

2. 复制文献文本到 original.txt

3. 运行main.py，翻译后的文本在translated.txt，润色后的文本在polished.txt。再次运行前需要删除这两个txt文件。

### 存在问题

1. 容易漏输出一些插图代码。 
2. 公式和插图代码较多时，token不能有效限制，输出结果容易超出chatGPT最大输出行数而导致漏内容。
3. 一些label会被删除。
4. 建议将 polished.txt 与 original.txt 对比后再使用。
