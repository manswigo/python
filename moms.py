pris = float(input('pris: '))
moms = float(input('moms i procent: '))
pris, moms = float(pris), float(moms)
moms_dec = moms/100
o_pris = pris/(1 + moms_dec)
moms_pris = pris - o_pris

print(f"Originalpriset var: {o_pris: .2f} kr och den totala momsen var: {moms_pris: .2f} kr")

