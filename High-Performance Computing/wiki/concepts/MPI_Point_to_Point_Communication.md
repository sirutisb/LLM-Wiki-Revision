---
title: "MPI Point-to-Point Communication"
tags: [hpc, week-4, mpi, communication]
date: 2026-05-05
---

# MPI Point-to-Point Communication

Point-to-point communication in MPI involves passing messages between a specific pair of processes within a given communicator. It relies on explicit send and receive function calls.

## Blocking Send and Receive

The basic point-to-point operations are blocking, meaning they halt execution until it is safe to proceed (e.g., until the buffer can be reused or the message is fully received).

*   **`MPI_Send`**: Sends a message to a specific destination process.
    ```c
    int MPI_Send(void *buf, int count, MPI_Datatype datatype, int dest, int tag, MPI_Comm comm)
    ```
    *   `buf`: Send buffer.
    *   `count`: Number of data items to send (not bytes).
    *   `datatype`: The type of data being sent.
    *   `dest`: The rank of the destination process.
    *   `tag`: A user-defined integer label to identify the communication.
    *   `comm`: The communicator.

*   **`MPI_Recv`**: Receives a message from a specific source process.
    ```c
    int MPI_Recv(void *buf, int count, MPI_Datatype datatype, int source, int tag, MPI_Comm comm, MPI_Status *status)
    ```
    *   `buf`: Receive buffer.
    *   `source`: The rank of the source process.
    *   `status`: Output structure containing the rank and tag received from.

## MPI Data Types

Message lengths in MPI are defined by the number of elements of a specific `MPI_Datatype`, rather than the total number of bytes. Examples of MPI C data types include `MPI_CHAR`, `MPI_INT`, `MPI_LONG`, `MPI_FLOAT`, and `MPI_DOUBLE`.

See also: [MPI Non-blocking Communication](../concepts/MPI_Non_blocking_Communication.md)