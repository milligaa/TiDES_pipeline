#! /bin/bash

spectrum=$1
NGSF_path="/Users/andrew/Desktop/Python_Stuff/SN_and_Galaxy/NGSF-main"

echo "Running Pipeline on: $spectrum"

# get redshift from SNID
# redshift="0.069973"
snid verbose=0 inter=0 plot=0 iquery=0 rlapmin=5 wmin=4000 wmax=8500 $spectrum
redshift=$(python3 "$(pwd)"/source/get_SNID_redshift.py --snidout "$(pwd)"/*_snid.output)
rm "$(pwd)"/*_snid.output
rm "$(pwd)"/*.param

# run snid
snid verbose=0 inter=0 plot=0 iquery=0 rlapmin=5 wmin=4000 wmax=8500 forcez=$redshift $spectrum

# convert snid output into class probabilities same as Milligan+2025
# note that this code assumes the spectrum ends in .txt, easily changed to match
python3 "$(pwd)"/source/SNID_output.py --outputs "$(pwd)/" --save "$(pwd)"/config/SNID_interim.csv --spectra "$(pwd)/$spectrum"
rm "$(pwd)"/*_snid.output
rm "$(pwd)"/*.param

# dash here
python3 "$(pwd)"/source/DASH_output.py --spectrum $spectrum --redshift $redshift --output "$(pwd)"/config/
rm "$(pwd)"/DASH_matches.txt

#setup ngsf (god help us), note for now that this is set up for sg error since it is fresh NGSF install

python3 "$(pwd)"/source/create_NGSF_json.py --path "$(pwd)"/ --redshift $redshift
# had to create a folder in this folder called NGSF to store the maximum brightness csv for pathing issues (I hate NGSF)
python3 "$NGSF_path"/run.py "$(pwd)"/config/parameters.json
rm *_binned.txt
rm *.png
# now get the NGSF result
python3 "$(pwd)"/source/NGSF_output.py --csvpath "$(pwd)"/*.csv --savepath "$(pwd)"/config/NGSF_interim.csv
# clean up
rm parameters_used.json
rm *.csv

#now combine these results

python3 "$(pwd)"/source/M25_pipeline.py --configpath "$(pwd)"/config --specpath $spectrum