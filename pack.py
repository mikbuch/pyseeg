from modules.read_csv import read

a = read('data/201507091402.csv')
a = [i[0] for i in a]

count = 0
total_lost = 0

for i in range(len(a)):
    if i != 0:
        prev = int(a[i-1])
        current = int(a[i])
        if current - prev > 1 and prev != 0:
            count += 1
            print('%d th PACKAGE LOSS' % (count))
            print('at prev:'),
            print(prev),
            print(', current:'),
            print(a[i]),
            print(' ||| difference:'),
            print(current - prev)
            total_lost += current - prev

print('\n')
print('total lost: '), 
print(total_lost)
print('number of samples aquired:'),
print(len(a))

