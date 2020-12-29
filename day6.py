
class Celeste:
    def __init__(self,objname,parent,lvl):
        self.objname = objname
        self.level = lvl
        self.parent = parent
        self.children = []

    def add_child(self,child):
        self.children += [child]

with open('inputday6.txt','r') as f:
    connections = f.readlines()

parents = []
children = []
for connection in connections:
    carr = connection.split(')')
    if len(carr)==2:
        parents.append(carr[0].strip())
        children.append(carr[1].strip())


def traversing_builder(cur):
    ida = [i for i,nm in enumerate(parents) if nm == cur.objname]

    for idx in ida:
        child = Celeste(children[idx],cur,cur.level + 1)
        traversing_builder(child)        
        cur.add_child(child)
    
    return cur

def traversing_counter(cur):
    orbits = cur.level
    for child in cur.children:
        orbits += traversing_counter(child)
    return orbits

def find_target(tar,cur):
    ret = None    
    if cur.objname == tar:
        ret = (0,cur)
    else:
        for child in cur.children:
            ret = find_target(tar,child)
            if ret is not None:
                ret = (ret[0]+1,ret[1])
                break
    return ret

def transfers(tar,cur):
    down = find_target(tar,cur)
    if down is None:
        ret = transfers(tar,cur.parent) + 1
    else:
        ret = down[0]
    return ret
    
tree = traversing_builder(Celeste('COM',None,0))

you = find_target('YOU',tree)[1]

counts = transfers('SAN',you)-2

print(counts)

