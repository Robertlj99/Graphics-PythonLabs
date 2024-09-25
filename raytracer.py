import json
from typing import Any

from numpy import ndarray, dtype

from myshapes import Sphere, Triangle, Plane
import numpy as np
import matplotlib.pyplot as plt

# Scene variables
# Set input directory and file here
scene_fn = "./scenes/my_scene.json"
# Set output directory here
im_out = "./images/"
fname = im_out + scene_fn.split("/")[2].split(".json")[0] + "-x.png"
# Don't change these (the universe will explode!)
resx = 256
resy = 256
# Scene Loader
def loadScene():
    with open(scene_fn) as f:
        data = json.load(f)

    spheres = []

    for sphere in data["Spheres"]:
        spheres.append(
            Sphere(sphere["Center"], sphere["Radius"],
                   sphere["Mdiff"], sphere["Mspec"], sphere["Mgls"], sphere["Refl"],
                   sphere["Kd"], sphere["Ks"], sphere["Ka"]))

    triangles = []

    for triangle in data["Triangles"]:
        triangles.append(
            Triangle(triangle["A"], triangle["B"], triangle["C"],
                     triangle["Mdiff"], triangle["Mspec"], triangle["Mgls"], triangle["Refl"],
                     triangle["Kd"], triangle["Ks"], triangle["Ka"]))

    planes = []

    for plane in data["Planes"]:
        planes.append(
            Plane(plane["Normal"], plane["Distance"],
                  plane["Mdiff"], plane["Mspec"], plane["Mgls"], plane["Refl"],
                  plane["Kd"], plane["Ks"], plane["Ka"]))

    objects = spheres + triangles + planes

    camera = {
        "LookAt": np.array(data["Camera"]["LookAt"], ),
        "LookFrom": np.array(data["Camera"]["LookFrom"]),
        "Up": np.array(data["Camera"]["Up"]),
        "FieldOfView": data["Camera"]["FieldOfView"]
    }

    light = {
        "DirectionToLight": np.array(data["Light"]["DirectionToLight"]),
        "LightColor": np.array(data["Light"]["LightColor"]),
        "AmbientLight": np.array(data["Light"]["AmbientLight"]),
        "BackgroundColor": np.array(data["Light"]["BackgroundColor"]),
    }

    return camera, light, objects

camera, light, objects = loadScene()

# Ray Tracer
# YOUR CODE HERE
# I'm making a lot of things global similar to the scene objects so I dont have to bother passing or recalculating them
# Useful global variables
mamb = light["AmbientLight"]
s = light["LightColor"]
camb = light["AmbientLight"] * light["LightColor"]
l = light["DirectionToLight"]
lhat = l / np.linalg.norm(l)
r_0 = camera["LookFrom"]
pat = camera["LookAt"]
up = camera["Up"]
fov = camera["FieldOfView"]

def generate_rays():
    # Gram-Schmidt
    e3 = (pat - r_0) / np.linalg.norm(pat - r_0)
    e1 = np.cross(e3, up) / np.linalg.norm(np.cross(e3, up))
    e2 = np.cross(e1, e3) / np.linalg.norm(np.cross(e1, e3))
    # Window calculations
    fovx, fovy = np.deg2rad(fov), np.deg2rad(fov)
    dist = np.linalg.norm(pat - r_0)
    u_max = dist * np.tan(fovx / 2)
    v_max = dist * np.tan(fovy / 2)
    u_min = -u_max
    v_min = -v_max
    # Pixel distances
    dist_u = (u_max - u_min) / (resx + 1)
    dist_v = (v_max - v_min) / (resy + 1)
    # Create empty matrix to store ray direction values
    rd_matrix = np.empty((resx, resy, 3), dtype=np.float32)
    # Populate matrix
    x_range = int(resx/2)
    y_range = int(resy/2)
    for i in range(-x_range, x_range):
        for j in range(-y_range, y_range):
            # S
            s = pat + (dist_u * (j + 0.5) * e1) + (dist_v * (i + 0.5) * e2)
            # Ray distance
            rd = (s - r_0) / np.linalg.norm(s - r_0)
            rd_matrix[i + 128][j + 128] = rd
    return rd_matrix

