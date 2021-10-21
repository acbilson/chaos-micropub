import os


def read_notes(dir):
    return [os.path.join(dir, name) for name in os.listdir(dir)]
