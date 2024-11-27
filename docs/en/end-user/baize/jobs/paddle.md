# PaddlePaddle Jobs

PaddlePaddle is an open-source deep learning platform developed by Baidu, supporting a rich variety of neural network models and distributed training methods. PaddlePaddle jobs can be trained using either single-node or distributed modes. On the AI Lab platform, we provide support for PaddlePaddle jobs, allowing you to quickly create PaddlePaddle jobs for model training through a graphical interface.

This tutorial will guide you on how to create and run both single-node and distributed PaddlePaddle jobs on the AI Lab platform.

## Job Configuration Overview

- **Job Type** : `PaddlePaddle`, supporting both single-node and distributed modes.
- **Running Environment** : Choose an image that includes the PaddlePaddle framework or install necessary dependencies within the job.

## Job Running Environment

We use the `registry.baidubce.com/paddlepaddle/paddle:2.4.0rc0-cpu` image as the base running environment for the job. This image comes pre-installed with the PaddlePaddle framework and is suitable for CPU computations. If you need to use GPU, choose the proper GPU version of the image.

> **Note** : For information on how to create and manage environments, refer to the [Environment List](../dataset/environments.md).

## Creating a PaddlePaddle Job

### PaddlePaddle Single-node Training Job

#### Steps to Create

1. **Log in to the Platform** : Log in to the AI Lab platform and click **Job Center** in the left navigation bar to enter the **Training Jobs** page.
2. **Create Job** : Click the **Create** button in the upper right corner to enter the job creation page.
3. **Select Job Type** : In the pop-up window, select the job type as `PaddlePaddle`, then click **Next**.
4. **Fill in Job Information** : Enter the job name and description, for example, “PaddlePaddle Single-node Training Job”, then click **Confirm**.
5. **Configure Job Arguments** : Configure the running arguments, image, resources, and other information according to your needs.

#### Running Arguments

- **Start Command** : `python`
- **Command Arguments** :

    ```bash
    -m paddle.distributed.launch run_check
    ```

    **Explanation** :

    - `-m paddle.distributed.launch`: Uses the distributed launch module provided by PaddlePaddle, which can also be used in single-node mode for easier future migration to distributed mode.
    - `run_check`: A test script provided by PaddlePaddle to check if the distributed environment is set up correctly.

#### Resource Configuration

- **Replica Count** : 1 (single-node job)
- **Resource Requests** :
    - **CPU** : Set according to needs, recommended at least 1 core
    - **Memory** : Set according to needs, recommended at least 2 GiB
    - **GPU** : If GPU is needed, choose the GPU version of the image and allocate proper GPU resources

#### Complete PaddleJob Configuration Example

Below is the YAML configuration for a single-node PaddleJob:

```yaml
apiVersion: kubeflow.org/v1
kind: PaddleJob
metadata:
    name: paddle-simple-cpu
    namespace: kubeflow
spec:
    paddleReplicaSpecs:
        Worker:
            replicas: 1
            restartPolicy: OnFailure
            template:
                spec:
                    containers:
                        - name: paddle
                          image: registry.baidubce.com/paddlepaddle/paddle:2.4.0rc0-cpu
                          command:
                              [
                                  'python',
                                  '-m',
                                  'paddle.distributed.launch',
                                  'run_check',
                              ]
```

**Configuration Explanation** :

- `apiVersion` and `kind`: Specify the API version and type of resource; here it is `PaddleJob`.
- `metadata`: Metadata including the job name and namespace.
- `spec`: Detailed configuration of the job.
    - `paddleReplicaSpecs`: Replica configuration for the PaddlePaddle job.
        - `Worker`: Specifies the configuration for worker nodes.
            - `replicas`: Number of replicas, here set to 1 for single-node training.
            - `restartPolicy`: Restart policy set to `OnFailure`, indicating that the job will automatically restart if it fails.
            - `template`: Pod template defining the running environment and resources for the container.
                - `containers`: List of containers.
                    - `name`: Container name.
                    - `image`: The image used.
                    - `command`: Start command and arguments.

#### Submitting the Job

Once the configuration is complete, click the **Submit** button to start running the PaddlePaddle single-node job.

#### Viewing the Results

After the job is successfully submitted, you can enter the **Job Details** page to view resource usage and the job's running status. You can access **Workload Details** from the upper right corner to see the log output during the run.

**Example Output** :

```bash
run check success, PaddlePaddle is installed correctly on this node :)
```

