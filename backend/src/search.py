def levenshtein_distance(x: str, y: str) -> int:
    n, m = len(x), len(y)

    T = [[0] * (m + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        T[i][m] = n - i + 1
    for j in range(1, m + 1):
        T[n][j] = m - j + 1

    for i in range(n - 1, -1, -1):
        for j in range(m - 1, -1, -1):
            delta = 0 if x[i] == y[j] else 1
            T[i][j] = min(delta + T[i + 1][j + 1], 1 + T[i + 1][j], 1 + T[i][j + 1])

    return T[0][0] - 1
