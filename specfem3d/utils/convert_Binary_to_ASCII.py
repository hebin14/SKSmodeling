#!/usr/bin/env python
#
# reads in an Binary-format seismogram file generated by SPECFEM and outputs ASCII files for each trace
#
# the binary seismogram file should have been stored with these Par_file settings:
#   USE_BINARY_FOR_SEISMOGRAMS      = .true.
#   WRITE_SEISMOGRAMS_BY_MAIN       = .true.
#   SAVE_ALL_SEISMOS_IN_ONE_FILE    = .true.
#
"""
usage: ./convert_Binary_to_ASCII.py file_in [show]

  with
    file_in - input Binary-format file, e.g., OUTPUT_FILES/all_seismograms_d_main.bin
    show    - (optional) show stream plot
"""
from __future__ import print_function

import sys,os
import array

## numpy
import numpy as np
print("numpy version: ",np.__version__)

## obspy
try:
    import obspy
except:
    print("Failed importing obspy. Please make sure to have version >= 1.1.0 working properly.")
    sys.exit(1)
print("obspy version: ",obspy.__version__)

#############################################################################
# PARAMETERS

# sets default custom_real type
# defines float 'f' or double precision 'd' for binary values
custom_type = 'f'

#############################################################################

def read_marker(file):
    """
    reads array marker from fortran binary file
    (each time a fortran write(*)-routine call is executed, a marker at beginning and end is placed)
    """
    binlength = array.array('i')
    try:
        binlength.fromfile(file,1)
    except:
        # no more data from file available
        binlength = array.array('i',[0])

    return binlength[0]


def read_binary_file_character_array(file,got_next_name_marker):
    """
    reads character data array from file
    """

    # we might have name marker read already when reading in last trace
    if got_next_name_marker:
        # name record has 512-bytes
        binlength = 512
    else:
        # gets array length in bytes
        binlength = read_marker(file)

    # checks if anything to do
    if binlength == 0:
        return ""

    # character (1 bytes)
    num_points = int(binlength / 1)

    # debug
    if False:
        print("  array length = ",binlength," Bytes")
        print("  number of points in array = ",num_points)
        print("")

    # reads in array data
    char_values = array.array('B')  # unsigned char
    char_values.fromfile(file,num_points)

    # fortran binary file: file ends with array-size again
    # checks markers
    binlength_end = read_marker(file)
    if binlength_end != binlength:
        print("Error array markers in fortran binary file:",binlength,binlength_end)
        print("start array length = ",binlength," Bytes")
        print("final array length = ",binlength_end," Bytes")
        print("array lengths should match, please check your file")
        raise Exception('array markers invalid')

    # converts to string
    s = char_values.tobytes().decode('utf-8')
    # strip whitespace
    s = s.strip()

    return s


def read_binary_file_trace_custom_real_array(file):
    """
    reads trace data array from file
    """
    global custom_type

    # trace is written by:
    #   do isample = 1,current_seismos
    #     write(IOUT) time_t,val
    #   enddo
    #

    dat_t = np.empty((0),dtype=custom_type)
    dat_v = np.empty((0),dtype=custom_type)

    # loops over all time samples
    isample = 0
    got_next_name_marker = False

    while True:
        # gets array length in bytes
        binlength = read_marker(file)

        # checks if anything to do
        if binlength == 0:
            break

        if custom_type == 'f':
            # float (4 bytes) for single precision
            num_points = int(binlength / 4)
        else:
            # double precision
            num_points = int(binlength / 8)

        # debug
        if False:
            print("  sample: ",isample)
            print("    array length = ",binlength," Bytes")
            print("    number of points in array = ",num_points)
            print("")

        # each record must have two custom_real values
        if num_points == 2:
            # reads in array data
            binvalues = array.array(custom_type)
            binvalues.fromfile(file,num_points)

            # fortran binary file: file ends with array-size again
            # checks markers
            binlength_end = read_marker(file)
            if binlength_end != binlength:
                print("Error array markers in fortran binary file:",binlength,binlength_end)
                print("start array length = ",binlength," Bytes")
                print("final array length = ",binlength_end," Bytes")
                print("array lengths should match, please check your file")
                raise Exception('array markers invalid')

            # counter
            isample += 1

            dat_t = np.append(dat_t,binvalues[0])
            dat_v = np.append(dat_v,binvalues[1])

        elif binlength == 512:
            # name marker
            got_next_name_marker = True
            break

        else:
            print("Error: wrong number of points ",num_points," and binlength ",binlength)
            sys.exit(1)

    # returns data from list-output (first item)
    # converts into 2d array
    data_array = np.stack((dat_t,dat_v))

    return data_array,got_next_name_marker


