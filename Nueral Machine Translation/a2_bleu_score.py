""""
This code is provided solely for the personal and private use of students
taking the CSC401H/2511H course at the University of Toronto. Copying for
purposes other than this use is expressly prohibited. All forms of
distribution of this code, including but not limited to public repositories on
GitHub, GitLab, Bitbucket, or any other online platform, whether as given or
with any changes, are expressly prohibited.

Authors: Sean Robertson, Jingcheng Niu, Zining Zhu, and Mohamed Abdall
Updated by: Arvie Frydenlund, Raeid Saqur and Jingcheng Niu

All of the files in this directory and all subdirectories are:
Copyright (c) 2024 University of Toronto
"""

"""
Calculate BLEU score for one reference and one hypothesis

You do not need to import anything more than what is here
"""

from math import exp  # exp(x) gives e^x
from collections.abc import Sequence


def grouper(seq: Sequence[str], n: int) -> list:
    """
    Extract all n-grams from a sequence

    An n-gram is a contiguous sub-sequence within `seq` of length `n`. This
    function extracts them (in order) from `seq`.

    Parameters
    ----------
    seq : sequence
        A sequence of words or token ids representing a transcription.
    n : int
        The size of sub-sequence to extract.

    Returns
    -------
    ngrams : list
    """
    
    seq = [word.lower() if type(word)==str else word for word in seq]
    ngrams = [seq[i:i+n] for i in range(len(seq)-(n-1))]
    return ngrams


def n_gram_precision(
    reference: Sequence[str], candidate: Sequence[str], n: int
) -> float:
    """
    Calculate the precision for a given order of n-gram

    Parameters
    ----------
    reference : sequence
        The reference transcription. A sequence of words or token ids.
    candidate : sequence
        The candidate transcription. A sequence of words or token ids
        (whichever is used by `reference`)
    n : int
        The order of n-gram precision to calculate

    Returns
    -------
    p_n : float
        The n-gram precision. In the case that the candidate has length 0,
        `p_n` is 0.
    """
    ngram_ref = grouper(reference, n)
    ngram_candidate = grouper(candidate, n)

    if len(candidate) < n:
        return 0.0
    
    if len(candidate) == 0:
        p_n = 0
    else:

        p_n = sum(1 for element in ngram_candidate if element in ngram_ref)/len(ngram_candidate)
    
    return p_n


def brevity_penalty(reference: Sequence[str], candidate: Sequence[str]) -> float:
    """
    Calculate the brevity penalty between a reference and candidate

    Parameters
    ----------
    reference : sequence
        The reference transcription. A sequence of words or token ids.
    candidate : sequence
        The candidate transcription. A sequence of words or token ids
        (whichever is used by `reference`)

    Returns
    -------
    BP : float
        The brevity penalty. In the case that the candidate transcription is
        of 0 length, `BP` is 0.
    """
    c = len(candidate)
    r = len(reference)

    if c == 0:
        BP = 0
        return BP
    
    brevity = r/c

    if brevity < 1:
        BP = 1
    
    else:
        BP = exp(1-brevity)
    
    return BP


def BLEU_score(reference: Sequence[str], candidate: Sequence[str], n) -> float:
    """
    Calculate the BLEU score.  Please scale the BLEU score by 100.0

    Parameters
    ----------
    reference : sequence
        The reference transcription. A sequence of words or token ids.
    candidate : sequence
        The candidate transcription. A sequence of words or token ids
        (whichever is used by `reference`)
    n : int
        The maximum order of n-gram precision to use in the calculations,
        inclusive. For example, ``n = 2`` implies both unigram and bigram
        precision will be accounted for, but not trigram.

    Returns
    -------
    bleu : float
        The BLEU score
    """

    BP = brevity_penalty(reference,candidate)
    p_n = 1

    for i in range(1,n+1):
        p_n = p_n * n_gram_precision(reference,candidate,i)
        
    BLEU = 100 * BP * (p_n ** (1/n))
    return BLEU
