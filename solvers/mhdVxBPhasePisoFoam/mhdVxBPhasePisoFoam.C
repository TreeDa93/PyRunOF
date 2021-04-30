/*---------------------------------------------------------------------------*\
  =========                 |
  \\      /  F ield         | OpenFOAM: The Open Source CFD Toolbox
   \\    /   O peration     | Website:  https://openfoam.org
    \\  /    A nd           | Copyright (C) 2011-2018 OpenFOAM Foundation
     \\/     M anipulation  |
-------------------------------------------------------------------------------
License
    This file is part of OpenFOAM.

    OpenFOAM is free software: you can redistribute it and/or modify it
    under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    OpenFOAM is distributed in the hope that it will be useful, but WITHOUT
    ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
    FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License
    for more details.

    You should have received a copy of the GNU General Public License
    along with OpenFOAM.  If not, see <http://www.gnu.org/licenses/>.

Application
    pisoFoam

Description
    Transient solver for incompressible, turbulent flow, using the PISO
    algorithm.

    Sub-models include:
    - turbulence modelling, i.e. laminar, RAS or LES
    - run-time selectable MRF and finite volume options, e.g. explicit porosity

\*---------------------------------------------------------------------------*/

#include "fvCFD.H"
#include "singlePhaseTransportModel.H"
#include "turbulentTransportModel.H"
#include "pisoControl.H"
#include "fvOptions.H"
#include "Elmer.H"


void computePhasor(volVectorField& re, volVectorField& im,
                   volVectorField& abs, volVectorField& phase)
{
    forAll(abs,fieldI) 
    {
        abs[fieldI].x() = Foam::sqrt(re[fieldI].x()*re[fieldI].x()+im[fieldI].x()*im[fieldI].x());
        abs[fieldI].y() = Foam::sqrt(re[fieldI].y()*re[fieldI].y()+im[fieldI].y()*im[fieldI].y());
        abs[fieldI].z() = Foam::sqrt(re[fieldI].z()*re[fieldI].z()+im[fieldI].z()*im[fieldI].z());
    }

    forAll(phase,fieldI) 
    {
        phase[fieldI].x() = Foam::atan2(im[fieldI].x(), re[fieldI].x());
        phase[fieldI].y() = Foam::atan2(im[fieldI].y(), re[fieldI].y());
        phase[fieldI].z() = Foam::atan2(im[fieldI].z(), re[fieldI].z());
    }
}

// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //

void computeJxB(volVectorField& JxB, volVectorField& Jabs, volVectorField& Jphase,
                volVectorField& Babs, volVectorField& Bphase, scalar& time,
                dimensionedScalar frequency)
{
    scalar timePhase = 2*Foam::constant::mathematical::pi*frequency.value()*time;

    forAll(JxB,fieldI) 
    {
        JxB[fieldI].x() = Jabs[fieldI].y()*Foam::cos(Jphase[fieldI].y()+timePhase)
                        * Babs[fieldI].z()*Foam::cos(Bphase[fieldI].z()+timePhase)
                        - Jabs[fieldI].z()*Foam::cos(Jphase[fieldI].z()+timePhase)
                        * Babs[fieldI].y()*Foam::cos(Bphase[fieldI].y()+timePhase);

        JxB[fieldI].y() = Jabs[fieldI].z()*Foam::cos(Jphase[fieldI].z()+timePhase)
                        * Babs[fieldI].x()*Foam::cos(Bphase[fieldI].x()+timePhase)
                        - Jabs[fieldI].x()*Foam::cos(Jphase[fieldI].x()+timePhase)
                        * Babs[fieldI].z()*Foam::cos(Bphase[fieldI].z()+timePhase);

        JxB[fieldI].z() = Jabs[fieldI].x()*Foam::cos(Jphase[fieldI].x()+timePhase)
                        * Babs[fieldI].y()*Foam::cos(Bphase[fieldI].y()+timePhase)
                        - Jabs[fieldI].y()*Foam::cos(Jphase[fieldI].y()+timePhase)
                        * Babs[fieldI].x()*Foam::cos(Bphase[fieldI].x()+timePhase);
    }
}

// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //

void computeUxBxB(volVectorField& UxBxB, volVectorField& U, volVectorField& Babs,
                  volVectorField& Bphase, scalar& time, dimensionedScalar frequency)
{
    scalar timePhase = 2*Foam::constant::mathematical::pi*frequency.value()*time;


    forAll(UxBxB,fieldI) 
    {
        scalar Bx = Babs[fieldI].x()*Foam::cos(Bphase[fieldI].x()+timePhase);
        scalar By = Babs[fieldI].y()*Foam::cos(Bphase[fieldI].y()+timePhase);
        scalar Bz = Babs[fieldI].z()*Foam::cos(Bphase[fieldI].z()+timePhase);

        UxBxB[fieldI].x() = By*(Bx*U[fieldI].y()-By*U[fieldI].x())
                          + Bz*(Bx*U[fieldI].z()-Bz*U[fieldI].x());

        UxBxB[fieldI].y() = Bx*(By*U[fieldI].x()-Bx*U[fieldI].y())
                          + Bz*(By*U[fieldI].z()-Bz*U[fieldI].y());

        UxBxB[fieldI].z() = Bx*(Bz*U[fieldI].x()-Bx*U[fieldI].z())
                          + By*(Bz*U[fieldI].y()-By*U[fieldI].z());
    }
}


