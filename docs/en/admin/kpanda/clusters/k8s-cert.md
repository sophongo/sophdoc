# Update Kubernetes Cluster Certificate

To ensure secure communication between various components of Kubernetes, TLS authentication is performed during calls between components, which requires configuring the cluster PKI certificates.

The validity period of cluster certificates is 1 year. To avoid service interruptions due to certificate expiration, please update the certificates in a timely manner.

This article explains how to manually update the certificates.

## Check if the Certificates are Expired

You can execute the following command to check if the certificates are expired:

```shell
kubeadm certs check-expiration
```

The output will be similar to the following:

```output
CERTIFICATE                EXPIRES                  RESIDUAL TIME   CERTIFICATE AUTHORITY   EXTERNALLY MANAGED
admin.conf                 Dec 14, 2024 07:26 UTC   204d                                    no      
apiserver                  Dec 14, 2024 07:26 UTC   204d            ca                      no      
apiserver-etcd-client      Dec 14, 2024 07:26 UTC   204d            etcd-ca                 no      
apiserver-kubelet-client   Dec 14, 2024 07:26 UTC   204d            ca                      no      
controller-manager.conf    Dec 14, 2024 07:26 UTC   204d                                    no      
etcd-healthcheck-client    Dec 14, 2024 07:26 UTC   204d            etcd-ca                 no      
etcd-peer                  Dec 14, 2024 07:26 UTC   204d            etcd-ca                 no      
etcd-server                Dec 14, 2024 07:26 UTC   204d            etcd-ca                 no      
front-proxy-client         Dec 14, 2024 07:26 UTC   204d            front-proxy-ca          no      
scheduler.conf             Dec 14, 2024 07:26 UTC   204d                                    no      

CERTIFICATE AUTHORITY   EXPIRES                  RESIDUAL TIME   EXTERNALLY MANAGED
ca                      Dec 12, 2033 07:26 UTC   9y              no      
etcd-ca                 Dec 12, 2033 07:26 UTC   9y              no      
front-proxy-ca          Dec 12, 2033 07:26 UTC   9y              no      
```

## Manually Update Certificates

You can manually update the certificates using the following command with appropriate command-line options. Please back up the current certificates before updating.

To update a specific certificate:

```shell
kubeadm certs renew
```

To update all certificates:

```shell
kubeadm certs renew all
```

The updated certificates can be viewed in the `/etc/kubernetes/pki` directory, with a validity period extended by 1 year. The following corresponding configuration files will also be updated:

- /etc/kubernetes/admin.conf
- /etc/kubernetes/controller-manager.conf
- /etc/kubernetes/scheduler.conf

!!! note

    - If you are deploying a high-availability cluster, this command needs to be executed on all control nodes.
    - This command updates using the CA (or front-proxy-CA) certificate and the keys stored in `/etc/kubernetes/pki`.

## Restart Services

After executing the update operation, you need to restart the control plane Pods. Since dynamic certificate reloading is currently not supported by all components and certificates, this operation is necessary.

Static Pods are managed by the local kubelet rather than the API server, so kubectl cannot be used to delete or restart them.

To restart static Pods, you can temporarily remove the manifest files from `/etc/kubernetes/manifests/` and wait for 20 seconds. Refer to the `fileCheckFrequency` value in the [KubeletConfiguration structure](https://kubernetes.io/docs/reference/config-api/kubelet-config.v1beta1/).

If the Pods are not in the manifest directory, the kubelet will terminate them. After another `fileCheckFrequency` cycle, you can move the files back, and the kubelet will recreate the Pods, completing the certificate update operation.

```shell
mv ./manifests/* ./temp/
mv ./temp/* ./manifests/
```

!!! note

    If the container service uses Docker, to make the certificates take effect, you can use the following command to restart the services involved with the certificates:
    
    ```shell
    docker ps | grep -E 'k8s_kube-apiserver|k8s_kube-controller-manager|k8s_kube-scheduler|k8s_etcd_etcd' | awk -F ' ' '{print $1}' | xargs docker restart
    ```

## Update KubeConfig

During cluster setup, the **admin.conf** certificate is usually copied to **$HOME/.kube/config**. To update the contents of $HOME/.kube/config after updating admin.conf, you must run the following commands:

```shell
sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
sudo chown $(id -u):$(id -g) $HOME/.kube/config
```

## Configure Certificate Rotation for Kubelet

After completing the above operations, the update for all cluster certificates is basically complete, except for kubelet.

Kubernetes includes a feature for kubelet certificate rotation that automatically generates new keys and requests new certificates from the Kubernetes API when the current certificates are about to expire. Once the new certificates are available, they will be used for connection authentication with the Kubernetes API.

!!! note

    This feature is available in Kubernetes version 1.8.0 or higher.

To enable client certificate rotation, configure the following parameters:

- The kubelet process receives the `--rotate-certificates` parameter, which determines whether kubelet will automatically request new certificates when the currently used certificates are about to expire.

- The kube-controller-manager process receives the `--cluster-signing-duration` parameter (previously `--experimental-cluster-signing-duration` before version 1.19) to control the validity period of issued certificates.

For more details, refer to [Configure Certificate Rotation for Kubelet](https://kubernetes.io/docs/tasks/tls/certificate-rotation/).

## Automatically Update Certificates

For more efficient and convenient handling of expired or soon-to-expire Kubernetes cluster certificates, you can refer to the [K8s Version Cluster Certificate Update](https://github.com/yuyicai/update-kube-cert/blob/master/README.md).