This indicates that the PaddlePaddle single-node job has run successfully and the environment is configured correctly.

---

### PaddlePaddle Distributed Training Job

In distributed mode, PaddlePaddle jobs can utilize multiple computing nodes to complete training, improving training efficiency.

#### Steps to Create

1. **Log in to the Platform** : Same as above.
2. **Create Job** : Click the **Create** button in the upper right corner to enter the job creation page.
3. **Select Job Type** : Select the job type as `PaddlePaddle`, then click **Next**.
4. **Fill in Job Information** : Enter the job name and description, for example, “PaddlePaddle Distributed Training Job”, then click **Confirm**.
5. **Configure Job Arguments** : Configure the running arguments, image, resources, and other information according to your needs.

#### Running Arguments

- **Start Command** : `python`
- **Command Arguments** :

    ```bash
    -m paddle.distributed.launch train.py --epochs=10
    ```

    **Explanation** :

    - `-m paddle.distributed.launch`: Uses the distributed launch module provided by PaddlePaddle.
    - `train.py`: Your training script, which needs to be included in the image or mounted into the container.
    - `--epochs=10`: Sets the number of training epochs to 10.

#### Resource Configuration

- **Job Replica Count** : Set according to `Worker` replica count; here it is 2.
- **Resource Requests** :
    - **CPU** : Set according to needs, recommended at least 1 core
    - **Memory** : Set according to needs, recommended at least 2 GiB
    - **GPU** : If GPU is needed, choose the GPU version of the image and allocate proper GPU resources

#### Complete PaddleJob Configuration Example

Below is the YAML configuration for a distributed PaddleJob:

```yaml
apiVersion: kubeflow.org/v1
kind: PaddleJob
metadata:
    name: paddle-distributed-job
    namespace: kubeflow
spec:
    paddleReplicaSpecs:
        Worker:
            replicas: 2
            restartPolicy: OnFailure
            template:
                spec:
                    containers:
                        - name: paddle
                          image: registry.baidubce.com/paddlepaddle/paddle:2.4.0rc0-cpu
                          command:
                              [
                                  'python',
                                  '-m',
                                  'paddle.distributed.launch',
                                  'train.py',
                              ]
                          args:
                              - '--epochs=10'
```

**Configuration Explanation** :

- `Worker`:
    - `replicas`: Set to 2, indicating that 2 worker nodes will be used for distributed training.
    - Other configurations are similar to the single-node mode.

#### Setting Job Replica Count

When creating a distributed PaddlePaddle job, you need to set the **Job Replica Count** correctly based on the replica count configured in `paddleReplicaSpecs`.

- **Total Replicas** = `Worker` replica count
- In this example:
    - `Worker` replica count: 2
    - **Total Replicas** : 2

Therefore, in the job configuration, you need to set the **Job Replica Count** to **2**.

#### Submitting the Job

Once the configuration is complete, click the **Submit** button to start running the PaddlePaddle distributed job.

#### Viewing the Results

You can enter the **Job Details** page to view the job's running status and resource usage. You can check the log output from each worker node to confirm that the distributed training is running correctly.

**Example Output** :

```bash
Worker 0: Epoch 1, Batch 100, Loss 0.5
Worker 1: Epoch 1, Batch 100, Loss 0.6
...
Training completed.
```

This indicates that the PaddlePaddle distributed job has run successfully, and the model training has been completed.

---

## Summary

Through this tutorial, you have learned how to create and run both single-node and distributed PaddlePaddle jobs on the AI Lab platform. We provided detailed information on configuring the PaddleJob and how to specify running commands and resource requirements in the job. We hope this tutorial is helpful to you; if you have any questions, refer to other documents provided by the platform or contact technical support.

---

## Appendix

- **Notes** :
    - **Training Script** : Ensure that `train.py` (or other training scripts) exists inside the container. You can place the script in the container through custom images or by mounting persistent storage.
    - **Image Selection** : Choose the appropriate image based on your needs, such as using `paddle:2.4.0rc0-gpu` for GPU.
    - **Argument Adjustment** : You can modify the `command` and `args` to pass different training arguments.

- **Reference Documents** :
    - [PaddlePaddle Official Documentation](https://www.paddlepaddle.org.cn/documentation/docs/en/2.6/guides/index_en.html)
    - [Kubeflow PaddleJob Guide](https://www.kubeflow.org/docs/components/training/user-guides/paddle/)
