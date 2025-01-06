def mergesort(a):
    if len(a) < 2:
        return a
    m = len(a) // 2
    b = a[:m]
    c = a[m:]
    b = mergesort(b)
    c = mergesort(c)
    d = []
    while len(b) > 0 and len(c) > 0:
        if b[0] > c[0]:
            d.append(b.pop())
        else:
            d.append(c.pop())
    d += b
    d += c
    return d[::-1]
