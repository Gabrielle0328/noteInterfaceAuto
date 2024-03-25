import unittest


class CheckMethod(unittest.TestCase):
    def output_check(self, expect, actual):
        """
        通用的断言方法
        :param actual: 字典类型，接口返回结果
        :param expect: 字典类型，接口期望的返回结果
        :return:
        """
        self.assertEqual(len(expect.keys()), len(actual.keys()), msg='keys len error!')
        for k, v in expect.items():
            self.assertIn(k, actual.keys(), msg=f'key:【{k}】 not in response!')
            if isinstance(v, type):
                self.assertEqual(v, type(actual[k]), msg=f'key:【{k}】 type error!')
            elif isinstance(v, list):
                self.assertEqual(len(v), len(actual[k]), msg=f'key:【{k}】 len error!')
                for i in range(len(v)):
                    # self.assertEqual(len((v)[i]), len(actual[k]), msg=f'key:【{k}】 len error!')
                    if isinstance(v[i], type):
                        self.assertEqual(v[i], type(actual[k][i]), msg=f'list value:【{v[i]}】type error!')
                    elif isinstance(v[i], dict):
                        self.output_check(v[i], actual[k][i])
                    else:
                        self.assertEqual(v[i], actual[k][i], msg=f'list value:【{v[i]}】value error!')
            elif isinstance(v, dict):
                self.output_check(v, actual[k])
            else:
                self.assertEqual(v, actual[k], msg=f'key:【{k}】 value error!')

    def output_check2(self, expect, actual):
        """
        通用的断言方法
        :param actual: 字典类型，接口返回结果
        :param expect: 字典类型，接口期望的返回结果
        :return:
        """
        self.assertEqual(len(expect.keys()), len(actual.keys()), msg='keys len error!')
        for k, v in expect.items():
            self.assertIn(k, actual.keys(), msg=f'key:【{k}】 not in response!')
            if isinstance(v, type):
                self.assertEqual(v, type(actual[k]), msg=f'key:【{k}】 type error!')
            elif isinstance(v, list):
                for a in range(len(v)):
                    if isinstance(v[a], dict):
                        self.assertEqual(len(v[a]), len(actual[k][a]), msg=f'key:【{k}】 len error!')
                        self.output_check(v[a], actual[k][a])
                    else:
                        self.assertEqual(len(v), len(actual[k]), msg=f'key:【{k}】 len error!')
                        for i in range(len(v)):
                            # self.assertEqual(len((v)[i]), len(actual[k]), msg=f'key:【{k}】 len error!')
                            if isinstance(v[i], type):
                                self.assertEqual(v[i], type(actual[k][i]), msg=f'list value:【{v[i]}】type error!')
                            elif isinstance(v[i], dict):
                                self.output_check(v[i], actual[k][i])  # 递归
                            else:
                                self.assertEqual(v[i], actual[k][i], msg=f'list value:【{v[i]}】value error!')
            elif isinstance(v, dict):
                self.output_check(v, actual[k])
            else:
                self.assertEqual(v, actual[k], msg=f'key:【{k}】 value error!')