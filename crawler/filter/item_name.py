
def have_prohibit_name(name):
    with open("crawler/filter/item_name.txt", "r") as f:
        prohibit_item_name = f.read().split("\n")

    for p in prohibit_item_name:
        if p in name:
            return True        

    return False        
