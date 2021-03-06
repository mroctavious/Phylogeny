"""
The four point condition.

The Four Point Condition holds for any additive matrix.

Let's say we have the following unrooted tree:

    1 -\    /- 3
        >--<
    2 -/    \- 4
    
Let the distance between leaves 'a' and 'b' be D(a,b). 
Consider the three following pairwise sums:

    * D(1,2) + D(3,4)
    * D(1,3) + D(2,4)
    * D(1,4) + D(2,3)

The smallest of these sums has to be D(1,2)+D(3,4), since
it covers all the edges of the tree connecting the four 
leaves, EXCEPT for the ones on the path separating 1 and 2 
from 3 and 4. Furthermore, the two larger of the three 
pairwise sums have to be identical, since they cover the 
same set of edges.

The Four Point Condition is the statement that the two 
largest values of the three pairwise distance sums are 
the same. 

    -- Based on an explanation from the book:
        "Computational Phylogenetics. An introduction 
        to designing methods for phylogeny estimation"
        by Tandy Warnow
"""

_fpc_permutations = [(0,1,2,3),
                     (0,2,1,3),
                     (0,3,1,2)]

def fpc_sums(distances, quartet):
    """From a quartet of pairwise distances, return the
    sums needed to check the four point condition.
    """
    q = tuple(quartet)
    # Map indices
    permutations = [ tuple(q[i] for i in p)
                        for p in _fpc_permutations ]
    # Calculate the relevant pairwise sums
    sums = { ((i,j), (k,l)): distances[i][j] + distances[k][l]
                for i,j,k,l in permutations }
    
    return sums
# ---

def four_point_condition(dist_matrix, quartet, tolerance=1e-2):
    """The Four Point Condition is the statement that 
    the two largest values of the three pairwise 
    distance sums are the same. 
    """
    sums = list(fpc_sums(dist_matrix, quartet).values())
    # Now, we must verify that the largest one 
    # is repeated
    s_max = max(sums)
    if sum( (s_max-s)**2 < tolerance for s in sums) < 2:
        return False
    return True
# ---
    
def is_additive(dist_matrix, tolerance=1e-2):
    """Is the distances matrix additive?
    
    Check the four point condition on each quartet of
    indices of the matrix.
    """
    n = len(dist_matrix)
    quartets = list(itr.combinations(range(n), 4))
    
    return all(four_point_condition(dist_matrix, q, tolerance)
                  for q in quartets)
# ---   