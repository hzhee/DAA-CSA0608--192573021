# Student B Initial Design
Split at the midpoint. Base case: a single change. For a crossing candidate, scan left from midpoint for the best suffix and right for the best prefix. Combine their sums. Strength: makes the boundary explicit. Weakness: needs the left/right recursive results to cover candidates wholly on either side.
