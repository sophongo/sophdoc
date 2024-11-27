# MPI Jobs

MPI (Message Passing Interface) is a communication protocol used for parallel computing, allowing multiple computing nodes to exchange messages and collaborate. An MPI job is a job that performs parallel computation using the MPI protocol, suitable for applications requiring large-scale parallel processing, such as distributed training and scientific computing.

In AI Lab, we provide support for MPI jobs, allowing you to quickly create MPI jobs through a graphical interface for high-performance parallel computing. This tutorial will guide you on how to create and run an MPI job in AI Lab.

## Job Configuration Overview

- **Job Type** : `MPI`, used for running parallel computing jobs.
- **Running Environment** : Choose an image that has the MPI environment pre-installed or specify the installation of necessary dependencies in the job.
- **MPIJob Configuration** : Understand and configure various arguments of MPIJob, such as the number of replicas, resource requests, etc.

## Job Running Environment

Here we will use the `baize-notebook` base image and the **associated environment** method as the foundational running environment for the job. Ensure that the running environment includes MPI and related libraries, such as OpenMPI and `mpi4py`.

> **Note** : For information on how to create an environment, please refer to the [Environment List](../dataset/environments.md).

## Creating an MPI Job

### Steps to Create an MPI Job

1. **Log in to the Platform** : Log in to the AI Lab platform and click **Job Center** in the left navigation bar to enter the **Training Jobs** page.
2. **Create Job** : Click the **Create** button in the upper right corner to enter the job creation page.
3. **Select Job Type** : In the pop-up window, select the job type as `MPI`, then click **Next**.
4. **Fill in Job Information** : Fill in the job name and description, for example, “benchmarks-mpi”, then click **Next**.
5. **Configure Job Arguments** : Configure the running arguments, image, resources, and other information according to your needs.

#### Running Arguments

- **Start Command** : Use `mpirun`, which is the command to run MPI programs.
- **Command Arguments** : Input the arguments for the MPI program you want to run.

**Example: Running TensorFlow Benchmarks**

In this example, we will run a TensorFlow benchmark program using Horovod for distributed training. First, make sure that the image you are using contains the necessary dependencies, such as TensorFlow, Horovod, Open MPI, etc.

**Image Selection** : Use an image that includes TensorFlow and MPI, such as `mai.daocloud.io/docker.io/mpioperator/tensorflow-benchmarks:latest`.

**Command Arguments** :

```bash
mpirun --allow-run-as-root -np 2 -bind-to none -map-by slot \
  -x NCCL_DEBUG=INFO -x LD_LIBRARY_PATH -x PATH \
  -mca pml ob1 -mca btl ^openib \
  python scripts/tf_cnn_benchmarks/tf_cnn_benchmarks.py \
  --model=resnet101 --batch_size=64 --variable_update=horovod
```

**Explanation**:

- `mpirun`: The MPI start command.
- `--allow-run-as-root`: Allows running as the root user (usually the root user in containers).
- `-np 2`: Specifies the number of processes to run as 2.
- `-bind-to none`, `-map-by slot`: Configuration for MPI process binding and mapping.
- `-x NCCL_DEBUG=INFO`: Sets the debug information level for NCCL (NVIDIA Collective Communication Library).
- `-x LD_LIBRARY_PATH`, `-x PATH`: Passes necessary environment variables in the MPI environment.
- `-mca pml ob1 -mca btl ^openib`: MPI configuration arguments specifying transport and message layer protocols.
- `python scripts/tf_cnn_benchmarks/tf_cnn_benchmarks.py`: Runs the TensorFlow benchmark script.
- `--model=resnet101`, `--batch_size=64`, `--variable_update=horovod`: Arguments for the TensorFlow script, specifying the model, batch size, and using Horovod for argument updates.

#### Resource Configuration

In the job configuration, you need to allocate appropriate resources for each node (Launcher and Worker), such as CPU, memory, and GPU.

**Resource Example** :

- **Launcher** :

    - **Number of Replicas** : 1
    - **Resource Request** :
        - CPU: 2 cores
        - Memory: 4 GiB

- **Worker** :

    - **Number of Replicas** : 2
    - **Resource Request** :
        - CPU: 2 cores
        - Memory: 4 GiB
        - GPU: Allocate as needed

