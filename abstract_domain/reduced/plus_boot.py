import random

def make_even(a, d):
    if a % 2 != 0:
        return a + d
    return a

def make_odd(a, d):
    if a % 2 == 0:
        return a + d
    return a

def l(N):
    pos  = []
    neg = []
    for i in range(N):
        lo1 = random.randint(-100, 100)
        lo1 = make_odd(lo1, -1)
        do1 = random.randint(4, 10)
        do1 = make_even(do1,-1)
        uo1 = lo1 + do1
        uo1 = make_odd(uo1, 1)
        lo2 = random.randint(-100, 100)
        lo2 = make_odd(lo2, -1)
        do2 = random.randint(4, 10)
        do2 = make_even(do2,-1)
        uo2 = lo2 + do2
        uo2 = make_odd(uo2, 1)


        le1 = random.randint(-100, 100)
        le1 = make_even(le1, -1)
        de1 = random.randint(4, 10)
        de1 = make_even(de1,-1)
        ue1 = le1 + de1
        ue1 = make_even(ue1, 1)
        #print("even 1",le1, ue1, de1)

        #de1 = random.randint(4, 10)
        le2 = random.randint(-100, 100)
        le2 = make_even(le2, -1)
        de2 = random.randint(4, 10)
        de2 = make_even(de2,-1)
        ue2 = le2 + de2
        ue2 = make_even(ue2, 1)
        #print("even",le2, ue2, de2)

        Se1 = random.sample(range(le1, ue1+1), de1)
        Se2 = random.sample(range(le2, ue2+1), de2)
        #print(Se1, Se2)


        So1 = random.sample(range(le1-1, ue1+2), de1)
        So2 = random.sample(range(le2-1, ue2+2), de2)

        even = set(Se2).intersection(set(So2))
        odd = set(Se1).intersection(set(So1))

        a_ap = [(x) + (y) for x in odd for y in even]
        a_ap.sort()
        if not a_ap:
            continue
        #print(a_ap)
        #d = max(d1, d2)
        #positive example
        for i in range(len(a_ap)):
            a = [le1-1, ue1+1, le1, ue1, le2-1, ue2+1, le2, ue2,a_ap[i]]
            if a not in pos:
                pos.append(a)

        #left negative example
        #neg.append([l1, u1, l2, u2, a_ap[0] - d, a_ap[0] - d])
        #right negative example
        #neg.append([l1, u1, l2, u2, a_ap[-1] + d, a_ap[-1] + d])

    return pos, neg

print("main ",l(5))
