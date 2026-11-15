"""Strassen multiplication with zero padding and conventional cutover."""

def add(a, b): return [[a[i][j] + b[i][j] for j in range(len(a))] for i in range(len(a))]
def sub(a, b): return [[a[i][j] - b[i][j] for j in range(len(a))] for i in range(len(a))]

def conventional(a, b):
    n = len(a)
    return [[sum(a[i][k] * b[k][j] for k in range(n)) for j in range(n)] for i in range(n)]

def strassen(a, b, cutoff=1):
    n = len(a)
    if n <= cutoff: return conventional(a, b)
    h = n // 2
    a11, a12 = [r[:h] for r in a[:h]], [r[h:] for r in a[:h]]
    a21, a22 = [r[:h] for r in a[h:]], [r[h:] for r in a[h:]]
    b11, b12 = [r[:h] for r in b[:h]], [r[h:] for r in b[:h]]
    b21, b22 = [r[:h] for r in b[h:]], [r[h:] for r in b[h:]]
    m1 = strassen(add(a11, a22), add(b11, b22), cutoff)
    m2 = strassen(add(a21, a22), b11, cutoff)
    m3 = strassen(a11, sub(b12, b22), cutoff)
    m4 = strassen(a22, sub(b21, b11), cutoff)
    m5 = strassen(add(a11, a12), b22, cutoff)
    m6 = strassen(sub(a21, a11), add(b11, b12), cutoff)
    m7 = strassen(sub(a12, a22), add(b21, b22), cutoff)
    c11 = add(sub(add(m1, m4), m5), m7)
    c12 = add(m3, m5)
    c21 = add(m2, m4)
    c22 = add(sub(add(m1, m3), m2), m6)
    return [c11[i] + c12[i] for i in range(h)] + [c21[i] + c22[i] for i in range(h)]

def strassen_multiply(a, b, cutoff=64):
    """Pad square input to a power of two, then remove padding from C."""
    n = len(a)
    if n == 0 or any(len(row) != n for row in a + b):
        raise ValueError("A and B must be non-empty square matrices of the same size")
    size = 1
    while size < n: size *= 2
    pa = [row + [0] * (size - n) for row in a] + [[0] * size for _ in range(size - n)]
    pb = [row + [0] * (size - n) for row in b] + [[0] * size for _ in range(size - n)]
    return [row[:n] for row in strassen(pa, pb, cutoff)[:n]]

if __name__ == "__main__":
    a, b = [[1, 7], [3, 5]], [[1, 3], [7, 5]]
    print("A =", a); print("B =", b)
    print("Strassen C =", strassen_multiply(a, b, cutoff=1))
    print("Verification conventional C =", conventional(a, b))
