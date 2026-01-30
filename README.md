Note that in the current form this code takes, the bank of NGSF templates must be downloaded from https://www.wiserep.org/content/wiserep-getting-started#supyfit

This is a very dumb way to path this procedure, but it is what it is. I may try and change it

Code should be run from the TiDES_pipeline folder, and you probably should go into the run_pipeline.sh file and change the path to the NGSF folder if you want it to actually run. Good luck :)

!!! NOTE !!!
There are two major differences between this code and the pipeline that is presented in Milligan+2025

1. The photometric cut to find transients brighter than 21.8mag in the LSST r-band currently just checks the magnitude of the combined galaxy and transient flux. This should be fixed when incorperated into the TiDES marshall and it is known where photometric data from LSST will be

2. Currently the pipeline is using SNID to estimate the redshift. In reality we will know the redshift of some transients from galaxy surveys, or possibly from galaxy emission in the spectrum. Will need to update the code of the TiDES marshall to pull in these known redshifts in some form, or run without them