import sys
import os
import pickle

parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parentdir)
grandfatherdir = os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))))
from graph.belief_graph import Graph




def pickle_():
    graph_dir = os.path.join(grandfatherdir, "model/graph/belief_graph.pkl")
    with open(graph_dir, "rb") as input_file:
        belief_graph = pickle.load(input_file)
    slots_trans = belief_graph.slots_trans
    slots_trans['entity'] = '实体'
    slots_trans['search_'] = '搜索:'
    slots_trans['request_'] = '确认:'
    slots_trans['rhetorical_'] = '反问:'
    slots_trans['placeholder'] = '占位'
    slots_trans['ambiguity_removal'] = '消除歧义:'
    slots_trans['slot_'] = '槽位:'
    slots_trans['virtual_'] = '虚'
    slots_trans['api_call_'] = ''

    translator_graph_dir=os.path.join(grandfatherdir, "model/graph/translator_graph.pkl")
    with open(translator_graph_dir,'wb') as f:
        pickle.dump(slots_trans,f)


class Translator():
    def __init__(self,path):
        self.dic=self._load(path)

    def _load(self,path):
        with open(path,'rb') as f:
            return pickle.load(f)

    def en2cn(self,query):
        for k,v in self.dic.items():
            query=query.replace(k,v)
        return query

    def cn2en(self,query):
        for k,v in self.dic.items():
            query=query.replace(v,k)
        return query

def test():
    with open(os.path.join(grandfatherdir,'data/memn2n/train/tree/candidates.txt'),'r') as f:
        candidates=f.readlines()
    translator=Translator(os.path.join(grandfatherdir, "model/graph/translator_graph.pkl"))
    with open(os.path.join(grandfatherdir,'data/test.txt'),'w') as f:
        for line in candidates:
            f.write(translator.en2cn(line))



if __name__ == '__main__':
    pickle_()
    test()