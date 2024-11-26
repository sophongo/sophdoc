# PersistentVolumeClaim (PVC)

A persistent volume claim (PersistentVolumeClaim, PVC) expresses a user's request for storage. PVC consumes PV resources and claims a volume with a specific size and specific access mode. For example, the PV volume is required to be mounted in ReadWriteOnce, ReadOnlyMany or ReadWriteMany modes.

## Create volume statement

Currently, there are two ways to create PersistentVolumeClaims: YAML and form. These two ways have their own advantages and disadvantages, and can meet the needs of different users.

- There are fewer steps and more efficient creation through YAML, but the threshold requirement is high, and you need to be familiar with the YAML file configuration of the PersistentVolumeClaim.

- It is more intuitive and easier to create through the form, just fill in the proper values ​​according to the prompts, but the steps are more cumbersome.

### YAML creation

1. Click the name of the target cluster in the cluster list, and then click __Container Storage__ -> __PersistentVolumeClaim (PVC)__ -> __Create with YAML__ in the left navigation bar.

    

2. Enter or paste the prepared YAML file in the pop-up box, and click __OK__ at the bottom of the pop-up box.

    > Supports importing YAML files from local or downloading and saving filled files to local.

    

### Form Creation

1. Click the name of the target cluster in the cluster list, and then click __Container Storage__ -> __PersistentVolumeClaim (PVC)__ -> __Create PersistentVolumeClaim (PVC)__ in the left navigation bar.

    

2. Fill in the basic information.

    - The name, namespace, creation method, volume, capacity, and access mode of the PersistentVolumeClaim cannot be changed after creation.
    - Creation method: dynamically create a new volume claim in an existing StorageClass or volume, or create a new volume claim based on a snapshot of a volume claim.

        > The declared capacity of the volume cannot be modified when the snapshot is created, and can be modified after the creation is complete.

    - After selecting the creation method, select the desired StorageClass/volume/snapshot from the drop-down list.
    - access mode:

      - ReadWriteOnce, the PersistentVolumeClaim can be mounted by a node in read-write mode.
      - ReadWriteMany, the PersistentVolumeClaim can be mounted by multiple nodes in read-write mode.
      - ReadOnlyMany, the PersistentVolumeClaim can be mounted read-only by multiple nodes.
      - ReadWriteOncePod, the PersistentVolumeClaim can be mounted by a single Pod in read-write mode.

        

## View volume statement

Click the name of the target cluster in the cluster list, and then click __Container Storage__ -> __PersistentVolumeClaim (PVC)__ in the left navigation bar.

- On this page, you can view all PersistentVolumeClaims in the current cluster, as well as information such as the status, capacity, and namespace of each PersistentVolumeClaim.

- Supports sorting in sequential or reverse order according to the declared name, status, namespace, and creation time of the volume.

    

- Click the name of the PersistentVolumeClaim to view the basic configuration, StorageClass information, labels, comments and other information of the PersistentVolumeClaim.

    

## Expansion volume statement

1. In the left navigation bar, click __Container Storage__ -> __PersistentVolumeClaim (PVC)__ , and find the PersistentVolumeClaim whose capacity you want to adjust.

    

2. Click the name of the PersistentVolumeClaim, and then click the operation button in the upper right corner of the page and select __Expansion__ .

    

3. Enter the target capacity and click __OK__ .

    

## Clone volume statement

By cloning a volume claim, a new volume claim can be recreated based on the configuration of the cloned volume claim.

1. Enter the clone page

    - On the PersistentVolumeClaim list page, find the PersistentVolumeClaim that needs to be cloned, and select __Clone__ under the operation bar on the right.

        > You can also click the name of the PersistentVolumeClaim, click the operation button in the upper right corner of the details page and select __Clone__ .

        

2. Use the original configuration directly, or modify it as needed, and click __OK__ at the bottom of the page.

    

## Update volume statement

There are two ways to update volume claims. Support for updating volume claims via form or YAML file.

!!! note

    Only aliases, labels, and annotations for volume claims are updated.

- On the volume list page, find the PersistentVolumeClaim that needs to be updated, select __Update__ in the operation bar on the right to update it through the form, and select __Edit YAML__ to update it through YAML.

    

- Click the name of the PersistentVolumeClaim, enter the details page of the PersistentVolumeClaim, select __Update__ in the upper right corner of the page to update through the form, select __Edit YAML__ to update through YAML.

    

## Delete volume statement

On the PersistentVolumeClaim list page, find the data to be deleted, and select Delete in the operation column on the right.

> You can also click the name of the volume statement, click the operation button in the upper right corner of the details page and select __Delete__ .



## common problem

1. If there is no optional StorageClass or volume in the list, you can [Create a StorageClass](sc.md) or [Create a volume](pv.md).

2. If there is no optional snapshot in the list, you can enter the details page of the PersistentVolumeClaim and create a snapshot in the upper right corner.

    

3. If the StorageClass (SC) used by the PersistentVolumeClaim is not enabled for snapshots, snapshots cannot be made, and the page will not display the "Make Snapshot" option.
4. If the StorageClass (SC) used by the PersistentVolumeClaim does not have the capacity expansion feature enabled, the volume does not support capacity expansion, and the page will not display the capacity expansion option.

    