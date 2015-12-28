 #coding=utf-8
from numpy import *
#你好
def loadDataSet():
    return [[1,3,4],
            [2,3,5],
            [1,2,3,5],
            [2,5]]
    
#遍历数据集每项物品，建立1-项集
def createC1(dataSet):
    #记录每项物品的列表
    C1 = []
    #遍历每条记录
    for transaction in dataSet:
        #遍历每条记录中的物品
        for item in transaction:
            #判断如果该物品没在列表中
            if not [item] in C1:
                #将该物品加入到列表中
                C1.append([item])
    #对所有物品进行排序            
    C1.sort()
    #将列表元素映射到frozenset()中，返回列表。
    #frozenset数据类型，指被冰冻的集合，
    #集合一旦完全建立，就不能被修改。
    #即用户不能修改他们。
    return map(frozenset, C1)
#输入：数据集D、候选集Ck、最小支持度。
#候选集Ck由上一层(第k-1层)的频繁项集Lk-1组合得到。
#用最小支持度minSupport对候选集Ck过滤
#输出：本层(第k层)的频繁项集Lk，每项的支持度

#例如，由频繁1-项集(L1)内部组合生成候选集(C2)
#去除不满足最小支持度的项，得到频繁2-项集(L2)
def scanD(D, Ck, minSupport):
    #建立字典<key,value>
    #候选集Ck中每项及在所有物品记录中出现的次数
    #key-->候选集中的每项
    #value-->该物品在所有物品记录中出现的次数
    ssCnt = {}
    
    
    #对比候选集中的每项与原物品记录，统计出现的次数
    #遍历每条物品记录
    for tid in D:
        #遍历候选集Ck中的每一项，用于对比
        for can in Ck:
            #如果候选集Ck中该项在该条物品记录出现
            #即当前项是当前物品记录的子集
            if can.issubset(tid):
                #如果选集Ck中该项第一次被统计到，次数记为1
                if not ssCnt.has_key(can): ssCnt[can]=1
                #否则次数在原有基础上
                else: ssCnt[can] += 1
                
    #数据集中总的记录数，物品购买记录总数，用于计算支持度            
    numItems = float(len(D))
    #记录经最小支持度过滤后的频繁项集
    retList = []
    #记录候选集中满足条件的项的支持度<key,value>结构
    #key-->候选集中满足条件的项
    #value-->该项支持度
    supportData = {}
    
    #遍历候选集中的每项出现次数
    for key in ssCnt:
        #计算每项的支持度
        support = ssCnt[key]/numItems
        #用最小支持度过滤，
        if support >= minSupport:
            #保留满足条件物品组合
            #使用retList.insert(0,key)
            #在列表的首部插入新的集合，
            #只是为了让列表看起来有组织。
            retList.insert(0,key)
        #记录该项的支持度
        #注意：候选集中所有项的支持度均被保存下来了
        #不仅仅是满足最小支持度的项，其他项也被保存        
        supportData[key] = support
    #返回满足条件的物品项，以及每项的支持度
    return retList, supportData
    

    
#由上层频繁k-1项集生成候选k项集
#如输入为{0}，{1}，{2}会生成{0,1} {0,2} {1,2} 
#输入：频繁k-1项集，新的候选集元素个数k
#输出：候选集
def aprioriGen(Lk, k):
    #保存新的候选集 
    retList = []
    #输入的频繁项集记录数，用于循环遍历
    lenLk = len(Lk)
    
    #比较频繁项集中的每项与其他项，
    #若两项的前面k-1个元素都相同，那么就将两项合并。
    #每项与其他项元素比较，通过使用两个for循环实现
    for i in range(lenLk):
        #遍历候选集中除前项后的其他项，与当前项比较
        for j in range(i+1, lenLk): 
            #候选集当前项的k-1个元素
            L1 = list(Lk[i])[:k-2]; 
            #候选集其余项的k-1个元素，每次只有其余项中一项
            L2 = list(Lk[j])[:k-2]
            
            #排序
            L1.sort(); 
            L2.sort()
            
            #相同，则两项合并
            if L1==L2: 
                #合并，生成k+1项集
                retList.append(Lk[i] | Lk[j]) 
    #返回最终k+1项集            
    return retList

#输入：数据集、最小支持度    
def apriori(dataSet, minSupport = 0.5):
    #生成1-项集
    C1 = createC1(dataSet)
    #对数据集进行映射至D，去掉重复的数据记录
    D = map(set, dataSet)
    #过滤最小支持度，得到频繁1-项集L1以及每项的支持度
    L1, supportData = scanD(D, C1, minSupport)
    
    #将L1放入列表L中，L会包含L1、L2、L3
    #L存放所有的频繁项集
    #由L1产生L2，L2产生L3
    L = [L1]
    #Python中使用下标0表示第一个元素，k=2表示从1-项集产生2-项候选集
    #L0为频繁1-项集
    k = 2
    
    #根据L1寻找L2、L3通过while循环来完成，
    #它创建包含更大项集的更大列表，直到下一个更大的项集为空。
    #候选集物品组合长度超过原数据集最大的物品记录长度
    #如原始数据集物品记录最大长度为4，那么候选集最多为4-项集
    while (len(L[k-2]) > 0):
        #由频繁k-1项集，产生k项候选集
        #(连接步)
        Ck = aprioriGen(L[k-2], k)
        
        #由k项候选集，经最小支持度筛选，生成频繁k项集
        #(剪枝步)
        Lk, supK = scanD(D, Ck, minSupport)
        #更新支持度字典，用于加入新的支持度
        supportData.update(supK)
        #将新的频繁k项集加入已有频繁项集的列表中
        L.append(Lk)
        #k加1，用于产生下一项集
        k += 1
    #前面找不到支持的项，构建出更高的频繁项集Lk时，算法停止。
    #返回所有频繁项集及支持度列表    
    return L, supportData

    

