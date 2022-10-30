The GPSR protocol is being used to route messages between OBU's(on-board units).

GPSR makes greedy forwarding decisions based on only information about a router’s immediate neighbours in the network topology.\ 
When a packet reaches a region where greedy forwarding is impossible, the algorithm recovers by routing around the perimeter of the region.

Greedy forwarding’s great advantage is its reliance only on knowledge of the forwarding node’s immediate neighbors. The state required is negligible, and
dependent on the density of nodes in the wireless network, not the total number of destinations in the network.

It has significant advantages when compared to existing protocols like distance-vector routing and link-state routing protocol.
