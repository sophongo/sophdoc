# MXNet Jobs

!!! warning

    Since the Apache MXNet project has been archived, the Kubeflow MXJob will be deprecated and removed in the future Training Operator version 1.9.

Apache MXNet is a high-performance deep learning framework that supports multiple programming languages. MXNet jobs can be trained using various methods, including single-node and distributed modes. In AI Lab, we provide support for MXNet jobs, allowing you to quickly create MXNet jobs for model training through an interface.

This tutorial will guide you on how to create and run both single-node and distributed MXNet jobs on the AI Lab platform.

## Job Configuration Overview

- **Job Type** : `MXNet`, supporting both single-node and distributed modes.
- **Running Environment** : Choose an image that contains the MXNet framework or install necessary dependencies in the job.

## Job Running Environment

We will use the `release-ci.daocloud.io/baize/kubeflow/mxnet-gpu:latest` image as the base running environment for the job. This image comes pre-installed with MXNet and its related dependencies, supporting GPU acceleration.

> **Note** : For information on how to create and manage environments, please refer to the [Environment List](../dataset/environments.md).

## Creating an MXNet Job

### MXNet Single-node Job

#### Steps to Create

1. **Log in to the Platform** : Log in to the AI Lab platform and click **Job Center** in the left navigation bar to enter the **Training Jobs** page.
2. **Create Job** : Click the **Create** button in the upper right corner to enter the job creation page.
3. **Select Job Type** : In the pop-up window, select the job type as `MXNet`, then click **Next**.
4. **Fill in Job Information** : Enter the job name and description, for example, “MXNet Single-node Training Job”, then click **Confirm**.
5. **Configure Job Arguments** : Configure the job's running arguments, image, resources, and other information according to your needs.

#### Running Arguments

- **Start Command** : `python3`
- **Command Arguments** :

    ```bash
    /mxnet/mxnet/example/gluon/mnist/mnist.py --epochs 10 --cuda
    ```

    **Explanation** :

    - `/mxnet/mxnet/example/gluon/mnist/mnist.py`: The MNIST handwritten digit recognition example script provided by MXNet.
    - `--epochs 10`: Sets the number of training epochs to 10.
    - `--cuda`: Uses CUDA for GPU acceleration.

#### Resource Configuration

- **Replica Count** : 1 (single-node job)
- **Resource Requests** :
    - **CPU** : 2 cores
    - **Memory** : 4 GiB
    - **GPU** : 1 unit

#### Complete MXJob Configuration Example

Below is the YAML configuration for a single-node MXJob:

```yaml
apiVersion: "kubeflow.org/v1"
kind: "MXJob"
metadata:
  name: "mxnet-single-job"
spec:
  jobMode: MXTrain
  mxReplicaSpecs:
    Worker:
      replicas: 1
      restartPolicy: Never
      template:
        spec:
          containers:
            - name: mxnet
              image: release-ci.daocloud.io/baize/kubeflow/mxnet-gpu:latest
              command: ["python3"]
              args:
                [
                  "/mxnet/mxnet/example/gluon/mnist/mnist.py",
                  "--epochs",
                  "10",
                  "--cuda",
                ]
              ports:
                - containerPort: 9991
                  name: mxjob-port
              resources:
                limits:
                  cpu: "2"
                  memory: 4Gi
                  nvidia.com/gpu: 1
                requests:
                  cpu: "2"
                  memory: 4Gi
                  nvidia.com/gpu: 1
```

**Configuration Explanation** :

- `apiVersion` and `kind`: Specify the API version and type of resource; here it is `MXJob`.
- `metadata`: Metadata including the job name and other information.
- `spec`: Detailed configuration of the job.
    - `jobMode`: Set to `MXTrain`, indicating a training job.
    - `mxReplicaSpecs`: Replica configuration for the MXNet job.
        - `Worker`: Specifies the configuration for worker nodes.
            - `replicas`: Number of replicas, here set to 1.
            - `restartPolicy`: Restart policy set to `Never`, indicating that the job will not restart if it fails.
            - `template`: Pod template defining the running environment and resources for the container.
                - `containers`: List of containers.
                    - `name`: Container name.
                    - `image`: The image used.
                    - `command` and `args`: Start command and arguments.
                    - `ports`: Container port configuration.
                    - `resources`: Resource requests and limits.

#### Submitting the Job

Once the configuration is complete, click the **Submit** button to start running the MXNet single-node job.

#### Viewing the Results

After the job is successfully submitted, you can enter the **Job Details** page to view resource usage and the job's running status. You can access **Workload Details** from the upper right corner to see the log output during the run.

**Example Output** :

```bash
Epoch 1: accuracy=0.95
Epoch 2: accuracy=0.97
...
Epoch 10: accuracy=0.98
Training completed.
```

This indicates that the MXNet single-node job has run successfully and the model training has been completed.

---

### MXNet Distributed Job

In distributed mode, the MXNet job can utilize multiple computing nodes to complete training, improving training efficiency.

#### Steps to Create

1. **Log in to the Platform** : Same as above.
2. **Create Job** : Click the **Create** button in the upper right corner to enter the job creation page.
3. **Select Job Type** : Select the job type as `MXNet`, then click **Next**.
4. **Fill in Job Information** : Enter the job name and description, for example, “MXNet Distributed Training Job”, then click **Confirm**.
5. **Configure Job Arguments** : Configure the running arguments, image, resources, and other information according to your needs.

#### Running Arguments

