def print_color(text, color):
    r,g,b = tuple(int(color[i:i+2], 16) for i in (0, 2, 4))
    coloresc = '\033[{};2;{};{};{}m'.format(38, r, g, b)
    resetesc = '\033[0m'
    print(coloresc + text + resetesc)