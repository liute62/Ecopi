import os
from timeit import default_timer as timer

from tenacity import retry, stop_after_attempt

from code_templates import get_code_template, get_function_parameter_template
from prompts import get_analyze_prompt, get_start_prompt, get_analyze_function_params_prompt, get_coder_prompt
from python_exe import PythonREPL
from tools import get_support_tools


class Agent:
    """Simulates a agent."""

    model = None
    tokenizer = None
    __chatCallBack = None
    __codeCallBack = None
    system_prompt = 'You are Ecopi, a world-class coder and bioinformatics engineer'
    language = 'zh'
    history = []
    task = []
    tools = get_support_tools()

    def __init__(self, model, tokenizer, chatCallback, codeCallBack):
        self.model = model
        self.tokenizer = tokenizer
        self.__chatCallBack = chatCallback
        self.__codeCallBack = codeCallBack

    def check_goal(self, goal):
        prompt = get_start_prompt(self.language, goal, self.tools)
        response, history = self.model.chat(self.tokenizer, prompt,
                                            meta_instruction=self.system_prompt, history=self.history)
        return response

    def analyze_goal(self, goal, task):
        prompt = get_analyze_prompt(self.language, task, goal, self.tools)
        response, history = self.model.chat(self.tokenizer, prompt,
                                            meta_instruction=self.system_prompt, history=self.history)
        return response

    @retry(stop=stop_after_attempt(3))
    def choose_tools(self, goal, tool_type):
        function, parameters = get_function_parameter_template(tool_type)
        function_prompt = get_analyze_function_params_prompt(self.language, goal, function, parameters)

        response, history = self.model.chat(self.tokenizer, function_prompt,
                                            meta_instruction=self.system_prompt, history=self.history)
        return function, response

    def get_tool_valid_input(self, function, parameters):
        prompt = get_code_template(function)
        code_prompt = get_coder_prompt(self.language, parameters, prompt)
        response2, history = self.model.chat(self.tokenizer, code_prompt,
                                             meta_instruction=self.system_prompt, history=self.history)

        return response2

    @retry(stop=stop_after_attempt(3))
    def execute_tool(self, tool_input):
        r = PythonREPL()
        ret = r.run(tool_input, 100)
        return

    @retry(stop=stop_after_attempt(3))
    def get_tool_output(self):
        timestamp = 10
        start = timer()
        while True:
            end = timer()
            if end - start > timestamp:
                if os.path.exists("bar.pdf"):
                    return "bar.pdf"
                else:
                    raise Exception("not found")

    @retry(stop=stop_after_attempt(3))
    def run(self, goal) -> int:
        """Run command with own globals/locals and returns anything printed.
        Timeout after the specified number of seconds."""
        task = self.check_goal(goal)
        self.__chatCallBack(task)
        tool_type = self.analyze_goal(goal, task)
        # self.__chatCallBack(tool_type)
        function, parameters = self.choose_tools(goal, tool_type)
        # self.__chatCallBack(function)
        tool_input = self.get_tool_valid_input(function, parameters)
        self.__codeCallBack(tool_input)
        self.execute_tool(tool_input)
        self.get_tool_output()
        return tool_input
