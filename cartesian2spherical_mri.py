import numpy as np
import scipy as sp
from scipy import ndimage
import sys

from nibabel import load as load_nii, Nifti1Image

def main():
    args = sys.argv

    origin=(151,96,96)
    if len(args)<2:
        print("Usage: python cartesian2spherical.py <input nifti file> <output nifti file>")
        print("example: python cartesian2spherical.py mri_demo.nii.gz sph_mri_demo.nii.gz")
        exit(0)
    in_file = args[1]
    out_file = args[2]

    CartesianToPolar(in_file, out_file, origin)

def CartesianToPolar(in_file, out_file, origin):
    data = load_nii(in_file).get_data()
    polar_grid, r, theta, phi = reproject_image_into_polar_3D(data, origin)
    img = Nifti1Image(polar_grid, np.eye(4)) 
    img.to_filename(out_file)
                
def index_coords_3D(data, origin=None):
    """Creates x & y & z coords for the indicies in a numpy array "data".
    "origin" defaults to the center of the image. Specify origin=(0,0,0)
    to set the origin to the lower deeper and left corner of the image."""
    nx, ny, nz = data.shape[:3]
    if origin is None:
        origin_x, origin_y, origin_z = nx // 2, ny // 2, nz // 2
    else:
        origin_x, origin_y, origin_z = origin
    x, y, z = np.meshgrid(np.arange(nx), np.arange(ny), np.arange(nz))
    x -= origin_x
    y -= origin_y
    z -= origin_z
    return x, y, z

def cart2polar_3D(x, y, z):
    r = np.sqrt(x**2 + y**2 + z**2)
    theta = np.arctan2(y, x)
    phi = np.arctan2(z,np.sqrt(x**2 + y**2))
    return r, theta, phi

def polar2cart_3D(r, theta, phi): 
    x = r * np.cos(phi) * np.cos(theta)
    y = r * np.cos(phi) * np.sin(theta)
    z = r * np.sin(phi)
    return x, y, z

def reproject_image_into_polar_3D(data, origin=None):
    """Reprojects a 3D numpy array ("data") into a polar coordinate system.
    "origin" is a tuple of (x0, y0, z0) and defaults to the center of the image."""
    nx, ny, nz = data.shape[:3]
    if origin is None:
        origin = (nx//2, ny//2, nz//2)

    # Determine that the min and max r and theta coords will be...
    x, y, z = index_coords_3D(data, origin=origin)
    r, theta, phi = cart2polar_3D(x, y, z)

    # Make a regular (in polar space) grid based on the min and max r & theta & phi
    r_i = np.linspace(r.min(), r.max(), nx)
    theta_i = np.linspace(theta.min(), theta.max(), ny)
    phi_i = np.linspace(phi.min(), phi.max(), nz)
    r_grid, theta_grid, phi_grid = np.meshgrid(r_i, theta_i, phi_i)

    # Project the r and theta grid back into pixel coordinates
    xi, yi, zi = polar2cart_3D(r_grid, theta_grid, phi_grid)
    xi += origin[0] # We need to shift the origin back to 
    yi += origin[1] # back to the lower-left corner...
    zi += origin[2] # back to the deeper-left corner...
    xi, yi, zi = xi.flatten(), yi.flatten(), zi.flatten()
    coords = np.vstack((xi, yi, zi)) # (map_coordinates requires a 3xn array)

    # Reproject and the restack
    bands = []
    vi = sp.ndimage.map_coordinates(data, coords, order=1)
    bands.append(vi.reshape((nx, ny, nz)))

    output = np.dstack(bands)
    return output, r_i, theta_i, phi_i

if __name__ == '__main__':
    main()
