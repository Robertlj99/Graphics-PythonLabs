import numpy as np


#Changing coordinate spaces
def world2camera(theta, x, y, z, cx, cy, cz):

    theta = -np.deg2rad(theta)
    v = np.array([[x],
                  [y],
                  [z],
                  [1]])

    R = np.array([[np.cos(theta), -np.sin(theta), 0, 0],
                   [np.sin(theta), np.cos(theta), 0, 0],
                   [0, 0, 1, 0],
                   [0, 0, 0, 1]])

    Rz = np.array([[np.cos(-camera.r), -np.sin(-camera.r), 0, 0],
                   [np.sin(-camera.r), np.cos(-camera.r), 0, 0],
                   [0, 0, 1, 0],
                   [0, 0, 0, 1]])

    Ry = np.array([[np.cos(-camera)]])

    T = np.array([[1, 0, 0, -cx],
                  [0, 1, 0, -cy],
                  [0, 0, 1, -cz],
                  [0, 0, 0, 1]])

    print(R@T@v)


def obj2world(theta, x, y, z, tx, ty, tz):

    theta = np.deg2rad(theta)
    v = np.array([[x],
                  [y],
                  [z],
                  [1]])

    Ryt = np.array([[np.cos(theta), 0, np.sin(theta), tx],
                    [0, 1, 0, ty],
                    [-np.sin(theta), 0, np.cos(theta), tz],
                    [0, 0, 0, 1]])

    print(Ryt@v)


#Projection
def project2(far, near, fov_x, fov_y, v):

    fov_x = np.deg2rad(fov_x)
    fov_y = np.deg2rad(fov_y)

    zoom_x = 1/np.tan(fov_x/2)
    zoom_y = 1/np.tan(fov_y/2)

    clip_matrix = np.array([[zoom_x, 0, 0, 0],
                        [0, zoom_y, 0, 0],
                        [0, 0, 1, (far+near)/(far-near), (-2*near*far)/(far-near)],
                        [0, 0, 1, 0]])

    p = clip_matrix@v
    w = p[3]  # Homogenous value
    pn = p/w
    print(pn)


def to_screen(height, width, v):
    S = np.array([[width/2, 0, width/2],
                  [0, -height/2, height/2],
                  [0, 0, 1]])

    print(S@v)

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


if __name__ == '__main__':
    pt = np.array([[3],
                   [5],
                   [-2],
                   [1]])

    w = pt[3]
    pn = pt / w
    S = np.array([[1920 / 2, 0, 0, 1920 / 2],
                  [0, -1080 / 2, 0, 1080 / 2],
                  [0, 0, 1, 0],
                  [0, 0, 0, 1]])

    pns = S @ pn
    x = Point(pns[0][0].item(), pns[1][0].item())
    print(x.x)
    print(x.y)