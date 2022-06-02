
##
## ***************************************************
## Copyright © 2022 Shengkai Liu. All rights reserved.
## FileName:   expression.py
## Author:     Shengkai Liu
## Date:       2022-06-02
## ***************************************************
##

from typing import List
import unittest

class BinaryTree(object):
    def __init__(self, x: str) -> None:
        self.val = x
        self.left = None
        self.right = None
    
    def inorder(node, layer: int) -> None:
        '''
        Print the binary tree in the order of the in-order traversal.
        '''
        if node == None:
            return
        BinaryTree.inorder(node.left, layer + 1)
        print('  '*layer + node.val)
        BinaryTree.inorder(node.right, layer + 1)

    def encode(node) -> List:
        '''
        Serializing a binary tree into a list.
        '''
        if node == None:
            return [None]
        left = BinaryTree.encode(node.left)
        right = BinaryTree.encode(node.right)
        
        return right + left + [node.val]
    
    def decode(ls: List):
        '''
        Deserialize a list into a binary tree.
        '''
        if ls[-1] == None:
            ls.pop()
            return None
        node = BinaryTree(ls.pop())
        node.left = BinaryTree.decode(ls)
        node.right = BinaryTree.decode(ls)
        return node

def count_operator(s: str) -> int:
    '''
    Count the number of operators in string s.
    '''
    cnt = 0
    for ch in s:
        if ch in '+-*/':
            cnt += 1
    return cnt


def check_input_legality(stack: List, input_string: str) -> bool:
    '''
    Checking the legality of the stack when traversing to a right bracket.
    '''
    tmp = ''.join(stack)
    idx = tmp.rfind('(')
    if idx == -1:
        print(input_string, 'Not a valid expression, brackets mismatched.')
        return False
    else:
        opts = count_operator(tmp[idx+1:])
        if opts > 1:
            print(tmp[idx+1:])
            print(input_string, 'Not a valid expression, wrong number of operands.')
            return False
        if opts == 0:
            print(input_string, 'Not a valid expression, operator missing.') 
            return False
    return True

def binary_tree_to_file(node: BinaryTree, file_name: str) -> None:
    '''
    Saving a binary tree to a file.
    '''
    ls = BinaryTree.encode(node)
    with open(file_name,'w') as fd:
        fd.write(str(ls))

def file_to_binary_tree(file_name: str) -> BinaryTree:
    '''
    Read a binary tree from a file.
    '''
    with open(file_name, 'r') as fd:
        ls = eval(fd.read())
        node = BinaryTree.decode(ls)
    return node


def main():
    input_string = input("Please enter a valid expression:")

    ## Simulating expressions via the stack.
    stack = []       # Maintaining a stack of operands and operators.
    node_stack = []  # Maintaining a stack of binary trees.
    for ch in input_string:
        ## Traverse to the right bracket to compute an 
        ## operator operation at the top of the stack.
        if ch == ')':
            if check_input_legality(stack, input_string):
                val = eval(stack[-3] + stack[-2] + stack[-1])
                stack = stack[:-4]
                stack.append(str(val))

                node_stack[-2].left = node_stack[-3]
                node_stack[-2].right = node_stack[-1]
                node_stack[-3] = node_stack[-2]
                node_stack.pop()
                node_stack.pop()

            else:
                return 
        else:
            stack.append(ch)
            if ch != '(':
                node_stack.append(BinaryTree(ch))
    
    if len(stack) != 1:
        print(input_string, 'Not a valid expression, brackets mismatched.')
    else:
        print(stack[0])

    BinaryTree.inorder(node_stack[-1])

if __name__ == '__main__':
    main()