---
MTPE: WANG0608GitHub
Date: 2024-08-15
---

# Integrating Customer Systems into AI platform (OEM IN)

OEM IN refers to the partner's platform being embedded as a submodule in AI platform, appearing in the primary
navigation bar of AI platform. Users can log in and manage it uniformly through AI platform. The implementation
of OEM IN is divided into 5 steps:

1. [Unify Domain](#unify-domain-name-and-port)
1. [Integrate User Systems](#integrate-user-systems)
1. [Integrate Navigation Bar](#integrate-navigation-bar)
1. [Customize Appearance](#customize-appearance)
1. [Integrate Permission System (Optional)](#integrate-permission-system-optional)

For specific operational demonstrations, refer to the [OEM IN Best Practices Video Tutorial](../../../videos/use-cases.md#integrating-customer-systems-into-dce-50-oem-in).

!!! note

    The open source software Label Studio is used for nested demonstrations below. In actual scenarios,
    you need to solve the following issues in the customer system:

    The customer system needs to add a Subpath to distinguish which services belong to AI platform 
    and which belong to the customer system.

## Environment Preparation

1. Deploy the AI platform environment:

    `https://10.6.202.177:30443` as AI platform

    <!-- add image later -->

1. Deploy the customer system environment:

    `http://10.6.202.177:30123` as the customer system

    Adjust the operations on the customer system during the application according to the actual situation.

1. Plan the Subpath path of the customer system: `http://10.6.202.177:30123/label-studio` (It is recommended to use a recognizable name as the Subpath, which should not conflict with
   the HTTP router of the main AI platform). Ensure that users can access the customer system through
   `http://10.6.202.177:30123/label-studio`.

    <!-- add image later -->

## Unify Domain Name and Port

1. SSH into the AI platform server.

    ```bash
    ssh root@10.6.202.177
    ```

1. Create the __label-studio.yaml__ file using the `vim` command.

    ```bash
    vim label-studio.yaml
    ```

    ```yaml title="label-studio.yaml"
    apiVersion: networking.istio.io/v1beta1
    kind: ServiceEntry
    metadata:
      name: label-studio
      namespace: ghippo-system
    spec:
      exportTo:
      - "*"
      hosts:
      - label-studio.svc.external
      ports:
      # Add a virtual port
      - number: 80
        name: http
        protocol: HTTP
      location: MESH_EXTERNAL
      resolution: STATIC
      endpoints:
      # Change to the domain name (or IP) of the customer system
      - address: 10.6.202.177
        ports:
          # Change to the port number of the customer system
          http: 30123
    ---
    apiVersion: networking.istio.io/v1alpha3
    kind: VirtualService
    metadata:
      # Change to the name of the customer system
      name: label-studio
      namespace: ghippo-system
    spec:
      exportTo:
      - "*"
      hosts:
      - "*"
      gateways:
      - ghippo-gateway
      http:
      - match:
          - uri:
              exact: /label-studio # Change to the routing address of the customer system in the Web UI entry
          - uri:
              prefix: /label-studio/ # Change to the routing address of the customer system in the Web UI entry
        route:
        - destination:
            # Change to the value of spec.hosts in the ServiceEntry above
            host: label-studio.svc.external
            port:
              # Change to the value of spec.ports in the ServiceEntry above
              number: 80
    ---
    apiVersion: security.istio.io/v1beta1
    kind: AuthorizationPolicy
    metadata:
      # Change to the name of the customer system
      name: label-studio
      namespace: istio-system
    spec:
      action: ALLOW
      selector:
        matchLabels:
          app: istio-ingressgateway
      rules:
      - from:
        - source:
            requestPrincipals:
            - '*'
      - to:
        - operation:
            paths:
            - /label-studio # Change to the value of spec.http.match.uri.prefix in VirtualService
            - /label-studio/* # Change to the value of spec.http.match.uri.prefix in VirtualService (Note: add "*" at the end)
    ```

1. Apply the __label-studio.yaml__ using the `kubectl` command:

    ```bash
    kubectl apply -f label-studio.yaml
    ```

1. Verify if the IP and port of the Label Studio UI are consistent:

    <!-- add image later -->

## Integrate User Systems

Integrate the customer system with the AI platform platform through protocols like OIDC/OAUTH,
allowing users to enter the customer system without logging in again after logging into the AI platform platform.

1. In the scenario of two AI platform, you can create SSO access through __Global Management__ -> __Access Control__ -> __Docking Portal__.

    <!-- add image later -->

    <!-- add image later -->

2. After creating, fill in the details such as the Client ID, Client Secret, and Login URL in the
   customer system's __Global Management__ -> __Access Control__ -> __Identity Provider__ -> __OIDC__,
   to complete user integration.

    <!-- add image later -->

3. After integration, the customer system login page will display the OIDC (Custom) option.
   Select to log in via OIDC the first time entering the customer system from the AI platform platform,
   and subsequently, you will directly enter the customer system without selecting again.

    <!-- add image later -->

## Integrate Navigation Bar

Refer to the tar package at the bottom of the document to implement an empty frontend sub-application,
and embed the customer system into this empty shell application in the form of an iframe.

1. Download the gproduct-demo-main.tar.gz file and change the value of the src attribute in App-iframe.vue under the src folder (the user entering the customer system):

    - The absolute address: `src="https://10.6.202.177:30443/label-studio" (AI platform address + Subpath)`
    - The relative address, such as `src="./external-anyproduct/insight"`

    ```html title="App-iframe.vue"
    <template>
      <iframe>
        src="https://daocloud.io"
        title="demo"
        class="iframe-container"
      </iframe>
    </template>

    <style lang="scss">
    html,
    body {
      height: 100%;
    }

    # app {
      display: flex;
      height: 100%;
      .iframe-container {
        border: 0;
        flex: 1 1 0;
      }
    }
    </style>
    ```

1. Delete the App.vue and main.ts files under the src folder, and rename:

    - Rename App-iframe.vue to App.vue
    - Rename main-iframe.ts to main.ts

1. Build the image following the steps in the readme (Note: before executing the last step, replace the image address in __demo.yaml__ with the built image address)

    ```yaml title="demo.yaml"
    kind: Namespace
    apiVersion: v1
    metadata:
      name: gproduct-demo
    ---
    apiVersion: apps/v1
    kind: Deployment
    metadata:
      name: gproduct-demo
      namespace: gproduct-demo
      labels:
        app: gproduct-demo
    spec:
      selector:
        matchLabels:
          app: gproduct-demo
      template:
        metadata:
          name: gproduct-demo
          labels:
            app: gproduct-demo
        spec:
          containers:
          - name: gproduct-demo
            image: release.daocloud.io/gproduct-demo # Modify this image address
            ports:
            - containerPort: 80
    ---
    apiVersion: v1
    kind: Service
    ...
    ```

After integration, the __Customer System__ will appear in the primary navigation bar of AI platform,
and clicking it will allow users to enter the customer system.

<!-- add image later -->

## Customize Appearance

!!! note

    AI platform supports customizing the appearance by writing CSS. How the customer system implements
    appearance customization in actual applications needs to be handled according to the actual situation.

Log in to the customer system, and through __Global Management__ -> __Settings__ -> __Appearance__,
you can customize platform background colors, logos, and names. For specific operations, please refer to
[Appearance Customization](../../platform-setting/appearance.md).

## Integrate Permission System (Optional)

**Method One:**

Customized teams can implement a customized module that AI platform will notify each user login event to
the customized module via Webhook, and the customized module can call the [OpenAPI](https://docs.daocloud.io/openapi/index.html)
of AnyProduct and AI platform to synchronize the user's permission information.

**Method Two:**

Through Webhook, notify AnyProduct of each authorization change (if required, it can be implemented later).

### Use Other Capabilities of AI platform in AnyProduct (Optional)

The method is to call the AI platform [OpenAPI](../../../../openapi/index.md).

## References

- Refer to [OEM OUT Document](./oem-out.md)
- Download the [tar package for gProduct-demo-main integration](./examples/gproduct-demo-main.tar.gz)
