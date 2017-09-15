import matplotlib.pyplot as plt
import matplotlib as mpl


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
    return col + 0.4 - 1, row + 0.3 - 1, str(num_entry)


def main():
    print('\n'*100)
    print("Sudoku solver program\n=======================")
    print('\n'*2)
    make_board(data=[111])
#    code = int(input("Input three digit code\n>>>"))
#    print(read_cell_code(code))


if __name__ == "__main__":
    main()