- **Start Command** : `python3`
- **Command Arguments** :

    ```bash
    /mxnet/mxnet/example/image-classification/train_mnist.py --num-epochs 10 --num-layers 2 --kv-store dist_device_sync --gpus 0
    ```

    **Explanation** :

    - `/mxnet/mxnet/example/image-classification/train_mnist.py`: The image classification example script provided by MXNet.
    - `--num-epochs 10`: Sets the number of training epochs to 10.
    - `--num-layers 2`: Sets the number of layers in the model to 2.
    - `--kv-store dist_device_sync`: Uses distributed device synchronization mode.
    - `--gpus 0`: Uses GPU for acceleration.

#### Resource Configuration

- **Job Replica Count** : 3 (including Scheduler, Server, and Worker)
- **Resource Requests for Each Role** :
    - **Scheduler** :
        - **Replica Count** : 1
        - **Resource Requests** :
            - CPU: 2 cores
            - Memory: 4 GiB
            - GPU: 1 unit
    - **Server** :
        - **Replica Count** : 1
        - **Resource Requests** :
            - CPU: 2 cores
            - Memory: 4 GiB
            - GPU: 1 unit
    - **Worker** :
        - **Replica Count** : 1
        - **Resource Requests** :
            - CPU: 2 cores
            - Memory: 4 GiB
            - GPU: 1 unit

#### Complete MXJob Configuration Example

Below is the YAML configuration for a distributed MXJob:

```yaml
apiVersion: "kubeflow.org/v1"
kind: "MXJob"
metadata:
  name: "mxnet-job"
spec:
  jobMode: MXTrain
  mxReplicaSpecs:
    Scheduler:
      replicas: 1
      restartPolicy: Never
      template:
        spec:
          containers:
            - name: mxnet
              image: release-ci.daocloud.io/baize/kubeflow/mxnet-gpu:latest
              ports:
                - containerPort: 9991
                  name: mxjob-port
              resources:
                limits:
                  cpu: "2"
                  memory: 4Gi
                  nvidia.com/gpu: 1
                requests:
                  cpu: "2"
                  memory: 4Gi
    Server:
      replicas: 1
      restartPolicy: Never
      template:
        spec:
          containers:
            - name: mxnet
              image: release-ci.daocloud.io/baize/kubeflow/mxnet-gpu:latest
              ports:
                - containerPort: 9991
                  name: mxjob-port
              resources:
                limits:
                  cpu: "2"
                  memory: 4Gi
                  nvidia.com/gpu: 1
                requests:
                  cpu: "2"
                  memory: 4Gi
    Worker:
      replicas: 1
      restartPolicy: Never
      template:
        spec:
          containers:
            - name: mxnet
              image: release-ci.daocloud.io/baize/kubeflow/mxnet-gpu:latest
              command: ["python3"]
              args:
                [
                  "/mxnet/mxnet/example/image-classification/train_mnist.py",
                  "--num-epochs",
                  "10",
                  "--num-layers",
                  "2",
                  "--kv-store",
                  "dist_device_sync",
                  "--gpus",
                  "0",
                ]
              ports:
                - containerPort: 9991
                  name: mxjob-port
              resources:
                limits:
                  cpu: "2"
                  memory: 4Gi
                  nvidia.com/gpu: 1
                requests:
                  cpu: "2"
                  memory: 4Gi
```

**Configuration Explanation** :

- **Scheduler** : Responsible for coordinating job scheduling among nodes in the cluster.
- **Server** : Used for storing and updating model arguments, enabling distributed argument synchronization.
- **Worker** : Executes the training jobs.
- **Resource Configuration** : Appropriately allocates resources to each role to ensure smooth job execution.

#### Setting Job Replica Count

When creating a distributed MXNet job, you need to correctly set the **Job Replica Count** based on the replica counts configured in `mxReplicaSpecs`.

- **Total Replicas** = Scheduler replicas + Server replicas + Worker replicas
- In this example:
    - Scheduler replicas: 1
    - Server replicas: 1
    - Worker replicas: 1
    - **Total Replicas** : 1 + 1 + 1 = 3

Therefore, in the job configuration, you need to set the **Job Replica Count** to **3**.

#### Submitting the Job

Once the configuration is complete, click the **Submit** button to start running the MXNet distributed job.

#### Viewing the Results

You can enter the **Job Details** page to view the job's running status and resource usage. You can check the log output from each role (Scheduler, Server, Worker).

**Example Output** :

```bash
INFO:root:Epoch[0] Batch [50]     Speed: 1000 samples/sec   accuracy=0.85
INFO:root:Epoch[0] Batch [100]    Speed: 1200 samples/sec   accuracy=0.87
...
INFO:root:Epoch[9] Batch [100]    Speed: 1300 samples/sec   accuracy=0.98
Training completed.
```

This indicates that the MXNet distributed job has run successfully, and the model training has been completed.

---

## Summary

Through this tutorial, you have learned how to create and run both single-node and distributed MXNet jobs on the AI Lab platform. We provided detailed information on configuring the MXJob and how to specify running commands and resource requirements in the job. We hope this tutorial is helpful to you; if you have any questions, please refer to other documents provided by the platform or contact technical support.

---

## Appendix

- **Notes** :
    - Ensure that the image you are using contains the required version of MXNet and dependencies.
    - Adjust resource configurations according to actual needs to avoid resource shortages or wastage.
    - If you need to use custom training scripts, modify the start command and arguments accordingly.

- **Reference Documents** :
    - [MXNet Official Documentation](https://mxnet.apache.org/)
    - [Kubeflow MXJob Guide](https://v1-8-branch.kubeflow.org/docs/components/training/mxnet/)
