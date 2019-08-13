
"""
Example:
ohe = ConcatOneHotEncoder(['userId', 'movieId'])
ohe.fit(df)
encoded = ohe.apply(df)
df['userId_node'] = encoded['userId']
df['movieId_node'] = encoded['movieId']
"""

class ConcatOneHotEncoder():
    def __init__(self, columns):
        self.columns = columns
    
    def fit(self, dataframe):
        self.get_codomain(dataframe)
        self.assign_index()
        
    def get_codomain(self, dataframe):
        assert set(self.columns) <= set(dataframe.columns)
        col2codomain = {}
        for col in self.columns:
            codomain = dataframe[col].unique()
            codomain.sort()
            col2codomain.update({col : codomain})
        self.col2codomain = col2codomain
        
    def assign_index(self):
        offset = 0
        one_hot_encoders = {}
        for col, codomain in self.col2codomain.items():
            one_hot_encoders.update({ col : { str(v):i+offset for i, v in enumerate(codomain) } })
            offset += len(codomain)
        self.one_hot_encoders = one_hot_encoders
    
    def apply(self, dataframe):
        return { col : dataframe[col].apply(lambda x:str(x)).map(ohe) for col, ohe in self.one_hot_encoders.items() }


