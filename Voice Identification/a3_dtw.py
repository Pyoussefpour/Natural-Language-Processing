import numpy as np
from scipy.spatial.distance import euclidean
from typing import List

dataDir = '/u/cs401/A3/data/'

# Class definition for an individual table cell. DO NOT MODIFY
class TableCell(object):
    def __init__(self, cost:float = 0.0, trace_r:int = None, trace_h:int = None):
        """
        initialize: defines an individual table cell

        Parameters
        ----------
        cost :
        trace_r : the row index of last node, used for path tracing
        trace_h : the column index of last node, used for path tracing

        Returns
        -------
        N/A

        Examples
        --------
        Creating a cell
        >>> cell = TableCell(1.0, 0, 0)

        Checking the cost of a cell
        >>> if cell.cost == 1.0:
        ...     ...

        Modifying the last node indices
        >>> cell.trace_r, cell.trace_h = 1, 2
        """
        super().__init__()
        self.cost, self.trace_r, self.trace_h = cost, trace_r, trace_h

# Code for loading a set of testing MFCCs. DO NOT MODIFY!
def extract_mfcc_segment(mfccs, time_range, hop_length):
    """
    Extract an MFCC segment from the given time range.

    Parameters:
    mfccs (np.ndarray): 2D array of MFCCs (frames x coefficients).
    time_range (tuple): Start and end time in seconds (start_time, end_time).
    hop_length (int): Hop length used in MFCC extraction.(window_length x sr / 2)

    Returns:
    np.ndarray: 2D array of MFCCs corresponding to the time range.
    """
    start_frame = int(time_range[0] * 1000 / hop_length)
    end_frame = int(time_range[1] * 1000 / hop_length)
    return mfccs[start_frame:end_frame]

# Complete the following component for DTW
def initialize(U : int, T : int) -> List[List[TableCell]]:
    """
    initialize: allocate the table and initialize the first row and column

    Parameters
    ----------
    U : int, Number of elements in the reference sequence
    T : int, Number of elements in the hypothesis sequence

    Returns
    -------
    table: list of list of TableCell of size [U + 1, T + 1], the table used for dynamic programming.
        All elements of the table should be `TableCell` instances,
        but only the values of the first row and column need to be computed.
    """

    ############################################
    table = None
    table = np.zeros((U+1,T+1),dtype=TableCell)
    table[0,0] = TableCell(0)
    table[0,1:] = [TableCell(float('inf')) for i in range(T)]
    table[1:,0] = [TableCell(float('inf')) for i in range(U)]
    table[1:,1:] = TableCell(0,0,0)

    table = table.tolist()
    ############################################

    # Make sure the type of values are correct
    assert isinstance(table, list) and all(isinstance(row, list) and all(isinstance(cell, TableCell) for cell in row) for row in table)
    return table

def step(u : int, t : int, table : List[List[TableCell]], r : List[str], h : List[str]) -> None:
    """
    step: computes the value of the current cell

    Parameters
    ----------
    u : int, row index of the current cell
    t : int, col index of the current cell
    table : list of list of TableCell of size [U + 1][T + 1]
    r : mfcc of the reference audio
    h : mfcc of the candidate audio

    Returns
    -------
    N/A
    """
    ############################################
    
    operations_cost = [table[u-1][t-1].cost, table[u][t-1].cost, table[u-1][t].cost]
    min_i = np.argmin(operations_cost)

    cost = euclidean(r[u-1],h[t-1]) + operations_cost[min_i]

    if min_i == 0:      #diagonal
        table[u][t] = TableCell(cost,u-1,t-1)
    elif min_i == 1:    #left
        table[u][t] = TableCell(cost,u,t-1)
    else:               #up
        table[u][t] = TableCell(cost,u-1,t)

    ############################################
    return

def finalize(table):
    """
    finalize: computes the final results, DTW distance and OWP

    Parameters
    ----------
    table : accumulated cost matrix w/ path tracing

    Returns
    -------
    (dist, path): (float, list of (int, int)) DTW distance and optimal warping path
    """
    # Define results to be returned:
    dist = float('inf')
    path = []

    ############################################
    u = len(table) - 1
    t = len(table[0]) - 1
    dist = table[u][t].cost
    path.append((u,t))
    while u > 0 and t > 0:
        u_trace = table[u][t].trace_r
        t_trace = table[u][t].trace_h
        path.append((u_trace,t_trace))
        u = u_trace
        t = t_trace

    path.reverse()
    ############################################

    return (dist, path)

def DTW(r, h):
    """
    Calculation of DTW distance between two MFCCs.

    You should complete the core component of this function.
    DO NOT MODIFY ANYTHING IN HERE

    Parameters
    ----------
    r : mfcc of the reference audio
    h : mfcc of the candidate audio

    Returns
    -------
    (dist, path): (float, list) DTW distance and optimal warping path
    """

    # U: length of reference;
    # T: length of hypothesis
    U, T = len(r), len(h)

    ############################################
    ################### DTW: ###################
    ############################################

    # Define a matrix table[T + 1, U + 1] as accumulative cost matrix w/ backtrace decisions coordinates for OWP
    table = initialize(U, T)

    # Iterate over the remaining cols and rows
    # Use values of words and the previously computed cells to compute current cell
    for u in range(1, U + 1, 1):
        for t in range(1, T + 1, 1):
            step(u, t, table, r, h)

    # Use table to compute final results
    # A.K.A DTW and OWP
    return finalize(table)

if __name__ == "__main__":
    """
    Main Function: A small testing program as a sanity check. MODIFY WITH CAUTION!
    Note: Check if you can identify the candidate speaker that matches the reference speaker
          via your DTW distance. The answer is spoiled when we load them up! 

    Output Format: ([] contains argument)
    --------------
    Reference Speaker: Speaker #[Speaker Number]
    Speaker #[Speaker Number]: DTW = [DTW Value]
    ...
    Speaker #[Speaker Number]: DTW = [DTW Value]
    """

    # OG Some time stamps of useful segments:
    time_start = [76.500, 181.889, 47.285, 42.588, 110.223]
    time_end = [76.963, 182.302, 48.396, 43.162, 110.935]

    #Time stamps for testing
    # time_start = [78.750, 181.889, 47.285, 42.588, 112.3]
    # time_end = [80.95, 182.25, 48.4, 43.07, 114.9]

    # Load the segments of the above time stamps
    speaker_1 = extract_mfcc_segment(np.load(dataDir + 'S-24D/0.mfcc.npy'), (time_start[0], time_end[0]), 10)
    speaker_2 = extract_mfcc_segment(np.load(dataDir + 'S-24D/4.mfcc.npy'), (time_start[1], time_end[1]), 10)
    speaker_3 = extract_mfcc_segment(np.load(dataDir + 'S-16D/0.mfcc.npy'), (time_start[2], time_end[2]), 10)
    speaker_4 = extract_mfcc_segment(np.load(dataDir + 'S-22B/4.mfcc.npy'), (time_start[3], time_end[3]), 10)
    speaker_5 = extract_mfcc_segment(np.load(dataDir + 'S-5A/3.mfcc.npy'), (time_start[4], time_end[4]), 10)
    everyone = [speaker_1, speaker_2, speaker_3, speaker_4, speaker_5]

    # Define a reference
    ref = 3

    # Compute DTW distance
    print(f"Reference Speaker: Speaker #{ref + 1}")
    for i in range(0, len(everyone), 1):
        if i == ref:
            continue
        dist, path = DTW(everyone[ref], everyone[i])
        print(f"Speaker #{i + 1}: DTW = {dist :.4f}")