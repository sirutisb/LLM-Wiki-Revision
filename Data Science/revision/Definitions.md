
Reliability - A system behaving the way a user expects; it can tolerate user making mistakes, inputting invalid data without crashing and handling well. Performance is good enough for required use cases under expected load and volume. The system also prevents unauthorised access.

Fault-tolerance and resilience.
Fault: When a software or hardware doesnt work as expected.
Failure: when the entire system stops preventing the service

#### Hardware faults:
Typically related to faulty HDD, memory modules, power.
In large data centres, these faults happen all the time.
We use measures to try prevent this like: RAID (HDD), redundant PSU's hot-swappable CPUS.
But even with these large infrastructures and all these measures in place, systems will fail.

#### Software faults:
Software faults are more problematic, typically because bugs in software can be present in all devices. Its difficult to anticipate also. 
Example: CrowdStrike 2024, 8.5 million systems crashed.


Software vs Hardware fault:
Software faults are unpredictable, and all correlated, whereas hardware faults can be predictable and non correlated, we can isolate and replace those components individually, whereas software typically all ship together. 


#### Scalability:
The capability of a system to handle increased load.
Where is the bottleneck? Typically we need to find the bottlenecking factor which prevents us from scaling.



### Data Models
Relational vs Document models.
Document models struggle with many-to relationships, e.g. connections and Experiences.
If you have a document, joining those will be very costly.

Advantages of document model:
- Schema flexibility - can change fields very easily
- Locality - you have your file right there with you self contained
- Can offer closer representations to data structures used by the application
Advantages of relational:
- Better at join operations, and many-to-many relations

Document databases have schema flexibility
No schema means arbitrary keys and values can be added easily, however theres no guarantee what fields a document may contain.

They instead use a strategy called, `schema-on-read`. Attributes determined will only be defined when you read the data. 