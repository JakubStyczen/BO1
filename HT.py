#mieskończone

class Node:
    def __init__(self, key, data, height=None, left=None, right=None):
        self.key = key
        self.data = data
        self.left = left
        self.right = right
        self.height = height
    
    def __str__(self):
        return f'{self.key} {self.data}'

class BST:
    def __init__(self, root=None):
        self.root = root
    
    i=0
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
            self.root = Node(key, data, 0, None, None)
        else:
            self.__insert(key, data, self.root)
        
    def __insert(self, key, data, current_node):
        if current_node.key == key:
            current_node.data = data
            return 
        elif current_node.key > key and current_node.left is None:
            current_node.left = Node(key, data, None, None)
            return 
        elif current_node.key > key:
            return self.__insert(key, data, current_node.left)
        elif current_node.key < key and current_node.right is None:
            current_node.right = Node(key, data, None, None)
            return 
        elif current_node.key < key:
            return self.__insert(key, data, current_node.right)
        
    
    def delete(self, key):
        if self.root is None:
            return
        else:
            self.__delete(key, self.root)
        
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
            return self.__height(self.__height_from_node(starting_node_key, self.root))
        else:
            return self.__height(starting_node_key)
    
    def __height(self, node):
        if node is None:
            return -1 #0
        else:
            L_H = self.__height(node.left)
            R_H = self.__height(node.right)
            return R_H + 1 if R_H > L_H else L_H +1
    
    def __height_from_node(self, key, node):
        if node is None:
            return None
        if node.key > key:
            return self.__height_from_node(key, node.left)
        elif node.key < key:
            return self.__height_from_node(key, node.right)
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
            print(lvl*" ", node.key, node.height)
     
            self.__print_tree(node.left, lvl+5)

    def update_height(self):
        if self.root is None:
            return
        else:
            self.__update_height(self.root)
            
    def __update_height(self, node):
        if node!=None:
            self.__update_height(node.right)
            node.height = self.height(node.key)
            self.__update_height(node.left)
            
