from Cover import Cover
from List import List


vcover = Cover('I5308VM','same.aml')
fcover = Cover('COAST','same.aml')
l1 = vcover.getitems('arc')
l2 = fcover.getitems('arc')
l3 = l1[7:0]
l4 = l2[7:0]

code = '''
    &ty %s
    &ty %s
    ''' % (l3.isequal(l4),l3[2])

vcover.writecode(code)

