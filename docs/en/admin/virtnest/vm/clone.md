# Cloning a Cloud Host

This article will introduce how to clone a new cloud host.

Users can clone a new cloud host, which will have the same operating system and system configuration as the original cloud host. This enables quick deployment and scaling, allowing for the rapid creation of new cloud hosts with similar configurations without the need to install from scratch.

## Prerequisites

Before using the cloning feature, the following prerequisites must be met (which are the same as those for the snapshot feature):

- Only cloud hosts that are not in an error state can use the cloning feature.
- Install Snapshot CRDs, Snapshot Controller, and CSI Driver.
  For specific installation steps, refer to [CSI Snapshotter](https://github.com/kubernetes-csi/external-snapshotter?tab=readme-ov-file#usage).
- Wait for the snapshot-controller component to be ready. This component will monitor events related to VolumeSnapshot and VolumeSnapshotContent and trigger related operations.
- Wait for the CSI Driver to be ready, ensuring that the csi-snapshotter sidecar is running in the CSI Driver. The csi-snapshotter sidecar will monitor events related to VolumeSnapshotContent and trigger related operations.
    - If the storage is Rook-Ceph, refer to [ceph-csi-snapshot](https://rook.io/docs/rook/latest-release/Storage-Configuration/Ceph-CSI/ceph-csi-snapshot/)
    - If the storage is HwameiStor, refer to [huameistor-snapshot](https://hwameistor.io/cn/docs/volumes/volume_snapshot)

## Cloning a Cloud Host

1. Click__Container Management__ in the left navigation bar, then click__Cloud Hosts__ to enter the list page. Clickthe __┇__ on the right side of the list to perform snapshot operations on cloud hosts that are not in an error state.


2. A popup will appear, requiring you to fill in the name and description for the new cloud host being cloned. The cloning operation may take some time, depending on the size of the cloud host and storage performance.


3. After a successful clone, you can view the new cloud host in the cloud host list. The newly created cloud host will be in a powered-off state and will need to be manually powered on if required.



4. It is recommended to take a snapshot of the original cloud host before cloning. If you encounter issues during the cloning process, please check whether the prerequisites are met and try to execute the cloning operation again.