#输入：apriori函数生成频繁项集列表L
#支持度列表、最小置信度    
#输出：包含可信度规则的列表
#作用：产生关联规则
def generateRules(L, supportData, minConf=0.7):  
    #置信度规则列表，最后返回
    bigRuleList = []
    
    #L0为频繁1-项集
    #无法从1-项集中构建关联规则，所以从2-项集开始。
    #遍历L中的每一个频繁项集。
    for i in range(1, len(L)):
        #遍历频繁项集的每一项
        for freqSet in L[i]:
            #对每个频繁项集构建只包含单个元素集合的列表H1。
            #如{1,2,3,4}，H1为[{1},{2},{3},{4}]
            #关联规则从单个项开始逐步增加，
            #1,2,3——>4   1,2——>3,4   1——>2,3,4
            H1 = [frozenset([item]) for item in freqSet]
            
            #频繁项集中元素大于3个及以上，
            #规则右部需要不断合并作为整体，利用最小置信度进行过滤
            if (i > 1):
                #项集中元素超过2个，做合并。
                rulesFromConseq(freqSet, H1, supportData, bigRuleList, minConf)
            else:
                #频繁项集只有2个元素时，直接计算置信度进行过滤
                calcConf(freqSet, H1, supportData, bigRuleList, minConf)
    #返回最后满足最小置信的规则列表
    return bigRuleList         

    
    


#输入：freqSet频繁项集、H关联规则右部的元素列表且为单个元素项，
#默认最小支持度0.7
#置信度计算，使用集合减操作。

#作用：计算规则的可信度以及找到满足最小可信度要求的规则
#注意：把1,2,3—>4看做1,2,3为一个整体，4为一个整体，
#即规则的前件为一个整体，后件为一个整体。
#上述规则就只有两部分，箭头前的项 与 箭头后的项


#产生后件为1项关联规则，频繁项集{1,2,3,4}
#H为[[1],[2],[3],[4]]。
#H中元素依次做关联规则的后项
#1,2,3——>4 
#1,2,4——>3 
#1,3,4——>2
#2,3,4——>1        

#产生后件为2项关联规则，频繁项集{1,2,3,4}
#H为H = [[3,4],[2,4],[2,3],[1,4],[1,3],[1,2]]。
#H中元素依次做关联规则的后项
#1,2——>3,4 
#1,3——>2,4 
#1,4——>2,3
#2,3——>1,4        
#2,4——>1,3
#3,4——>1,2


def calcConf(freqSet, H, supportData, brl, minConf=0.7):
    #满足最小可信度要求的规则列表后项
    prunedH = [] 
    #遍历H中的所有项，用作关联规则的后项
    for conseq in H:
        #置信度计算，使用集合减操作
        conf = supportData[freqSet]/supportData[freqSet-conseq] 
        
        #置信度大于最小置信度
        if conf >= minConf:
            #输出关联规则前件freqSet-conseq
            #关联规则后件conseq            
            print freqSet-conseq,'-->',conseq,'conf:',conf
            #保存满足条件的关联规则
            #保存关联规则前件，后件，以及置信度
            brl.append((freqSet-conseq, conseq, conf))
            #满足最小可信度要求的规则列表后项
            prunedH.append(conseq)
    #返回满足条件的后项        
    return prunedH

    


#输入：频繁项集、关联规则右部的元素列表H
#supportData支持度列表
#brl需要填充的规则列表，最后返回

#H为关联关联规则右部的元素，如1,2—>3,4
#频繁项集为{1,2,3,4}，H为3,4
#因此，先计算H大小m(此处m=2)
    
def rulesFromConseq(freqSet, H, supportData, brl, minConf=0.7):
    #规则右边的元素个数
    m = len(H[0])
    
    #{1,2,3}产生规则1——>2,3 
    #规则右边的元素H 最多 比频繁项集freqSet元素少1，
    #超过该条件无法产生关联规则

    #如果H元素较少，那么可以对H元素进行组合。
    #产生规则右边新的组合H，
    #直到达到H元素 最多
    
    #若{1,2,3,4}，m=2时。可产生如下规则
        #1,2——>3,4 
        #1,3——>2,4 
        #1,4——>2,3
        #2,3——>1,4        
        #2,4——>1,3
        #3,4——>1,2
        
    if (len(freqSet) > (m + 1)): 
        #使用aprioriGen()函数对H元素进行无重复组合，
        #用于产生更多的候选规则，结果存储在Hmp1中。
        
        #Hmp1=[[1,2,3],[1,2,4],[1,3,4],[2,3,4]]
        Hmp1 = aprioriGen(H, m+1)
        
        #利用最小置信度对这些候选规则进行过滤
        Hmp1 = calcConf(freqSet, Hmp1, supportData, brl, minConf)
        
        #过滤后Hmp1=[[1,2,3],[1,2,4]]
        #如果不止一条规则满足要求，
        #继续使用Hmp1调用函数rulesFromConseq()
        #判断是否可以进一步组合这些规则。
        if (len(Hmp1) > 1):    
            rulesFromConseq(freqSet, Hmp1, supportData, brl, minConf)
 
if __name__ == "__main__":
#     dataSet=loadDataSet() 
#     L, supportData = apriori(dataSet, minSupport=0.5)
#     rules=generateRules(L, supportData, minConf=0.5)
#     print rules    
#   毒蘑菇 第一列特征值为2 根据最小支持度过滤 找出不能吃的毒蘑菇  
    mushDatSet = [line.split() for line in open('mushroom.dat').readlines()]
    L, supportData = apriori(mushDatSet, minSupport=0.3)
    
    for item in L[3]:
        if item.intersection('2'):
            print item
