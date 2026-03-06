# 2. Implement a Python function to search for a value in a binary search tree. 
# The method should take the root of the tree and the value to be searched as parameters. 
# It should return True if the value is found in the tree, and False otherwise.

def search(root, key):
    # Base Cases: root is null or key is present at root
    if root is None:
        return False
    if root.val == key:
        return True

    # Key is greater than root's key
    if root.val < key:
        return search(root.right, key)

    # Key is smaller than root's key
    return search(root.left, key)