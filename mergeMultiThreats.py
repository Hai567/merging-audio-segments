from pydub import AudioSegment
import glob
import concurrent.futures
from tqdm import tqdm
import numpy as np

def merge(index, folderContainsFiles, audioExtension, outputExtension, audioArray, pbar):
    mergedAudio = AudioSegment.empty()
    for currentAudioFile in audioArray:
        currentAudio = AudioSegment.from_file(currentAudioFile, format=audioExtension)
        mergedAudio += currentAudio
        pbar.update()
    output_filename = f"{folderContainsFiles}/output{index}.{outputExtension}"
    file_handle = mergedAudio.export(output_filename, format=outputExtension)

def createSmallerArraysOfAudioFiles(arr, numberOfSmallerArrays):
    smaller_arrays = np.array_split(arr, numberOfSmallerArrays)
    result = [sub_array.tolist() for sub_array in smaller_arrays]
    return result

def mergeAudioFiles(folderContainsFiles, audioExtension, outputExtension, numberOfSmallerArrays=10):
    folderContainsFiles = folderContainsFiles.rstrip("/")
    audioExtension = audioExtension.lstrip(".")
    outputExtension = outputExtension.lstrip(".")
    
    audioPath = f"{folderContainsFiles}/*.{audioExtension}"
    audioFilesInFolder = sorted(glob.glob(audioPath))
    audioFilesInFolder.sort(key=lambda f: int(''.join(filter(str.isdigit, f))))
    totalNumberOfAudioFiles = len(audioFilesInFolder)

    smallerArrayChunksOfAudioFiles = createSmallerArraysOfAudioFiles(audioFilesInFolder, numberOfSmallerArrays)

    # Use tqdm to create a progress bar
    with tqdm(total=totalNumberOfAudioFiles) as pbar:

        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = [executor.submit(merge, i, folderContainsFiles, audioExtension, outputExtension, audioArray, pbar) for i, audioArray in enumerate(smallerArrayChunksOfAudioFiles)]
        print("Done!")

