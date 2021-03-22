import sys
import csv

def data(file):
    with open (file,'r') as f:
        next(f)
        data=list()
        for row in f:
            data.append(row.strip().split('\t'))
    return data


def train(data,split_index): #training, get a dictionary
    attributelist=list()#get the two type of attributes
    resultlist=list()#get the two type of result
    for row in data:
        attribute=row[split_index]
        result=row[-1]
        if attribute not in attributelist:
            attributelist.append(attribute)
        if result not in resultlist:
            resultlist.append(result)
    attribute0=list()#list of attribute==0
    attribute1=list()#list of attribute==1      
    for row in data:
        if row[split_index]==attributelist[0]:
            attribute0.append([row[split_index],row[-1]])
        else:
            attribute1.append([row[split_index],row[-1]])
    
    att0_result0=attribute0.count([attributelist[0],resultlist[0]])
    att0_result1=attribute0.count([attributelist[0],resultlist[1]])
    att1_result0=attribute1.count([attributelist[1],resultlist[0]])
    att1_result1=attribute1.count([attributelist[1],resultlist[1]])
    
    match=dict()
    if att0_result0>att0_result1:
        match[attributelist[0]]=resultlist[0]
    else:
        match[attributelist[0]]=resultlist[1]
    if att1_result0>att1_result1:
        match[attributelist[1]]=resultlist[0]
    else:
        match[attributelist[1]]=resultlist[1]
    return match

def test(data,rule,split_index):#testing, get a forcast list
    testresult=list()
    for row in data:
        testresult.append(rule[row[split_index]])
    return testresult

def writefile(test_out,testlist):
    writefile=open(test_out,'w')
    for i in testlist:
        writefile.write('%s\n'%(i))
    writefile.close()

def errorno(data,rule,split_index):
    count=0
    errornum=0
    for row in data:
        count+=1
        if rule[row[split_index]]!=row[-1]:
            errornum+=1
    return(errornum/count)

def writemetrics(metrics_out,error_train,error_test):
    writefile=open(metrics_out,'w')
    writefile.write('error(train): %f\n'%(error_train))
    writefile.write('error(test): %f\n'%(error_test))
    writefile.close()

def main():
    train_input = 'politicians_train.tsv'
    test_input = 'politicians_test.tsv'
    split_index = 3
    train_out = 'pol_%s_train.labels' % split_index
    test_out = 'pol_%s_test.labels' % split_index
    metrics_out = 'pol_%s_metrics.txt' % split_index
    #train_input=sys.argv[1]
    #test_input=sys.argv[2]
    #split_index=int(sys.argv[3])
    #train_out=sys.argv[4]
    #test_out=sys.argv[5]
    #metrics_out=sys.argv[6]
    
    train_data=data(train_input)#import
    test_data=data(test_input)
    rule=train(train_data,split_index) #get the dicitionary
    trainlabel=test(train_data,rule,split_index) #get train_data result
    testlabel=test(test_data,rule,split_index) #get test_data result
    writefile(train_out,trainlabel) #write train_out file
    writefile(test_out,testlabel) #write test_out file
    
    train_error=errorno(train_data,rule,split_index)#get train_error
    test_error=errorno(test_data,rule,split_index)#get test_error
    writemetrics(metrics_out,train_error,test_error)#write metrics

if __name__=='__main__':
    main()