import time
import os


def getfilesize(filename):
    return os.path.getsize(filename)


def getlinecount(filename):
    fd = open(filename, 'r+')
    count = len(fd.readlines())
    fd.close()
    return count


def readline(filename, linenum=1):
    fd = open(filename, 'r+')
    line = fd.readlines()[linenum-1]
    fd.close()
    return line


def clearfile(filename):
    fd = open(filename, 'w+')
    fd.close()


# def auto_check:
    # time.sleep(5)


if __name__ == '__main__':
    g_file = "task.txt"
    old_count = getlinecount(g_file)
    while 1:
        if old_count > 10:
            clearfile(g_file)
            old_count = 0
        new_count = getlinecount(g_file)
        if old_count != new_count:
            print "new line : %s" % readline(g_file, new_count)
            old_count = new_count

        time.sleep(5)


