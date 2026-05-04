---
title: "MPI Non-blocking Communication"
tags: [hpc, week-4, mpi, communication]
date: 2026-05-05
---

# MPI Non-blocking Communication

Standard MPI point-to-point operations (`MPI_Send` and `MPI_Recv`) and traditional collectives are **blocking**. They halt execution until the message is safely received or the buffer can be reused. If sends and receives are not carefully matched across processes, blocking communications can easily lead to a deadlock.

## Non-blocking Operations

Non-blocking operations initiate a communication and immediately return, allowing the program to continue executing. This approach offers two major benefits:
1.  **Deadlock Avoidance**: Because functions return immediately, complex message exchanges don't need to be perfectly synchronized to avoid cyclic waiting.
2.  **Overlapping Computation and Communication**: A process can perform other computations while waiting for data to be transferred over the network, improving efficiency.

### Functions

*   **`MPI_Isend`**: Initiates a non-blocking send.
    ```c
    int MPI_Isend(void *buf, int count, MPI_Datatype datatype, int dest, int tag, MPI_Comm comm, MPI_Request *request)
    ```
*   **`MPI_Irecv`**: Initiates a non-blocking receive.
    ```c
    int MPI_Irecv(void *buf, int count, MPI_Datatype datatype, int source, int tag, MPI_Comm comm, MPI_Request *request)
    ```

Both functions output an `MPI_Request` handle instead of an `MPI_Status`. This handle is used to track the progress of the operation.

## Synchronization

When the data involved in the non-blocking communication is finally needed (or before the send buffer is modified again), the program must explicitly wait for the operation to complete using synchronization functions:

*   **`MPI_Wait(MPI_Request *request, MPI_Status *status)`**: Blocks until the specific request completes.
*   **`MPI_Waitall(int count, MPI_Request array_of_requests[], MPI_Status array_of_statuses[])`**: Blocks until an array of requests all complete.

*Note: Starting from version 3 of the MPI standard, non-blocking collective operations were also introduced.*