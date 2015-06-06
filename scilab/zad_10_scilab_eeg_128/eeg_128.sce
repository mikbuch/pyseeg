////////////////////////////////////////////
//                                        //
// This script operates on data           //
// from a 128-electrodes EEG              //
//                                        //
////////////////////////////////////////////


///////////////////////////////
//   variables declaration   //
///////////////////////////////


//// use either csv file or mat file to 
//// create variable EEGdata
//EEGdata=csvRead("eeg_128.csv");
loadmatfile("zajecia.mat");

Fs=256;

second_begin=8;
second_end=10;

t=(second_begin:1/Fs:second_end);

plots_width=1400;
plots_heigth=800;

alpha_lower=8;
alpha_upper=13;
beta_lower=13;
beta_upper=30;
gamma_lower=30;
gamma_upper=80;
delta_lower=1;
delta_upper=4;
theta_lower=4;
theta_upper=8;

alpha_electrode=21
beta_electrode=85
gamma_electrode=3
delta_electrode=83
theta_electrode=115


filter_order=4;

alpha_filter = iir(filter_order,'bp','butt', [alpha_lower/Fs, alpha_upper/Fs],[]);
beta_filter = iir(filter_order,'bp','butt',[beta_lower/Fs, beta_upper/Fs],[]);
gamma_filter = iir(filter_order,'bp','butt',[gamma_lower/Fs, gamma_upper/Fs],[]);
delta_filter = iir(filter_order,'bp','butt',[delta_lower/Fs, delta_upper/Fs],[]);
theta_filter = iir(filter_order,'bp','butt',[theta_lower/Fs, theta_upper/Fs],[]);

// specify the heigth and the width of EEG data set
[row_eeg col_eeg]=size(EEGdata);

////
alpha_data = EEGdata(alpha_electrode,:);
alphaF = flts(alpha_data,alpha_filter);
alpha_x_sec = alphaF(1,second_begin*Fs:1:second_end*Fs);
alpha_Y = abs(2*fft(alphaF(1,1+second_begin*Fs:second_end*Fs))./length(alphaF(1,1+second_begin*Fs:second_end*Fs))); //FFT signal second_begin to second_end second
alpha_f = 1/2:1/2:128; // frequency axis creation

beta_data = EEGdata(beta_electrode,:);
betaF = flts(beta_data,beta_filter);
beta_x_sec = betaF(1,second_begin*Fs:1:second_end*Fs);
beta_Y = abs(2*fft(betaF(1,1+second_begin*Fs:second_end*Fs))./length(betaF(1,1+second_begin*Fs:second_end*Fs))); 
beta_f = 1/2:1/2:128; // frequency axis creation


gamma_data = EEGdata(gamma_electrode,:);
gammaF = flts(gamma_data,gamma_filter);
gamma_x_sec = gammaF(1,second_begin*Fs:1:second_end*Fs);
gamma_Y = abs(2*fft(gammaF(1,1+second_begin*Fs:second_end*Fs))./length(gammaF(1,1+second_begin*Fs:second_end*Fs)));
gamma_f = 1/2:1/2:128; // frequency axis creation 


delta_data=EEGdata(delta_electrode,:);
deltaF = flts(delta_data,delta_filter);
delta_x_sec = deltaF(1,second_begin*Fs:1:second_end*Fs);
delta_Y=abs(2*fft(deltaF(1,1+second_begin*Fs:second_end*Fs))./length(deltaF(1,1+second_begin*Fs:second_end*Fs)));
delta_f=1/2:1/2:128; // frequency axis creation


theta_data=EEGdata(theta_electrode,:);
thetaF = flts(theta_data,theta_filter);
theta_x_sec = thetaF(1,second_begin*Fs:1:second_end*Fs);
theta_Y=abs(2*fft(thetaF(1,1+second_begin*Fs:second_end*Fs))./length(thetaF(1,1+second_begin*Fs:second_end*Fs)));
theta_f=1/2:1/2:128; // frequency axis creation


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
xlabel("seconds (s)","fontsize",5);
ylabel("signal amplitude (µV)","fontsize",5);
//subplot(521);
plot(t,alpha_x_sec(1,:))

// alpha_freq plot
f1=scf(11);
f=get("current_figure")
f.figure_size=[plots_width,plots_heigth]
a=gca();  
a.font_size=5;
title("Alpha waves frequency domain","fontsize",6);
xlabel("frequency (Hz)","fontsize",5);
ylabel("signal amplitude (µV)","fontsize",5);
//subplot(522);
plot(alpha_f(1,1:256),alpha_Y(1,1:256));

