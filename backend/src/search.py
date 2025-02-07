def edit(i, j, x, y):
    """
    Args:
        i (int): suffix start for string x
        j (int): suffix start for string y
        x (str): complete examined string
        y (str): complete examined string

    Returns:
        (int): edit distance from x_i,..., x_n to y_j,..., y_m
    """

    if i > len(x):
        return len(y) - j + 1
    if j > len(y):
        return len(x) - i + 1

    swap_cost = edit(i + 1, j + 1, x, y)

    if x[i-1] != y[j-1]:
        swap_cost += 1

    delete_cost = edit(i + 1, j, x, y) + 1
    insert_cost = edit(i, j + 1, x, y) + 1

    return min(
        swap_cost,
        delete_cost,
        insert_cost,
    )

def edit2(x, y):
    """
    Args:
        x (str)
        y (str)

    Returns:
        (int): distance
    """
    t = [[]] * len(max(x, y, key=len))
    print(t)

print(edit2("str", "sto"))
