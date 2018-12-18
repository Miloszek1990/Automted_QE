#! /bin/bash

#module add tryton/mpi/intel/2017

### INPUT TEST PARAMETERS
# Test range parameters
cut_beg=50
cut_end=650
step=1

# Energy cutoff for charge density
PSI=47

# Parallel computing parameters
N_NODES=1
N_PROCE=1
GN_CPU=$[$N_NODES*$N_PROCE]
MPI_par="false"

# Functional
FUNC="pbe"
USPP="true"

# File with results name and title
TITLE="E_psi"
PREFIX="Si"

rm $TITLE"_RESULTS_rho_phys.txt"
rm $TITLE"_RESULTS_rho_comp.txt"
RESULTS_1=$TITLE"_RESULTS_rho_phys.txt"
RESULTS_2=$TITLE"_RESULTS_rho_comp.txt"

# Put pseudo directory and output directory
cd `echo $0 | sed 's/\(.*\)\/.*/\1/'` # extract pathname
PSEUDO_DIR="../pseudo"
OUTPUT_DIR="./out"
WORKING_DIR=`pwd`
ESPRESSO_DIR="/home/foton/QE/qe-6.1/bin/pw.x"

### PRINT AND CHECK TEST PARAMETERS
OUTPUT_FILES_DIR="./"ouputfiles_"$TITLE"
mkdir $OUTPUT_FILES_DIR
echo "Work directory is:                "$(readlink -f "$WORKING_DIR")
echo "Pseudo directory is:              "$PSEUDO_DIR
echo "Output directory is:              "$OUTPUT_DIR
echo "Output files will be stored in:   "$OUTPUT_FILES_DIR

### PREPARE SET OF CUTOFF ENERGIES FOR WAVEFUNCTIONS
let range=psi_cut_end-psi_cut_beg
CUT=$(seq $cut_beg $step $cut_end)	
echo $range" SCF calculations for yours system will be done."
echo "Test starts at "$cut_beg" Ry and ends at "$cut_end" Ry, with "$step" Ry sampling."
if [ "$USPP" = "true" ]
then
	echo "We are using USPP so we shoud set E_rho = 12*E_psi or even more"
else
	echo "We are not using USPP so we can set E_rho = 4*E_psi or more"
fi

### FIT THE INITIAL KINETIC ENERGY CUTOFF ENRGY TO THE E_psi
if [ "$USPP" = "true" ]
then
	RHO=$[$PSI*12]
else
	RHO=$[$PSI*4]
fi

echo
echo
echo "!!!CALCULATIONS STARTS!!!"
echo
echo

for i in $CUT; 
do

### MAKE TEMPORARY FILE NAME
TITLE_TMP=$TITLE"_"$cut_beg"-"$i"-"$cut_end"_"$FUNC

### IMPORT QE INPUT FILE AND CHANGE ITS PARAMETERS
cat > $TITLE_TMP".in" << EOF

&control
    calculation     = "scf"
    title           = "$TITLE_TMP",
    restart_mode    = "from_scratch",
    pseudo_dir      = "$PSEUDO_DIR",
    outdir          = "$OUTPUT_DIR",
    prefix          = "$PREFIX",
    wf_collect      = .true.
/
&system
    ibrav           = 2,
    celldm(1)       = 10.263048,
    nat             = 2,
    ntyp            = 1,
    nbnd            = 30,
    ecutwfc         = $PSI , 
    ecutrho         = $i ,
    input_dft       = "$FUNC" ,
    nosym           =.false.
    noinv           =.false.
/
&electrons
    diagonalization = 'david'
    mixing_mode     = 'plain'
    mixing_beta     = 0.7
    conv_thr        = 1.0d-10
/
ATOMIC_SPECIES
Si  28.08  Si.pbe-n-kjpaw_psl.1.0.0.UPF
ATOMIC_POSITIONS
Si 0.00 0.00 0.00
Si 0.25 0.25 0.25
K_POINTS {gamma}

EOF

cp $TITLE_TMP".in" input_tmp.in

echo $TITLE_TMP" calculation for ecutwfc = "$i" just started, please wait."

### CHECK THE PARALLELIZATION AND RUN THE CALCULATIONS
if [ "$MPI_par" = "false" ]
then
	$ESPRESSO_DIR < $TITLE_TMP".in" > $TITLE_TMP".out"
else
	mpirun -np $N_CPU $ESPRESSO_DIR -nt $N_NODES < $TITLE_TMP".in" > $TITLE_TMP".out"
fi

### EXTRACT THE MOST IMPORTANT DATA TO THE EXTERNAL FILE
### COULD DEPENDS ON THE VERSION!
### QUITE INDIVIDUAL GREP PART...

# OUT FILE 1 - Physical data
# KINETIC ENERGY CUTOFF FOR WAVEFUNCTION AND CHARGE DENSITY [Ry]
LINE_1=$i" "$RHO" "

# TOTAL ENERGY [Ry]
GREP_TOTAL_ENERGY=$(grep "!" $TITLE_TMP".out")
set -- $GREP_TOTAL_ENERGY
LINE_1=$LINE_1" "$5 # energy is 5th word

# HOMO AND LUMO ENERGY [eV]
HOMO_LUMO=$(grep "highest" $TITLE_TMP".out")
set -- $HOMO_LUMO
LINE_1=$LINE_1" "$7" "$8 # HOMO and LUMO are 5 and 6 word

# BAND GAP [eV]
LINE_1=$LINE_1" "$(bc <<< "$8-$7")

echo -e $LINE_1
echo -e $LINE_1 >> $RESULTS_1

# OUT FILE 2 - computational data 
# TIME [s]
CPU_TIME=$(grep "PWSCF" $TITLE_TMP".out" | tail -1)
LINE_2=$CPU_TIME

echo -e $LINE_2
echo -e $LINE_2 >> $RESULTS_2

### COPY OUTPUTS TO THE 
cp $TITLE_TMP".out" $OUTPUT_FILES_DIR"/"$TITLE_TMP".out"

### REMOVE TEMPORARY FILES
rm $TITLE_TMP".in"
rm $TITLE_TMP".out"

echo
done

echo
echo "!!!CALCULATIONS ENDS!!!"
echo
echo

### REMOVE REST OF TEMPORARY FILES
rm input_tmp.in
rm -r out
