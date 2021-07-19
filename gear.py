import matplotlib.pyplot as plt
import math
import numpy as np

def arc(r, t1, t2): 
    coords = np.array([[], []])
    for t in np.arange(t1, t2, 0.001):
        coords = np.append(coords, [[r * math.cos(t)], [r * math.sin(t)]], axis=1)
    return coords
def rot_matrix(t):
    return [[math.cos(t), -math.sin(t)], [math.sin(t), math.cos(t)]]
def radial_line(t, r1, r2): 
    return [[r1 * math.cos(t), r2 * math.cos(t)], [r1 * math.sin(t), r2 * math.sin(t)]]

N = int(input("Number of teeth"))
p = float(input("Enter pressure angle in degree"))
m = float(input("Enter module"))


tooth_length_base = float(input("Enter tooth length base"))
p = p * math.pi / 180
r_p = m * N / 2
r_b = r_p * math.cos(p)
r_d = r_p - 1.25 * m
r_a = r_p + m
tooth = tooth_length_base / r_b  
right_side = np.array([[], []])
left_side = np.array([[], []])
gear_coords = np.array([[], []])
tooth_coords = np.array([[], []])

# Construction of involute curve
t = 0
while True:  # Right side of tooth
    x = r_b * (math.cos(t) + t * math.sin(t))
    y = r_b * (math.sin(t) - t * math.cos(t))
    if (r_d*r_d <= x*x + y*y <= r_a*r_a):
        right_side = np.append(right_side, [[x], [y]], axis=1)
    elif (x*x + y*y > r_a*r_a):
        t1 = math.atan(y / x)
        break
    t += 0.001

left_side = np.flip(np.dot(rot_matrix(tooth), [right_side[0], right_side[1] * -1]), 1)    


# Construction of tooth profile
if r_d < r_b:
    tooth_coords = radial_line(0, r_d, r_b)  # line connecting dedentum circle and involute curve

tooth_coords = np.concatenate((tooth_coords, right_side, arc(r_a, t1, tooth - t1), left_side), axis=1)  # Tooth

if r_d < r_b:
    tooth_coords = np.concatenate((tooth_coords, radial_line(tooth, r_d, r_b)),
                                  axis=1)  # line connecting dedentum circle and involute curve

tooth_coords = np.concatenate((tooth_coords, arc(r_d, tooth, 2*math.pi/N)), axis=1)  # Dedendum arc



for j in range(N):
    t = j * 2 * math.pi / N
    gear_coords = np.concatenate((gear_coords, np.dot(rot_matrix(t), tooth_coords)), axis=1)


plt.plot(gear_coords[0], gear_coords[1])
plt.show()
