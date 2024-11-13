---
hide:
  - toc
---

# 算丰 AI 算力平台 - 管理员

这是算丰 AI 算力平台面向管理员的运维文档。

<div class="grid cards" markdown>

- :fontawesome-solid-user:{ .lg .middle } __用户注册__

    ---

    用户注册是使用 AI 算力平台的第一步。

    - [用户注册](register/index.md)
    - [绑定工作空间](register/bindws.md)
    - [为工作空间分配资源](register/wsres.md)

- :octicons-fiscal-host-16:{ .lg .middle } __独享云主机__

    ---

    云主机是部署在云端的云主机。

    - [创建云主机](host/createhost.md)
    - [使用云主机](host/usehost.md)

- :material-share-all:{ .lg .middle } __共享云资源__

    ---

    共享云端资源构建 AI 负载，使用 Notebook 创建训练和推理任务。

    - [配额管理](share/quota.md)
    - [使用 Notebook](share/notebook.md)
    - [创建训练任务](baize/developer/jobs/create.md)
    - [创建推理服务](baize/developer/inference/models.md)

- :simple-kubernetes:{ .lg .middle } __云上 K8s 集群__

    ---

    使用 K8s 集群高效调度算力资源。

    - [创建云上 K8s 集群](k8s/create-k8s.md)
    - [添加工作节点](k8s/add-node.md)
    - [移除 GPU 工作节点](k8s/remove-node.md)

- :octicons-gear-16:{ .lg .middle } __个人中心__

    ---

    在个人中心设置密码、密钥和语言。

    - [安全设置](admin/ghippo/personal-center/security-setting.md)
    - [访问密钥](admin/ghippo/personal-center/accesstoken.md)
    - [语言设置](admin/ghippo/personal-center/language.md)

</div>

![home](images/home.png)
