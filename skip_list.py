#nieskończone
from random import random
MAX_LEVEL = 6

class SkipList:
    def __init__(self, head=None, max_level=MAX_LEVEL):
        self.head = SkipListElement("HEADS ELEMENT", "", max_level=max_level, levels=max_level)
        self.max_level = max_level
    
    def search(self, search_key):
        current_node = self.head
        layer = self.max_level - 1
        while layer >= 0:
            while current_node.tab[layer] and current_node.tab[layer].key < search_key:
                current_node = current_node.tab[layer]
            layer -= 1  

        current_node = current_node.tab[0]
        return current_node.data if (current_node is not None and current_node.key == search_key) else None
    
    
    def insert(self, key, data):
        if self.search(key) is not None:
            self.remove(key)
        element = SkipListElement(key, data, self.max_level)
        prevs = [None for _ in range(self.max_level)]
        current_node = self.head
        layer = self.max_level - 1
        while layer >= 0:
            while current_node.tab[layer] and current_node.tab[layer].key < key:
                current_node = current_node.tab[layer]
            prevs[layer] = current_node 
            layer -= 1 
        # if current_node.tab[0] is not None and current_node.tab[0].key == key:

        #     current_node.tab[0].data = data
        if  current_node is None or current_node.key != key:
            for layer in range(element.levels):
                #nexts
                element.tab[layer] = prevs[layer].tab[layer]
                
                #previous
                if prevs[layer] is not None:
                    prevs[layer].tab[layer] = element
                else:
                    self.head.tab[layer] = element
                    


                
    
    
    def remove(self, remove_key):
        prevs = [None for _ in range(self.max_level)]
        current_node = self.head
        layer = self.max_level - 1
        while layer >= 0:
            while current_node.tab[layer] and current_node.tab[layer].key < remove_key:
                current_node = current_node.tab[layer]
            prevs[layer] = current_node 
            layer -= 1 
        current_node = current_node.tab[0]
    
        if current_node is not None and current_node.key == remove_key:  
            for layer in range(self.max_level):
                if prevs[layer].tab[layer] != current_node:
                    break
                prevs[layer].tab[layer] = current_node.tab[layer]
            
    
    def __str__(self):
        current_node = self.head.tab[0]
        
        str_rep = "[ "
        while current_node is not None:
            str_rep += f'({current_node.key}:{current_node.data}), '
            current_node = current_node.tab[0]

        return f"{str_rep[:-2]} ]"

    def displayList_(self):
        node = self.head.tab[0]  # first element on level 0
        keys = []  # list of keys on this level
        while node is not None:
            keys.append(node.key)

            node = node.tab[0]

        for lvl in range(self.max_level - 1, -1, -1):
            print("{}: ".format(lvl), end=" ")
            node = self.head.tab[lvl]
            idx = 0
            while node is not None:
                while node.key > keys[idx]:
                    print("  ", end=" ")
                    idx += 1
                idx += 1
                print("{:2d}".format(node.key), end=" ")
                node = node.tab[lvl]
            print("")
        
class SkipListElement:
    def __init__(self, key=None, data=None, max_level=MAX_LEVEL, levels = 0):
        self.key = key
        self.data = data
        self.max_level = max_level
        if levels:
            self.levels = levels
        else:
            self.levels = self.random_level()    
        self.tab = [None for _ in range(self.levels)]
    
    def random_level(self, p=0.5):
        lvl = 1
        while random() < p and lvl < self.max_level:
            lvl += 1
        return lvl 
        
        
        
    def __str__(self):
        return f'{self.key}: {self.data}'
    
    
    
if __name__ == '__main__':
    skip_list = SkipList(MAX_LEVEL)
    for idx, letter in enumerate(["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O"], 1):
        skip_list.insert(idx, letter)
    skip_list.displayList_()
    print(skip_list.search(2))
    skip_list.insert(2, "Z")
    print(skip_list.search(2))
    skip_list.remove(5)
    skip_list.remove(6)
    skip_list.remove(7)
    print(skip_list)
    skip_list.insert(6, "W")
    print(skip_list)
    
    
    #końcowe sprawdzenie
    print("\n------------------ODWROTNA KOLEJNOSC-------------------------\n")
    skip_list = SkipList(MAX_LEVEL)
    letters = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O"]
    for i in range(15, 0, -1):
        skip_list.insert(i, letters[i-1])
    skip_list.displayList_()
    print(skip_list.search(2))
    skip_list.insert(2, "Z")
    print(skip_list.search(2))
    skip_list.remove(5)
    skip_list.remove(6)
    skip_list.remove(7)
    print(skip_list)
    skip_list.insert(6, "W")
    print(skip_list)
    