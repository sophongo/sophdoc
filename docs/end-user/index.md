---
hide:
  - toc
---

# 算丰 AI 算力平台 - 终端用户

这是算丰 AI 算力平台面向终端用户的使用文档。

<div class="grid cards" markdown>

- :fontawesome-solid-user:{ .lg .middle } __用户注册__

    ---

    用户注册是使用 AI 算力平台的第一步。

    - [用户注册](register/index.md)

- :octicons-fiscal-host-16:{ .lg .middle } __云主机__

    ---

    云主机是部署在云端的虚拟机。

    - [创建云主机](host/createhost.md)
    - [使用云主机](host/usehost.md)

- :simple-kubernetes:{ .lg .middle } __容器管理__

    ---

    容器管理是 AI 算力中心的核心模块。

    - [云上 K8s 集群](./kpanda/clusters/integrate-cluster.md)
    - [节点管理](./kpanda/nodes/labels-annotations.md)
    - [工作负载](./kpanda/workloads/create-deployment.md)
    - [Helm 应用和模板](./kpanda/helm/README.md)

- :simple-smart:{ .lg .middle } __算法开发__

    ---

    管理数据集，执行 AI 训练和推理任务。

    - [创建 AI 工作负载](./share/workload.md)
    - [使用 Notebook](share/notebook.md)
    - [创建训练任务](baize/jobs/create.md)
    - [创建推理服务](./baize/developer/inference/models.md)

- :fontawesome-solid-diagram-project:{ .lg .middle } __可观测性__

    ---

    通过仪表盘监控集群、节点、工作负载状况。

    - [监控集群/节点](./insight/infra/cluster.md)
    - [指标](./insight/data-query/metric.md)
    - [日志](./insight/data-query/log.md)
    - [链路追踪](./insight/trace/trace.md)

- :octicons-gear-16:{ .lg .middle } __个人中心__

    ---

    在个人中心设置密码、密钥和语言。

    - [安全设置](./ghippo/personal-center/security-setting.md)
    - [访问密钥](./ghippo/personal-center/accesstoken.md)
    - [语言设置](./ghippo/personal-center/language.md)

</div>
