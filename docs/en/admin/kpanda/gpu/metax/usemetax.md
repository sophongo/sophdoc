# MetaX GPU Component Installation and Usage

This chapter provides installation guidance for MetaX's gpu-extensions, gpu-operator, and other components, as well as usage methods for both the full GPU and vGPU modes.

## Prerequisites

1. The required tar package has been downloaded and installed from the [MetaX Software Center](https://sw-download.metax-tech.com/software-list). This article uses metax-gpu-k8s-package.0.7.10.tar.gz as an example.
2. Prepare the basic Kubernetes environment.

## Component Introduction

Metax provides two helm-chart packages: metax-extensions and gpu-operator. Depending on the usage scenario, different components can be selected for installation.

1. Metax-extensions: Includes two components, gpu-device and gpu-label. When using the Metax-extensions solution, the user's application container image needs to be built based on the MXMACA® base image. Moreover, Metax-extensions is only suitable for scenarios using the full GPU.
2. gpu-operator: Includes components such as gpu-device, gpu-label, driver-manager, container-runtime, and operator-controller. When using the gpu-operator solution, users can choose to create application container images that do not include the MXMACA® SDK. The gpu-operator is suitable for both full GPU and vGPU scenarios.

## Operation Steps

1. Extract the following from the `/home/metax/metax-docs/k8s/metax-gpu-k8s-package.0.7.10.tar.gz` file:
  
    - deploy-gpu-extensions.yaml # Deployment YAML 
    - metax-gpu-extensions-0.7.10.tgz, metax-operator-0.7.10.tgz # Helm chart files
    - metax-k8s-images.0.7.10.run # Offline image

2. Check if the system has the driver installed:

    ```bash
    $ lsmod | grep metax 
    metax 1605632 0 
    ttm 86016 3 drm_vram_helper,metax,drm_ttm_helper 
    drm 618496 7 drm_kms_helper,drm_vram_helper,ast,metax,drm_ttm_helper,ttm
    ```

    - If no content is displayed, it indicates that the software package has not been installed. If content is displayed, it indicates that the software package has been installed.
    - When using metax-operator, it is not recommended to pre-install the MXMACA kernel driver on worker nodes; if it has already been installed, there is no need to uninstall it.

3. Install the driver.

### gpu-extensions

1. Push the image:
  
    ```bash
    tar -xf metax-gpu-k8s-package.0.7.10.tar.gz
    ./metax-k8s-images.0.7.10.run push {registry}/metax
    ```

2. Push the Helm Chart:
  
    ```bash
    helm plugin install https://github.com/chartmuseum/helm-push
    helm repo add --username rootuser --password rootpass123  metax http://172.16.16.5:8081
    helm cm-push metax-operator-0.7.10.tgz metax
    helm cm-push metax-gpu-extensions-0.7.10.tgz metax
    ```

3. Install metax-gpu-extensions on the AI computing platform. 
  
    After successful deployment, resources can be viewed on the node.

    

4. After successful modification, you can see the label with `Metax GPU` on the node.
  
    

### gpu-operator

Known issues when installing `gpu-operator`:

1. The images for the components `metax-operator`, `gpu-label`, `gpu-device`, and `container-runtime` must have the `amd64` suffix.
  
2. The image for the `metax-maca` component is not included in the `metax-k8s-images.0.7.13.run` package and needs to be separately downloaded, such as `maca-mxc500-2.23.0.23-ubuntu20.04-x86_64.tar.xz`. After loading it, the image for the `metax-maca` component needs to be modified again.
  
3. The image for the `metax-driver` component needs to be downloaded from `https://pub-docstore.metax-tech.com:7001` as the `k8s-driver-image.2.23.0.25.run` file, and then execute the command `k8s-driver-image.2.23.0.25.run push {registry}/metax` to push the image to the image repository. After pushing, modify the image address for the `metax-driver` component.

## Using GPU

After installation, you can [use MetaX GPU in workloads](../../workloads/create-deployment.md#_5). Note that after enabling the GPU, you need to select the GPU type as Metax GPU.


Enter the container and execute `mx-smi` to view the GPU usage.


