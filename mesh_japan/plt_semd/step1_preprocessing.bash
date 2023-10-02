#shell to prepare data from plotting
export SAC_DISPLAY_COPYRIGHT=0
#!/bin/bash
path=$1
mkdir -p $path
rm $path/*
cp ../OUTPUT_FILES/*.semd $path
evlo=`grep  "longorUTM" ../DATA/FORCESOLUTION | awk -F":" '{print $2}'`
evla=`grep  "latorUTM" ../DATA/FORCESOLUTION | awk -F":" '{print $2}'`
evdp=`grep  "depth" ../DATA/FORCESOLUTION | awk -F":" '{print $2}'`


iline=1
for file in `ls $path/*.BXZ.semd`;do
    prefix=`echo ${file##*/}`
    net=`echo $prefix | awk -F. '{print $1}'`
    sta=`echo $prefix | awk -F. '{print $2}'`
    stanm=`echo $net $sta |awk '{print $1"."$2}'`
    
    while read line; do
        local_stanm=`echo $line |awk '{print $2"."$1}'`
        if [ $local_stanm == $stanm ];then
            stla=`echo $line | awk '{print $3}'`
            stlo=`echo $line | awk '{print $4}'`
            stdp=`echo $line | awk '{print $5/1000}'`
            echo $local_stanm $stanm $stla $stlo $stdp
            break;
        fi
    done <../DATA/STATIONS
        cmpaz=0; cmpinc=0
        sh asc2sac $file $cmpaz $cmpinc
        #for N comp
        cmpaz=0; cmpinc=90
        sh asc2sac $path/$net.$sta.BXN.semd $cmpaz $cmpinc
        #for E comp
        cmpaz=90; cmpinc=90 
        sh asc2sac $path/$net.$sta.BXE.semd $cmpaz $cmpinc
        sac <<EOF
          r $path/$stanm.BXZ.semd.sac $path/$stanm.BXN.semd.sac $path/$stanm.BXE.semd.sac 
          CHNHDR EVLA $evla EVLO $evlo EVDP $evdp
          CHNHDR STLA $stla STLO $stlo STDP $stdp
          w $path/$stanm.BXZ.semd.sac $path/$stanm.BXN.semd.sac $path/$stanm.BXE.semd.sac
          r $path/$stanm.BXN.semd.sac $path/$stanm.BXE.semd.sac
          rotate to GCP
          w $path/$stanm.BXR.semd.sac $path/$stanm.BXT.semd.sac
          r $path/$stanm.BXZ.semd.sac
          CHNHDR KCMPNM BXZ
          w over
          r $path/$stanm.BXR.semd.sac
          CHNHDR KCMPNM BXR
          w over
          r $path/$stanm.BXT.semd.sac
          CHNHDR KCMPNM BXT
          w over
          q 
EOF
done

