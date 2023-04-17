#skończone
class Node:
    def __init__(self, key, data, left=None, right=None):
        self.key = key
        self.data = data
        self.left = left
        self.right = right
    
    def __str__(self):
        return f'{key} {data}'

class BST:
    def __init__(self, root=None):
        self.root = root

    def search(self, key):
        if self.root is None:
            return None
        else:
            return self.__search(key, self.root)

            
    def __search(self, key, node):
        #lewe
        if node.key > key:
            node_r = self.__search(key, node.left)
        #prawe
        elif node.key < key:
            node_r = self.__search(key, node.right)
        #równe
        else:
            return node.data
        return node_r
            
    
    def insert(self, key, data):
        if self.root is None:
            self.root = Node(key, data, None, None)
        else:
            return self.___insert(key, data, self.root)
        
    def ___insert(self, key, data, current_node):
        if current_node.key == key:
            current_node.data = data
            return 
        elif current_node.key > key and current_node.left is None:
            current_node.left = Node(key, data, None, None)
            return 
        elif current_node.key > key:
            return self.___insert(key, data, current_node.left)
        elif current_node.key < key and current_node.right is None:
            current_node.right = Node(key, data, None, None)
            return 
        elif current_node.key < key:
            return self.___insert(key, data, current_node.right)
        
    
    def delete(self, key):
        if self.root is None:
            return
        else:
            return self.__delete(key, self.root)
        
    def __delete(self, key, current_node):    
        #lewe
        if current_node.key > key:
            current_node.left = self.__delete(key, current_node.left)
        #prawe
        elif current_node.key < key:
            current_node.right = self.__delete(key, current_node.right)
        #równe
        else:
            #bez dzieci
            if current_node.left is None and current_node.right is None:
                return None
            #tylko prawe 
            elif current_node.left is None:
                return current_node.right
            #tylko lewe
            elif current_node.right is None:
                return current_node.left
            #oba 
            lowest = current_node.right
            while lowest.left is not None:
                lowest = lowest.left
            
            current_node.key = lowest.key
            current_node.data = lowest.data
            
            current_node.right = self.__delete(lowest.key, current_node.right)
            
        return current_node
        
    
    def print(self):
        if self.root is None:
            return ""
        else:
            return self.__print(self.root)
    
    def __print(self, node):
        if node.left is not None:
            self.__print(node.left)
        print(f'{node.key} {node.data},', end="")
        if node.right is not None:
            self.__print(node.right)
    
    def height(self, starting_node_key=None):
        if starting_node_key is None:
            starting_node_key = self.root
        if starting_node_key != self.root:
            return self.___height(self.___height_from_node(starting_node_key, self.root))
        else:
            return self.___height(starting_node_key)
    
    def ___height(self, node):
        if node is None:
            return -1 #0
        else:
            L_H = self.___height(node.left)
            R_H = self.___height(node.right)
            return R_H + 1 if R_H > L_H else L_H +1
    
    def ___height_from_node(self, key, node):
        if node.key > key:
            return self.___height_from_node(key, node.left)
        elif node.key < key:
            return self.___height_from_node(key, node.right)
        else:
            return node
    
    def print_tree(self):
        print("==============")
        self.__print_tree(self.root, 0)
        print("==============")

    def __print_tree(self, node, lvl):
        if node!=None:
            self.__print_tree(node.right, lvl+5)

            print()
            print(lvl*" ", node.key, node.data)
     
            self.__print_tree(node.left, lvl+5)
            
            
class NodeAVL(Node):
    def __init__(self, key, data):
        super().__init__(key, data)
        self.height = 1