void computeB(volVectorField& B, volVectorField& Babs, volVectorField& Bphase, scalar& time, dimensionedScalar frequency)
{
    scalar timePhase = 2*Foam::constant::mathematical::pi*frequency.value()*time;

    forAll(B,fieldI) 
    {
        B[fieldI].x() = Babs[fieldI].x()*Foam::cos(Bphase[fieldI].x()+timePhase);
        B[fieldI].y() = Babs[fieldI].y()*Foam::cos(Bphase[fieldI].y()+timePhase);
        B[fieldI].z() = Babs[fieldI].z()*Foam::cos(Bphase[fieldI].z()+timePhase);
    }
}

void computeJ(volVectorField& j, volVectorField& Jabs, volVectorField& Jphase, scalar& time, dimensionedScalar frequency)
{
    scalar timePhase = 2*Foam::constant::mathematical::pi*frequency.value()*time;

    forAll(j,fieldI) 
    {
        j[fieldI].x() = Jabs[fieldI].x()*Foam::cos(Jphase[fieldI].x()+timePhase);
        j[fieldI].y() = Jabs[fieldI].y()*Foam::cos(Jphase[fieldI].y()+timePhase);
        j[fieldI].z() = Jabs[fieldI].z()*Foam::cos(Jphase[fieldI].z()+timePhase);
    }
}

int main(int argc, char *argv[])
{
    #include "postProcess.H"

    #include "setRootCaseLists.H"
    #include "createTime.H"
    #include "createMesh.H"
    #include "createControl.H"
	#include "createTimeControls.H"
    #include "createFields.H"
    #include "initContinuityErrs.H"

    turbulence->validate();

    // * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //

   Info<< "\nStarting time loop\n" << endl;

    elcond = elcond_melt;

    // Send fields to Elmer
    Elmer<fvMesh> sending(mesh,1); // 1=send, -1=receive
    sending.sendStatus(1); // 1=ok, 0=lastIter, -1=error
    sending.sendScalar(elcond);

    if(sendVelocity > 0.001)
	sending.sendVector(U);

    // Receive fields from Elmer
    Elmer<fvMesh> receiving(mesh,-1); // 1=send, -1=receive
    receiving.sendStatus(1); // 1=ok, 0=lastIter, -1=error
    receiving.recvVector(Jre);
    receiving.recvVector(Jim);
    receiving.recvVector(Bre);
    receiving.recvVector(Bim);

    computePhasor(Jre, Jim, Jabs, Jphase);
    computePhasor(Bre, Bim, Babs, Bphase);

    while (runTime.loop())
    {
        Info<< "Time = " << runTime.timeName() << nl << endl;

        
		#include "CourantNo.H"
		
		computeJxB(JxB, Jabs, Jphase, Babs, Bphase, runTime.value(), frequency);
        computeUxBxB(UxBxB, U, Babs, Bphase, runTime.value(), frequency);
		computeB(B, Babs, Bphase, runTime.value(), frequency);
		computeJ(j, Jabs, Jphase, runTime.value(), frequency);

        if(sendVelocity < 0.001) JxB += elcond*UxBxB;
        // Pressure-velocity PISO corrector
        {
            #include "UEqn.H"

            // --- PISO loop
            while (piso.correct())
            {
                #include "pEqn.H"
            }
        }

        laminarTransport.correct();
        turbulence->correct();

        runTime.write();

        Info<< "ExecutionTime = " << runTime.elapsedCpuTime() << " s"
            << "  ClockTime = " << runTime.elapsedClockTime() << " s"
            << nl << endl;
			
			// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //
			
			
		dimensionedScalar smallU
        (
            "smallU",
            dimensionSet(0, 1, -1, 0, 0, 0 ,0),
            1e-6
        );

        // Check whether we need to update electromagnetic stuff with Elmer
        scalar maxRelDiff_local = (max(mag(U_old-U)/(average(mag(U))+smallU))).value();

		bool doElmer = false;
        if(maxRelDiff_local>maxRelDiff && (maxRelDiff<SMALL || maxRelDiff+SMALL<=1.0))
	    doElmer = true;

        if(doElmer || !runTime.run()) {
            U_old = U;

            // Send fields to Elmer
            sending.sendStatus(runTime.run());
	    sending.sendScalar(elcond);

	    if(sendVelocity > 0.001)
		sending.sendVector(U);

            // Receive fields form Elmer
            receiving.sendStatus(runTime.run());
            receiving.recvVector(Jre);
            receiving.recvVector(Jim);
            receiving.recvVector(Bre);
            receiving.recvVector(Bim);

            computePhasor(Jre, Jim, Jabs, Jphase);
            computePhasor(Bre, Bim, Babs, Bphase);
        }

        Info<< "ExecutionTime = " << runTime.elapsedCpuTime() << " s"
            << "  ClockTime = " << runTime.elapsedClockTime() << " s"
            << nl << endl;
    }

    Info<< "End\n" << endl;

    return 0;
}


// ************************************************************************* //
