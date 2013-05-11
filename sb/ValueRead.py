import collections
import re

file = open("data.txt")

bin = {10**(count+.5) : 0  for count in xrange(10)}
bin = collections.OrderedDict(sorted(bin.items()))
 
while 1:
    line = file.readline()
    if not line:
        break
        
    s = re.findall("[-+]?\d*\.\d+|\d+", line)

    for k, v in bin.items():
        if val < k:
            print val,  k 
            bin[k] += 1
            break;
  
   
print bin



original = ['0.061', '0.012', '0.017', '0.030', '0.093', '0.016', '0.016', 
'0.049', '0.050', '0.001', '0.006', '0.034', '0.018', '0.052', '0.055',
 '0.013', '0.001', '0.041', '0.050', '0.069', '0.021', '0.007', '0.017',
 '0.001', '0.013', '0.000', '0.159']

result = [sum(float(item) for item in original[0:rank+1]) for rank in xrange(len(original))]

print result