#### Complete MPIJob Configuration Example

Below is a complete MPIJob configuration example for your reference.

```yaml
apiVersion: kubeflow.org/v1
kind: MPIJob
metadata:
  name: tensorflow-benchmarks
spec:
  slotsPerWorker: 1
  runPolicy:
    cleanPodPolicy: Running
  mpiReplicaSpecs:
    Launcher:
      replicas: 1
      template:
        spec:
          containers:
            - name: tensorflow-benchmarks
              image: mai.daocloud.io/docker.io/mpioperator/tensorflow-benchmarks:latest
              command:
                - mpirun
                - --allow-run-as-root
                - -np
                - "2"
                - -bind-to
                - none
                - -map-by
                - slot
                - -x
                - NCCL_DEBUG=INFO
                - -x
                - LD_LIBRARY_PATH
                - -x
                - PATH
                - -mca
                - pml
                - ob1
                - -mca
                - btl
                - ^openib
                - python
                - scripts/tf_cnn_benchmarks/tf_cnn_benchmarks.py
                - --model=resnet101
                - --batch_size=64
                - --variable_update=horovod
              resources:
                limits:
                  cpu: "2"
                  memory: 4Gi
                requests:
                  cpu: "2"
                  memory: 4Gi
    Worker:
      replicas: 2
      template:
        spec:
          containers:
            - name: tensorflow-benchmarks
              image: mai.daocloud.io/docker.io/mpioperator/tensorflow-benchmarks:latest
              resources:
                limits:
                  cpu: "2"
                  memory: 4Gi
                  nvidia.com/gpumem: 1k
                  nvidia.com/vgpu: "1"
                requests:
                  cpu: "2"
                  memory: 4Gi
```

**Configuration Explanation**:

- `apiVersion` and `kind`: Indicate the API version and type of resource; `MPIJob` is a custom resource defined by Kubeflow for creating MPI-type jobs.
- `metadata`: Metadata containing the job name and other information.
- `spec`: Detailed configuration of the job.
    - `slotsPerWorker`: Number of slots per Worker node, typically set to 1.
    - `runPolicy`: Running policy, such as whether to clean up Pods after job completion.
    - `mpiReplicaSpecs`: Replica configuration for the MPI job.
        - `Launcher`: The launcher responsible for starting the MPI job.
            - `replicas`: Number of replicas, usually 1.
            - `template`: Pod template defining the container's running image, command, resources, etc.
        - `Worker`: The worker nodes that actually execute the job.
            - `replicas`: Number of replicas set according to parallel needs, here set to 2.
            - `template`: Pod template defining the container's running environment and resources.

#### Setting Job Replica Count

When creating an MPI job, you need to correctly set the **Job Replica Count** according to the number of replicas configured in `mpiReplicaSpecs`.

- **Total Replicas** = `Launcher` replicas + `Worker` replicas
- In this example:

    - `Launcher` replicas: 1
    - `Worker` replicas: 2
    - **Total Replicas** : 1 + 2 = 3

Therefore, in the job configuration, you need to set the **Job Replica Count** to **3**.

#### Submitting the Job

Once the configuration is complete, click the **Submit** button to start running the MPI job.

## Viewing the Running Results

After the job is successfully submitted, you can enter the **Job Details** page to view resource usage and the job's running status. From the upper right corner, you can access **Workload Details** to see the log output from each node during the run.

**Example Output** :

```bash
TensorFlow: 1.13
Model: resnet101
Mode: training
Batch size: 64
...

Total images/sec: 125.67
```

This indicates that the MPI job has successfully run, and the TensorFlow benchmark program has completed distributed training.

---

## Summary

Through this tutorial, you have learned how to create and run an MPI job on the AI Lab platform. We detailed the configuration methods for MPIJob and how to specify the running commands and resource requirements in the job. We hope this tutorial is helpful to you; if you have any questions, please refer to other documents provided by the platform or contact technical support.

---

**Appendix** :

- If your running environment does not have the required libraries pre-installed (such as `mpi4py`, Horovod, etc.), please add installation commands in the job or use an image with the relevant dependencies pre-installed.
- In practical applications, you can modify the MPIJob configuration according to your needs, such as changing the image, command arguments, resource requests, etc.
