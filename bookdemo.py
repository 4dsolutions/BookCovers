"""
A Visual Python animation showing a "triangular page" going back and
forth between triangular book covers laid flat against the XY plane.
The page tip traces a semi-circle (not displayed but certainly computed).
As a result of two triangular "flaps" (cover and page) at some dihedral
angle, a tetrahedron is defined, actually two, one with each cover as
base, tip as opposite vertex.  Their volumes will always be the same.
The video pauses in two places (time.sleep()).  The Tetrahedron class
(imported) is designed to natively return volume in "tetravolumes"
but you can flip that switch easily to use xyz_volume instead.

Dependencies:
Python 3.x (python.org)
Visual Python (vpython.org)

First committed to Github:  Oct 27, 2013

stickworks.py (3.x version)
https://mail.python.org/pipermail/edu-sig/2013-September/010896.html

tetravolumes.py
https://mail.python.org/pipermail/edu-sig/2013-August/010872.html
(watch for / repair word-wrapping in this code -- too wide for
mailman defaults)

Video and more explanation:
http://controlroom.blogspot.com/2013/09/polyhedrons-at-play.html
"""

import time

from visual import *

from tetravolumes import Tetrahedron
from stickworks import Vector, Edge



# This module runs as "__main__" so the visual stuff kicks it off


D = 2    # diameter of unit-radius sphere
R = D/2  # radius of unit-radius sphere

scene2 = display(title = "Book Covers", background=(0, 0, 0), center=(0, 0, 0))
scene2.exit = True
scene2.fullscreen = True
scene2.forward = (0, 1, -.3)
scene2.autocenter = False
scene2.range = (2*D, 2*D, 4)
scene2.select()


lamp = local_light(pos=(0,-3,0), color=color.white)


# In this namespace, a rod with its tail at the origin is a Vector while some line
# segment floating in space with neither end at the origin is an Edge.

# So rods like C0--S1 and even the spine and axis themselves are modeled
# as Edges, not Vectors.  Edges are *defined* using two Vectors however,
# one pointing to each end.

# S0 --- S1 is the spine, two XYZ Vectors (defined in a different module named
# stickworks.  I use the Y axis, with Z considered vertical.



#S0 = Vector((0,D/2,0))
S0 = Vector((0,math.sqrt(2)/2,0))

S1 = -S0
spine = Edge(S0, S1, color = color.yellow) # spine of a book (equilateral triangular book covers)

# C0 -- C1 would be the book cover axis from cover to cover, nailed down and
# fixed.  Again, these are modeled as Vectors.  X axis is used.

# C0 = Vector((R * math.sqrt(3),0,0))
C0 = Vector((1, 0, 0))

C1 = -C0
axis = Edge(C0, C1)  # another fixed Edge

# spine to C0
S0C0 = Edge(S0,C0, color=color.orange)
S1C0 = Edge(S1,C0, color=color.orange)

# spine to C1
S0C1 = Edge(S0,C1, color=color.orange)
S1C1 = Edge(S1,C1, color=color.orange)

rhomb_length = S0C1.length # 4 edges of book covers diamond

# angles
dihedral_regular = math.degrees(math.asin( 1/sqrt(3))) * 2
print("Degrees: ", dihedral_regular)

# print(axis.length, spine.length, S0C0.length, S0C1.length, S1C0.length, S1C1.length)

class Page:
    """
    triangular page modeled by its tip oscillating
    between pages.
    """

    def __init__(self, angle=0, up=True):
        """
            :param angle:  dihedral angle to book cover C0
            :param up:     should point in +z direction
            """
        self.angle = angle  # degrees
        self.up = up
        self.tip = self._getVector()

    def delta_angle(self, degrees):
        self.angle += degrees
        self.tip = self._getVector()

    def _getVector(self):
        #The page tip's job is to make an arc using sine and cosine of the dihedral
        # angle the page is making with the flap, starting with tip at C0.
        z = math.sin(math.radians(self.angle)) * axis.length/2
        x = math.cos(math.radians(self.angle)) * axis.length/2
        if not self.up:  # mirror the above
            z = -z
            x = -x
        y = 0
        return Vector((x,y,z))

    def __repr__(self):
        return "<Page at angle {} pointing {}>".format(self.angle, "up" if self.up else "down")

