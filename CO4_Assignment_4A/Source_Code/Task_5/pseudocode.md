# Task 5 - Dijkstra, Bellman-Ford, and Floyd-Warshall

## Dijkstra for non-negative edges

```text
ALGORITHM Dijkstra(Graph, Source)
FOR each vertex v DO
    distance[v] <- INFINITY
    predecessor[v] <- NONE
END FOR
distance[Source] <- 0
Unsettled <- all vertices
WHILE an unsettled vertex has finite distance DO
    u <- unsettled vertex with minimum distance
    REMOVE u from Unsettled
    FOR each edge (u,v,w) DO
        IF v is in Unsettled AND distance[u] + w < distance[v] THEN
            distance[v] <- distance[u] + w
            predecessor[v] <- u
        END IF
    END FOR
END WHILE
RETURN distances and predecessors
```

## Bellman-Ford when edges may be negative

```text
ALGORITHM BellmanFord(Graph, Source)
INITIALISE distances and predecessors as for Dijkstra
REPEAT |V|-1 times
    FOR each edge (u,v,w) DO
        IF distance[u] is not INFINITY AND distance[u] + w < distance[v] THEN
            distance[v] <- distance[u] + w
            predecessor[v] <- u
        END IF
    END FOR
END REPEAT
FOR each edge (u,v,w) DO
    IF distance[u] is not INFINITY AND distance[u] + w < distance[v] THEN
        RETURN reachable negative-weight cycle detected
    END IF
END FOR
RETURN distances and predecessors; no reachable negative cycle
```

## Floyd-Warshall for all pairs

`D[k,i,j]` represents the shortest distance from `i` to `j` using only vertices `1..k` as intermediate vertices. Initialize `D[i,j]` to 0 when `i=j`, to the minimum direct-edge weight when an edge `i->j` exists, and to infinity otherwise. The in-place transition is:

```text
FOR each vertex k DO
    FOR each vertex i DO
        FOR each vertex j DO
            D[i,j] <- MIN(D[i,j], D[i,k] + D[k,j])
        END FOR
    END FOR
END FOR
```

Initialize diagonal entries to zero, direct edges to their weights, and all other entries to infinity. The state is an all-pairs matrix, unlike the single-source distance vector used by Dijkstra and Bellman-Ford.
