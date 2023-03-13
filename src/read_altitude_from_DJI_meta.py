# Script read RelativeAltitude information from DJI meta data for all the cameras in the active chunk
# and loads it to the Reference pane instead of the existing data.
#
# This is python script for Metashape Pro. Scripts repository: https://github.com/agisoft-llc/metashape-scripts

import Metashape

# Checking compatibility
compatible_major_version = "2.0"
found_major_version = ".".join(Metashape.app.version.split('.')[:2])
if found_major_version != compatible_major_version:
    raise Exception("Incompatible Metashape version: {} != {}".format(found_major_version, compatible_major_version))


def read_DJI_relative_altitude():
    """
    Reads DJI/RelativeAltitude information from the image meta-date and writes it to the Reference pane
    """

    doc = Metashape.app.document
    if not len(doc.chunks):
        raise Exception("No chunks!")

    print("Script started...")
    chunk = doc.chunk

    for camera in chunk.cameras:
        if not camera.type == Metashape.Camera.Type.Regular: #skip camera track, if any
            continue
        if (not camera.reference.location):
            continue
        if ("DJI/RelativeAltitude" in camera.photo.meta.keys()) and camera.reference.location:
            z = float(camera.photo.meta["DJI/RelativeAltitude"])
            camera.reference.location = (camera.reference.location.x, camera.reference.location.y, z)

    print("Script finished!")


label = "Scripts/Read RelativeAltitude from DJI metadata"
Metashape.app.addMenuItem(label, read_DJI_relative_altitude)
print("To execute this script press {}".format(label))
