def circle():
    pass


def reach_wall(p):
    x, y = p
    return x == 0 or x == 79 or y == 0 or y == 75


def horizontal_opposite(p1, p2):
    return (p1[1] == 0 and p2[1] == 75) or (p1[1] == 75 and p2[1] == 0)
