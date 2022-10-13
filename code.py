import pandas as pd
data=pd.read_csv('data.csv',)

data=data.values

while True:
    try:
        minsup=int(input('please Enter Minimum Support: '))
        break
    except Exception :
        print('please enter a intger number!!')

class Fp_Growth:
    # cleaning the data by removing the None values
    def preprossing(data):
            newdata=[]
            for i in range(len(data)):
                transaction=[]
                for j in range(len(data[i])):
                    if str(data[i,j])=='nan':
                        continue
                    else:
                        transaction.append(data[i,j])
                newdata.append(set(transaction))
            return newdata
    # get the list of single item set in the data set
    def firstitemset(data):
        firstitemset=[]
        for i in data:
            for j in i:
                item=set({})
                item.add(j)
                if item in firstitemset:
                    continue
                else:
                    firstitemset.append(item)
        return firstitemset

    def frequent_candidate(frequent_itemset):
        pattern_generate=[]
        for i in frequent_itemset:
            
            pattern_generate.append(set(i))
        return pattern_generate

    def support_count(data,candidate,minsup):
        frequent_item={}
        for i in candidate:
            support=0
            for j in data:
                element=[ s for s in i if s in j ]
                if len(element)==len(i):
                    support+=1
            if support >=minsup:
                frequent_item[tuple(i)]=support
        frequent_item = sorted(frequent_item.items(), key=lambda x: x[1], reverse=True)
        return dict(frequent_item)
    
    def candidate_generated(frequent_itemset,scan):
        candidate=[]
        i=0
        while i<len(frequent_itemset):
                    j=i+1
                    while j<len(frequent_itemset):
                        pattren=list(dict.fromkeys(list(frequent_itemset[i])+list(frequent_itemset[j])))
                        if set(pattren) not in candidate and len(pattren)==scan:
                            candidate.append(set(pattren))
                        j+=1
                    i+=1
        return candidate

    def ordered_itemlist(data,first_itemset):
        i=0
        while i<len(data):
            transaction=[]
            for j in first_itemset:
                if j[0] in data[i]:
                    transaction.append(j[0])
            data[i]=transaction
            i+=1
        return data

    def conditional_pattern(data,first_itemset):
        tree={}
        for i in data:
            for j in first_itemset:
                if j[0] in i:
                    index=i.index(j[0])
                    if index==0:
                        continue
                    if i[index] in tree:
                        tree[i[index]].append(i[0:index])
                    else:
                        tree[i[index]]=[i[0:index]]
        return tree

    def conditional_fptree(tree,first_itemset,minsup):
        for i in tree:
            support_item=Fp_Growth.support_count(tree[i],first_itemset,minsup)
            support_item=[set(i) for i in list(support_item.keys())]
            tree[i]=support_item
        return tree

    def frequent_itemset_generated(data,conditional_fptree,minsup):
        frequent_pattern=[]
        for i in conditional_fptree:
            if len(conditional_fptree[i])==1:
                conditional_fptree[i][0].add(i)
                frequent_pattern+=Fp_Growth.support_count(data,conditional_fptree[i],minsup)
            else:
                L=[set(list(item)+[i]) for item in conditional_fptree[i]]
                conditional_fptree[i]=L
                frequent_itemset=Fp_Growth.support_count(data,conditional_fptree[i],minsup)
                frequent_pattern+=frequent_itemset
                scan=2
                while scan<=len(conditional_fptree[i]):
                    scan+=1
                    frequent_itemset=Fp_Growth.frequent_candidate(frequent_itemset)
                    candidate_itemset=Fp_Growth.candidate_generated(frequent_itemset,scan)
                    frequent_itemset=Fp_Growth.support_count(data,candidate_itemset,minsup)
                    frequent_pattern+=frequent_itemset
        return frequent_pattern

    def show(first_itemset,frequent_pattern):
        frequent_itemsets=list(first_itemset)+frequent_pattern
        frequent_itemsets=[ set(pattren)  for pattren in frequent_itemsets]
        print('frequent items sets :')
        print(frequent_itemsets)




data=Fp_Growth.preprossing(data)
first_condidate=Fp_Growth.firstitemset(data)
first_itemset=Fp_Growth.support_count(data,first_condidate,minsup)
sort_items=Fp_Growth.ordered_itemlist(data,first_itemset)
conditional_pattern=Fp_Growth.conditional_pattern(data,first_itemset)
conditional_fptree=Fp_Growth.conditional_fptree(conditional_pattern,first_itemset,minsup)
frequent_pattern=Fp_Growth.frequent_itemset_generated(data,conditional_fptree,minsup)
Fp_Growth.show(first_itemset,frequent_pattern)