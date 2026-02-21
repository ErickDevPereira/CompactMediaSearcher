from typing import List
from numpy import ndarray
from math import sqrt

class SearchFilter:

    @staticmethod
    def get_inner_product(vec1: List[float | int] | ndarray, vec2: List[float | int] | ndarray) -> float:
        
        vec1_size: int = len(vec1)
        vec2_size: int = len(vec2)

        if vec1_size != vec2_size:
            raise ValueError(f'ERROR: both vectors must be inside the same vector space IR{vec1_size} or IR{vec2_size}')
        
        inner_prod: float = 0.0
        for pos in range(vec1_size):
            inner_prod += vec1[pos] * vec2[pos]
        
        return inner_prod

    @staticmethod
    def vec_normalizer(vec: ndarray) -> ndarray:
        is_null = True
        for _ in vec:
            if _ != 0:
                is_null = False
        if is_null:
            return vec
        norm_vec: ndarray = vec / sqrt(SearchFilter.get_inner_product(vec, vec))
        return norm_vec

    @staticmethod
    def get_cos(tf_idf_matrix: ndarray, docs: List[str], query_vec: ndarray) -> float:
        organized_cos: List[List[float, str]] = [[SearchFilter.get_inner_product(
            SearchFilter.vec_normalizer(query_vec),
            SearchFilter.vec_normalizer(tf_idf_matrix[doc_pos])
            ), docs[doc_pos]] for doc_pos in range(len(tf_idf_matrix))]
        return organized_cos
if __name__ == '__main__':
    import numpy as np
    print(SearchFilter.get_cos(
        np.array([np.array([0, 0, 0, 0, 0]), np.array([0, 0, 0.37497958, 0, 0.4336766]), np.array([0, 0, 0.22498775, 0, 0])]),
        ['You are not gay', 'Erick Pereira Ichigo', 'Erick 007 Curtidor de gatinhas'], np.array([0.320412, 0.320412, 0.22498775, 0.320412, 0.260206])
    ))