def complementary(page):
    a = Edge(page.tip, S0).length
    b = Edge(page.tip, C0).length
    c = Edge(page.tip, S1).length
    d = S0C0.length
    e = S1C0.length
    f = spine.length
    t0 = Tetrahedron(a,b,c,d,e,f, pv=D)

    a = Edge(page.tip, S0).length
    b = Edge(page.tip, C1).length
    c = Edge(page.tip, S1).length
    d = S0C1.length
    e = S1C1.length
    f = spine.length
    t1 = Tetrahedron(a,b,c,d,e,f, pv=D)

    return t0, t1


def inadvertent(page):
    """
    page:  page tip at some dihedral angle

    Tetrahedron with 4 edges 2 and opposite edges
    determined by variable edges of the complementary
    tets defined by the moving page tip.

    """
    P_len = Edge(page.tip, C1).length
    Q_len = Edge(page.tip, C0).length
    QmQ0_len  = Q_len/2
    PmP1_len  = P_len/2
    # Oct 24: allowing rhomb_length other than D
    PmQ0_len  = math.sqrt(rhomb_length**2 - PmP1_len**2)
    x = math.sqrt(PmQ0_len**2 - QmQ0_len**2)
    Pm = Vector((-x/2, 0, 0))
    Qm = Vector(( x/2, 0, 0))
    P0 = Pm + Vector((0, -P_len/2, 0))
    P1 = Pm + Vector((0,  P_len/2, 0))
    Q0 = Qm + Vector((0,  0,  Q_len/2))
    Q1 = Qm + Vector((0,  0, -Q_len/2))
    return P0, P1, Q0, Q1


def draw_bookcovers():
    spine.draw()
    S0C0.draw()
    S1C0.draw()
    S0C1.draw()
    S1C1.draw()

def drawit(page):
    s=Edge(page.tip, S0, color=color.orange)
    t=Edge(page.tip, C1, color=color.magenta)
    u=Edge(page.tip, S1, color=color.orange)
    v=Edge(page.tip, C0, color=color.green)
    s.draw()
    t.draw()
    u.draw()
    v.draw()
    return s,t,u,v

def drawit2(page):
    s=Edge(page.tip, S0, color.orange)
    t=Edge(page.tip, C1, color=color.green)
    u=Edge(page.tip, S1, color.orange)
    v=Edge(page.tip, C0, color=color.magenta)
    s.draw()
    t.draw()
    u.draw()
    v.draw()
    return s,t,u,v

def drawit3(P0,P1,Q0,Q1):
    """
    draws the six edges of the inadvertent tetrahedron
    give its four vertexes as input
    """
    P0P1 = Edge(P0, P1, color=color.magenta)
    Q0Q1 = Edge(Q0, Q1, color=color.green)
    P1Q0 = Edge(P1, Q0, color=color.orange)
    P1Q1 = Edge(P1, Q1, color=color.orange)
    P0Q0 = Edge(P0, Q0, color=color.orange)
    P0Q1 = Edge(P0, Q1, color=color.orange)
    P0P1.draw()
    Q0Q1.draw()
    P1Q0.draw()
    P1Q1.draw()
    P0Q0.draw()
    P0Q1.draw()
    return P0P1, P0Q0, P0Q1, P1Q0, Q0Q1, P1Q1

def eraseit(*seq):
    for obj in seq:
        obj.erase()


