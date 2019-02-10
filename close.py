from Cover import *
import sys,string
file = 'test.aml'

args = string.split(sys.stdin.read())

#SourceCover. The cover that the TargetCover is tested against.
SourceCover = Cover(args[0],file)

# Create a subset of the Source Cover to exclude features that
# are not tested
SourceCover = SourceCover.reselect('polygon','perennial = 2')

#TargetCover. The cover which is being tested.
TargetCover = Cover(args[1],file)

# Create a subset of the Target Cover to exclude the features which
# are not tested


# Buffer the source cover polygons by 0.1m on both sides
# of its bounding lines
buf01 = SourceCover.buffer(0.1,'line')

# Buffer the source cover polygons on both sides
# its bounding lines
buf50 = SourceCover.buffer(50,'line')

# Find target arcs that fall within 50m of source lines
# Use identity and inside = 100 to find those which are only
# inside the buffer corridor.
trgclip = TargetCover.clip(buf50,'line')
trgident = trgclip.identity(buf50,'line')
inside50 = trgident.reselect('line','inside = 100')

# Remove the inside item because well add it again later
inside50.dropitem('line','inside')

# Find those which are 0.1m of the the source lines
trgident2 = inside50.identity(buf01,'line')
notonline = trgident2.reselect('line','inside =  1')

#Remove those arcs which cross the 50m buffer at right angles
#notonline = notonline.reselect('line','length  > 250')
print notonline.name
notonline.reduce('line','length  > 250')
print notonline.name

# Kill temporary cover
buf01.kill()
buf50.kill()
trgclip.kill()
trgident.kill()
inside50.kill()
trgident2.kill()


sys.stderr.write('%s\n' % file)
