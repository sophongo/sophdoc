# Cold Migration within the Cluster

This article will introduce how to move a cloud host from one node to another within the same cluster while it is powered off.

The main feature of cold migration is that the cloud host will be offline during the migration process, which may impact business continuity. Therefore, careful planning of the migration time window is necessary, taking into account business needs and system availability. Typically, cold migration is suitable for scenarios where downtime requirements are not very strict.

## Prerequisites

Before using cold migration, the following prerequisites must be met:

- The cloud host must be powered off to perform cold migration.

## Cold Migration

1. Click__Container Management__ in the left navigation bar, then click__Cloud Hosts__ to enter the list page. Clickthe __┇__ on the right side of the list to initiate the migration action for the cloud host that is in a powered-off state. The current node of the cloud host cannot be viewed while it is powered off, so prior planning or checking while powered on is required.


    !!! note

        If you have used local-path in the storage pool of the original node, there may be issues during cross-node migration. Please choose carefully.

2. After clicking migrate, a prompt will appear allowing you to choose to migrate to a specific node or randomly. If you need to change the storage pool, ensure that there is an available storage pool in the target node. Also, ensure that the target node has sufficient resources. The migration process may take a significant amount of time, so please be patient.


3. The migration will take some time, so please be patient. After it is successful, you need to restart the cloud host to check if the migration was successful. This example has already powered on the cloud host to check the migration effect.

