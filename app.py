# 导入所需的库
import os.path

import streamlit as st
import torch
from pdf2image import convert_from_path
from transformers import AutoTokenizer, AutoModelForCausalLM
from modelscope import snapshot_download

from agent import Agent

# 在侧边栏中创建一个标题和一个链接
with st.sidebar:
    st.markdown("## E.Copi")
    "[Ecopi](https://openxlab.org.cn/models/detail/max08/Ecopi)"
    # 创建一个滑块，用于选择最大长度，范围在0到1024之间，默认值为512
    max_length = st.slider("max_length", 0, 1024, 512, step=1)
    system_prompt = st.text_input("System_Prompt", "你是Ecopi，顶级生物信息研究员")

# 创建一个标题和一个副标题
st.title("💬 InternLM2-Chat-7B 生信研究员版")
st.caption("🚀 Ecopi 顶级生物信息研究员")

# 定义模型路径
# A Comprehensive Guide to Setting the Right Price for Your Masterpieces
# model_id = 'max08/Ecopi'
# mode_name_or_path = snapshot_download(model_id, revision='master')

base_path = './model'
# download repo to the base_path directory using git
os.system('apt install git')
os.system('apt install git-lfs')
os.system('git lfs install')
os.system(f'git clone https://code.openxlab.org.cn/max08/Ecopi.git {base_path}')
os.system(f'cd {base_path} && git lfs pull')

mode_name_or_path = base_path

# 定义一个函数，用于获取模型和tokenizer
@st.cache_resource
def get_model():
    # 从预训练的模型中获取tokenizer
    tokenizer = AutoTokenizer.from_pretrained(mode_name_or_path, trust_remote_code=True)
    # 从预训练的模型中获取模型，并设置模型参数
    model = AutoModelForCausalLM.from_pretrained(mode_name_or_path, trust_remote_code=True,
                                                 torch_dtype=torch.bfloat16).cuda()
    model.eval()
    return tokenizer, model


# 加载Chatglm3的model和tokenizer
tokenizer, model = get_model()

# 如果session_state中没有"messages"，则创建一个包含默认消息的列表
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# 遍历session_state中的所有消息，并显示在聊天界面上
for msg in st.session_state.messages:
    st.chat_message("user").write(msg[0])
    st.chat_message("assistant").write(msg[1])


def chatCallback(msg):
    print(msg)
    # 将模型的输出添加到session_state中的messages列表中
    st.write(msg)


def codeCallBack(code):
    print(code)
    st.code(code, language='python')


agent = Agent(model, tokenizer, chatCallback, codeCallBack)
# 如果用户在聊天输入框中输入了内容，则执行以下操作
if prompt := st.chat_input():
    # 在聊天界面上显示用户的输入
    goal = prompt
    progress_text = "Operation in progress. Please wait."
    my_bar = st.progress(0, text=progress_text)

    if os.path.exists('bar.pdf'):
        os.remove('bar.pdf')

    st.chat_message("user").write(prompt)
    # 在聊天界面上显示模型的输出
    with st.chat_message("assistant"):
        msg = agent.run(goal)
        st.session_state.messages.append((goal, msg))
        if os.path.exists('bar.pdf'):
            images = convert_from_path('bar.pdf')
            for image in images:
                st.image(image, caption='output')
            my_bar.empty()