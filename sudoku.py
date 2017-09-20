#!/usr/bin/env python 3
# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
import functools
from time import time


def get_empty_cells(data):
    filled_cells = data//10
    whole_board = np.setdiff1d(np.array(range(11, 100)),
                               np.array(range(20, 100, 10)))
    return np.setdiff1d(whole_board, filled_cells)


def select_same_(entry_code, data):
    same_box = np.intersect1d(
                    data[(data - 100)//300 == (entry_code - 100)//300],
                    data[(data % 100 - 10)//30 == (entry_code % 100 - 10)//30])
    same_col = data[data % 100 // 10 == entry_code % 100 // 10]
    same_row = data[data//100 == entry_code//100]
    return same_row, same_col, same_box


def get_allowed_cell_values(cell_code, data):
    nums = np.array(range(1, 10))
    allowed_vals = [np.setdiff1d(nums, axis % 10)
                    for axis in select_same_(cell_code*10, data)]
    allowed_vals = functools.reduce(np.intersect1d, allowed_vals)
    return [cell_code*10 + vals for vals in allowed_vals]


def is_valid_entry(entry_code, data):
    same_row, same_col, same_box = select_same_(entry_code, data)
    if any([(entry_code - row_code) % 10 == 0 for row_code in same_row]):
        return False
    elif any([(entry_code - col_code) % 10 == 0 for col_code in same_col]):
        return False
    elif any([(entry_code - box_code) % 10 == 0 for box_code in same_box]):
        return False
    else:
        return True


def draw_entries(init_data, sol_data, ax):
    for entry_code in init_data:
        ax.text(*read_cell_code(entry_code), color="k", fontsize=14)
    for entry_code in sol_data:
        ax.text(*read_cell_code(entry_code), color="b", fontsize=14)


def make_board(init_data, sol_data):
    sudoku = plt.figure()
    ax = sudoku.add_subplot(111)
    ax.set_xlim(0, 9)
    ax.set_ylim(0, 9)
    ax.xaxis.set_major_locator(mpl.ticker.MultipleLocator(3))
    ax.yaxis.set_major_locator(mpl.ticker.MultipleLocator(3))
    ax.xaxis.set_major_locator(mpl.ticker.MultipleLocator(3))
    ax.yaxis.set_major_locator(mpl.ticker.MultipleLocator(3))
    ax.xaxis.set_minor_locator(mpl.ticker.MultipleLocator(1))
    ax.yaxis.set_minor_locator(mpl.ticker.MultipleLocator(1))
    ax.xaxis.set_major_formatter(mpl.ticker.NullFormatter())
    ax.yaxis.set_major_formatter(mpl.ticker.NullFormatter())
    ax.tick_params(which="both", bottom="off", left="off")
    ax.grid(lw=3, color="k")
    ax.grid(which="minor", lw=1, color="k")
    draw_entries(init_data, sol_data, ax)
    return sudoku


def read_cell_code(code):
    row, r1 = divmod(code, 100)
    col, num_entry = divmod(r1, 10)
    return col - 0.6, 9.3 - row, str(num_entry)


def is_valid_state(data, bad_codes, sol_data):
    choices_list = [get_allowed_cell_values(code, data)
                    for code in get_empty_cells(data)]
#    choices_list = [np.setdiff1d(x, bad_codes) for x in choices_list]
#    choices_list = [np.setdiff1d(x, sol_data) for x in choices_list]
    return all([len(x)!=0 for x in choices_list])


def main():
#    print('\n'*100)
#    print("Sudoku solver program\n=======================")
#    data = np.array([118, 135, 156, 164, 192,
#                     216, 222, 253, 311, 337, 358,
#                     375, 426, 443, 461, 495, 538,
#                     546, 565, 571, 615, 647, 668,
#                     887, 896, 914, 942, 957, 979,
#                     683, 731, 755, 773, 794, 851,
#                     991])

#    data = np.array([126, 138, 142, 153, 199,
#                     213, 232, 249, 254, 271,
#                     335, 361,
#                     412, 496,
#                     516, 525, 537, 544, 568, 572, 581, 593,
#                     618, 694,
#                     741, 774,
#                     834, 852, 863, 876, 898,
#                     917, 956, 964, 979, 982])
    # evil
#    data = np.array([128, 133, 161, 199,
#                     221, 256, 264,
#                     315, 334,
#                     412, 436, 447,
#                     554,
#                     663, 677, 698,
#                     778, 793,
#                     841, 855, 889,
#                     917, 944, 976, 981])

# XXX might have something wrong with this puzzle. Input error?
#    data = np.array([168, 182, 193,
#                     235, 242,
#                     331, 347, 359,
#                     449, 476, 499,
#                     514, 595,
#                     611, 633, 667,
#                     756, 769, 777,
#                     821, 862, 878,
#                     912, 928, 944])

#    data = np.array([118, 125, 157, 174,
#                     227, 242,
#                     326, 369,
#                     419, 456,
#                     513, 538, 577, 591,
#                     652, 695,
#                     748, 782,
#                     861, 889,
#                     937, 953, 985, 998])
#    data = np.array([118, 121, 193,
#                     241, 264,
#                     322, 335, 343, 397,
#                     433, 444, 458, 487,
#                     631, 667, 672, 698,
#                     712, 725, 779,
#                     849, 894,
#                     938, 986])

    data = np.array([139, 141, 198,
                     227, 259, 274, 293,
                     316, 362,
                     435, 452, 489, 494,
                     612, 629, 657, 676,
                     742, 795,
                     818, 831, 855, 883,
                     917, 969, 971])
    init_data = data
    sol_data = np.array([], dtype=int)
    bad_codes = []
    loop_count = 0
    try_next = False
    branch_head = []
    t0 = time()
    while loop_count < 600:
        loop_count += 1
#        print(loop_count)
        choices_list = [get_allowed_cell_values(code, data)
                        for code in get_empty_cells(data)]
        choices_list = [np.setdiff1d(x, bad_codes) for x in choices_list]
#        choices_list = [np.setdiff1d(x, sol_data) for x in choices_list]
        choices_list = sorted(choices_list, key=lambda x: len(x))
        # check if the board is solved
        if len(choices_list) != 0:
            for choices in choices_list:
                if len(choices) == 0:
                    make_board(init_data, sol_data)
                    raise ValueError("Unsolvable state encountered")
                else:
#                    print("Available choices ", choices)
                    for c in choices:
                        if len(choices) > 1:
                            branch_head.append(c)
#                            print("Branch head at: %d" % c)
#                        print("Trying %d " % c)
                        if is_valid_state(np.r_[data, c], bad_codes, sol_data):
                            data, sol_data = np.r_[data, c], np.r_[sol_data, c]
                            try_next = False
                            break
                        else:
#                            print("%d is an invalid code" % c)
                            #bad_codes.append(c)
                            try_next = True
                if not try_next:
                    break
                else:
                    try:
                        latest = branch_head.pop(-1)
                    except:
                        print("Bad codes", bad_codes)
                        print("Solution", sol_data)
                        make_board(init_data, sol_data)
                        raise ValueError("Unsolvable state")
#                    print("Current branch heads", branch_head)
#                    print("Deleting %d" % latest)
                    bad_codes = [latest]
                    data = np.delete(
                        data, np.s_[np.where(data == latest)[0][0]: ]
                        )
                    sol_data = np.delete(
                        sol_data, np.s_[
                            np.where(sol_data == latest)[0][0]: ]
                        )
                    break
      # board is solved
        else:
#            make_board(init_data, sol_data)
            print("Solved! in %.4f" % (time()-t0))
            break
#    if all([is_valid_entry(codes, data) for codes in sol_data]):
#        print("Solution validated!")
#    else:
#        print("Solution invalid")
    make_board(init_data, sol_data)

if __name__ == "__main__":
    main()