class AVL(BST):
    
    def insert(self, key, data):
        if self.root is None:
            self.root = NodeAVL(key, data)
        else:
            self.root = self.__insert(key, data, self.root)

    def __insert(self, key, data, current_node):
        if current_node is None:
            return NodeAVL(key, data)
        elif key < current_node.key:
            current_node.left = self.__insert(key, data, current_node.left)
        else:
            current_node.right = self.__insert(key, data, current_node.right)

        #rebalnace

        current_node.height = max(self.__height(current_node.left), self.__height(current_node.right)) + 1
        balance_coefficient = self.__balance_coefficient(current_node)

        #RL
        if balance_coefficient < -1 and key < current_node.right.key:
            current_node.right = self._rotate_right(current_node.right)
            return self._rotate_left(current_node)
        #LR
        elif balance_coefficient > 1 and key > current_node.left.key:
            current_node.left = self._rotate_left(current_node.left)
            return self._rotate_right(current_node)
        #RR
        elif balance_coefficient > 1 and key < current_node.left.key:
            return self._rotate_right(current_node)
        #LL
        elif balance_coefficient < -1 and key > current_node.right.key:
            return self._rotate_left(current_node)

        



        return current_node

    def delete(self, key):
        if self.root is None:
            return
        self.root = self.__delete(key, self.root)

    def __delete(self, key, current_node):
        if current_node is None:
            return current_node
        elif key < current_node.key:
            current_node.left = self.__delete(key, current_node.left)
        elif key > current_node.key:
            current_node.right = self.__delete(key, current_node.right)
        else:
            if current_node.left is None:
                return current_node.right
            elif current_node.right is None:
                return current_node.left
            else:
                lowest = current_node.right
                while lowest.left is not None:
                    lowest = lowest.left
                
                current_node.key = lowest.key
                current_node.data = lowest.data
                
                current_node.right = self.__delete(lowest.key, current_node.right)
        if current_node is None:
            return current_node

        #rebalance
        current_node.height = max(self.__height(current_node.left), self.__height(current_node.right)) + 1
        balance_coefficient = self.__balance_coefficient(current_node)
        
        #LR
        if balance_coefficient > 1 and self.__balance_coefficient(current_node.left) < 0:
            current_node.left = self._rotate_left(current_node.left)
            return self._rotate_right(current_node)
        #RL 
        elif balance_coefficient < -1 and self.__balance_coefficient(current_node.right) > 0:
            current_node.right = self._rotate_right(current_node.right)
            return self._rotate_left(current_node)
        
        #RR
        elif balance_coefficient > 1 and self.__balance_coefficient(current_node.left) >= 0:
            return self._rotate_right(current_node)

        #LL
        elif balance_coefficient < -1 and self.__balance_coefficient(current_node.right) <= 0:
            return self._rotate_left(current_node)

        return current_node
    
    def _rotate_left(self, current_node):
        new_start_node = current_node.right
        current_node.right = new_start_node.left
        new_start_node.left = current_node
        
        #update height of rebalanced nodes
        current_node.height = max(self.__height(current_node.left), self.__height(current_node.right)) + 1
        new_start_node.height = max(self.__height(new_start_node.left), self.__height(new_start_node.right)) + 1
        
        return new_start_node

    def _rotate_right(self, current_node):
        new_start_node = current_node.left
        current_node.left = new_start_node.right
        new_start_node.right = current_node
        
        #update height of rebalanced nodes
        current_node.height = max(self.__height(current_node.left), self.__height(current_node.right)) + 1
        new_start_node.height = max(self.__height(new_start_node.left), self.__height(new_start_node.right)) + 1
        
        return new_start_node

    def __height(self, current_node):
        if current_node is None:
            return 0
        return current_node.height

    def __balance_coefficient(self, current_node):
        if current_node is None:
            return 0
        else:
            return self.__height(current_node.left) - self.__height(current_node.right)


if __name__ == "__main__":   
    avl = AVL()
    for key, data in {50:'A', 15:'B', 62:'C', 5:'D', 2:'E', 1:'F', 11:'G', 100:'H', 7:'I', 6:'J', 55:'K', 52:'L', 51:'M', 57:'N', 8:'O', 9:'P', 10:'R', 99:'S', 12: 'T'}.items():
            avl.insert(key, data)
    avl.print_tree()
    avl.print()
    print()
    print(avl.search(10))
    avl.delete(50)
    avl.delete(52)
    avl.delete(11)
    avl.delete(57)
    avl.delete(1)
    avl.delete(12)
    avl.insert(3, 'AA')
    avl.insert(4, 'BB')
    avl.delete(7)
    avl.delete(8)
    avl.print_tree()
    avl.print()
