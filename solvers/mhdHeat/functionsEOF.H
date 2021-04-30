	void computePhasor(volVectorField& re, volVectorField& im, volVectorField& abs, volVectorField& phase)
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
	
	bool logical_expr_run_EOF(scalar maxRelDiff, volVectorField& U_old, volVectorField& U, 
								dimensionedScalar smallU)
	{
		scalar maxRelDiff_local = (max(mag(U_old-U)/(average(mag(U))+smallU))).value();
		
		if(maxRelDiff_local>maxRelDiff && (maxRelDiff<SMALL || maxRelDiff+SMALL<=1.0)) {
            return  true;
        } else {
			return false; 
		}
		
	}
		
	
	