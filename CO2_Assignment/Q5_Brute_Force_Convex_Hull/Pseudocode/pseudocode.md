# Q5 – Brute-Force Convex Hull Pseudocode
## Drone Flight Zone Boundary Detection
### Student: HRUZHEECAYSHAN T K | Reg No: 192573021 | CO2 Assignment

---

## Geometric Foundation

**Design Starting Point (given):**
> An edge from point Pᵢ to Pⱼ is on the convex hull if and only if
> ALL other points lie on the SAME SIDE of (or on) the line through Pᵢ and Pⱼ.

**Cross Product Test:**
For directed edge Pᵢ → Pⱼ and test point Pₖ:
```
cross = (Pⱼ.x − Pᵢ.x) × (Pₖ.y − Pᵢ.y) − (Pⱼ.y − Pᵢ.y) × (Pₖ.x − Pᵢ.x)

cross > 0  →  Pₖ is to the LEFT  of edge Pᵢ→Pⱼ
cross < 0  →  Pₖ is to the RIGHT of edge Pᵢ→Pⱼ
cross = 0  →  Pₖ is COLLINEAR with Pᵢ and Pⱼ
```

---

## Algorithm: BruteForceConvexHull

```
ALGORITHM BruteForceConvexHull(P[0..n-1])
// Find all edges forming the convex hull boundary
// Input : Array P of n points
// Output: Set of hull vertices (ordered), edge_check_count

  hull_edges  ← empty set
  edge_checks ← 0

  FOR i ← 0 TO n-1 DO
      FOR j ← 0 TO n-1 DO
          IF i = j THEN CONTINUE END IF

          all_same_side ← TRUE
          sign          ← 0           // 0=undecided, 1=left, -1=right

          FOR k ← 0 TO n-1 DO
              IF k = i OR k = j THEN CONTINUE END IF
              edge_checks ← edge_checks + 1

              cross ← (P[j].x − P[i].x) × (P[k].y − P[i].y)
                     − (P[j].y − P[i].y) × (P[k].x − P[i].x)

              IF cross ≠ 0 THEN
                  s ← SIGN(cross)
                  IF sign = 0 THEN
                      sign ← s
                  ELSE IF s ≠ sign THEN
                      all_same_side ← FALSE
                      BREAK          // Points on BOTH sides → not a hull edge
                  END IF
              END IF
          END FOR

          IF all_same_side THEN
              ADD (i, j) TO hull_edges
          END IF
      END FOR
  END FOR

  hull_vertices ← EXTRACT_UNIQUE_POINTS(hull_edges)
  SORT hull_vertices by angle from centroid    // For ordered boundary
  RETURN hull_vertices, edge_checks
```

**Step-by-Step Logic:**
1. Consider every ORDERED pair of points (Pᵢ, Pⱼ) as a candidate directed edge.
2. For each candidate edge, examine ALL remaining points Pₖ.
3. Compute the **cross product** to determine which side of edge Pᵢ→Pⱼ point Pₖ lies on.
4. Track the sign of the first non-collinear cross product encountered.
5. If ANY subsequent cross product has the **opposite sign** → points on both sides → NOT a hull edge.
6. If ALL points are on the SAME side (or collinear) → edge IS on the convex hull.
7. Collect all hull edges; extract unique hull vertices; order by angle for boundary visualisation.

---

## Correctness Argument (Geometric Reasoning)

**Why the cross product test correctly identifies hull edges:**

The convex hull is the **smallest convex polygon** containing all points.
By the definition of convexity, every edge of this polygon must have ALL
interior points (and all other polygon vertices) on **one side only** — the interior side.

If even ONE point lay on the **opposite side** of a hull edge, then:
- The polygon would be non-convex at that edge (a dent or concavity).
- This contradicts the requirement that the hull is convex.

The cross product of vectors (Pᵢ→Pⱼ) and (Pᵢ→Pₖ) gives the **signed area**
of triangle (Pᵢ, Pⱼ, Pₖ). Its sign tells which side of directed line Pᵢ→Pⱼ
point Pₖ lies on. If ALL signs agree, ALL points are on ONE side → valid hull edge.

**This is a geometric necessity, not an empirical observation.**

---

## Complexity Analysis

```
Edge candidates   = n × (n-1)                    [ordered pairs]
Checks per edge   = up to (n-2)                   [remaining points]
Total edge checks = n × (n-1) × (n-2) ∈ O(n³)
```

| n   | Edge Checks     | When n doubles |
|-----|-----------------|---------------|
| 5   | 60              | —             |
| 10  | 720             | 12x           |
| 20  | 6,840           | ~9.5x         |
| 50  | 117,600         | ~8x           |
| 100 | 970,200         | ~8x           |

When n doubles → edge checks multiply by ~8 (**confirms O(n³)**)

**Improvement:** Graham Scan / Jarvis March → O(n log n) or O(nh) where h = hull size.

---

## Test Configurations

**Test 1 – Mixed boundary + interior:**
```
Points: (0,0),(4,0),(4,4),(0,4),(2,2),(1,1),(3,3),(2,0.5)
Expected hull: (0,0),(4,0),(4,4),(0,4)
```

**Test 2 – Challenging: collinear points + near-boundary points:**
```
Points: (0,0),(1,0),(2,0),(2,2),(1,2),(0,2),(1,1),(0.5,0.5)
Tests: collinear edge points, interior points close to boundary
Expected hull: (0,0),(2,0),(2,2),(0,2)
```
