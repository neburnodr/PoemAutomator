from data.processing_verses import clean_verses as clean


with open("f_tst.txt") as f:
    lines = f.read().split("\n")


lines_clean = clean(lines)


with open("/home/nebur/Desktop/poemautomator/tests/f_to_comp_w_f_tst.txt", "w") as f:
    f.write("\n".join(lines_clean))
