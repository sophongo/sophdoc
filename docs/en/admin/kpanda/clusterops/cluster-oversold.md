# Dynamic Resource Overprovision in the Cluster

Currently, many businesses experience peaks and valleys in demand. To ensure service performance and stability, resources are typically allocated based on peak demand when deploying services. However, peak periods may be very short, resulting in resource waste during off-peak times. **Cluster resource overprovision** utilizes these allocated but unused resources (i.e., the difference between allocation and usage) to enhance cluster resource utilization and reduce waste.

This article mainly introduces how to use the cluster dynamic resource overprovision feature.

## Prerequisites

- The container management module has been [integrated with a Kubernetes cluster](../clusters/integrate-cluster.md) or a [Kubernetes cluster has been created](../clusters/create-cluster.md), and access to the cluster's UI interface is available.
- A [namespace has been created](../namespaces/createns.md), and the user has been granted [Cluster Admin](../permissions/permission-brief.md) permissions. For details, refer to [Cluster Authorization](../permissions/cluster-ns-auth.md).

## Enable Cluster Overprovision

1. click **Clusters** in the left navigation bar, then clickthe name of the target cluster to enter the **Cluster Details** page.

    ![Clusters](../images/cluster-oversold-01.png)

2. On the cluster details page, click **Cluster Operations** -> **Cluster Settings** in the left navigation bar, then select the **Advanced Configuration** tab.

    ![Advanced Settings](../images/cluster-oversold-02.png)

3. Enable cluster overprovision and set the overprovision ratio.

    - If the cro-operator plugin is not installed, click the **Install Now** button and follow the installation process as per [Managing Helm Apps](../helm/helm-app.md).
    - If the cro-operator plugin is already installed, enable the cluster overprovision switch to start using the cluster overprovision feature.

    !!! note

        The proper namespace in the cluster must have the following label applied for the cluster overprovision policy to take effect.

    ```shell
    clusterresourceoverrides.admission.autoscaling.openshift.io/enabled: "true"
    ```

    ![Cluster Overprovision](../images/cluster-oversold-03.png)

## Using Cluster Overprovision

Once the cluster dynamic resource overprovision ratio is set, it will take effect while workloads are running. The following example uses nginx to validate the use of resource overprovision capabilities.

1. Create a workload (nginx) and set the proper resource limits. For the creation process, refer to [Creating Stateless Workloads (Deployment)](../workloads/create-deployment.md).

    ![Create Workload](../images/cluster-oversold-04.png)

2. Check whether the ratio of the Pod's resource requests to limits meets the overprovision ratio.

    ![View Pod Resources](../images/cluster-oversold-05.png)
