

Info<< "\nIt is the first iterations" << endl;
// Send fields to Elmer
Elmer<fvMesh> sending(mesh,1); // 1=send, -1=receive
sending.sendStatus(1); // 1=ok, 0=lastIter, -1=error
sending.sendVector(U);

// Receive fields from Elmer
Elmer<fvMesh> receiving(mesh,-1); // 1=send, -1=receive
receiving.sendStatus(1); // 1=ok, 0=lastIter, -1=error
receiving.recvVector(Jre);
receiving.recvVector(Jim);
receiving.recvVector(Bre);
receiving.recvVector(Bim);
receiving.recvVector(JxB_avg);

