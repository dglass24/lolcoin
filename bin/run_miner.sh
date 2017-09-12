#!/bin/sh

SEEDHOST="0.0.0.0"
MINERHOST=`python bin/find_ip.py`
MINERPORT=5001


function usage()
{
    echo "example usage:"
    echo ""
    echo "./run_miner.sh"
    echo "\t--seedhost=$SEEDHOST"
    echo "\t--minerport=$MINERPORT"
    echo ""
}

while [ "$1" != "" ]; do
    PARAM=`echo $1 | awk -F= '{print $1}'`
    VALUE=`echo $1 | awk -F= '{print $2}'`
    case $PARAM in
        -h | --help)
            usage
            exit
            ;;
        --seedhost)
            SEEDHOST=$VALUE
            ;;
        --minerport)
            MINERPORT=$VALUE
            ;;
        *)
            echo "ERROR: unknown parameter \"$PARAM\""
            usage
            exit 1
            ;;
    esac
    shift
done


echo "SEEDHOST is $SEEDHOST";
echo "MINERPORT is $MINERPORT";

# pull latest image
docker pull dglass/lolcoin

# remove old containers
#docker rm miner

# start the container
docker run \
    --env MINERHOST=$MINERHOST \
    --env MINERPORT=$MINERPORT \
    --env SEEDHOST=$SEEDHOST \
    -p $MINERPORT:5000 \
    dglass/lolcoin python lolcoin.py