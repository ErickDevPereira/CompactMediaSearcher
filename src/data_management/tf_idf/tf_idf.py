from typing import List, Dict
import numpy as np

class TfIdfMatrix:

    def __init__(self, query: str, docs: List[str]):
        self.__query = query.upper()
        self.__docs = docs
        self.__num_docs = len(self.__docs)
        self.__vocab_docs: List[np.ndarray] = [np.array(doc.upper().split()) for doc in self.__docs]
        self.__therms: np.ndarray = np.unique(np.array(self.__query.split()))
        self.__matrix_tfidf: np.ndarray = self.__get_tfidf_matrix()
    
    def __get_qtt_of_docs_with_therm(self, therm):
        self.qtt = 0
        for doc in self.__vocab_docs:
            if therm.upper() in doc:
                self.qtt += 1
        return self.qtt
    
    def __get_tf(self, therm: str, vocab_doc: List[str]) -> float:
        
        self.__num_ape: int = 0
        
        for word in vocab_doc:
            if word == therm.upper():
                self.__num_ape += 1
        
        self.__tf: float = self.__num_ape / len(vocab_doc)
        return self.__tf
        

    def __get_idf_vector(self) -> np.ndarray:
        self.__qtt_vec: np.ndarray = np.array([
            self.__get_qtt_of_docs_with_therm(therm) for therm in self.__therms
            ])
        self.__idf_vec: np.ndarray = np.log10((self.__num_docs + 1) / (self.__qtt_vec + 1)) + 1
        return self.__idf_vec
    
    def __get_tfidf_matrix(self) -> np.ndarray:
        self.__idf_vec = self.__get_idf_vector()
        self.__matrix = np.array(
            [
                np.array(
                    [
                        self.__get_tf(therm, doc) for therm in self.__therms
                    ]
                ) * self.__get_idf_vector() for doc in self.__vocab_docs
            ]
        )
        return self.__matrix

    def __get_tfidf_query_vec(self) -> np.ndarray:
        self.__qwords: List[str] = self.__query.split()
        self.tf_query: np.ndarray = np.array([self.__get_tf(therm, self.__qwords) for therm in self.__therms])
        self.query_vec: np.ndarray = self.tf_query * self.__get_idf_vector()
        return self.query_vec

    @property
    def matrix(self) -> Dict[str, np.ndarray | List[str]]:
        return {
            'matrix': self.__matrix_tfidf,
            'documents': self.__docs
        } #The documents and the lines of the matrix are at the same order.  

    @property
    def query_as_vec(self) -> np.ndarray:
       return self.__get_tfidf_query_vec()

if __name__ == '__main__':
    mat = TfIdfMatrix('Erick Pereira Call of Duty', ['You are not gay', 'Erick Pereira Ichigo', 'Erick 007 Curtidor de gatinhas'])
    print(mat.matrix)
    print(mat.query_as_vec)