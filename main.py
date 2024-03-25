import unittest
from BeautifulReport import BeautifulReport
import os
from datetime import datetime

ENVIRON = "Online"  # 线上 Online 测试环境 Offline
Dir = os.path.dirname(os.path.abspath(__file__))


def run(test_suite):
    # 定义输出的文件位置和名字

    # 获取当前的日期和时间
    now = datetime.now()
    # 按照"年月日时分秒"的格式输出
    time_mark = now.strftime("%Y_%m_%d-%H_%M_%S")
    filename = f"{time_mark}_report.html"
    result = BeautifulReport(test_suite)
    result.report(filename=filename, description='测试报告', report_dir='./report')


if __name__ == '__main__':
    run_pattern = 'all'  # all 全量测试用例执行/smoking 冒烟测试执行/指定执行文件
    if run_pattern == 'all':
        pattern = 'test_*.py'
    elif run_pattern == 'smoking':
        pattern = 'test_major*.py'
    else:
        pattern = run_pattern + '.py'
    print("#")
    suite = unittest.TestLoader().discover('./testCase/inquire_groups_page_8', pattern=pattern)

    run(suite)
