
"""
Example:
split_result = split_dataset(df, keys='userId', ratios=[8,2])
df['Is_train'] = split_result['Is_train']
"""


import numpy as np
def split_dataset(df, keys, ratios, result_keys=['train'], seed=0):
    """
        dev = test ? validation ?
        ToDo:
            * ? change function into class
            * allow two patterns : train-test, train-dev-test
            * fixed samples instead of ratios
            * allow multiple keys
            * add result_keys (not implemented)
                + 'train' -> return Is_train key
                ...
    """
    assert len(ratios) in [2,3] and all(map(lambda x:x>0, ratios))
    #assert set(result_keys) <= set(['train', 'validation', 'dev', 'test'])
    ### temporal
    if isinstance(keys, str):
        pass
    elif isinstance(keys, list) and len(keys) == 1:
        keys = keys[0]
    ###
    
    dev_included = len(ratios) == 3

    values = df[keys].unique()
    values.sort()
    num_values = len(values)
    np.random.seed(seed)

    total = sum(ratios)
    train_ratio = ratios[0] / total
    test_ratio = ratios[-1] / total
    
    shuffle = np.random.permutation(np.arange(num_values))
    num_train = int(train_ratio * num_values)
    train_values = values[shuffle[:num_train]]
    if dev_included:
        num_test = int(test_ratio * num_values)
        validation_values = values[shuffle[num_train:-num_test]]
    #else:
    #    num_test = num_values - num_train
    #test_values = values[shuffle[-num_test:]]
    
    train_values_ = set(train_values)
    df_train = df[keys].apply(lambda x:x in train_values_)
    if dev_included:
        test_values_ = set(test_values)
        df_test = df[keys].apply(lambda x:x in test_values_)
        #validation_values_ = set(validation_values)
        return { 'Is_train' : df_train, 'Is_test' : df_test }
    else:
        return { 'Is_train' : df_train }


