

Week 7
### SLOW
Performance degradation factors:
Starvation: insufficient parallel work to keep processors busy, or uneven work
Latency: time taken for information to travel from one part of the system to the other (network, memory, Disk, system calls)
Overheads: Computational overheads involved in additional computation in starting parallel work such as starting and ending OpenMP parallel regions.
Waiting: multiple threads accessing shared resources need to wait for contention / mutexes to unblock etc.



Strong Scaling:
How much faster can we run the same problem (fixed problem) but increase the processors in order to reduce execution time.

Amdahl's Law
$$S_N=\frac{1}{s+\frac{p}{N}}$$
Weak Scaling:
let
$$T(N) = s + p = 1$$
then
$$T(1) = s + Np$$
$$S_N=\frac{T(1)}{T(N)} = \frac{s+Np}{s+p} = s + Np$$