"""
 * @author: zkyuan
 * @date: 2025/7/1 9:41
 * @description: 文法生成句子

 这段代码实现了一个基于文法规则的句子生成器

"""

import random

from icecream import ic

# 定义语法描述，用于生成句子
# 这里的语法描述定义了复合句子、连词、句子、主语、谓语和宾语的结构
rules = """
复合句子 = 句子 , 连词 复合句子 | 句子
连词 = 而且 | 但是 | 不过 | 因为 | 所以 | 因此 | 那么 
句子 = 主语 谓语 宾语
主语 = 你| 我 | 他 | 张三 | 我们
谓语 = 吃| 玩 | 打 | 看 | 听 | 想 | 要 
宾语 = 桃子| 篮球 | 苹果 | 无畏契约 | 绝地求生 | 英雄联盟
"""


def get_grammer_by_description(description):
    """"
    将语法描述转换为文法规则
    :param description: 语法描述
    :return: 文法规则
    从语法描述中构建语法字典
    该函数解析语法描述，并将其转换为字典形式，便于后续生成句子
    """
    # 按行分割描述内容，并以等号=拆分，得到规则名和候选表达式
    rules_pattern = [r.split('=') for r in description.split('\n') if r.strip()]
    # 将每个规则的候选式再按竖线|拆分为多个选项
    target_with_expend = [(t, ex.split('|')) for t, ex in rules_pattern]
    # 构建最终字典，键为目标规则名，值为其候选式的列表形式
    grammar = {t.strip(): [e.strip() for e in ex] for t, ex in target_with_expend}

    return grammar


def generate_by_grammer(grammer, target='句子'):
    """
    根据文法规则生成句子
    :param grammer: 文法规则
    :param target: 目标生成句子的文法符号
    :return: 生成的句子
    通过随机选择和递归调用生成句子
    该函数根据提供的语法字典生成句子。如果目标不是字典的键，则直接返回目标
    否则，它将随机选择一个与目标关联的规则，并递归地生成句子的每个部分
    """
    if target not in grammer:
        # 如果目标生成语法不在规则中，则直接返回目标
        return target

    return ''.join([generate_by_grammer(grammer, t) for t in random.choice(grammer[target]).split()])


if __name__ == '__main__':
    grammer_rule = get_grammer_by_description(rules)

    ic(generate_by_grammer(grammer_rule, target='复合句子'))

    # for i in range(10):
    #     print(generate_by_grammer(grammer_rule, target='句子'))
    #
    # for i in range(10):
    #     print(generate_by_grammer(grammer_rule, target='复合句子'))
