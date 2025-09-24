def moms(pris, proc):
    proc *= 0.01
    return(pris + (pris*proc))
print(moms(100, 20))