# I'm also making this global
rdmatrix = generate_rays()

def cast_ray(r0, rd):
    # Initialize t_min to -1
    tmin = -1
    # Boolean to set first t-min
    first = True
    # Closest object tracker
    closest = [-1]
    # Loop through[] objects in scene
    for obj in objects:
        # Get t-value
        t = obj.intersect(r0, rd)
        # Check t
        if t > 0:
            if first:
                tmin = t
                closest.append(obj)
                first = False
            elif t < tmin:
                tmin = t
                closest.append(obj)

    return tmin, closest[-1]

# Same as cast ray but it excludes the object the ray was cast from
def recast_ray(closest_obj, r0, rd):
    # Initialize t_min to -1
    tmin = -1
    # Boolean to set first t-min
    first = True
    # Closest object tracker
    closest = [-1]
    # Exclude object casting ray from object iteration
    objs = [x for x in objects if x != closest_obj]
    # Loop through rest of objects in scene
    for obj in objs:
        # Get t-value
        t = obj.intersect(r0, rd)
        # Check t
        if t > 0:
            if first:
                tmin = t
                closest.append(obj)
                first = False
            elif t < tmin:
                tmin = t
                closest.append(obj)

    return tmin, closest[-1]

# Step by step lighting
def diffuse(p, closest_obj):
    mdiff = closest_obj.getDiffuse()

    if isinstance(closest_obj, Sphere):
        n = closest_obj.getNormal(p)
    else:
        n = closest_obj.getNormal()

    nhat = n / np.linalg.norm(n)
    dot_product = np.sum(nhat * lhat)

    if dot_product < 0:
        dot_product = 0

    cdiff = (s * mdiff) * dot_product
    return cdiff, nhat

def specular(vhat, nhat, closest_obj):
    mspec = closest_obj.getSpecular()
    mgls = closest_obj.getGloss()
    rhat = 2*np.sum(lhat*nhat)*nhat - lhat
    dot_product = np.sum(vhat*rhat)
    if dot_product < 0:
        dot_product = 0

    cspec = (s*mspec)*dot_product**mgls
    return cspec

def final_color(cspec, cdiff, crefl, closest_obj):
    kd = closest_obj.getKd()
    ks = closest_obj.getKs()
    ka = closest_obj.getKa()
    kr = closest_obj.getRefl()
    return kd*cdiff + ks*cspec + ka*camb + kr*crefl

def generate_image():
    pixel_values = np.empty((resx, resy, 3), dtype=np.float32)
    i = resx - 1
    j = 0
    for row in rdmatrix:
        for r_d in row:
            t_min, closest_obj = cast_ray(r_0, r_d)
            if t_min < 0:
                pixel_values[i][j] = light["BackgroundColor"]
            else:
                p = r_0 + r_d * t_min
                t_min, temp = recast_ray(closest_obj, p, lhat)
                if t_min > 0:
                    pixel_values[i][j] = light["AmbientLight"]
                else:
                    v = -r_d
                    vhat = v / np.linalg.norm(v)
                    cdiff, nhat = diffuse(p, closest_obj)
                    cspec = specular(vhat, nhat, closest_obj)
                    rehat = 2 * np.sum(nhat*vhat) * nhat - vhat
                    t_min, temp = recast_ray(closest_obj, p, rehat)
                    if t_min > 0:
                        crefl = temp.getDiffuse()
                    else:
                        crefl = light["BackgroundColor"]
                    pixel_values[i][j] = final_color(cspec, cdiff, crefl, closest_obj)
            j = j + 1
        i = i - 1
        j = 0

    return pixel_values

if __name__ == "__main__":
    # No need to do anything here
    image = generate_image()
    plt.imsave(fname, image)
