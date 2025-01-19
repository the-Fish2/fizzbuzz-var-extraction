def binarysearch(a):
    x=5
    for i in range(len(a)):
        for j in range(len(a)):
            if a[i]==a[j]:
                a[i]=a[i]+1
    return a

a=[4,2,7,1,3]
print(binarysearch(a))