# Install insight-agent in Suanova 4.0

In AI platform, previous Suanova 4.0 can be accessed as a subcluster. This guide provides potential issues and solutions when installing insight-agent in a Suanova 4.0 cluster.

## Issue One

Since most Suanova 4.0 clusters have installed dx-insight as the monitoring system, installing insight-agent at this time will conflict with the existing prometheus operator in the cluster, making it impossible to install smoothly.

### Solution

Enable the parameters of the prometheus operator, retain the prometheus operator in dx-insight, and make it compatible with the prometheus operator in insight-agent in 5.0.

### Steps

1. Log in to the console.
2. Enable the __--deny-namespaces__ parameter in the two prometheus operators respectively.
3. Run the following command (the following command is for reference only, the actual command needs to replace the prometheus operator name and namespace in the command).

    ```bash
    kubectl edit deploy insight-agent-kube-prometh-operator -n insight-system
    ```

    ![operatoryaml](https://docs.daocloud.io/daocloud-docs-images/docs/insight/images/promerator.png)

!!! note
    - As shown in the figure above, the dx-insight component is deployed under the dx-insight tenant, and the insight-agent is deployed under the insight-system tenant.
      Add __--deny-namespaces=insight-system__ in the prometheus operator in dx-insight,
      Add __--deny-namespaces=dx-insight__ in the prometheus operator in insight-agent.
    - Just add deny namespace, both prometheus operators can continue to scan other namespaces, and the related collection resources under kube-system or customer business namespaces are not affected.
    - Please pay attention to the problem of node exporter port conflict.

### Supplementary Explanation

The open-source __node-exporter__ turns on hostnetwork by default and the default port is 9100.
If the monitoring system of the cluster has installed __node-exporter__ , then installing __insight-agent__ at this time will cause node-exporter port conflict and it cannot run normally.

!!! note
    Insight's __node exporter__ will enable some features to collect special indicators, so it is recommended to install.

Currently, it does not support modifying the port in the installation command. After __helm install insight-agent__ , you need to manually modify the related ports of the insight node-exporter daemonset and svc.

## Issue Two

After Insight Agent is successfully deployed, fluentbit does not collect logs of Suanova 4.0.

### Solution

The docker storage directory of Suanova 4.0 is __/var/lib/containers__ , which is different from the path in the configuration of insigh-agent, so the logs are not collected.

### Steps

1. Log in to the console.
2. Modify the following parameters in the insight-agent Chart.

    ```diff
    fluent-bit:
    daemonSetVolumeMounts:
        - name: varlog
        mountPath: /var/log
        - name: varlibdockercontainers
    -     mountPath: /var/lib/docker/containers
    +     mountPath: /var/lib/containers/docker/containers
        readOnly: true
        - name: etcmachineid
        mountPath: /etc/machine-id
        readOnly: true
        - name: dmesg
        mountPath: /var/log/dmesg
        readOnly: true
    ```