class AVL(BST):
    
    # def __insert_balance_check(self, node, path = []):
    #     if node is self.root:
    #         return
    #     path = [node] + path
    #     left_sub_tree_height = self.height(node.left.key)
    #     right_sub_tree_height = self.height(node.right.key)
        
    #     if abs(right_sub_tree_height - left_sub_tree_height) > 1:
    #         pass
        
    def insert(self, key, data):
        super().insert(key, data)
        self.rebalance()
        self.update_height()
    
    def delete(self, key):
        super().delete(key)
        self.rebalance()
        self.update_height()
    
    
    def rebalance(self, node='root'):
        if node is None:
            return
        

        #rebalance roota
        if node == 'root':
            self.__rebalance(self.root)
            self.root.left = self.__rebalance(self.root.left)
            # #rebalance lewej
            self.root.right = self.__rebalance(self.root.right)
            return
        node.left = self.__rebalance(node.left)
        # #rebalance lewej
        node.right = self.__rebalance(node.right)

        # #rebalance prawej

        
    # def check_balance(self):
    #     return self.__check_balance(self.root)
        
    # def __check_balance(self, node):
        
    
    def __rebalance(self, z):
        if z is None:
            return None
        
        old_root = self.root if z is self.root else None
        # #rebalance lewej
        # z.left = self.__rebalance(z.left)
        # #rebalance prawej
        # z.right = self.__rebalance(z.right)
        
        if z.left is not None:
            left_sub_tree_height = self.height(z.left.key)
        else:
            left_sub_tree_height = -1
            
        if z.right is not None:
            right_sub_tree_height = self.height(z.right.key)
        else:
            right_sub_tree_height = -1
            
        unbalanced_coeff = left_sub_tree_height-right_sub_tree_height
        #left
        if unbalanced_coeff < 0:
            if z.right and z.right.left is not None:
                left_sub_tree_height = self.height(z.right.left.key)
            else:
                left_sub_tree_height = -1
                
            if z.right and z.right.right is not None:
                right_sub_tree_height = self.height(z.right.right.key)
            else:
                right_sub_tree_height = -1
            #check right child
            if left_sub_tree_height - right_sub_tree_height > 0:
                #R
                z.right = self.rotate_right(z.right)
            #L
            new_z = self.rotate_left(z)
            self.update_height()
            if old_root is not None:
                self.root = new_z
                return
            return new_z
            
  
        #right
        if unbalanced_coeff > 0:
            if z.left and z.left.left is not None:
                left_sub_tree_height = self.height(z.left.left.key)
            else:
                left_sub_tree_height = -1
                
            if z.left and z.left.right is not None:
                right_sub_tree_height = self.height(z.left.right.key)
            else:
                right_sub_tree_height = -1
            
            #check left child
            if left_sub_tree_height - right_sub_tree_height < 0:
                #L
                z.left = self.rotate_left(z.left)
                self.update_height()
            #r
            new_z = self.rotate_right(z)
            self.update_height()
            if old_root is not None:
                self.root = new_z
                return
            return new_z

        return z
            
    def rebalance2(self, z):
        if z is None:
            return None
        
        old_root = self.root if z is self.root else None
        
        if z.left is not None:
            left_sub_tree_height = self.height(z.left.key)
        else:
            left_sub_tree_height = -1
            
        if z.right is not None:
            right_sub_tree_height = self.height(z.right.key)
        else:
            right_sub_tree_height = -1
            
        unbalanced_coeff = left_sub_tree_height-right_sub_tree_height
        #left
        if unbalanced_coeff < 0:
            if z.right and z.right.left is not None:
                left_sub_tree_height = self.height(z.right.left)
            else:
                left_sub_tree_height = -1
                
            if z.rightt and z.right.right is not None:
                right_sub_tree_height = self.height(z.right.right)
            else:
                right_sub_tree_height = -1
            #check right child
            if left_sub_tree_height - right_sub_tree_height > 0:
                #R
                z.right = self.rotate_right(z.right)
            #L
            new_z = self.rotate_left(z)
            self.update_height()
            if old_root is not None:
                self.root = new_z
                return
            return new_z
            

        #right
        if unbalanced_coeff > 0:
            if z.left and z.left.left is not None:
                left_sub_tree_height = self.height(z.left.left.key)
            else:
                left_sub_tree_height = -1
                
            if z.left and z.left.right is not None:
                right_sub_tree_height = self.height(z.left.right.key)
            else:
                right_sub_tree_height = -1
            
            #check left child
            if left_sub_tree_height - right_sub_tree_height < 0:
                #L
                z.left = self.rotate_left(z.left)
                self.update_height()
            #r
            new_z = self.rotate_right(z)
            self.update_height()
            if old_root is not None:
                self.root = new_z
                return
            return new_z

        return z            

    def rotate_left(self, z):
        y = z.right
        y_left_subtree = y.left
        z.right = y_left_subtree
        y.left = z

        return y
    
    def rotate_right(self, z):
        y = z.left
        y_right_subtree = y.right
        z.left = y_right_subtree
        y.right = z

        return y
    
if __name__ == "__main__":
    bst = AVL()
    nodes = {50:'A', 15:'B', 62:'C', 5:'D', 2:'E', 1:'F', 11:'G', 100:'H', 7:'I', 6:'J', 55:'K', 52:'L', 51:'M', 57:'N', 8:'O', 9:'P', 10:'R', 99:'S', 12:'T'}
    # nodes = {50:'A', 45:'B',40:'C'}
    for key, data in nodes.items():
        bst.insert(key, data)
    bst.print_tree()
    # bst.rebalance(bst.root.left)
    # bst.root.left = bst.rebalance2(bst.root.left)
    # bst.root.left.right = bst.rebalance2(bst.root.left.right)
    # bst.root.left.left = bst.rebalance2(bst.root.left.left)
    bst.print_tree()
    # bst.print()
    # print()
    # print(bst.search(10))
    # bst.delete(50)
    # bst.delete(52)
    # bst.delete(11)
    # bst.delete(57)
    # bst.delete(1)
    # bst.delete(12)
    # bst.insert(3, 'AA')
    # bst.insert(4, 'BB')
    # bst.delete(7)
    # bst.delete(8)
    # bst.print_tree()
    # bst.print()