def page_loop(two_pages=False):
# a loop drives the page back and forth by upping and lowering
# the degrees, of the dihedral angle.  So you'll spot where, when I'm
# close to "regular tetrahedron" (71 degree) I swap in a dihedral angle
# computed with trig -- you could say it's a still snap shot of the ideal,
# whereas the animation skips such "irrational" dihedrals.

    draw_bookcovers() # book covers lying flat

    for i in range(5):
        for t in range(181):
            a,b,c,d = drawit(page_up)
            if two_pages:
                e,f,g,h = drawit2(page_dwn)
            rate(30)
            if False: # i == 2 and t == 71:
                page = Page(dihedral_regular)
                T1, T2 = complementary(page)
                # choose T1.ivm_volume OR T1.xyz_volume
                tx =text(text="Vol = {:>6.3f}".format(T1.ivm_volume()), pos=(1, 0, 1),
                         height=0.4, depth=-0.1, up=(0,0,1), color = color.orange)
                time.sleep(4)
                tx.visible = False

            eraseit(a,b,c,d)
            page_up.delta_angle(1)
            if two_pages:
                eraseit(e,f,g,h)
                page_dwn.delta_angle(1)





        # The two stops to display volumes are programmed in.  It's not like
        # I can stop it arbitrarily and have the volume displayed, although the
        # 2nd video may give that illusion.

        for t in range(181):
            a,b,c,d = drawit(page_up)
            if two_pages:
                e,f,g,h = drawit2(page_dwn)
            rate(30)
            if i == 0 and t == 90:
                T1, T2 = complementary(page_up)
                # choose T1.ivm_volume OR T1.xyz_volume
                tx =text(text="Vol = {:>6.3f}".format(T1.ivm_volume()), pos=(1, 0, 1),
                         height=0.4, depth=-0.1, up=(0,0,1), color = color.orange)
                time.sleep(4)
                tx.visible = False

            eraseit(a,b,c,d)
            page_up.delta_angle(-1)
            if two_pages:
                eraseit(e,f,g,h)
                page_dwn.delta_angle(-1)

def inadvert_loop():
    for i in range(5):
        for t in range(181):
            if False: # i == 2 and t == 71:
                page = Page(math.degrees(dihedral_regular))
                P0,P1,Q0,Q1 = inadvertent(page)
                to_erase = drawit3(P0,P1,Q0,Q1)
                # P0P1, P0Q0, P0Q1, P1Q0, Q0Q1, P1Q1
                edge_lengths = [edge.length for edge in to_erase]
                T3 = Tetrahedron(*edge_lengths, pv=D)

                # choose T3.ivm_volume OR T3.xyz_volume
                tx =text(text="Vol = {:>6.3f}".format(T3.ivm_volume()), pos=(1, 0, 1),
                         height=0.4, depth=-0.1, up=(0,0,1), color = color.orange)
                time.sleep(4)
                tx.visible = False
            else:
                P0,P1,Q0,Q1 = inadvertent(page_up)
                to_erase = drawit3(P0,P1,Q0,Q1)

            rate(30)
            page_up.delta_angle(-1)
            eraseit(*to_erase)

        for t in range(181):
            P0,P1,Q0,Q1 = inadvertent(page_up)
            to_erase = drawit3(P0,P1,Q0,Q1)

            rate(30)
            if i == 0 and t == 90:
                edge_lengths = [edge.length for edge in to_erase]
                T3 = Tetrahedron(*edge_lengths, pv=D)
                # choose T3.ivm_volume OR T3.xyz_volume
                tx =text(text="Vol = {:>6.3f}".format(T3.ivm_volume()), pos=(1, 0, 1),
                         height=0.4, depth=-0.1, up=(0,0,1), color = color.orange)
                time.sleep(4)
                tx.visible = False

            page_up.delta_angle(-1)
            eraseit(*to_erase)

#define one or two pages
page_up = Page()
page_dwn = Page(up=False)

page_loop(two_pages=True)
inadvert_loop()

