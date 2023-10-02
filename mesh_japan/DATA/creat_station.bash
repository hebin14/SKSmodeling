stfile=../model/topo_japan/station.dat
nstat=`cat $stfile |wc -l`
echo 'num of stations:',$nstat

:>station
for istat in `seq 2 $nstat`;do
  line=`cat $stfile |sed -n "${istat}p"` # loop over all virtual evts
  station=`echo $line | awk '{print $1}'`
  stnw=`echo $station | awk -F. '{print $1}'`
  stnm=`echo $station | awk -F. '{print $2}'`
  stla=`echo $line | awk '{print $2}'`
  stlo=`echo $line | awk '{print $3}'`
  stdp=`echo $line | awk '{print $4}'`
  echo $stla $stlo
  echo $stnw $stnm $stla $stlo $stdp | awk '{print $1, $2, $3, $4, $5, 0}' >>station
done <$stfile
