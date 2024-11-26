# 将集群分配给多个工作空间（租户）

集群资源通常由运维人员进行管理。在分配资源分配时，他们需要创建命名空间来隔离资源，并设置资源配额。
这种方式有个弊端，如果企业的业务量很大，手动分配资源需要较大的工作量，而想要灵活调配资源额度也有不小难度。

AI 算力中心为此引入了工作空间的概念。工作空间通过共享资源可以提供更高维度的资源限额能力，实现工作空间（租户）在资源限额下自助式创建 Kubernetes 命名空间的能力。

举例而言，如果想要让几个部门共享不同的集群。

|                   | Cluster01（普通） | Cluster02（高可用） |
| ----------------- | ----------------- | ------------------- |
| 部门（工作空间）A | 50 quota          | 10 quota            |
| 部门（工作空间）B | 100 quota         | 20 quota            |

可以参照以下流程将集群分享给多个部门/工作空间/租户：

```mermaid
graph TB

preparews[准备工作空间] --> preparecs[准备集群]
--> share[将集群共享到工作空间]
--> judge([判断工作空间剩余额度])
judge -.大于剩余额度.->modifyns[修改命名空间额度]
judge -.小于剩余额度.->createns[创建命名空间]

classDef plain fill:#ddd,stroke:#fff,stroke-width:1px,color:#000;
classDef k8s fill:#326ce5,stroke:#fff,stroke-width:1px,color:#fff;
classDef cluster fill:#fff,stroke:#bbb,stroke-width:1px,color:#326ce5;

class preparews,preparecs,share, cluster;
class judge plain
class modifyns,createns k8s
```

## 准备一个工作空间

工作空间是为了满足多租户的使用场景，基于集群、集群命名空间、网格、网格命名空间、多云、多云命名空间等多种资源形成相互隔离的资源环境，
工作空间可以映射为项目、租户、企业、供应商等多种概念。

1. 使用 admin/folder admin 角色的用户登录 AI 算力中心，点击左侧导航栏底部的 __全局管理__ -> __工作空间与层级__ 。

    ![全局管理](../images/ws01.png)

2. 点击右上角的 __创建工作空间__ 按钮。

    ![创建工作空间](https://docs.daocloud.io/daocloud-docs-images/docs/ghippo/images/ws02.png)

3. 填写工作空间名称、所属文件夹等信息后，点击 __确定__ ，完成创建工作空间。

    ![确定](https://docs.daocloud.io/daocloud-docs-images/docs/ghippo/images/ws03.png)

## 准备一个集群

工作空间是为了满足多租户的使用场景，基于集群、集群命名空间、网格、网格命名空间、多云、多云命名空间等多种资源形成相互隔离的资源环境，工作空间可以映射为项目、租户、企业、供应商等多种概念。

参照以下步骤准备一个集群。

1. 点击左侧导航栏底部的 __容器管理__ ，选择 __集群列表__ 。

    ![容器管理](https://docs.daocloud.io/daocloud-docs-images/docs/ghippo/images/clusterlist01.png)

1. 点击 __创建集群__ [创建一个集群](../../kpanda/clusters/create-cluster.md)，或点击 __接入集群__ [接入一个集群](../../kpanda/clusters/integrate-cluster.md)。

## 在工作空间添加集群

返回 __全局管理__ ，为工作空间添加集群。

1. 依次点击 __全局管理__ -> __工作空间与层级__ -> __共享资源__ ，点击某个工作空间名称后，点击 __新增共享资源__ 按钮。

    ![新增资源](https://docs.daocloud.io/daocloud-docs-images/docs/ghippo/images/addcluster01.png)

1. 选择集群，填写资源限额后，点击 __确定__ 。

    ![新增资源](https://docs.daocloud.io/daocloud-docs-images/docs/ghippo/images/addcluster02.png)
