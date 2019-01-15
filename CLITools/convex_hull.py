import math

def graham_scan(points):
    ''' Graham Scan 
    This function calculates the convex hull of 2-dimensional coordinates
    Input:
        points  List of 2-dimensional points

    Output:   
        Sorted list of points in convex hull
    '''    
    # If less than two coordinates are in the list, the Algorithm will not be called
    if len(points)<3:
        return points

    changedX=False
    changedY=False

    #The algorithm (as programmed) only works for positive X and Y values, therefore the coordinates might have to be moved altogether
    minX=min(points, key=lambda x: x[0])
    j=0
    if minX[0]<0:
        changedX=True
        while j < len(points):
            points[j][0]=points[j][0]-minX[0]

    
    minY=min(points, key=lambda x: x[1])
    j=0
    if minY[1]<0:
        changedY=True
        while j < len(points):
            points[j][1]=points[j][1]-minY[1]



    # sorts the coordinates based on the y value and, if those are equal, on the x value
    coords = sorted(points, key = lambda x: x[0])
    coords = sorted(coords, key = lambda x: x[1])


   
    def calcTriangle(a, b, c):
        ''' Triangle Calculation
        Determines whether a given point C is left (return value 1) or right (return value 0) of a vector AB
        Input:
            a : 2D point as List
            b : 2D point as List
            c : 2D point as List

        Output: 
            true : if c is left of AB
            false : if c is right of AB
        '''
        res = (b[0]-a[0])*(c[1]-a[1])-(c[0]-a[0])*(b[1]-a[1])
        if res > 0:
            return True
        else:
            return False
            


            
    
    def calcAngle(p0, p1):
        ''' Angle Calculation
        Calculates the angle of a vector between two points and the x-axis
        Input:
            p0: 2D point as List
            p1: 2D point as List
        '''
        if (p1[0]-p0[0])==0:
            return 90

        if (p1[1]-p0[1])==0:
            return 0


        m = float((p1[1]-p0[1])/(p1[0]-p0[0]))
        b = p0[1]-m*p0[0]
        x0 = -(b/m)

        deg = math.degrees(math.atan(p1[1]/(p1[0]-x0)))
        return deg

    #Starting point
    point0 = [coords[0][0], coords[0][1], 0]

    #Initialise list which contains the original points plus the angles they form with p0 towards the x-axis
    coordAngles = [point0]

    i = 1; 

    #Lists the coordinate points and the angle between each point and p0 and the x-axis
    while i < len(coords):
        angle = calcAngle(point0, coords[i])
        if angle<0:
            angle=180+angle
        coordAngles.append([coords[i][0], coords[i][1], angle])
        i=i+1
    
    #sort coordinate points by angles
    coords = sorted(coordAngles, key= lambda x: x[2])

    #Actual Graham Scan starts here
    points = []
    points.insert(0,[coords[0][0], coords[0][1]])
    points.insert(0,[coords[1][0], coords[1][1]])

    i=2
    #Generate output (convex hull)
    while i < len(coords):
        s1=points[0]
        s2=points[1]
        #If the new point is left of the two points last added or if the set contains only two points, it is added to the set
        if  len(points)==2 or calcTriangle(s2, s1, coords[i]):
            points.insert(0,[coords[i][0], coords[i][1]])
            i=i+1
        #If the new point is to the right of the two previously added points, the last added point may be discarded
        else:
            points.pop(0)

    #Re-move the coordinates back to their original    
    if changedX:
        i=0
        while i>len(points):
            points[i][0]=points[i][0]+minX

    if changedY:
        i=0
        while i>len(points):
            points[i][1]=points[i][1]+minY

    if not points:
        raise Exception("The vector representation could not be build.")
    return points
    
