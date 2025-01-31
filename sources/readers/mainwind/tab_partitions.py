import psutil

from sources.readers import memory, time

mmrysize = memory()
timevalu = time()


def return_storage_counters():
    diskioqt, partlist = psutil.disk_io_counters(), psutil.disk_partitions(all=True)
    retndata = {
        "loadqant": diskioqt.read_count,
        "saveqant": diskioqt.write_count,
        "loadbyte": mmrysize.format(diskioqt.read_bytes),
        "savebyte": mmrysize.format(diskioqt.write_bytes),
        "loadtime": timevalu.format(diskioqt.read_time),
        "savetime": timevalu.format(diskioqt.write_time),
        "loadmgqt": diskioqt.read_merged_count,
        "savemgqt": diskioqt.write_merged_count,
        "partqant": len(partlist),
    }
    return retndata


def return_logical_partition_statistics():
    retnlist, partlist, partqant = (
        [],
        [
            indx
            for indx in psutil.disk_partitions(all=True)
            if indx not in psutil.disk_partitions(all=False)
        ],
        0,
    )
    for indx in partlist:
        partqant += 1
        try:
            partdiuj = psutil.disk_usage(indx.mountpoint)
            partfree, partused, partcomp, partperc = (
                partdiuj.free,
                partdiuj.used,
                partdiuj.total,
                partdiuj.percent,
            )
        except Exception:
            partfree, partused, partcomp, partperc = 0, 0, 0, 0
        partdict = {
            "lgptdevc": indx.device,
            "lgptfutl": {
                "free": mmrysize.format(partfree),
                "used": mmrysize.format(partused),
                "comp": mmrysize.format(partcomp),
                "perc": partperc,
            },
            "lgptfsys": {"mtpt": indx.mountpoint, "fsys": indx.fstype},
        }
        retnlist.append(partdict)
    return retnlist


def return_physical_partition_statistics():
    retnlist, partlist, partqant = [], psutil.disk_partitions(all=False), 0
    for indx in partlist:
        partqant += 1
        try:
            partdiuj = psutil.disk_usage(indx.mountpoint)
            partfree, partused, partcomp, partperc = (
                partdiuj.free,
                partdiuj.used,
                partdiuj.total,
                partdiuj.percent,
            )
        except Exception:
            partfree, partused, partcomp, partperc = 0, 0, 0, 0
        partdict = {
            "phptdevc": indx.device,
            "phptfutl": {
                "free": mmrysize.format(partfree),
                "used": mmrysize.format(partused),
                "comp": mmrysize.format(partcomp),
                "perc": partperc,
            },
            "phptfsys": {"mtpt": indx.mountpoint, "fsys": indx.fstype},
        }
        retnlist.append(partdict)
    return retnlist
