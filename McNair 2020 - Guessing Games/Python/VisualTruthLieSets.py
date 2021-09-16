import pygame

size = 2 ** 9
num_questions = 4
numlies = 1
setup_ratios = []
rep_ratios = [1/2]
setup_answers = []
rep_answers = [1]
questions = []
# [[[0, 1 / 2]],
#              [[0, 1/2]],
#              [[0, 1/4], [2/4, 3/4]],
#              [[0, 1/8], [2/8, 3/8], [4/8, 5/8], [6/8, 7/8]]]
square = True
save_pics = True

all_nums = [i for i in range(size)]
lie_colors = []
bad = (0, 0, 0)
maybe = (255 // 2, 255 // 2, 255 // 2)
good = (255, 255, 255)
white = (255, 255, 255)


def show(image):
    screen = pygame.display.get_surface()
    screen.blit(image, (0, 0))
    pygame.display.flip()


def question(round_num):
    q = []
    if questions:
        realnumquestion = questions[round_num - 1]
        for interval in realnumquestion:
            interval[0] = round(interval[0] * size)
            interval[1] = round(interval[1] * size)
            for num in range(interval[0], interval[1]):
                q.append(num)
    else:
        sr = setup_ratios
        rr = rep_ratios

        q = [[i for i in range(size)]]
        temp = []
        for i in range(round_num):
            if i < len(sr):
                ratio = sr[i]
            else:
                ratio = rr[(i - len(sr)) % len(rr)]

            for alist in q:
                temp.append(alist[:int(len(alist) * ratio)])
                temp.append(alist[int(len(alist) * ratio):])

            q = temp
            temp = []

        temp = q
        q = []

        for i in range(len(temp)):
            if i % 2 == 0:
                q += temp[i]

    return q


def makegamestart(surface):
    # create the PixelArray
    ar = pygame.PixelArray(surface)

    # graph triangle or square
    if square:
        for x in range(size):
            for y in range(size):
                ar[x, y] = good
    else:
        for x in range(size):
            for y in range(size):
                if x >= size - y:
                    ar[x, y] = good
                else:
                    ar[x, y] = white

    for x in range(size):
        ar[x, 0] = bad
        ar[x, size-1] = bad
    for y in range(size):
        ar[0, y] = bad
        ar[size-1, y] = bad

    del ar


def makeliecolors():
    lie_colors.append(good)
    lie_colors.append(bad)
    for i in range(numlies):
        if i == 0:
            lie_colors.insert(-1, (255 // 2, 255 // 2, 255 // 2))
        else:
            lc = lie_colors[-2]
            lc0 = lc[0]
            lc1 = lc[1]
            lc2 = lc[2]
            lie_colors.insert(-1, (lc0 // 2, lc1 // 2, lc2 // 2))


def save(surface, round_num):
    filename = "Pics/Manuscript/"
    filename += f"After_{round_num + 1}_Questions.png"
    pygame.image.save(surface, filename)


def main():
    pygame.init()

    pygame.display.set_mode((size, size))
    surface = pygame.Surface((size, size))

    pygame.display.flip()

    makegamestart(surface)
    makeliecolors()
    show(surface)

    # ask question and answer it
    for round_num in range(num_questions):
        ar = pygame.PixelArray(surface)
        q = question(round_num + 1)
        sa = setup_answers
        ra = rep_answers

        if round_num < len(sa):
            answer = sa[round_num]
        else:
            answer = ra[(round_num - len(sa)) % len(ra)]

        # go through every necessary pixel
        for x in range(size):
            if square:
                lower_y = 0
            else:
                lower_y = size - x

            for y_pixel in range(lower_y, size):
                y_coord = size - y_pixel
                color = surface.get_at((x, y_pixel))[:3]
                colorindex = lie_colors.index(color)

                if int(x in q) + int(y_coord in q) != answer:
                    if colorindex < numlies + 1:
                        ar[x, y_pixel] = lie_colors[colorindex + 1]

        del ar

        if save_pics:
            save(surface, round_num)

        show(surface)


if __name__ == '__main__':
    main()
    while 1:
        event = pygame.event.wait()
        if event.type == pygame.QUIT:
            raise SystemExit
