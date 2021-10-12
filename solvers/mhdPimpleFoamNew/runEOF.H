// Define type of recalculation of the MF task
// 0 is to recalculate every iteration
// 1 is to use logical expression 
// 2 is to recalculate the Nth iteration (timesRecal)
// 3 is to recalculate every given time step (timeRecal)
// 4 is to calculate only at the first time

if (typeRecalculateMF == 0 || !runTime.run()) {
	Info<< "\nRun EOF as typeRecalculateMF = 0!!!\n" << endl;

	#include "calcMF.H"
	
} else if (typeRecalculateMF == 1 || !runTime.run()) {
	
	bool doElmer = logical_expr_run_EOF(maxRelDiff, U_old, U, smallU);
	if(doElmer) {
		Info<< "\nRun EOF as typeRecalculateMF = 1!!!\n" << endl;
			
		#include "calcMF.H"
		U_old = U;
	}		
} else if (typeRecalculateMF == 2 || !runTime.run()) {
	if (!(fmod(counter, timesRecal))) {
		Info<< "\nRun EOF as typeRecalculateMF = 2!!!\n" << endl;

		#include "calcMF.H"
		
	}
		counter++; 
} else if (typeRecalculateMF == 3 || !runTime.run()) {
	if (!(fmod(runTime.value(), timeRecal))) {
		Info<< "\nRun EOF as typeRecalculateMF = 3!!!\n" << endl;
		
		#include "calcMF.H"		
	}
} else {
	Info<< "\n***************************\n****Do not call EOF!!!****\n" << endl;
	Info<< "***************************\n****Do not call EOF!!!****\n" << endl;
}
	






