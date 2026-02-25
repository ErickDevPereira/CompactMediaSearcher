from src.data_management.tf_idf import TfIdfMatrix, TfIDfOperator
from src.data_management.extractor import Extractor
from src.api_requester import requester_sgt
from typing import List, Dict
import numpy as np

class DocumentFilter:

    def __init__(self, query: str, docs: List[str], precision: float | np.float64 = 0.7):

        if not isinstance(precision, (np.float64, float)):
            raise TypeError("Precision must be a flaoting point number")
        
        if not 0.0 <= precision <= 1.0:
            raise ValueError("Precision out of range (the range is from 0.0 to 1.0 as float)")

        self.__query: str = query
        self.__docs: List[str] = docs
        self.__prec: float | np.float64 = precision
        self.__tfidfmat: TfIdfMatrix = TfIdfMatrix(self.__query, self.__docs)
        self.__matrix_dict: Dict[str, np.ndarray | List[str]] = self.__tfidfmat.matrix
        self.__matrix: np.ndarray = self.__matrix_dict['matrix']
        self.__query_vec: np.ndarray = self.__tfidfmat.query_as_vec
        self.__similar_docs: None | List[Dict[str, str | float]] = None
    
    def __filter_docs(self) -> List[Dict[str, str | float]]:
        self.__filtered: List[Dict[str, str | float]] = list()
        self.__report: List[List[float | str]] = TfIDfOperator.get_cos(self.__matrix, self.__docs, self.__query_vec)
        for result in self.__report:
            if result[0] > self.__prec:
                self.__filtered.append({'doc' : result[1], 'cos' : result[0]})
        return self.__filtered
    
    @property
    def similar_docs(self) -> List[Dict[str, str | float]]:
        self.__similar_docs = self.__filter_docs()
        return self.__similar_docs