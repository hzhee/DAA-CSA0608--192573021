```text
ALGORITHM Kruskal(G=(V,E))
    Sort edges by increasing weight
    Initialize one disjoint set per vertex; MST <- empty
    FOR each edge (u,v,w) in sorted order DO
        IF FIND(u) != FIND(v) THEN
            Add edge to MST; UNION(u,v)
        ELSE record rejection because it would create a cycle
        END IF
        Stop when MST contains |V|-1 edges
    END FOR
    IF fewer than |V|-1 edges were selected, report disconnected graph
    RETURN MST and its weight
END

ALGORITHM Prim(G, start)
    Put start in the visited set; add its outgoing edges to a min-priority queue
    WHILE not all vertices are visited DO
        Remove the least-weight edge crossing from visited to unvisited
        IF its unvisited endpoint is new THEN add it to MST and visited
        Add that endpoint's outgoing crossing edges to the queue
    END WHILE
    RETURN MST and its weight
END

ALGORITHM Boruvka(G)
    Initialize each vertex as its own component; MST <- empty
    WHILE more than one component remains DO
        Scan edges and record the cheapest outgoing edge for each component
        UNION each distinct recorded edge that joins different components
        Add successful unions to MST
    END WHILE
    RETURN MST and its weight
END
```
