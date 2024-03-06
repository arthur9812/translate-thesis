##################
# Copyright: Yueheng Li
# Time: 2024.3.6
# Free to share.
##################

import os
from openai import OpenAI
import tiktoken

os.environ["OPENAI_API_KEY"] = "****" # 星号是自己的API密钥; 将密钥加入至环境变量
os.environ["http_proxy"] = "http://127.0.0.1:7890"                # 指定代理，解决连接问题
os.environ["https_proxy"] = "http://127.0.0.1:7890"               # 指定代理，解决连接问题

client = OpenAI()
model = 'gpt-3.5-turbo'
encoding = tiktoken.encoding_for_model(model)

def process(mode):
  if mode == 'translate':
    input_f = 'original.txt'
    output_f = 'translated.txt'
    system = 'You are good at translating English to Chinese.'
    prompts = 'Translate the paragraphs to Chinese. Keep all the latex code as the original. Do not answer other words. This is the paragraphs:\n'
  elif mode == 'polish':
    input_f = 'translated.txt'
    output_f = 'polished.txt'
    system = '你是一个善于润色中文硕士学位论文的教授。'
    prompts = '我正在写我的中文硕士毕业论文，我之前发表过一些中文论文。请你帮我把他们润色一下，使他们达到中文硕士毕业论文的标准。要求：1.保证语法正确和用词恰达。提升表达清晰度。' \
              '2.里面的latex代码无需翻译并保持原样输出。尤其是begin{figure}和end{figure}之间的内容。3.仅输出润色结果，不要输出其他无关的话。以下是我之前写的论文：\n'
  else:
    raise RuntimeError('Wrong mode.')

  fopen = open(input_f, 'r', encoding='utf-8')
  token_count = 0
  tokens = 0
  message = ""
  paragraph = ""
  with open(output_f, 'x', encoding='utf-8') as f:
    for line in fopen.readlines():  # 按行读取text中的内容
      if line.isspace() or line.strip()[0] == '%': # 空行和注释行
        if tokens == 0:
          continue
        if token_count + tokens > 1000: # 每次prompt最大数量，避免超出token界限
          completion = client.chat.completions.create(
            model=model,
            messages=[
              {"role": "system", "content": system},
              {"role": "user", "content": prompts + message}
            ]
          )
          print('\nmessage:\n', message)
          print('\nchatgpt:\n', completion.choices[0].message.content)
          f.write(completion.choices[0].message.content)
          f.write('\r\n')
          f.flush()
          token_count = tokens
          message = paragraph + '\n'
        else:
          token_count += tokens
          message = message + paragraph + '\n'
        tokens = 0
        paragraph = ""
      else:
        tokens += len(encoding.encode(line))
        paragraph = paragraph + line

    message = message + paragraph + '\n'
    completion = client.chat.completions.create(
      model="gpt-3.5-turbo",
      messages=[
        {"role": "system", "content": system},
        {"role": "user", "content": prompts + message}
      ]
    )
    print(completion.choices[0].message.content)
    f.write(completion.choices[0].message.content + '\n')
    f.flush()


def main():
  process(mode = 'translate')
  process(mode = 'polish')

if __name__ == "__main__":
  main()
