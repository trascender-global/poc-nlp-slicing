from itertools import permutations
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
from itertools import combinations, chain

def split_list(data, n):
    # split a list into its possible n groups combinations, maintaining order
    for splits in combinations(range(1, len(data)), n-1):
        result = []
        prev = None
        for split in chain(splits, [None]):
            result.append(data[prev:split])
            prev = split
        yield result

def get_min_n(groups):
    # groups: list of different index combinations
    # return new_groups: return the groups that contain lists larger than 3 sentences
    new_groups = []
    for group in groups:
        flag = 0
        for parr in group:
            if len(parr) < 3:
                flag = 1
        if flag == 0:
            new_groups.append(group)
            
    return new_groups

def get_lists(partition, splited_data):
    # partition: the list of lists of indexes that represent each sentence
    # splitted_data: list of sentences of the original text
    # return final_text: list of lists representing the separation of the 
    # original text into parragraphs and sentences

    final_text = []
    for parr in partition:
        final_parr = []
        for sent in parr:
            final_parr.append(splited_data[sent])
        final_text.append(final_parr)
    return final_text

def compute_similarities(lista):
    # Get a list of texts and return the mean of the similarity matrix

    vect = TfidfVectorizer(min_df=1, stop_words="english")                                                                                                                                                                                                   
    tfidf = vect.fit_transform(lista)                                                                                                                                                                                                                       
    pairwise_similarity = tfidf * tfidf.T
    return pairwise_similarity.toarray().mean()

def get_inner_outer_similarity(indexes, splited_data):
    # Return the mean similarities between sentences inside parragraphs (inner) and
    # by parragraphs (outer)

    # indexes: list of combination of the indexes of the list of sentences in the text.
    # splitted_data: original text splitted into sentences

    final_list = []
    outer_similarities = []
    inner_similarities = []
    for comb in indexes:
        final_list = get_lists(comb, splited_data)        
        final_text_list = []
        parr_sim = []
        for parr in final_list:
            parr_sim.append(compute_similarities(parr))
            joined_parr = ".".join(parr)
            final_text_list.append(joined_parr)
        
            
        mean_sim = compute_similarities(final_text_list)
        outer_similarities.append(mean_sim)
        inner_similarities.append(np.mean(parr_sim))
    return np.array(outer_similarities), np.array(inner_similarities)

def raw2parr(raw, n):
    raw = raw.replace("?", ".")
    raw = raw.replace("!", ".")
    splited_data = raw.split(".")
    if len(splited_data) < 3*n:
        return "min sentence error"
    indexes = list(split_list(list(range(len(splited_data))), n))
    indexes = get_min_n(indexes)
    outer_similarities, inner_similarities = get_inner_outer_similarity(indexes, splited_data)
    scores = inner_similarities + (1/outer_similarities)
    final_list = get_lists(indexes[np.argmin(scores)], splited_data)
    final_parrs = []
    for p in final_list:
        final_parrs.append(".".join(p))

    return final_parrs