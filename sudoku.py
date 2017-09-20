#!/usr/bin/env python 3
# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
import functools
from time import time
from puzzles import puzzle3


def get_empty_cells(data):
    filled_cells = data//10
    whole_board = np.setdiff1d(np.array(range(11, 100)),
                               np.array(range(20, 100, 10)),
                               assume_unique=True)
    return np.setdiff1d(whole_board, filled_cells, assume_unique=True)


def select_same_(entry_code, data):
    same_box = np.intersect1d(
        data[(data - 100)//300 == (entry_code - 100)//300],
        data[(data % 100 - 10)//30 == (entry_code % 100 - 10)//30],
        assume_unique=True)
    same_col = data[data % 100 // 10 == entry_code % 100 // 10]
    same_row = data[data//100 == entry_code//100]
    return same_row, same_col, same_box


def get_allowed_cell_values(cell_code, data):
    nums = np.array(range(1, 10))
    allowed_vals = [np.setdiff1d(nums, axis % 10, assume_unique=True)
                    for axis in select_same_(cell_code*10, data)]
    allowed_vals = functools.reduce(np.intersect1d, allowed_vals)
    return [cell_code*10 + vals for vals in allowed_vals]


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


def is_valid_state(data):
    return all([
        len(get_allowed_cell_values(code, data)) != 0
        for code in get_empty_cells(data)
        ])


def main():
    init_data = puzzle3
    data = init_data
    sol_data = np.array([], dtype=int)
    bad_codes = []
    branch_head = []
    loop_count = 0
    reach_end_of_choices = False
    t0 = time()
    while loop_count < 1000:
        loop_count += 1
        choices_list = [
            np.setdiff1d(
                get_allowed_cell_values(code, data),
                bad_codes,
                assume_unique=True
                )
            for code in get_empty_cells(data)
        ]
        choices_list = sorted(choices_list, key=len)
        # check if the board is solved
        if len(choices_list) != 0:
            choices = choices_list[0]
            for c in choices:
                if len(choices) > 1:
                    branch_head.append(c)
                if is_valid_state(np.r_[data, c]):
                    data, sol_data = np.r_[data, c], np.r_[sol_data, c]
                    reach_end_of_choices = False
                    break
                else:
                    reach_end_of_choices = True
            if reach_end_of_choices:
                latest = branch_head.pop(-1)
                bad_codes = [latest]
                data = np.delete(
                    data, np.s_[np.where(data == latest)[0][0]:]
                    )
                sol_data = np.delete(
                    sol_data, np.s_[
                        np.where(sol_data == latest)[0][0]:]
                    )
        # board is solved
        else:
            print("Solved! in %.4f" % (time()-t0))
            break
    make_board(init_data, sol_data)


if __name__ == "__main__":
    main()
