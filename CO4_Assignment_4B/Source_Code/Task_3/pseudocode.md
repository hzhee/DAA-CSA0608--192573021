```text
ALGORITHM Dijkstra(Graph, Source)
    REQUIRE every edge weight is nonnegative
    Set all distances to INFINITY and predecessors to NONE; distance[Source] <- 0
    WHILE an unsettled vertex has finite distance DO
        Choose the unsettled vertex u with minimum distance; finalize u
        FOR each outgoing edge (u,v,w) to an unsettled v DO
            IF distance[u] + w < distance[v] THEN
                distance[v] <- distance[u] + w; predecessor[v] <- u
            END IF
        END FOR
    END WHILE
    RETURN distances, predecessors, finalization order
END

ALGORITHM BellmanFord(Graph, Source)
    Initialize distances and predecessors; set distance[Source] <- 0
    REPEAT |V|-1 times, or stop early if no edge relaxes
        FOR each edge (u,v,w) DO
            IF distance[u] is finite AND distance[u]+w < distance[v] THEN
                Update distance[v] and predecessor[v]
            END IF
        END FOR
    END REPEAT
    Scan every edge once more; if a reachable edge can relax, report negative cycle
    RETURN distances, predecessors, cycle status
END

ALGORITHM FloydWarshall(Graph)
    Initialize D[i,j] to 0 on the diagonal, edge weight on an edge, INFINITY otherwise
    FOR each intermediate vertex k, each i, each j DO
        D[i,j] <- MIN(D[i,j], D[i,k] + D[k,j])
    END FOR
    RETURN D
END

ALGORITHM Warshall(Graph)
    Initialize R[i,j] from direct edges and R[i,i] <- TRUE
    FOR each intermediate vertex k, each i, each j DO
        R[i,j] <- R[i,j] OR (R[i,k] AND R[k,j])
    END FOR
    RETURN R
END
```
