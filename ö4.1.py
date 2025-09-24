först = float(input('nytt: '))
nytt= först
störst = först
minst = först

while nytt >= 0:
    nytt = float(input('nytt: '))
    if nytt > störst:
        störst = nytt
    elif nytt < minst:
        minst = nytt 
print(störst, minst)
