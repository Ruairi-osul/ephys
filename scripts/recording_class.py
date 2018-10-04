import re


pattern = r'/d{2}-/d{2}-d{2}_PRE$'
pattern1 = r'..-..-.._PRE$'
pattern3 = r'_'

s = r'/media/ruairi/UBUNTU/CIT_WAY/dat_files/Chronic_40_2018-08-13_15-16-21_PRE'

s1 = 'hello'
print(bool(re.search(pattern1, s)))
