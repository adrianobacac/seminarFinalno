import queue 

class Node(object):
    def __init__(self, children, fail, content,debth, name):
        self.children=children
        self.fail=fail
        self.content=content
        self.name=name
        self.debth=debth
    def __repr__(self):
        return self.name
    def __str__(self):
        return self.name
    def addChild(self,child, name):
        self.children.update({child:Node({}, None, None,self.debth+1, name)})
    
    def letterP(self, base):
        me="\t"
        
        for index, i in enumerate(base.children):
            if index!=0:
                me+="\t"*(base.debth)
              
            
            me+="->("+i+")"

            if(not base.children[i].children):
                me+="\n"
            me+= self.letterP(base.children[i])
        return me
    def contentP(self, base):
        me="\t"
        
        for index, i in enumerate(base.children):
            if index!=0:
                me+="\t"*(self.debth)
                """content"""
            if base.children[i].content==None:
                me+="-><NONE>"
            else:    
                me+="->{"+base.children[i].content+"}"
            if(not base.children[i].children):
                me+="\n"
            me+= self.contentP(base.children[i])
        return me
    def failP(self, base):
        me="\t"
        
        for index, i in enumerate(base.children):
            if index!=0:
                me+="\t"*(self.debth)
                """fail"""
            if base.children[i].fail==None:
                me+="-><NONE>"
            else:    
                me+="->{"+str(base.children[i].fail.name)+"}"
            if(not base.children[i].children):
                me+="\n"
            me+= self.failP(base.children[i])
        return me





class ACAlgo(object):
    root=Node({},None, None,0,"ROOT")
    root.fail=root
    state=root
    foundWords={};
    def printTree(self):    
        print (self.root.letterP(self.root))       
    def printContent(self):
        print (self.root.contentP(self.root))      
    def printFail(self):
        print (self.root.failP(self.root)) 
    
    def getWordData(self):
        return self.foundWords
    
    def addWord(self, word):
        noder=self.root
        #rjeènik u koji spremamo sve pronadene lokacije
        
        self.foundWords.update({word.lower():[]});
        
        for index, c in enumerate(word):
            if c.lower() not in noder.children:
                
                noder.addChild(c.lower(), word[0:index+1])  
                         
            noder=noder.children[c.lower()]
            if(index==len(word)-1):
                noder.content=word
                
    def addFails(self):
        fifoNode=queue.Queue()
        
        for a in self.root.children:
            self.root.children[a].fail=self.root
            fifoNode.put(self.root.children[a])
            
        while(not fifoNode.empty()):
            
            noder=fifoNode.get()
            
            for child in noder.children:
                pom=noder.fail
                while child not in pom.children:
                    
                    if(pom==pom.fail):
                        noder.children[child].fail=pom
                        break
                    pom=pom.fail
                else:   
                    for i in pom.children:
                        if i==child:
                            noder.children[child].fail=pom.children[i]
                            break
                
                fifoNode.put(noder.children[child])
                          
        
        
    def nextState(self, char):
        current=self.state
        while char not in current.children:
            current=current.fail
            if char in current.children:
                return current.children[char]
            if current==current.fail:
                return current
        else:
            return current.children[char]
        
    def checkState(self,pos):
        current=self.state
        
        while(current!=self.root):
            if(current.content!=None):
                if (pos-len(current.content)+1) not in self.foundWords[current.content.lower()]: #dodano 12.5. radi visestrukih prolaza
                    self.foundWords[current.content.lower()].append(pos-len(current.content)+1)
            current=current.fail
            

        
    def readFile(self, filePath):
        f=open(filePath, mode='r+')
        
        char=f.read(1)
        self.checkState(f.tell())
        while(char!=""):
            
            self.state=self.nextState(char.lower())
            self.checkState(f.tell())
            char=f.read(1)

        f.close()
    
    def resetTree(self):
        self.root.children={}
        self.foundWords={}
        self.state=self.root
        
