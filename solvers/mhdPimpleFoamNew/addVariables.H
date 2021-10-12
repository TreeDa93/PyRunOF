Info<< "Initializing field Jre\n" << endl;
volVectorField Jre
(
    IOobject
    (
        "Jre",
        runTime.timeName(),
        mesh,
        IOobject::NO_READ,
        IOobject::NO_WRITE
    ),
    mesh,
	dimensionedVector("zero", dimensionSet(0, -2, 0, 0, 0, 1, 0), vector::zero)
);

Info<< "Initializing field Jim\n" << endl;
volVectorField Jim
(
    IOobject
    (
        "Jim",
        runTime.timeName(),
        mesh,
        IOobject::NO_READ,
        IOobject::NO_WRITE
    ),
    mesh,
	dimensionedVector("zero", dimensionSet(0, -2, 0, 0, 0, 1, 0), vector::zero)
);

Info<< "Initializing field Jabs\n" << endl;
volVectorField Jabs
(
    IOobject
    (
        "Jabs",
        runTime.timeName(),
        mesh,
        IOobject::NO_READ,
        IOobject::NO_WRITE
    ),
    mesh,
	dimensionedVector("zero", dimensionSet(0, -2, 0, 0, 0, 1, 0), vector::zero)
);

Info<< "Initializing field Jphase\n" << endl;
volVectorField Jphase
(
    IOobject
    (
        "Jphase",
        runTime.timeName(),
        mesh,
        IOobject::NO_READ,
        IOobject::NO_WRITE
    ),
    mesh,
	dimensionedVector("zero", dimless, Foam::vector(0,0,0))
);

Info<< "Initializing field Bre\n" << endl;
volVectorField Bre
(
    IOobject
    (
        "Bre",
        runTime.timeName(),
        mesh,
        IOobject::NO_READ,
        IOobject::NO_WRITE
    ),
    mesh,
	dimensionedVector("zero", dimensionSet(1, 0, -2, 0, 0, -1, 0), vector::zero)
);

Info<< "Initializing field Bim\n" << endl;
volVectorField Bim
(
    IOobject
    (
        "Bim",
        runTime.timeName(),
        mesh,
        IOobject::NO_READ,
        IOobject::NO_WRITE
    ),
    mesh,
	dimensionedVector("zero", dimensionSet(1, 0, -2, 0, 0, -1, 0), vector::zero)
);

Info<< "Initializing field Babs\n" << endl;
volVectorField Babs
(
    IOobject
    (
        "Babs",
        runTime.timeName(),
        mesh,
        IOobject::NO_READ,
        IOobject::NO_WRITE
    ),
    mesh,
	dimensionedVector("zero", dimensionSet(1, 0, -2, 0, 0, -1, 0), vector::zero)
);

Info<< "Initializing field Bphase\n" << endl;
volVectorField Bphase
(
    IOobject
    (
        "Bphase",
        runTime.timeName(),
        mesh,
        IOobject::NO_READ,
        IOobject::NO_WRITE
    ),
    mesh,
	dimensionedVector("zero", dimless, vector::zero)
);

Info<< "Initializing field UxBxB\n" << endl;
volVectorField UxBxB
(
    IOobject
    (
        "UxBxB",
        runTime.timeName(),
        mesh,
        IOobject::NO_READ,
        IOobject::AUTO_WRITE
    ),
    mesh,
	dimensionedVector("zero", dimensionSet(2, 1, -5, 0, 0, -2, 0), vector::zero)
);

volVectorField B
(
    IOobject
    (
        "B",
        runTime.timeName(),
        mesh,
        IOobject::NO_READ,
        IOobject::AUTO_WRITE
    ),
    mesh
);

volVectorField j
(
    IOobject
    (
        "j",
        runTime.timeName(),
        mesh,
        IOobject::NO_READ,
        IOobject::AUTO_WRITE
    ),
    mesh
);
Info<< "Initializing field JxB\n" << endl;
volVectorField JxB
(
    IOobject
    (
        "JxB",
        runTime.timeName(),
        mesh,
        IOobject::MUST_READ,
        IOobject::AUTO_WRITE
    ),
    mesh
);

Info<< "Initializing field JxB_avg\n" << endl;
volVectorField JxB_avg
(
    IOobject
    (
        "JxB_avg",
        runTime.timeName(),
        mesh,
        IOobject::NO_READ,
        IOobject::AUTO_WRITE
    ),
    mesh
);

Info<< "Initializing field JxB_inst\n" << endl;
volVectorField JxB_inst
(
    IOobject
    (
        "JxB_inst",
        runTime.timeName(),
        mesh,
        IOobject::NO_READ,
        IOobject::AUTO_WRITE
    ),
    mesh
);

Info<< "Initializing field F_mot\n" << endl;
volVectorField F_mot
(
    IOobject
    (
        "F_mot",
        runTime.timeName(),
        mesh,
        IOobject::NO_READ,
        IOobject::AUTO_WRITE
    ),
    mesh
);

Info<< "Initializing field U_old\n" << endl;
volVectorField U_old
(
    IOobject
    (
        "U_old",
        runTime.timeName(),
        mesh,
        IOobject::NO_READ,
        IOobject::NO_WRITE
    ),
    U
);


// Melt's density
dimensionedScalar rho("rho", dimDensity, laminarTransport);

//frequency of magnetic field 

dimensionedScalar frequency("frequency", dimensionSet(0, 0, -1, 0, 0, 0, 0), laminarTransport);

dimensionedScalar elcond ("elcond_melt", dimensionSet(-1, -3, 3, 0, 0, 2, 0), laminarTransport);


//dimensionedScalar elcond
 //       (
  //          "elcond",
  //          dimensionSet(-1, -3, 3, 0, 0, 2, 0),
    //        1
      //  );

// Check whether we need to update electromagnetic stuff with Elmer
// Maximum allowable relative field difference in any cell comparing
// to last Elmer update. This option controls frequency Elmer is called.
//     1     - once
//     (0,1) - when relative difference in any cell exceeds given value
//     0     - every iteration

scalar maxRelDiff(readScalar(laminarTransport.lookup("maxRelDiff")));


// Define type of recalculation of the MF task
// 0 is to recalculate every iteration
// 1 is to use logical expression 
// 2 is to recalculate the Nth iteration (timesRecal)
// 3 is to recalculate every given time step (timeRecal)
// 4 is to calculate only at the first time

scalar typeRecalculateMF(readScalar(laminarTransport.lookup("typeRecalculateMF")));
scalar timesRecal(readScalar(laminarTransport.lookup("timesRecal")));
scalar timeRecal(readScalar(laminarTransport.lookup("timeRecal")));

dimensionedScalar smallU
        (
            "smallU",
            dimensionSet(0, 1, -1, 0, 0, 0 ,0),
            1e-6
        );


scalar counter = 0;

// 1 is to send U and reccive JxB
// 2 is to send U and recive J and B 
// 3 is to send nothing and recive JxB 
// 3 is to send nothing and recive J and B

scalar typeForce(readScalar(laminarTransport.lookup("typeForce")));

scalar typeUxBxB(readScalar(laminarTransport.lookup("typeUxBxB")));

