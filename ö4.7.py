
while True:
    points = []
    diff = float(input('Svårighet: '))
    if diff < 0:
        break
    antal = int(input('Hur många domare'))
    if antal < 3:
        antal = -1
    if antal < 0:
        break
    
    for n in range(1, antal + 1):
        new_point = float(input('Poäng: '))
        if new_point < 0:
            break
        points.append(new_point)
    points.sort()
    points.pop(0)
    points.pop(-1)
    final = (sum(points)/len(points))*3*diff
    print(f'Det blev {final: .2f} poäng')
