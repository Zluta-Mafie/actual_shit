import lineDetApi
def getMoveInstructions():
    offset, angle  = lineDetApi.GetVisualInfo()
    lateralMove = -1/540*offset
    rotation = (angle-90)
    return (lateralMove, rotation)
