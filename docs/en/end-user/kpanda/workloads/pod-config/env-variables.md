---
hide:
  - toc
---

# Configuring Environment Variables

Environment variables refer to variables set in the container's runtime environment, used to add environment flags to Pods or pass configurations, supporting the configuration of environment variables for Pods in the form of key-value pairs.

The Suanfeng AI computing power platform's container management adds a graphical interface for configuring environment variables for Pods based on native Kubernetes, supporting the following configuration methods:

- **Key/Value Pair**: Use custom key-value pairs as environment variables for the container.
- **Resource Reference**: Use fields defined in the Container as the value of environment variables, such as memory limits, replica counts, etc.
- **Variable/Variable Reference (Pod Field)**: Use Pod fields as the value of environment variables, such as the Pod's name.
- **Import ConfigMap Key**: Import the value of a specific key from a ConfigMap as the value of an environment variable.
- **Import Secret Key**: Define the value of an environment variable using data from a Secret.
- **Import Secret**: Import all key-value pairs from a Secret as environment variables.
- **Import ConfigMap**: Import all key-value pairs from a ConfigMap as environment variables.
