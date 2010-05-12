import random, math

class Mover(object):
    """ A renderable object with a location, color, and movement method. """
    def __init__(self, grid, location, color):
        self.grid = grid
        self.node = grid.get_node_at(location)
        self.color = color
    
    def move(self):
        pass

    def get_location(self):
        return self.node.get_location()

    def render(self, area, surface):
        surface.fill(self.color, area)

    def get_distance(self, loc1, loc2):
        """ Returns the distance between 2 locations. """

        distance = math.sqrt((loc1[0]-loc2[0])**2 + (loc1[1]-loc2[1])**2 +
                        (loc1[2]-loc2[2])**2)
        return distance

    def hide(self, mynode, neighbors, seekers):
        """ Finds node furthest from closest seeker. """
        if len(seekers) == 0:
            return mynode

        # find nearest seeker
        closestseeker = seekers[0]
        shortestsofar = self.get_distance(mynode.get_location(), 
                                             closestseeker.get_location())

        for seeker in seekers:
            currentdistance = self.get_distance(mynode.get_location(), 
                                                seeker.get_location())
            if currentdistance < shortestsofar:
                shortestsofar = currentdistance
                closestseeker = seeker


        # find escape square
        furthestsofar = self.get_distance(mynode.get_location(), 
                                          closestseeker.get_location())
        furthestescapes = [mynode]

        for n in neighbors:
            currentdistance = self.get_distance(n.get_location(),
                                                closestseeker.get_location())
            if currentdistance > furthestsofar:
                furthestsofar = currentdistance
                furthestescapes = [n]
            elif currentdistance == furthestsofar:
                furthestescapes.append(n)

        return random.choice(furthestescapes)

    def seek(self, mynode, neighbors, hiders):
        """ Finds node closest to closest hider. """
        if len(hiders) == 0:
            return mynode

        # find nearest hider
        closesthider = hiders[0]
        shortestsofar = self.get_distance(mynode.get_location(), 
                                          closesthider.get_location())

        for hider in hiders:
            currentdistance = self.get_distance(mynode.get_location(), 
                                                hider.get_location())
            if currentdistance < shortestsofar:
                shortestsofar = currentdistance
                closesthider = hider


        # find chase node
        nearestsofar = self.get_distance(mynode.get_location(), 
                                         closesthider.get_location())
        chasenodes = [mynode]

        for n in neighbors:
            currentdistance = self.get_distance(n.get_location(),
                                                closesthider.get_location())
            if currentdistance < nearestsofar:
                nearestsofar = currentdistance
                chasenodes = [n]
            elif currentdistance == nearestsofar:
                chasenodes.append(n)

        return random.choice(chasenodes)
        

class RandomMover(Mover):
    """ A mover that moves randomly between adjacent nodes."""
    def __init__(self, grid, location, color=(255, 0, 0)):
        Mover.__init__(self, grid, location, color)

    def move(self):
        neighbors = self.grid.neighbors(self.node)
        self.node = random.choice(neighbors)

class Hider(Mover):
    """ A mover that runs from the nearest seeker.  They're yellow
        because they're yellow. """
    def __init__(self, grid, location, color=(255, 255, 0)):
        Mover.__init__(self, grid, location, color)

    def move(self, movers):
        neighbors = self.grid.neighbors(self.node)
        
        seekers = []
        for m in movers:
            if isinstance(m, Seeker):
                seekers.append(m)
            
        self.node = self.hide(self.node, neighbors, seekers)


class Seeker(Mover):
    """ A mover that runs toward the nearest hider. """
    def __init__(self, grid, location, color=(255, 255, 255)):
        Mover.__init__(self, grid, location, color)

    def move(self, movers):
        neighbors = self.grid.neighbors(self.node)
        
        hiders = []
        for m in movers:
            if isinstance(m, Hider):
                hiders.append(m)
            
        self.node = self.seek(self.node, neighbors, hiders)








        
