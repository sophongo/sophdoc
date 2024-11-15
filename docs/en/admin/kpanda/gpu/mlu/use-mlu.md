# Using Cambricon GPU

This article introduces how to use Cambricon GPU in the Suanova AI computing platform.

## Prerequisites

- The Suanova AI computing platform's container management platform has been deployed and is running normally.
- The container management module has either [integrated with a Kubernetes cluster](../../clusters/integrate-cluster.md) or [created a Kubernetes cluster](../../clusters/create-cluster.md), and is able to access the cluster's UI interface.
- The current cluster has installed the Cambricon firmware, drivers, and DevicePlugin components. For installation details, please refer to the official documentation:
    - [Driver Firmware Installation](https://www.cambricon.com/docs/sdk_1.15.0/driver_5.10.22/user_guide/index.html)
    - [DevicePlugin Installation](https://github.com/Cambricon/cambricon-k8s-device-plugin/blob/master/device-plugin/README.md)
    
When installing DevicePlugin, please disable the **--enable-device-type** parameter; otherwise, the Suanova AI computing platform will not be able to correctly recognize the Cambricon GPU.

## Introduction to Cambricon GPU Modes

Cambricon GPUs have the following modes:

- Full Card Mode: Register the Cambricon GPU as a whole card for use in the cluster.
- Share Mode: Allows one Cambricon GPU to be shared among multiple Pods, with the number of shareable containers set by the `virtualization-num` parameter.
- Dynamic SMLU Mode: Further refines resource allocation, allowing control over the size of memory and computing power allocated to containers.
- MIM Mode: Allows the Cambricon GPU to be divided into multiple GPUs of fixed specifications for use.

## Using Cambricon in Suanova AI Computing Platform

Here, we take the Dynamic SMLU mode as an example:

1. After correctly installing the DevicePlugin and other components, click the proper **Cluster** -> **Cluster Maintenance** -> **Cluster Settings** -> **Addon Plugins** to check whether the proper GPU type has been automatically enabled and detected.
  
   

2. Click the node management page to check if the nodes have correctly recognized the proper GPU type.
  
   

3. Deploy workloads. Click the proper **Cluster** -> **Workloads**, and deploy workloads using images. After selecting the type (MLU VGPU), you need to configure the GPU resources used by the App:

    - GPU Computing Power (cambricon.com/mlu.smlu.vcore): Indicates the percentage of cores the current Pod needs to use. 
    - GPU Memory (cambricon.com/mlu.smlu.vmemory): Indicates the size of memory the current Pod needs to use, in MB.
    
   

## Using YAML Configuration

Refer to the following YAML file:

```yaml
apiVersion: v1  
kind: Pod  
metadata:  
  name: pod1  
spec:  
  restartPolicy: OnFailure  
  containers:  
    - image: ubuntu:16.04  
      name: pod1-ctr  
      command: ["sleep"]  
      args: ["100000"]  
      resources:  
        limits:  
          cambricon.com/mlu: "1" # use this when device type is not enabled, else delete this line.  
          #cambricon.com/mlu: "1" #uncomment to use when device type is enabled  
          #cambricon.com/mlu.share: "1" #uncomment to use device with env-share mode  
          #cambricon.com/mlu.mim-2m.8gb: "1" #uncomment to use device with mim mode  
          #cambricon.com/mlu.smlu.vcore: "100" #uncomment to use device with mim mode  
          #cambricon.com/mlu.smlu.vmemory: "1024" #uncomment to use device with mim mode
```
