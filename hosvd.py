import numpy as np


def next_unfolding(mat, dimension_product, new_dim):
    """
    Get A_(n + 1) tensor unfolding based on A_(n).
    On the same column in A_(n) all indices except i_(n) are the same,
    thus we can write them consequently in a row of A_(n+1).
    """
    h = new_dim
    w = dimension_product // new_dim
    mat_new = np.zeros((h, w))
    for i in range(mat.shape[1]):
        new_col = (i * mat.shape[0]) % w
        mat_new[(i * mat.shape[0]) // w, new_col : new_col + mat.shape[0]] = np.array(mat[:, i])
    return mat_new


def get_frobenius_norm(mat):
    flat = mat.flat
    res = 0
    for el in flat:
        res += el.conjugate() * el
    return np.sqrt(res)


def read_unfolded_tensor():
    # ---Read tensor in lexicographic order-----------------

    dim_am = int(input())  # Read how many dimensions the tensor has
    dim = np.array(list(map(int, input().split())))
    dimension_product = dim.prod()
    unfolded_tensor = np.zeros((dim[0], dimension_product // dim[0]))
    for i in range(dim[0]):
        unfolded_tensor[i] = np.array(list(map(float, input().split())))
    return unfolded_tensor, dim


def get_hosvd(unfolded_tensor, dim):
    dim_am = len(dim)
    # ---Find U^(1), U^(2), ..., U^(dim_am) matrices, use equation 15----------
    U = []  # All U matrices
    for i in range(dim_am):
        U.append(np.linalg.svd(unfolded_tensor)[0])
        unfolded_tensor = next_unfolding(unfolded_tensor, np.prod(dim), dim[(i + 1) % dim_am])

    unfolded_res = U[0].T.conjugate() @ unfolded_tensor
    kron_prod = U[1]
    for i in range(2, dim_am):
        kron_prod = np.kron(kron_prod, U[i])
    unfolded_res = unfolded_res @ kron_prod
    return unfolded_res, U



