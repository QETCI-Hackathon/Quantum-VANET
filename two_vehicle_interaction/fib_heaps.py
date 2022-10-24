

from copy import copy
from dataclasses import dataclass
from random import shuffle
from time import process_time_ns
from typing import List


class Node:
    def __init__(self, data):
        self.data = data
        self.children=[]
        self.len = 0
    def __eq__(self, __o) -> bool:
        return self.data==__o.data
    def __ne__(self, __o) -> bool:
        return self.data!=__o.data
    def __lt__(self, __o) -> bool:
        return self.data<__o.data
    def __gt__(self, __o) -> bool:
        return self.data>__o.data
    def __le__(self, __o) -> bool:
        return self.data<=__o.data
    def __ge__(self, __o) -> bool:
        return self.data>=__o.data
    def insert(self, val):
        self.len+=1
        self.children.append(val)
    def __repr__(self) -> str:
        return f"Node({self.data})"

class FibHeap:
    def __init__(self) -> None:
        self.trees = []
        self.treelens = []
        self.minimum = None
    def insert(self, val):
        node = Node(val)
        if self.minimum is None:
            self.minimum = 0
        else:
            self.minimum, _ = min((self.minimum,self.trees[self.minimum]), (len(self.trees),node), key=lambda x: x[1])
        self.trees.append(node)
        self.treelens.append(1)
        return self
    def insertNode(self, node: Node):
        if self.minimum is None:
            self.minimum = 0
        else:
            self.minimum, _ = min((self.minimum,self.trees[self.minimum]), (len(self.trees),node), key=lambda x: x[1])
        self.trees.append(node)
        self.treelens.append(node.len)
        return self
    def min(self) :
        return self.trees[self.minimum].data
    def pop(self) :
        if len(self.trees)==0: return None
        node = self.trees.pop(self.minimum)
        self.treelens.pop(self.minimum)
        self.minimum = 0 if len(self.trees)>0 else None
        for n in node.children:
            self.insertNode(n)
        if len(self.trees)==0:
            return node.data
        dic = dict()
        for i,n in enumerate(self.trees):
            if n.len not in dic:
                dic[n.len] = [n]
            else:
                dic[n.len].append(n)
        key=list(dic.keys())[0]
        prevlen = float('inf')
        while prevlen!=0:
            lis: List[Node] = dic[key]
            prevlen = len(lis)
            key = key+1
            if key not in dic: dic[key] = []
            while len(lis)>=2:
                a,b=lis.pop(0),lis.pop(0)
                if a<b:
                    a.insert(b)
                    dic[key].append(a)
                else:
                    b.insert(a)
                    dic[key].append(b)
        self.trees = []
        self.treelens = []
        self.minimum = None
        for key in dic:
            for n in dic[key]:
                self.insertNode(n)
        return node.data

if __name__=="__main__":
    lis = list(range(100000))
    shuffle(lis)
    heap = FibHeap()
    maxtime = (0,-1)
    avgtime = 0
    mintime = (float('inf'),-1)
    for i in lis:
        #print(i)
        heap.insert(i)
    for i in range(100000):
        st = process_time_ns()
        x = heap.pop()
        delta = process_time_ns()-st
        maxtime = max(maxtime,(delta,i),key=lambda x:x[0])
        mintime = min(mintime,(delta,i),key=lambda x:x[0])
        avgtime = (i*avgtime+delta)/(i+1)
        #print(x,delta,avgtime)
    print("max:",maxtime,"\navg:",avgtime,"\nmin:",mintime)
