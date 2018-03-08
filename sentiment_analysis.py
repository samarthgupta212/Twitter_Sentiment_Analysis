from __future__ import division
import codecs,math,os
vocabulary={}
categories=['neg','pos']
bucket='1'
def train(category,bucket):
    s='C:\Users\Superuser\Documents\stopwords.txt'
    stopwords=open(s,'r')
    stopwords=stopwords.readlines()
    counts={}
    total=0
    c=os.listdir('C:/txt_sentoken'+'/'+category)
    for i in c:
        if i!=bucket:            
            k=os.listdir('C:/txt_sentoken'+'/'+category+'/'+i)
            for j in k:
                currentdir='C:/txt_sentoken'+'/'+category+'/'+i+'/'+j
                f=codecs.open(currentdir,'r')
                for line in f:
                    tokens=line.split()
                    for token in tokens:
                        token=token.strip(',.:;/-')
                        token=token.lower()
                        if token!='' and not token+'\n' in stopwords:
                            counts.setdefault(token,0)
                            counts[token]+=1
                            vocabulary.setdefault(token,0)
                            vocabulary[token]+=1
                            total+=1

                f.close()

    return counts,total

def bayestext(bucket):
    prob={}
    totals={}
    delete=[]
    
    for category in categories:
        prob[category],totals[category]=train(category,bucket)

    for word in vocabulary:
        if vocabulary[word]<2+1:
            delete.append(word)

    for word in delete:
        del vocabulary[word]

    length=len(vocabulary)
    for category in categories:
        denominator=totals[category]+length
        for word in vocabulary:
            if word in prob[category]:
                count=prob[category][word]
            else:
                count=1

            prob[category][word]=float(count+1)/denominator

    print 'Done Training'
    return prob,totals


x,y=bayestext(bucket)
def classify(category):
    
    currentdir='C:/txt_sentoken'+'/'+category+'/'+ bucket
    c=os.listdir(currentdir)
    
    result={}
    m=0
    n=len(c)
    z=y['pos']+y['neg']
    for i in categories:
        result[i]=math.log(0.5)
        
    for i in c:
        f=codecs.open(currentdir+'/'+i,'r')
        for line in f:
            tokens=line.split()
            for token in tokens:            
                token=token.strip(',.:;/-')
                token=token.lower()
                if token in vocabulary:
                    for i in categories:
                        result[i]+=math.log(x[i][token])

        f.close()
        r=list(result.items())
        r.sort(key=lambda tuple: tuple[1], reverse = True)
        if r[0][0]==category:
            m+=1
            
        for i in categories:
            result[i]=math.log(y[i]/len(vocabulary))

    return m,n
    
def test():
    p=0
    q=0
    for category in categories:
        m,n=classify(category)
        p+=m
        q+=n
        
    print p,q
          
test()            
            
    
    
    
            
