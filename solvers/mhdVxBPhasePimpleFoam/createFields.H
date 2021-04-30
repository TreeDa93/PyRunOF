Info<< "Reading field p\n" << endl;
volScalarField p
(
    IOobject
    (
        "p",
        runTime.timeName(),
        mesh,
        IOobject::MUST_READ,
        IOobject::AUTO_WRITE
    ),
    mesh
);

Info<< "Reading field U\n" << endl;
volVectorField U
(
    IOobject
    (
        "U",
        runTime.timeName(),
        mesh,
        IOobject::MUST_READ,
        IOobject::AUTO_WRITE
    ),
    mesh
);

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


volScalarField elcond
(
    IOobject
    (
        "elcond",
        runTime.timeName(),
        mesh,
        IOobject::MUST_READ,
        IOobject::AUTO_WRITE
    ),
    mesh
);

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
    mesh
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
        IOobject::MUST_READ,
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
        IOobject::MUST_READ,
        IOobject::AUTO_WRITE
    ),
    mesh
);


#include "createPhi.H"


label pRefCell = 0;
scalar pRefValue = 0.0;
setRefCell(p, simple.dict(), pRefCell, pRefValue);
mesh.setFluxRequired(p.name());


singlePhaseTransportModel laminarTransport(U, phi);

autoPtr<incompressible::turbulenceModel> turbulence
(
    incompressible::turbulenceModel::New(U, phi, laminarTransport)
);

#include "createMRF.H"
#include "createFvOptions.H"

dimensionedScalar rho("rho", dimDensity, laminarTransport);

scalar maxRelDiff(readScalar(laminarTransport.lookup("maxRelDiff")));
scalar sendVelocity(readScalar(laminarTransport.lookup("sendVelocity")));

dimensionedScalar elcond_melt("elcond_melt", dimensionSet(-1, -3, 3, 0, 0, 2, 0), laminarTransport);

dimensionedScalar frequency("frequency", dimensionSet(0, 0, -1, 0, 0, 0, 0), laminarTransport);





