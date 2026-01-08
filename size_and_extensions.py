
import os

def get_datasize_and_extensions(paths_list):
    # The function sums the sizes of all the files in a data folder. It returns two strings: the size (including the
    # unit) and the extensions.
    # The argument has to be a list of paths for all the files in the folder.
    # todo: maybe add the possibility to process also files in subfolders?
    sizes_sum = 0
    file_extensions = ""
    for singlefile in paths_list:
        singlesize = os.path.getsize(singlefile)  # in bytes
        sizes_sum += singlesize
        current_extension = singlefile.split(".")[-1]
        if current_extension not in file_extensions:
            #file_extensions.append(current_extension)
            file_extensions += current_extension + ", "
    #print("bytes", sizes_sum)
    if sizes_sum > 1024**3:
        sizestr =  f"{sizes_sum / 1024**3:.1f} GiB"
    elif sizes_sum > 1024**2:
        sizestr = f"{sizes_sum / 1024**2:.1f} MiB"
    elif sizes_sum > 1024:
        sizestr = f"{sizes_sum / 1024:.1f} KiB"
    else:
        sizestr = f"{sizes_sum} Bytes"
    return sizestr, file_extensions[:-2]  # -2 to remove the last comma and space
