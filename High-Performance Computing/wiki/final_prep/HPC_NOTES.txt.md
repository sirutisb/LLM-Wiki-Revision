MPP:
One computer with a lot of processors, however
Multiple processors, lower latency
They have much better performance

Commodity cluster:
A Lot cheapers, just combine compute nodes together via interconnect.
Infiniband for example for interconnect

Loop carried dependencies:
Flow (true dependency): Read after Write
for (int i = 0; i < n; ++i) a[i] = a[i] + a[i - 1];
i depends on i-1

Anti-Dependency: Write after Read
for (int i = 0; i < n; ++i) a[i] = a[i] + a[i + 1];
i requires value at i+1 is not updated before reading

can be avoided/mitigated by writing to a different array:
b[i] = a[i] + a[i + 1];


Output Dependency: Write after Write
for (int i = 0; i < n; ++i) x = i;
// we cannot guarantee that x will end with n - 1
// we can scope x as lastprivate:
#pragma omp paralllel for default(none) lastprivate(x)

Each parallel thread will have a private copy of x, and at the end
it will "reduce" to using the last value of x


MPI:
Point to point communication functions:

int MPI_Send(void *buf, int count, MPI_Datatype datatype, int dest, int tag, MPI_Comm comm);
int MPI_Recv(void *dest, int count, MPI_Datatype datatype, int source, int tag, MPI_Comm comm, MPI_Status *status);

struct MPI_Status {
	int count;
	int cancelled;
	int MPI_SOURCE;
	int MPI_TAG;
	int MPI_ERROR;
};

Collective communication:
MPI_Bcast(void *buffer, int count, MPI_Datatype datatype, int root, MPI_Comm comm);
MPI_Scatter(void *sendbuf, int sendcount, MPI_Datatype sendtype, void *recvbuf, int recvcount, MPI_Datatype recvtype, int root, MPI_Comm comm);
MPI_Gather(void *sendbuf, int sendcount, MPI_Datatype sendtype, void *recvbuf, int recvcount, MPI_Datatype recvtype, int root, MPI_Comm comm);

MPI_Reduce(void *sendbuf, void *recvbuf, int count, MPI_Datatype type, MPI_Op op, int root, MPI_Comm comm);

MPI_Gather / MPI_AllGather
MPI_Reduce / MPI_AllReduce

AllGather and AllReduce: same signatures but no root.
They gather or reduce and send result to all processes.

Reduction operators prefixed by MPI: (MAX,MIN,SUM,PROD,LAND,BAND,LOR,BOR,LXOR,BXOR,...)


Caches and Memory:
Cache Blocking:
Exploiting the cache by storing our data which would fit onto cachelines when processing
Split work into cache-sized blocks

Test cases:
When testing performance you would use a small size but also large sizes (representative of real applications),
because larger will need stuff that doesnt fit on cache.
- Use o3 optimisation etc



Numa:
Non uniform memory access

