import cv2
import sys
import random


def image_show(imgdir):
    img = cv2.imread(imgdir)
    print imgdir
    cv2.namedWindow("Hello")
    cv2.imshow("Hello", img)
    cv2.waitKey(0)


def guess_game():
    orgdigit = random.randint(0,100)
    for i in range(0, 10, 1):
        i += 1
        print "i =", i
        inputdigit = raw_input("Please guess:")
        print int(inputdigit)
        if int(inputdigit) > orgdigit:
            print "Bigger than org digit !!"
        elif int(inputdigit) < orgdigit:
            print "Smaller than org digit !!"
        else:
            print "Correct !!"
            break


def prime():
    for i in range(1, 1000):
        if i == 2 or i == 3 or i == 5 or i == 7:
            print str(i) + " is primer"
            continue
        if i % 2 == 0 or i % 3 == 0 or i % 5 == 0 or i % 7 == 0:
            continue
        j = 3
        while j * j < i:
            if i % j == 0:
                break
            else:
                j += 1
        else:
            print str(i) + " primer"


if __name__ == '__main__':
    # image_show(sys.argv[1])
    # guess_game()
    prime()
