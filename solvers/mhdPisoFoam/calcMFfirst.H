computePhasor(Jre, Jim, Jabs, Jphase); // calculate Jabs and Jphase
computePhasor(Bre, Bim, Babs, Bphase); // calculate Babs and Bphase

computeJxB(JxB_inst, Jabs, Jphase, Babs, Bphase, runTime.value(), frequency); // calculate instants Force
			
computeB(B, Babs, Bphase, runTime.value(), frequency); // calculate vecotr of B
computeJ(j, Jabs, Jphase, runTime.value(), frequency); // calculate vector of J 

computeUxBxB(UxBxB, U, Babs, Bphase, runTime.value(), frequency);

F_mot = elcond*UxBxB;

if(typeForce == 0) {
	JxB = JxB_inst;
} else {
	JxB = JxB_avg;
}
if (typeUxBxB == 0) { 
	JxB += F_mot;
}