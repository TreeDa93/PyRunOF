// Gmsh project created on Thu Feb 25 19:51:40 2021
SetFactory("OpenCASCADE");

Mesh 3;
//Mesh.Algorithm = 8;

//Parameters
w_duct = w_var;
h_duct = h_var;
l_duct = L_var;
N_height = hy_var;
N_width = hz_var;
N_length = hx_var;
Bump_coef = k_var;
//

//+
Point(1) = {0, -h_duct/2, -w_duct/2, 1.0};
//+
Point(2) = {0, -h_duct/2, w_duct/2, 1.0};
//+
Point(3) = {0, h_duct/2, w_duct/2, 1.0};
//+
Point(4) = {0, h_duct/2, -w_duct/2, 1.0};
//+
Line(1) = {4, 1};
//+
Line(2) = {4, 3};
//+
Line(3) = {3, 2};
//+
Line(4) = {1, 2};
//+
Line Loop(1) = {1, 2, 3, -4};
//+
Plane Surface(1) = {1};
//+
Recombine Surface {1};
//+
Extrude {l_duct, 0, 0} {
  Surface{1}; Layers{N_length}; Recombine;
}
//+
Physical Volume("Duct") = {1};
//+
Physical Surface("inlet") = {1};
//+
Physical Surface("outlet") = {6};
//+
Physical Surface("frontAndBack") = {4, 2};
//+
Physical Surface("upperWall") = {3};
//+
Physical Surface("lowerWall") = {5};
//+
Transfinite Line {3, 1} = N_height Using Bump Bump_coef;
//+
Transfinite Line {2, 4} = N_width Using Bump Bump_coef;

Recombine Surface {1};
//+
Transfinite Surface {1};


//+

//+

//+

