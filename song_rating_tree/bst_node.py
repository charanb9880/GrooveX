from song_rating_tree.rating_bucket import RatingBucket

class BSTNode:
    """
    Node of the Binary Search Tree. Each node represents a rating bucket.
    """
    def __init__(self, rating):
        # The rating this node represents (int, e.g., 1-5)
        self.rating = rating

        # Bucket to store multiple Song objects with this rating
        self.bucket = RatingBucket(rating)

        # Left and right child in BST
        self.left = None
        self.right = None
