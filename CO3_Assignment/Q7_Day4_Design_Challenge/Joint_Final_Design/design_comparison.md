# Joint Final Design and Comparison
The proposals agree on halves, a singleton base case and returning an interval. Student A's proposal contributes the three-candidate result; Student B's contributes linear-time crossing computation. The final combine returns the maximum of left, right and crossing candidates. This yields `T(n)=2T(n/2)+Theta(n)`.