def read_Binary_allseismos_file(filename,st):
    """
    reads binary seismograms file, e.g., all_seismograms_d_main.bin
    """

    # checks if file exists
    if not os.path.isfile(filename):
        print("file %s does not exist, please check..." % filename)
        sys.exit(1)

    # empty array
    num_receivers = 0
    num_samples = 0
    trace_ending = ""

    with open(filename,'rb') as f:
        # fortran file format:
        # the binary formatted all_seismograms_*_main.bin is written like
        # (see write_output_ASCII_or_binary.f90)
        #
        #   write(IOUT) sisname        # e.g. DB.X20.BXX.semd
        #   do isample = 1,seismo_current
        #     write( ) time_t,value
        #   enddo
        #
        #   write( ) sisname           # next trace DB.X40.BXX.semd etc...
        #   do isample ..
        #     ..
        #   enddo
        #   ..

        irec = 0
        got_next_name_marker = False

        while True:
            # reads record
            # gets name
            name = read_binary_file_character_array(f,got_next_name_marker)

            # checks if anything left to do
            if not name: break

            # gets trace data with data[0] holding time_t values, data[1] trace values
            data,got_next_name_marker = read_binary_file_trace_custom_real_array(f)

            dat_time = data[0]
            dat_val  = data[1]

            # user output
            print("found trace: {}".format(name))
            print("             min/max = {:13.5e} / {:13.5e}".format(dat_val.min(),dat_val.max()))

            # gets trace samples
            nsamp = dat_time.size

            # checks if anything left to do
            if nsamp <= 0: break

            # counter
            irec += 1

            # sets obspy trace
            # name format: DB.X20.BXX.semd
            net = name.split('.')[0]
            sta = name.split('.')[1]
            cha = name.split('.')[2]

            # semd,..
            trace_ending = name.split('.')[3]

            # start time
            trace_t0 = dat_time[0]

            # time step size
            if nsamp > 1:
                DT = dat_time[1] - dat_time[0]
            else:
                DT = 1.0

            # artificial distance to plot stream as 'section'
            dist = irec * 1.0

            # creates new trace
            tr = obspy.Trace()

            tr.stats.station = sta
            tr.stats.network = net
            tr.stats.channel = cha
            tr.stats.distance = dist
            tr.stats.delta = DT
            tr.data = dat_val

            st.append(tr)

            # check consistent length
            if irec == 1:
                num_samples = nsamp
            else:
                if nsamp != num_samples:
                    print("Error: trace has different length {} instead of {}".format(nsamp,num_samples))
                    sys.exit(1)

        # sets number of receivers
        num_receivers = irec

    # user output
    print("")
    print("number of receivers     : ",num_receivers)
    print("number of trace samples : ",num_samples)
    print("")

    return trace_t0,trace_ending


def convert_Binary_to_ASCII(file,show=False):
    # user output
    print("")
    print("converting binary seismo file to ASCII...")
    print("")
    print("input file : ",file)
    print("")

    # obspy stream
    st = obspy.Stream()

    # adds traces to stream
    trace_t0,trace_ending = read_Binary_allseismos_file(file,st)

    # output info
    print("traces:")
    print(st)
    print("")

    # takes same output directory as input file
    # for example: OUTPUT_FILES/all_seismograms_d_main.bin
    #              -> output in OUTPUT_FILES/ directory
    out_dir = os.path.dirname(file)
    if out_dir == '':
        out_dir = "./"  # -> ./ + ..
    else:
        out_dir = out_dir + "/"  # OUTPUT_FILES -> OUTPUT_FILES/ + ..

    # prints traces
    # see: https://docs.obspy.org/tutorial/code_snippets/export_seismograms_to_ascii.html
    for i,tr in enumerate(st):
        # trace name
        # format: DB.X20.BXX.semd
        name = "{}.{}.{}".format(tr.stats.network,tr.stats.station,tr.stats.channel)

        # file output
        # adds file ending, .semd ..
        filename = name + "." + trace_ending
        print(filename)

        # adds output directory
        filename = out_dir + filename

        # length
        length = len(tr.data)
        t0 = trace_t0
        dt = tr.stats.delta
        print("  length = ",length," dt = ",dt)

        # SPECFEM won't fill station and channel header infos
        # station name
        if len(tr.stats.station) > 0:
            sta = tr.stats.station
        else:
            sta = 'A' + str(i)                    # A0, A1, ..
        # channel name
        if len(tr.stats.channel) > 0:
            cha = tr.stats.channel
        else:
            # using a guess
            cha = '*'

        # file output
        f = open(filename, "w")

        # file header
        f.write("# STATION %s\n" % (sta))
        f.write("# CHANNEL %s\n" % (cha))
        f.write("# START_TIME %s\n" % (str(tr.stats.starttime)))
        f.write("# SAMP_FREQ %f\n" % (tr.stats.sampling_rate))
        f.write("# NDAT %d\n" % (tr.stats.npts))

        # data section
        # fills numpy array
        xy = np.empty(shape=(0,2))
        for ii in range(length):
            time = ii*dt + t0
            xy = np.append(xy,[[time,tr.data[ii]]],axis=0)

        # data column
        #print(xy[:,1])
        #print(xy[0,1],xy[1,1],xy[2,1],xy[3,1])

        # saves as ascii
        np.savetxt(f, xy, fmt="%f\t%f")
        f.close()

    # user output
    print("written files to directory: ",out_dir)
    print("")

    # figure output
    if show:
        st.plot(type='default',size=(1800, 900))
        # Wait for the user input to terminate the program
        input("Press any key to terminate the program")


if __name__ == "__main__":
    # gets arguments
    show = False
    # arguments
    try:
        file = sys.argv[1]
    except:
        print(__doc__)
        sys.exit(1)

    # optional arguments
    for arg in sys.argv:
        if "--help" in arg:
            print(__doc__)
            sys.exit(1)
        elif "show" in arg:
            show = True

    # main routine
    convert_Binary_to_ASCII(file,show)
