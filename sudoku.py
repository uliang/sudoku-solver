#!/usr/bin/env python 3
# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
import functools


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


def draw_entries(data, ax):
    for entry_code in data:
        ax.text(*read_cell_code(entry_code), color="k", fontsize=14)


def make_board(data):
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
    draw_entries(data, ax)
    return sudoku


def read_cell_code(code):
    row, r1 = divmod(code, 100)
    col, num_entry = divmod(r1, 10)
    return col - 0.6, 9.3 - row, str(num_entry)


def main():
    print('\n'*100)
    print("Sudoku solver program\n=======================")
    data = np.array([118, 135, 156, 164, 192,
                     216, 222, 253, 311, 337, 358,
                     375, 426, 443, 461, 495, 538,
                     546, 565, 571, 615, 647, 668,
                     683, 731, 755, 773, 794, 851,
                     887, 896, 914, 942, 957, 979,
                     991])

    choices = {}
    loop_count = 0
    while loop_count < 200:
        loop_count += 1
        print(loop_count)
        choices = {cell: get_allowed_cell_values(cell, data)
                   for cell in get_empty_cells(data)}
        if choices != {}:
            # Find a cell with only one valid entry
            for key, val in choices.items():
                if len(val) == 1:
                    # print(data)
                    data = np.concatenate((data, val))
                    # print(data)

            #make_board(data)
            #searchable = False
        else:
            make_board(data)
            print("Solved!")
            break

#    print(choices)
#    make_board(data)


if __name__ == "__main__":
    main()
