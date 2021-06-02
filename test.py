import re


s = "A strange seed was\nplanted on its\nback at birth.\fThe plant sprouts\nand grows with\nthis POKéMON."

s = s.replace('\n', '').replace('\f', '')
print(s)
