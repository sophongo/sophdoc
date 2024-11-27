# Container Lifecycle Configuration

A Pod follows a predefined lifecycle, starting from the __Pending__ phase. If at least one container within the Pod starts successfully, it transitions to the __Running__ state. If any container in the Pod ends in a failed state, the status changes to __Failed__. The following __phase__ field values indicate which stage of the lifecycle a Pod is in.

Value | Description
:-----|:-----------
__Pending__ <br />(Pending) | The Pod has been accepted by the system, but one or more containers have not yet been created or started. This phase includes the time spent waiting for the Pod to be scheduled and the time taken to download the image over the network.
__Running__ <br />(Running) | The Pod has been bound to a node, and all containers in the Pod have been created. At least one container is still running, or is in the process of starting or restarting.
__Succeeded__ <br />(Succeeded) | All containers in the Pod have terminated successfully and will not restart.
__Failed__ <br />(Failed) | All containers in the Pod have terminated, and at least one container has terminated due to a failure. This means the container exited with a non-zero status or was terminated by the system.
__Unknown__ <br />(Unknown) | The status of the Pod cannot be obtained for some reason, typically due to a failure in communication with the host where the Pod is located.

When creating a workload in the AI computing platform, images are typically used to specify the runtime environment of the container. By default, during image build, the __Entrypoint__ and __CMD__ fields can be used to define the commands and parameters executed at runtime. If there is a need to change the commands and parameters before starting, after starting, or before stopping the container, the lifecycle event commands and parameters can be set to override the default commands and parameters in the image.

## Lifecycle Configuration

Configure the startup command, post-start command, and pre-stop command of the container according to business needs.

| Parameter | Description | Example Value |
| :-- | :--- | :---- |
| Startup Command | [Type] Optional <br /> [Meaning] The container will start according to the startup command. | |
| Post-Start Command | [Type] Optional <br /> [Meaning] The command triggered after the container starts. | |
| Pre-Stop Command | [Type] Optional <br /> [Meaning] The command executed by the container upon receiving a stop command. This ensures that running business processes can be drained in advance during upgrades or instance deletions. | |

### Startup Command

Configure the startup command according to the table below.

| Parameter | Description | Example Value |
| :-- | :--- | :---- |
| Run Command | [Type] Required <br /> [Meaning] Input an executable command, separating multiple commands with spaces. If the command itself contains spaces, it should be enclosed in quotes (“”). <br /> [Meaning] For multiple commands, it is recommended to use /bin/sh or another shell for the run command, passing all other commands as arguments. | /run/server |
| Run Parameters | [Type] Optional <br /> [Meaning] Input parameters to control the container's run command. | port=8080 |

### Post-Start Command

The AI computing platform provides two handling types for configuring the post-start command: command line scripts and HTTP requests. You can choose the configuration method that suits you based on the table below.

**Command Line Script Configuration**

| Parameter | Description | Example Value |
| :-- | :--- | :---- |
| Run Command | [Type] Optional <br /> [Meaning] Input an executable command, separating multiple commands with spaces. If the command itself contains spaces, it should be enclosed in quotes (“”). <br /> [Meaning] For multiple commands, it is recommended to use /bin/sh or another shell for the run command, passing all other commands as arguments. | /run/server |
| Run Parameters | [Type] Optional <br /> [Meaning] Input parameters to control the container's run command. | port=8080 |

### Pre-Stop Command

The AI computing platform provides two handling types for configuring the pre-stop command: command line scripts and HTTP requests. You can choose the configuration method that suits you based on the table below.

**HTTP Request Configuration**

| Parameter | Description | Example Value |
| :-- | :--- | :---- |
| URL Path | [Type] Optional <br /> [Meaning] The URL path for the request. <br /> [Meaning] For multiple commands, it is recommended to use /bin/sh or another shell for the run command, passing all other commands as arguments. | /run/server |
| Port | [Type] Required <br /> [Meaning] The port for the request. | port=8080 |
| Node Address | [Type] Optional <br /> [Meaning] The IP address for the request, defaulting to the IP of the node where the container is located. | |
