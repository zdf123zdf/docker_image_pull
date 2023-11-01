---
name: img-mirror issue template
about: 用于执行 img-mirror workflow 的 issue 模板
title: "[img-mirror] 请求执行任务"
labels: ["img-mirror"]
---

{
    "img-mirror": [
        "格式：你需要转换的原始镜像$自定义镜像名:自定义标签名",
        "其中 $自定义镜像名:自定义标签名 是可选的",
        "以下是三个正确示例",
        "registry.k8s.io/kube-apiserver:v1.27.4",
        "registry.k8s.io/kube-apiserver:v1.27.4$my-kube-apiserver",
        "registry.k8s.io/kube-apiserver:v1.27.4$my-kube-apiserver:mytag",
        "每次提交最多 5 个镜像地址",
        "错误的镜像都会被跳过",
        "请确保 json 格式是正确的，比如下面这个是最后一个，后面是没有逗号的",
        "好了，改成你想要转换的镜像吧"
    ]
}
