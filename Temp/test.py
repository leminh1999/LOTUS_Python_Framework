import math
n = 2
squareRootOfN = math.sqrt(n)

print('''\
{dashes}
{d:<16}{r:<15}{p:<}
{dashes}'''.format(dashes = '-'*50, d = ' # of Decimals', r = 'New Root', p = 'Percent error'))
for a in range(0,10):
    preRoot = float(int(squareRootOfN * 10**a))
    newRoot = preRoot/10**a
    percentError = (n - newRoot**2)/n
    print('  {d:<14}{r:<15}{p:13.9%}'.format(d = a, r = newRoot, p = percentError))
    
print('-'*100)