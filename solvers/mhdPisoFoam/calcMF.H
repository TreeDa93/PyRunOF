
// Send fields to Elmer
			
sending.sendStatus(runTime.run());
sending.sendVector(U);
			
// Receive fields form Elmer
receiving.sendStatus(runTime.run());
			
receiving.recvVector(Jre);
receiving.recvVector(Jim);
receiving.recvVector(Bre);
receiving.recvVector(Bim);
receiving.recvVector(JxB_avg);
