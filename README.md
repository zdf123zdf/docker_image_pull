# img-mirror

**思路参考：https://github.com/togettoyou/hub-mirror/**

使用 docker.io (hub.docker.com) 或其他镜像服务来提供（但不限于） gcr.io、registry.k8s.io、k8s.gcr.io、quay.io、ghcr.io 等国外镜像加速下载服务

目前支持转存到 **Docker hub(默认)、[腾讯云coding镜像服务](https://cloud.tencent.com/document/product/1726/97075)、阿里云镜像服务(ACR)、腾讯云镜像服务(TCR)**

为减少重复请求，合理利用资源，建议**提前在 issues 中搜索镜像是否已转换过**，可以直接复用

## Disclaimer/免责声明

本人郑重承诺

1. 本项目不以盈利为目的，过去，现在，未来都不会用于牟利。
2. 本项目不承诺永久可用（比如包括但不限于 DockerHub 关闭，或者 DockerHub  修改免费计划限制个人免费镜像数量，Github 主动关闭本项目，Github Action  免费计划修改），但会承诺尽量做到向后兼容（也就是后续有新的扩展 Registry 不会改动原有规则导致之前的不可用）。
3. 本项目不承诺所转存的镜像是安全可靠的，本项目只做转存（从上游 Registry pull 镜像，重新打tag，推送到目标  Registry（本项目是推到 Docker hub , 可以通过 Fork 到自己仓库改成私有  Registry）），不会进行修改（但是转存后的摘要和上游摘要不相同，这是正常的(因为镜像名字变了)），但是如果上游本身就是恶意镜像，那么转存后仍然是恶意镜像。目前支持的 `gcr.io` , `k8s.gcr.io` , `registry.k8s.io` , `quay.io`, `ghcr.io` 好像都是支持个人上传镜像的，在使用镜像前，请自行确认上游是否可靠，应自行避免供应链攻击。
4. 对于 DockerHub 和 Github 某些策略修改导致的 不可预知且不可控因素等导致业务无法拉取镜像而造成损失的，本项目不承担责任。
5. 对于上游恶意镜像或者上游镜像依赖库版本低导致的安全风险 本项目无法识别，删除，停用，过滤，要求使用者自行甄别，本项目不承担责任。

**如果不认可上面所述，请不要使用本项目，一旦使用，则视为同意。**

## 如何使用

#### 一、直接使用我的，点个 Star ，直接提交 issues，按照 issue 模板修改内容即可

要求：严格按照模板规范提交，当任务失败时，可以查看失败原因并直接修改 issues 的内容，即可重新触发任务执行

限制：每次提交最多 5 个镜像地址

本人 Docker 账号有每日镜像拉取限额，请勿滥用

#### 二：自己修改，Fork 本项目，绑定你自己的 DockerHub 账号或其他镜像服务账号

1. 绑定账号

   - 默认的 hub.docker.com 镜像服务

     在 `Settings`-`Secrets and variables`-`Actions` 选择 `New repository secret` 新建 `USERNAME`（你的 Docker用户名） 和 `PASSWORD`（你的 Docker 密码） 两个 Secrets

   - 腾讯云coding镜像服务

     在 `Settings`-`Secrets and variables`-`Actions` 选择 `New repository secret` 新建 `USERNAME`（用户名）、 `PASSWORD`（镜像服务密码）、 `REGISTRY` 和  `REPOSITORY`  四个 Secrets

     `REGISTRY `示例：`xxxx-docker.pkg.coding.net`

     `REPOSITORY` 示例：`xxxx-docker.pkg.coding.net/xxxx/xxxx`

   - 阿里云镜像服务

     在 `Settings`-`Secrets and variables`-`Actions` 选择 `New repository secret` 新建 `USERNAME`（用户名）、 `PASSWORD`（镜像服务密码）、 `REGISTRY` 和  `REPOSITORY`  四个 Secrets

     `REGISTRY `示例：`registry.cn-hangzhou.aliyuncs.com`

     `REPOSITORY` 示例：`registry.cn-hangzhou.aliyuncs.com/xxxx`

   - 腾讯云镜像服务

     在 `Settings`-`Secrets and variables`-`Actions` 选择 `New repository secret` 新建 `USERNAME`（用户名）、 `PASSWORD`（镜像服务密码）、 `REGISTRY` 和  `REPOSITORY`  四个 Secrets

     `REGISTRY `示例：`ccr.ccs.tencentyun.com`

     `REPOSITORY` 示例：`ccr.ccs.tencentyun.com/xxxx`

2. 在 Fork 的项目中开启 `Settings`-`General`-`Features` 中的 `Issues` 功能

3. 在 Fork 的项目中修改 `Settings`-`Actions`-`General` 中的 `Workflow permissions` 为 `Read and write permissions`

4. 在 `Issues`-`Labels` 选择 `New label` 依次添加三个 label ：`img-mirror`、`success`、`failure`

5. 在 `Actions` 里选择 `img-mirror` ，在右边 `···` 菜单里选择 `Enable Workflow`

6. 在 Fork 的项目中提交 issues
