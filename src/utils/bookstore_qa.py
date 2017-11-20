import os
import sys
from collections import OrderedDict

prefix = os.path.dirname(os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))))

template_path = os.path.join(prefix, 'data/gen_product/bookstore_qa.txt')
outpath = 'test.qa.txt'

table = [
    {"brand": ["苹果"], "virtual_category": "数码产品", "category": "手机", "pc.series": "iphone", "location": "一楼"},
    {"brand": ["苹果"], "virtual_category": "数码产品", "category": "平板", "pc.series": "ipad", "location": "一楼"},
    {"brand": ["oppo", "欧珀"], "virtual_category": "数码产品", "category": "手机", "location": "一楼"},
    {"brand": ["vivo", "维沃"], "virtual_category": "数码产品", "category": "手机", "location": "一楼"},
    {"brand": ["华为"], "virtual_category": "数码产品", "category": "手机", "location": "一楼"},
    {"brand": ["小天才"], "virtual_category": "数码产品", "category": "学习机", "location": "一楼"},
    {"poi": ["精品图书展台", "图书展台", "精品展台"], "location": "一楼中心区域"},
    {"poi": ["茶颜观色餐饮区"], "location": "二楼东侧"},
    {"poi": ["咖啡", "奶茶", "简餐"], "location": "二楼东侧"},
    {"poi": ["小确幸绿植区"], "location": "二楼西侧"},
    {"poi": ["亨通市民书房"], "location": "二楼西侧"},
    {"category": ["图书"], "book.category": ["文学类"], "location": "二楼"},
    {"category": ["图书"], "book.category": ["杂志", "期刊", "杂志期刊"], "location": "二楼"},
    {"category": ["图书"], "book.category": ["社会科学", "社科书", "科学书"], "location": "二楼"},
    {"category": ["图书"], "book.category": ["科技", "科技书", "生活书"], "location": "二楼"},
    {"category": ["图书"], "book.category": ["生活书"], "location": "二楼"},
    {"category": ["图书"], "book.category": ["少儿图书"], "location": "三楼"},
    {"brand": ["诺亚舟"], "virtual_category": "电教产品", "category": "电子词典", "location": "三楼"},
    {"brand": ["步步高"], "virtual_category": "电教产品", "category": "学习平板电脑", "location": "三楼"},
    {"brand": ["读书郎"], "virtual_category": "电教产品", "category": "点读机", "location": "三楼"},
    {"brand": ["创想"], "virtual_category": "电教产品", "category": "学习桌", "location": "三楼"},
    {"category": ["文具", "文化用品"], "location": "四楼"},
    {"category": ["图书"], "book.category": ["教辅", "小升初", "中考", "高考"], "location": "四楼"},
    {"facility": ["服务总台", "收银台"], "location": "在一楼的电梯出来后右手边,在屏幕平面图的正上方"},
    {"facility": ["卫生间", "厕所"], "location": "在三楼的电梯出来后右手走到底,咨询工作人员"},
    {"facility": ["电梯"], "location": "在屏幕平面图的右上方"},
    {"facility": ["楼梯"], "location": "在屏幕平面图的右上方"}]

facility_poi_prefix = ['我要去']
facility_poi_postfix = ['怎么走', '在哪里', '在几楼', '在什么地方']

other_prefix = ['我要买', '我来买', '我要', '我想要', '我想要买', '有没有']
other_postfix = ['在哪里', '在几楼', '在什么地方']

label_prefix = 'api_call_qa_location_'


def gen2(outpath=outpath):
    res = set()
    for line in table:
        keys = list(line.keys())
        print(keys)
        if 'poi' in keys or 'facility' in keys:
            prefix = facility_poi_prefix
            postfix = facility_poi_postfix
        else:
            prefix = other_prefix
            postfix = other_postfix
        for key in keys:
            if key=='location':
                continue
            values = line[key]

            values=values if isinstance(values,list) else [values]
            print(values)
            for v in values:
                for pre in prefix:
                    query = pre + v
                    label = label_prefix + key + ':' + v
                    res.add(query + '\t' + label + '\t' + 'placeholder')
                for post in postfix:
                    query = v + post
                    label = label_prefix + key + ':' + v
                    res.add(query + '\t' + label + '\t' + 'placeholder')

    res=list(res)
    res.sort()
    with open(outpath, 'w') as f:
        for line in res:
            f.write(line + '\n\n')


def parse(lines):
    keys = lines[0].split(':')[1].split('|')
    lines = lines[1:]
    middle = OrderedDict()
    prefix = OrderedDict()
    postfix = OrderedDict()
    for line in lines:
        name, entities = line.split(':')
        entities = entities.strip().split('|')
        if name.startswith('prefix_'):
            prefix[name] = entities
        elif name.startswith('postfix_'):
            postfix[name] = entities
        else:
            middle[name] = entities

    return middle, prefix, postfix


def gen(outpath=outpath, path=template_path):
    with open(path, 'r') as f:
        lines = f.readlines()[1:]
    middle, prefix, postfix = parse(lines)

    res = list()
    for key in middle.keys():
        middles = middle[key]
        prefixs = prefix['prefix_' + key]
        postfixs = postfix['postfix_' + key]

        for m in middles:
            for pre in prefixs:
                query = pre + m
                label = 'api_call_qa_location_' + key + ':' + m
                line = query.strip() + '\t' + label.strip() + '\t' + 'placeholder'
                res.append(line)
            for post in postfixs:
                query = m + post
                label = 'api_call_qa_location_' + key + ':' + m
                line = query.strip() + '\t' + label.strip() + '\t' + 'placeholder'
                res.append(line)
    with open(outpath, 'w') as f:
        for line in res:
            f.write(line + '\n\n')


def main():
    gen2()


if __name__ == '__main__':
    main()
