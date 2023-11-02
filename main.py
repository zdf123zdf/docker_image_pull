#!/usr/bin/env python
# -*- coding:utf-8 -*-

import json
import os
import threading
import docker


class Task(threading.Thread):
    def __init__(self, image_name, username, password, registry, repository, client, result_data):
        threading.Thread.__init__(self)
        self.image_name = image_name
        self.username = username
        self.password = password
        self.registry = registry
        self.repository = repository
        self.client = client
        self.result_data = result_data

    def run(self):
        try:
            if "$" in self.image_name:
                new_name = self.image_name[self.image_name.rfind("$") + 1:]
                version = self.image_name[self.image_name.rfind(":") + 1:self.image_name.rfind("$")]
                if ":" in new_name:
                    version = new_name[new_name.rfind(":") + 1:]
                    new_name = new_name[new_name.rfind("$") + 1:new_name.rfind(":")]
                self.image_name = self.image_name[:self.image_name.rfind("$")]
            else:
                new_name = self.image_name[self.image_name.rfind("/") + 1:self.image_name.rfind(":")]
                version = self.image_name[self.image_name.rfind(":") + 1:]

            print("开始下载镜像")
            self.client.images.pull(self.image_name)
            print("校验镜像")
            image = self.client.images.get(self.image_name)
            print(f"开始转换镜像 {self.image_name}")
            image.tag(f"{self.repository}/{new_name}", tag=version)  # 替换为新的仓库名称和标签
            tag = f"{self.repository}/{new_name}:{version}"
            self.client.login(username=self.username, password=self.password, registry=self.registry)
            # 检查登录状态
            login_info = self.client.info()
            if login_info['Name'] == "":
                print("登录失败!")
            self.client.images.push(tag)
            print("上传成功")
            self.result_data['performed'] += f'docker pull {tag} docker tag {tag} {self.image_name} '
            self.result_data['performed_manually'].append(f'docker pull {tag}')
            self.result_data['performed_manually'].append(f'docker tag {tag} {self.image_name}')
        except Exception as e:
            self.result_data['err_num'] += 1
            self.result_data['err_list'].append(self.image_name)
            print("转换失败", e)


def main():
    img_mirror = os.getenv("IMG_MIRROR")
    data = json.loads(img_mirror)
    image_names = data.get('img-mirror', [])
    if len(image_names) > 5:
        print("每次提交最多5个镜像地址，现在转换前5个")
        image_names = image_names[:5]

    username = os.getenv("USERNAME")
    password = os.getenv("PASSWORD")
    registry = os.getenv("REGISTRY")
    if registry == "":
        registry = "https://index.docker.io/v1/"  # 默认为dockerhub仓库
    repository = os.getenv("REPOSITORY")
    if repository == "":
        repository = username

    result_data = {
        "err_num": 0,
        "err_list": [],
        "performed": "",
        "performed_manually": []
    }
    print("初始化 Docker 客户端")
    client = docker.from_env()

    # 创建多个线程并启动
    threads = []
    for image_name in image_names:
        thread = Task(image_name, username, password, registry, repository, client, result_data)
        thread.start()
        threads.append(thread)

    # 等待所有线程执行完毕
    for thread in threads:
        thread.join()

    if result_data['err_num'] == len(image_names):
        raise ZeroDivisionError("所有镜像转换失败!")

    with open('output.json', 'w') as json_file:
        json.dump(result_data, json_file)


if __name__ == '__main__':
    main()
