/*---------------------------------------------------------------------------*\
  =========                 |
  \\      /  F ield         | OpenFOAM: The Open Source CFD Toolbox
   \\    /   O peration     | Website:  https://openfoam.org
    \\  /    A nd           | Copyright (C) YEAR OpenFOAM Foundation
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

Description
    Template for use with codeStream.

\*---------------------------------------------------------------------------*/

#include "dictionary.H"
#include "Ostream.H"
#include "Pstream.H"
#include "unitConversion.H"

//{{{ begin codeInclude
#line 39 "/home/ivan/mySolvers/RunnerForCases/Examples/Example1/PuiselFlowBase_solved/0/U.boundaryField.inlet.#codeStream"
#include "fvCFD.H"
//}}} end codeInclude

// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //

namespace Foam
{

// * * * * * * * * * * * * * * * Local Functions * * * * * * * * * * * * * * //

//{{{ begin localCode

//}}} end localCode


// * * * * * * * * * * * * * * * Global Functions  * * * * * * * * * * * * * //

extern "C"
{
    void codeStream_06e0f7ea1259bd5b9bd90003ec0164ab484c21cc
    (
        Ostream& os,
        const dictionary& dict
    )
    {
//{{{ begin code
        #line 56 "/home/ivan/mySolvers/RunnerForCases/Examples/Example1/PuiselFlowBase_solved/0/U.boundaryField.inlet.#codeStream"
const IOdictionary& d = static_cast<const IOdictionary&>
				(
					dict.parent().parent()
				);
				
				const fvMesh& mesh = refCast<const fvMesh>(d.db());
				const label id = mesh.boundary().findPatchID("inlet");
				const fvPatch& patch = mesh.boundary()[id];
				
				vectorField U(patch.size(), vector(0, 0, 0));
				
				const scalar U_avg = 2.; //average velocity
				const scalar p_ctr_y = 0.005; //patch center
				const scalar p_ctr_z = 0.01; //patch center
				const scalar U_max = 1/0.64; //patch center
				const scalar pi = constant::mathematical::pi;
				const scalar U_0 = 2.; //maximum velocity
				const scalar p_ctr = 8.; //patch center
				const scalar p_r = 8.; //patch radius
				
				forAll(U, i) 
				{
					const scalar y = patch.Cf()[i][1]; // 0 is x; 1 is y and 2 is z 
					const scalar z = patch.Cf()[i][2]; // 0 is x; 1 is y and 2 is z 
					
					U[i] = vector(U_max*(1-(pow((y-p_ctr_y)/p_ctr_y,6)))*(1-(pow((z-p_ctr_z)/p_ctr_z,6))), 0., 0.);
					//U[i] = vector(U_0*(1-(pow(y-p_ctr,2))/(p_r*p_r)), 0., 0.);
				}
				
				U.writeEntry("", os);
//}}} end code
    }
}


// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //

} // End namespace Foam

// ************************************************************************* //

