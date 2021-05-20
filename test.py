

def xp(a, b, L, Lp):
    xp = (
        ((a * b * L) / 5) * (((2 * L + 10) / (L + Lp + 10)) ** 2.5) + 1
    )

    return xp


def xp2(b, L):
    xp = (
        b * L / 5
    )
    return xp


print(xp(1, 154, 100, 90))
print(xp2(154, 100))
