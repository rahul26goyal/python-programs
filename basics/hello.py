import sys

print("Hello Python !!")
path = sys.path
print("Path " + str(path))


def dummy():
    print("Dummy imports")


if __name__ == '__main__':
    dummy()
