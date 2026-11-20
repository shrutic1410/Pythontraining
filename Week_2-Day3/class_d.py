import numpy as np



# Two example vectors
A = np.array([1, 2, 3])
B = np.array([2, 4, 6])
C = np.array([3, 1, 0])
# Compute the cosine similarity between A and B
def cosine_similarity(a,b):
 return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))
print(cosine_similarity(A, B))
print(cosine_similarity(A, C))