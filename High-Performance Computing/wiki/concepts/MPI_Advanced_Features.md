---
title: "Advanced MPI Features: Wildcards and Communicators"
tags: [hpc, week-8, mpi]
date: 2026-05-05
---

# Advanced MPI Features

To build dynamic patterns like the Manager-Worker model, standard point-to-point communication with fixed targets is insufficient.

## MPI Wildcards
When a manager process waits for a worker to request work, it does not know *which* worker will finish next.
*   `MPI_ANY_SOURCE`: Used in `MPI_Recv` to accept a message from any process rank.
*   `MPI_ANY_TAG`: Used to accept a message with any tag.
To respond to the specific worker that sent the message, the manager inspects the `MPI_Status` object, which populates `status.MPI_SOURCE` and `status.MPI_TAG` upon receiving the message.

## Groups and Communicators
Sometimes, a collective communication (like `MPI_Reduce`) should only involve a subset of processes (e.g., aggregating results from workers but ignoring the manager). `MPI_COMM_WORLD` includes everyone.
To isolate communication:
1.  Extract the group from the current communicator (`MPI_Comm_group`).
2.  Create a new group, for instance by excluding the manager rank (`MPI_Group_excl`) or including specific ranks (`MPI_Group_incl`).
3.  Create a new communicator from this group (`MPI_Comm_create`).
4.  Perform the collective operation using the new communicator.
5.  Free the group and communicator (`MPI_Group_free`, `MPI_Comm_free`).