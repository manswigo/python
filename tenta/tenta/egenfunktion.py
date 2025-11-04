import itertools

def circular_permutations_nodir(lst):
    n = len(lst)
    perms = set(itertools.permutations(lst))
    unique = set()
    result = []
    
    for p in perms:
        # skapa alla rotationer för p och för den spegelvända
        rotations = [tuple(p[i:] + p[:i]) for i in range(n)]
        mirrored = tuple(reversed(p))
        mirror_rotations = [tuple(mirrored[i:] + mirrored[:i]) for i in range(n)]
        
        # välj en "kanonisk" representation: minsta av alla rotationer (inklusive spegel)
        rep = min(rotations + mirror_rotations)
        
        if rep not in unique:
            unique.add(rep)
            result.append(list(rep))
    
    return result