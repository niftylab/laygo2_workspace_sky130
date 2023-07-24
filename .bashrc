#! /bin/sh

#  Licensing
#source /tools/commercial/flexlm/flexlm.cshrc
#
#setenv LORENTZ_LICENSE_FILE 27017@sunv20z-1.eecs.berkeley.edu
#setenv RLM_LICENSE 5053@sunv40z-1.eecs.berkeley.edu

# Cadence Settings
#setenv SPECTRE_DEFAULTS -E
#setenv CDS_Netlisting_Mode "Analog"
#setenv CDS_AUTO_64BIT ALL


# Setup Additional Tools
#setenv SPECTRE      /tools/cadence/SPECTRE/SPECTRE191
#setenv MMSIM_HOME   /tools/cadence/MMSIM/MMSIM151
#setenv CDS_INST_DIR /tools/cadence/IC/IC617
#setenv CDSHOME      $CDS_INST_DIR


#set path = ( ${SPECTRE}/bin \
#    ${MMSIM_HOME}/tools/bin \
#    ${CDS_INST_DIR}/tools/bin \
#    ${CDS_INST_DIR}/tools/dfII/bin \
#    ${CDS_INST_DIR}/tools/plot/bin \
#    $path \
#    )
#export TSMC_CAL_DFM_PATH="/TECH/tsmc/CLN45GS/TECH_LIB/PDK/current/Calibre/rcx/DFM"
#export PATH=$TSMC_CAL_DFM_PATH:$PATH
### Setup BAG
source .bashrc_bag

# >>> conda initialize >>>
# !! Contents within this block are managed by 'conda init' !!
__conda_setup="$('/usr/anaconda3/bin/conda' 'shell.bash' 'hook' 2> /dev/null)"
if [ $? -eq 0 ]; then
    eval "$__conda_setup"
else
    if [ -f "/usr/anaconda3/etc/profile.d/conda.sh" ]; then
        . "/usr/anaconda3/etc/profile.d/conda.sh"
    else
        export PATH="/usr/anaconda3/bin:$PATH"
    fi
fi
unset __conda_setup
# <<< conda initialize <<<
