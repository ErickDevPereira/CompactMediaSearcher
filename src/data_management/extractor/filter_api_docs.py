from src.data_management.similarity import DocumentFilter

df = DocumentFilter('Eu não sou gay', 'Ela gosta de Call of Duty', 'Eu sou gay', 'Eu sou hétero', 'Ela é gay', 'Eu não sou gay')
print(df.similar_docs)