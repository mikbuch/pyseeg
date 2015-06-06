////////////////////////////////////////////////////////////////
//                                                            //
// This script operates on data from a 128-electrodes EEG     //
//                                                            //
////////////////////////////////////////////////////////////////

////////////////////////////////
//                            //
// test scipt for alpha waves //
//                            //
////////////////////////////////

///////////////////////////////
//   variables declaration   //
///////////////////////////////

//EEGdata=csvRead("eeg_128.csv");
loadmatfile("zajecia.mat");

plots_width=1400;
plots_heigth=800;

alpha_lower=7.5;
alpha_upper=12.5;
beta_lower=12.5;
beta_upper=30;
gamma_lower=25;
gamma_upper=100;
delta_lower=1;
delta_upper=4;
theta_lower=4;
theta_upper=7;

// alpha c3 at rest (D19 when 128 electrodes)
alpha_electrode=115
beta_electrode=83
gamma_electrode=19
delta_electrode=83
theta_electrode=125

Fs=256;

filter_order=4;

alpha_filter = iir(filter_order,'bp','butt', [alpha_lower/Fs, alpha_upper/Fs],[]);
beta_filter = iir(filter_order,'bp','butt',[beta_lower/Fs, beta_upper/Fs],[]);
gamma_filter = iir(filter_order,'bp','butt',[gamma_lower/Fs, gamma_upper/Fs],[]);
delta_filter = iir(filter_order,'bp','butt',[delta_lower/Fs, delta_upper/Fs],[]);
theta_filter = iir(filter_order,'bp','butt',[theta_lower/Fs, theta_upper/Fs],[]);

// specify the heigth and the width of EEG data set
[row_eeg col_eeg]=size(EEGdata);

////loop to calculate millivolts from raw signal
//for i=1:1:wier_eeg
//    eeg_data(i,2)=((eeg_data(i,2)*(1.8/4096))/2000)*1000;
//end
////

alpha_data=EEGdata(alpha_electrode,:);
dataF = flts(alpha_data,alpha_filter);
alpha_Y=abs(2*fft(dataF(1,1+5*256:10*256))./length(dataF(1,1+5*256:10*256))); //wyznaczenie FFT sygnału od 5 do 10 sekundy sygnalu
// 1/2 for 2 seconds
alpha_f=1/5:1/5:128; //utworzenie osi częstotliwości

beta_data=EEGdata(beta_electrode,:);
dataF = flts(beta_data,beta_filter);
beta_Y=abs(2*fft(dataF(1,1+5*256:10*256))./length(dataF(1,1+5*256:10*256))); //wyznaczenie FFT sygnału od 5 do 10 sekundy sygnalu
beta_f=1/5:1/5:128; //utworzenie osi częstotliwości


gamma_data=EEGdata(gamma_electrode,:);
dataF = flts(gamma_data,gamma_filter);
gamma_Y=abs(2*fft(dataF(1,1+5*256:10*256))./length(dataF(1,1+5*256:10*256))); //wyznaczenie FFT sygnału od 5 do 10 sekundy sygnalu
gamma_f=1/5:1/5:128; //utworzenie osi częstotliwości


delta_data=EEGdata(delta_electrode,:);
dataF = flts(delta_data,delta_filter);
delta_Y=abs(2*fft(dataF(1,1+5*256:10*256))./length(dataF(1,1+5*256:10*256))); //wyznaczenie FFT sygnału od 5 do 10 sekundy sygnalu
delta_f=1/5:1/5:128; //utworzenie osi częstotliwości


theta_data=EEGdata(theta_electrode,:);
dataF = flts(theta_data,theta_filter);
theta_Y=abs(2*fft(dataF(1,1+5*256:10*256))./length(dataF(1,1+5*256:10*256))); //wyznaczenie FFT sygnału od 5 do 10 sekundy sygnalu
theta_f=1/5:1/5:128; //utworzenie osi częstotliwości


///////////////////////////////
//       plotting data       //
///////////////////////////////

///////////
// alpha //
///////////

// alpha_time plot
f1=scf(1);
f=get("current_figure") 
f.figure_size=[plots_width,plots_heigth]
a=gca();  
a.font_size=5;
title("Alpha waves time domain","fontsize",6);
xlabel("frequency (Hz)","fontsize",5);
ylabel("signal amplitude","fontsize",5);
plot(EEGdata(alpha_electrode,1+5*256:10*256));


// alpha_freq plot
f1=scf(11);
f=get("current_figure")
f.figure_size=[plots_width,plots_heigth]
a=gca();  
a.font_size=5;
title("Alpha waves frequency domain","fontsize",6);
xlabel("frequency (Hz)","fontsize",5);
ylabel("signal amplitude","fontsize",5);
plot(alpha_f(1,1:500),alpha_Y(1,1:500));



//beta waves plot
//figure();
//a=gca();  
//a.font_size=5;
//title("Beta waves of the brain","fontsize",6);
//xlabel("frequency (Hz)","fontsize",5);
//ylabel("amplitude","fontsize",5);
//subplot(524);
//plot(beta_f(1,1:500),beta_Y(1,1:500));


///////////////
// exporting //
///////////////



xs2pdf(1,'alpha_time');
//xs2pdf(gcf(),filename);
xs2pdf(11,'alpha_freq');

xs2pdf(2,'beta_time');
xs2pdf(22,'beta_freq');

//xs2pdf(3,'gamma_time');
//xs2pdf(33,'gamma_freq');

//xs2pdf(4,'delta_time');
//xs2pdf(44,'delta_freq');

//xs2pdf(5,'theta_time');
//xs2pdf(55,'theta_freq');


////
//debugging
/////////
//1+5*256
//disp(EEGdata(115,1+5*256))
//10*256
//disp(EEGdata(115,10*256))

