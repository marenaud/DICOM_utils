import dicom
import glob
import os
import random

def anonymize_dicom(dicomfile, new_patient_name="Anonymous", verbose=True):
    times = ["RTPlanTime", "ReviewTime", "StudyTime"]
    dates = ["RTPlanDate", "ReviewDate", "StudyDate", "PatientBirthDate"]

    # Not guaranteed to be unique, but they're not UIDs so it shouldn't matter.
    new_patientID = "ANON" + str(random.randint(0, 1000000))
    new_studyID = "ANON" + str(random.randint(0, 1000000))

    if verbose:
        print "Anonymizing %s" % dicomfile

    df = dicom.read_file(dicomfile)
    if "PatientName" in df:
        df.PatientName = new_patient_name
    if "PatientID" in df:
        df.PatientID = new_patientID
    if "StudyID" in df:
        df.StudyID = new_studyID
    if "ReviewerName" in df:
        df.ReviewerName = "ANON"

    for date in dates:
        if date in df:
            setattr(df, date, "19000101")

    for time in times:
        if time in df:
            setattr(df, time, "111111")

    df.save_as(dicomfile)


def anonymize_folder(folder, new_patient_name="Anonymous"):
    """
        Anonymizes all dicom files inside a given folder. By default,
        the patient name attribute is replaced by "Anonymous" but an
        alternative name can be provided as an argument to the function.

        NOTE: Assumes all files in the folder belong to the same patient.

        Currently, the following DICOM fields are mangled:
        RTPlanTime, ReviewTime, StudyTime, RTPlanDate, ReviewDate, StudyDate,
        PatientBirthDate, PatientName, PatientID, StudyID, ReviewerName.
    """

    files = glob.glob(os.path.join(folder, "*.dcm"))

    for dicomfile in files:
        anonymize_dicom(dicomfile, new_patient_name)

def main():
    import argparse
    parser = argparse.ArgumentParser(description="DICOM anonymizer.")
    parser.add_argument("folder", help="the patient folder containing DICOM files to anonymize")
    parser.add_argument("-n", "--name", help="the new patient name")

    args = parser.parse_args()
    if args.name:
        anonymize_folder(args.folder, args.name)
    else:
        anonymize_folder(args.folder)

if __name__ == "__main__":
    main()