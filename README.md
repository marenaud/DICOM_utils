# DICOM utils

Python scripts to do things with DICOM files. Depends heavily on [pydicom](https://github.com/darcymason/pydicom).

Scripts include:

* A [DICOM anonymizer](https://github.com/marenaud/DICOM_utils/wiki/DICOM-Anonymizer) which will remove identifiable information from DICOM files.


# Useful DICOM fields in PyDICOM
```python
import pydicom as dicom
dicom_file = dicom.read_file('filename.dcm')

dicom_file.Rows  # Rows in the DICOM image (vertical direction)
dicom_file.Columns  # Columns in the DICOM image (horizontal direction)
dicom_file.PixelSpacing  # (x, y) pixel size in mm
dicom_file.ImagePositionPatient  # (x, y, z) coordinates of the center of the top left pixel in the image in mm.
dicom_file.GridFrameOffsetVector  # Z offsets from ImagePositionPatient of each grid slice.
dicom_file.pixel_array  # Pixel values in the image. They are often not in the right units, see below for conversion.
num_slices = len(dicom_file.GridFrameOffsetVector)
# Since GridFrameOffsetVector gives the z coordinate of every slice, the size of the array is the number of slices.
# Unlike "Rows" and "Columns", there's no DICOM field for the 3rd dimension.

dicom_file.ImageOrientationPatient  # Direction vectors for pixel coordinates.
"""
The format of ImageOrientationPatient is [x1, x2, x3, y1, y2, y3]. Typical images are [1, 0, 0, 0, 1, 0]
which indicates the x coordinate of pixels increases "to the right" and the y coordinates
increase downwards. Other common vectors are [-1, 0, 0, 0, 1, 0] for feet-first supine patients and
[-1, 0, 0, 0, -1, 0] for feet-first prone.
"""
```


# DICOM recipes

## Obtaining Houndsfield units from a CT dicom file

```python
import dicom
ct_dicom = dicom.read_file('filename.dcm')
houndsfield_units = ct_dicom.pixel_array * ct_dicom.RescaleSlope + ct_dicom.RescaleIntercept
```

## Obtaining absolute dose values from a RT Dose dicom file

```python
import dicom
dose_dicom = dicom.read_file('filename.dcm')
dose_values = dose_dicom.pixel_array * dose_dicom.DoseGridScaling
```

# LICENSE

All scripts are released under the MIT license.
