import os
import re


from functools import reduce


def parse(template_path: str) -> str:
    if not os.path.isfile(template_path):
        raise RuntimeError("模板文件路径{}不存在".format(template_path))

    html = ""
    with open(template_path) as f:
        for line in f.readlines():
            html += line

    return html


def inject(template_path: str, texts: list, img_paths: list) -> str:
    html = parse(template_path)

    # 解析并插入文本
    text_splits = html.split("{{text}}")
    if len(text_splits) - 1 != len(texts):
        raise RuntimeError("模板文件{}所需和提供的文本数量不同".format(template_path))

    if len(texts) > 0:
        i = 1
        for text in texts:
            text_splits.insert(i, text)
            i += 2
        html = "".join(text_splits)

    # 解析并插入图片标签
    img_splits = html.split("{{img}}")
    if len(img_splits) - 1 != len(img_paths):
        raise RuntimeError("模板文件{}所需和提供的图片数量不同".format(template_path))

    if len(img_paths) > 0:
        for i in range(len(img_paths)):
            img_splits.insert(2 * i + 1, "<img src=\"cid:image{}\">".format(i))
        html = "".join(img_splits)

    return html


if __name__ == '__main__':
    s = inject("/Users/mopip77/project/pyhton/mail-tools/data/template/info.html", ["sdf", "zsdv", "vsdf"], ["adf", "xzcv"])
    print(s)