// alpha_raw plot
//plot(EEGdata(alpha_electrode,1+second_begin*256:second_end*256)); //raw signal alpha

///////////
// beta  //
///////////

// beta_time plot
f1=scf(2);
f=get("current_figure") 
f.figure_size=[plots_width,plots_heigth]
a=gca();  
a.font_size=5;
title("Beta waves time domain","fontsize",6);
xlabel("seconds (s)","fontsize",5);
ylabel("signal amplitude (µV)","fontsize",5);
//subplot(523);
plot(t,beta_x_sec(1,:))

// beta_freq plot
f1=scf(22);
f=get("current_figure")
f.figure_size=[plots_width,plots_heigth]
a=gca();  
a.font_size=5;
title("Beta waves frequency domain","fontsize",6);
xlabel("frequency (Hz)","fontsize",5);
ylabel("signal amplitude (µV)","fontsize",5);
//subplot(524);
plot(beta_f(1,1:256),beta_Y(1,1:256));

// beta_raw plot
//plot(EEGdata(beta_electrode,1+second_begin*256:second_end*256)); //raw signal beta

///////////
// gamma //
///////////

// gamma_time plot
f1=scf(3);
f=get("current_figure") 
f.figure_size=[plots_width,plots_heigth]
a=gca();  
a.font_size=5;
title("Gamma waves time domain","fontsize",6);
xlabel("seconds (s)","fontsize",5);
ylabel("signal amplitude (µV)","fontsize",5);
//subplot(525);
plot(t,gamma_x_sec(1,:))

// gamma_freq plot
f1=scf(33);
f=get("current_figure")
f.figure_size=[plots_width,plots_heigth]
a=gca();  
a.font_size=5;
title("Gamma waves frequency domain","fontsize",6);
xlabel("frequency (Hz)","fontsize",5);
ylabel("signal amplitude (µV)","fontsize",5);
//subplot(526);
plot(gamma_f(1,1:256),gamma_Y(1,1:256));

// gamma_raw plot
//plot(EEGdata(gamma_electrode,1+second_begin*256:second_end*256)); //raw signal gamma

///////////
// delta //
///////////

// delta_time plot
f1=scf(4);
f=get("current_figure") 
f.figure_size=[plots_width,plots_heigth]
a=gca();  
a.font_size=5;
title("Delta waves time domain","fontsize",6);
xlabel("seconds (s)","fontsize",5);
ylabel("signal amplitude (µV)","fontsize",5);
//subplot(527);
plot(t,delta_x_sec(1,:))

// delta_freq plot
f1=scf(44);
f=get("current_figure")
f.figure_size=[plots_width,plots_heigth]
a=gca();  
a.font_size=5;
title("Delta waves frequency domain","fontsize",6);
xlabel("frequency (Hz)","fontsize",5);
ylabel("signal amplitude (µV)","fontsize",5);
//subplot(528);
plot(delta_f(1,1:256),delta_Y(1,1:256));

// delta_raw plot
//plot(EEGdata(delta_electrode,1+second_begin*256:second_end*256)); /raw signal delta

///////////
// theta //
///////////

// theta_time plot
f1=scf(5);
f=get("current_figure") 
f.figure_size=[plots_width,plots_heigth]
a=gca();  
a.font_size=5;
title("Theta waves time domain","fontsize",6);
xlabel("seconds (s)","fontsize",5);
ylabel("signal amplitude (µV)","fontsize",5);
//subplot(529);
plot(t,theta_x_sec(1,:))

// theta_freq plot
f1=scf(55);
f=get("current_figure")
f.figure_size=[plots_width,plots_heigth]
a=gca();  
a.font_size=5;
title("Theta waves frequency domain","fontsize",6);
xlabel("frequency (Hz)","fontsize",5);
ylabel("signal amplitude (µV)","fontsize",5);
//subplot(5,2,10);
plot(theta_f(1,1:256),theta_Y(1,1:256));

// theta_raw plot
//plot(EEGdata(theta_electrode,1+second_begin*256:second_end*256)); /raw signal theta


///////////////
// exporting //
///////////////

xs2pdf(1,'alpha_time');
//xs2pdf(gcf(),filename);
xs2pdf(11,'alpha_freq');

xs2pdf(2,'beta_time');
xs2pdf(22,'beta_freq');

xs2pdf(3,'gamma_time');
xs2pdf(33,'gamma_freq');

xs2pdf(4,'delta_time');
xs2pdf(44,'delta_freq');

xs2pdf(5,'theta_time');
xs2pdf(55,'theta_freq');
