import functools
import inspect
import os
from datetime import datetime
from colorama import Fore
from main import Dir


def info(text):
    stack = inspect.stack()
    formatted_time = datetime.now().strftime('%H:%M:%S:%f')[:-3]  # 定义了日志的输出时间
    code_path = f"{os.path.basename(stack[1].filename)}:{stack[1].lineno}"  # 当前执行文件的绝对路径和执行代码行号
    content = f"[INFO]{formatted_time}-{code_path} >> {text}"
    print(Fore.LIGHTGREEN_EX + content)
    str_time = datetime.now().strftime("%Y%m%d")
    with open(file=Dir + '\\logs\\' + f'{str_time}_info.log', mode='a', encoding='utf-8') as f:
        f.write(content + '\n')


def error(text):
    stack = inspect.stack()
    formatted_time = datetime.now().strftime('%H:%M:%S:%f')[:-3]
    code_path = f"{os.path.basename(stack[1].filename)}:{stack[1].lineno}"
    content = f"[ERROR]{formatted_time}-{code_path} >> {text}"
    print(Fore.LIGHTRED_EX + content)
    str_time = datetime.now().strftime("%Y%m%d")
    with open(file=Dir + '\\logs\\' + f'{str_time}_error.log', mode='a', encoding='utf-8') as f:
        f.write(content + '\n')
    with open(file=Dir + '\\logs\\' + f'{str_time}_info.log', mode='a', encoding='utf-8') as f:
        f.write(content + '\n')


def step(text):
    stack = inspect.stack()
    formatted_time = datetime.now().strftime('%H:%M:%S:%f')[:-3]
    code_path = f"{os.path.basename(stack[1].filename)}:{stack[1].lineno}"
    content = f"[STEP]{formatted_time}-{code_path}  >> {text}"
    print(Fore.LIGHTCYAN_EX + content)
    str_time = datetime.now().strftime("%Y%m%d")
    with open(file=Dir + '\\logs\\' + f'{str_time}_info.log', mode='a', encoding='utf-8') as f:
        f.write(content + '\n')

# 装饰器 写法
# def case_page(func):
#     def inner(*args,  **kwargs):
#         print()
#         func()
#     return inner()
def case_page(func):
    @functools.wraps(func)  # 解决参数冲突问题
    def inner(*args, **kwargs):
        class_name = args[0].__class__.__name__  # 获取类名
        method_name = func.__name__  # 获取方法名
        docstring = inspect.getdoc(func)  # 获取方法注释
        print(Fore.LIGHTRED_EX + '----------------------------------------------------------------------')
        info(f"Class Name:{class_name}")
        info(f"Method Name:{method_name}")
        info(f"Test Description:{docstring}")
        func(*args, **kwargs)
    return inner

def class_case_log(cls):
    """用例的日志装饰器级别"""
    for name, method in inspect.getmembers(cls, inspect.isfunction):
        if name.startswith('testCase'):
            setattr(cls, name, case_page(method))
    return cls


# 调试
if __name__ == '__main__':
    info('用户A请求获取首页便签接口')
    info('用户A新增一条便签数据')


