# Removing GPU Worker Nodes

The cost of GPU resources is relatively high. If GPUs are not needed temporarily, you can remove the worker nodes with GPUs. The following steps also apply to removing regular worker nodes.

## Prerequisites

- The AI platform is installed
- An administrator account is available
- [A cluster with GPU nodes has been created](./create-k8s.md)

## Steps to Remove

1. Log into the AI platform as an **administrator**.
2. Navigate to **Container Management** -> **Clusters**, and click the name of the target cluster.



3. Enter the cluster overview page, click **Nodes**, find the node to be removed, click the __┇__ on the right side of the list, and select **Remove Node** from the pop-up menu.



4. In the pop-up window, enter the node name, and after confirming it is correct, click **Delete**.



5. You will automatically return to the node list, where the status will be **Removing**. After a few minutes, refresh the page, and if the node is no longer present, it indicates that the node has been successfully removed.



6. After removing the node from the UI list, SSH into the removed node's host and execute the shutdown command.

    ![shutdown](../images/remove05.png)

!!! tip

    After removing the node in the UI and shutting it down, the data on the node is not immediately deleted; the node's data will be retained for a period of time.
