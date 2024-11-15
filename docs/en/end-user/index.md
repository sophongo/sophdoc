---
hide:
  - toc
---

# Suanova AI Platform - End User

This is the user documentation for the Suanova AI Platform aimed at end users.

<div class="grid cards" markdown>

- :fontawesome-solid-user:{ .lg .middle } __User Registration__

    ---

    User registration is the first step to using the AI platform.

    - [User Registration](register/index.md)

- :octicons-fiscal-host-16:{ .lg .middle } __Cloud Host__

    ---

    A cloud host is a virtual machine deployed in the cloud.

    - [Create Cloud Host](host/createhost.md)
    - [Use Cloud Host](host/usehost.md)

- :simple-kubernetes:{ .lg .middle } __Container Management__

    ---

    Container management is the core module of the AI computing center.

    - [K8s Clusters on Cloud](./kpanda/clusters/integrate-cluster.md)
    - [Node Management](./kpanda/nodes/labels-annotations.md)
    - [Workloads](./kpanda/workloads/create-deployment.md)
    - [Helm Apps and Templates](./kpanda/helm/README.md)

- :simple-smart:{ .lg .middle } __AI Lab__

    ---

    Manage datasets and run AI training and inference jobs.

    - [Create AI Workloads](./share/workload.md)
    - [Use Notebook](share/notebook.md)
    - [Create Training Jobs](baize/jobs/create.md)
    - [Create Inference Services](./baize/developer/inference/models.md)

- :fontawesome-solid-diagram-project:{ .lg .middle } __Insight__

    ---

    Monitor the status of clusters, nodes, and workloads through dashboards.

    - [Monitor Clusters/Nodes](./insight/infra/cluster.md)
    - [Metrics](./insight/data-query/metric.md)
    - [Logs](./insight/data-query/log.md)
    - [Tracing](./insight/trace/trace.md)

- :octicons-gear-16:{ .lg .middle } __Personal Center__

    ---

    Set password, keys, and language in the personal center.

    - [Security Settings](./ghippo/personal-center/security-setting.md)
    - [Access Keys](./ghippo/personal-center/accesstoken.md)
    - [Language Settings](./ghippo/personal-center/language.md)

</div>
