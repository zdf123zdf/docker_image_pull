import json
import os
import docker


def img_conversion():
    """
    镜像转换
    :return:
    """

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
    print("1245",registry,repository)
    result_data = {
        "err_num": 0,
        "err_list": [],
        "performed": "",
        "performed_manually": []
    }
    print("初始化 Docker 客户端")
    client = docker.from_env()
    for image_name in image_names:
        try:
            if "$" in image_name:
                new_name = image_name[image_name.rfind("$") + 1:]
                version = image_name[image_name.rfind(":") + 1:image_name.rfind("$")]
                if ":" in new_name:
                    version = new_name[new_name.rfind(":") + 1:]
                    new_name = new_name[new_name.rfind("$") + 1:new_name.rfind(":")]
                image_name = image_name[:image_name.rfind("$")]
            else:
                new_name = image_name[image_name.rfind("/") + 1:image_name.rfind(":")]
                version = image_name[image_name.rfind(":") + 1:]

            print("开始下载镜像")
            client.images.pull(image_name)
            print("校验镜像")
            image = client.images.get(image_name)
            print(f"开始转换镜像 {new_name}:{version}")
            image.tag(f"{repository}/{new_name}", tag=version)  # 替换为新的仓库名称和标签
            tag = f"{repository}/{new_name}:{version}"
            client.login(username=username, password=password, registry=registry)
            # 检查登录状态
            login_info = client.info()
            if login_info['Name'] == "":
                print("登录失败!")
            client.images.push(tag)
            print("上传成功")
            result_data['performed'] += f'docker pull {tag} docker tag {tag} {image_name} '
            result_data['performed_manually'].append(f'docker pull {tag}')
            result_data['performed_manually'].append(f'docker tag {tag} {image_name}')
        except Exception as e:
            result_data['err_num'] += 1
            result_data['err_list'].append(image_name)
            print("转换失败", e)

    if result_data['err_num'] == len(image_names):
        raise ZeroDivisionError("所有镜像转换失败!")

    with open('output.json', 'w') as json_file:
        json.dump(result_data, json_file)


if __name__ == '__main__':
    img_conversion()
