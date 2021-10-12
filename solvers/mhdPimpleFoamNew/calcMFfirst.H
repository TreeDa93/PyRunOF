computePhasor(Jre, Jim, Jabs, Jphase); // calculate Jabs and Jphase
computePhasor(Bre, Bim, Babs, Bphase); // calculate Babs and Bphase

computeJxB(JxB_inst, Jabs, Jphase, Babs, Bphase, runTime.value(), frequency); // calculate instants Force
			
computeB(B, Babs, Bphase, runTime.value(), frequency); // calculate vecotr of B
computeJ(j, Jabs, Jphase, runTime.value(), frequency); // calculate vector of J 

computeUxBxB(UxBxB, U, Babs, Bphase, runTime.value(), frequency);


F_mot = elcond*UxBxB;
if(typeForce == 0) {
Info<< "\n***************************\n****Force is taken instaneous!!!****\n" << endl;
Info<< "***************************\n****!!!!!!****\n" << endl;
	if (typeUxBxB != 0) {
		JxB = JxB_inst;
	} else{
Info<< "\n***************************\n****Add F_mot!!!****\n" << endl;
Info<< "***************************\n****!!!!!!****\n" << endl;
		JxB = JxB_inst+F_mot;
	} 
} else {
Info<< "\n***************************\n****Force is taken average!!!****\n" << endl;
Info<< "***************************\n****!!!!!!****\n" << endl;
	if (typeUxBxB != 0) {
		JxB = JxB_avg;
	} else{
Info<< "\n***************************\n****Add F_mot!!!****\n" << endl;
Info<< "***************************\n****!!!!!!****\n" << endl;
		JxB = JxB_avg+F_mot;
	}
}
