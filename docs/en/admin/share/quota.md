# Quota Management

Once a user is bound to a workspace, resources can be allocated to the workspace, and resource quotas can be managed.

## Prerequisites

- The AI platform is installed
- There is an available administrator account

## Creating and Managing Quotas

1. Log in to the AI platform as an **Administrator**.
2. [Create a workspace and namespace, and bind users](../register/bindws.md).
3. [Allocate resource quotas to the workspace](../register/wsres.md#quota).


4. Manage the resource quotas for the namespace `test-ns-1`, ensuring that the values do not exceed the workspace's quota.


5. Log in to the AI platform as a **User** to check if they have been assigned the `test-ns-1` namespace.


Next step: [Create AI Workloads Using GPUs](./workload.md)
