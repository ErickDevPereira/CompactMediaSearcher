from src.data_management.tf_idf import TfIdfMatrix, TfIDfOperator
from src.data_management.extractor import Extractor
from src.api_requester import requester_sgt
from typing import List, Dict
import numpy as np

class DocumentFilter:

    def __init__(self, query: str, docs: List[str]):
        self.__query: str = query
        self.__docs: List[str] = docs
        self.__tfidfmat = TfIdfMatrix(self.__query, self.__docs)
        self.__matrix_dict: Dict[str, np.ndarray | List[str]] = self.__tfidfmat.matrix
        self.__matrix: np.ndarray = self.__matrix_dict['matrix']
        self.__query_vec = self.__tfidfmat.query_as_vec
        self.__similar_docs: None | List[str, float] = None
    
    def __filter_docs(self, min_cos = 0.5):
        self.__filtered = list()
        self.__report = TfIDfOperator.get_cos(self.__matrix, self.__docs, self.__query_vec)
        for result in self.__report:
            if result[0] > min_cos:
                self.__filtered.append({'doc' : result[1], 'cos' : result[0]})
        return self.__filtered
    
    @property
    def similar_docs(self):
        self.__similar_docs = self.__filter_docs()
        return self.__similar_docs