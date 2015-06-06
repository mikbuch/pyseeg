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

alpha_electrode=21

filter_order=4;

alpha_filter = iir(filter_order,'bp','butt', [alpha_lower/Fs, alpha_upper/Fs],[]);

// specify the heigth and the width of EEG data set
[row_eeg col_eeg]=size(EEGdata);

////
alpha_data = EEGdata(alpha_electrode,:);
alphaF = flts(alpha_data,alpha_filter);
alpha_x_sec = alphaF(1,second_begin*Fs:1:second_end*Fs);
alpha_Y = abs(2*fft(alphaF(1,1+second_begin*Fs:second_end*Fs))./length(alphaF(1,1+second_begin*Fs:second_end*Fs))); //FFT signal second_begin to second_end second
alpha_f = 1/2:1/2:128; // frequency axis creation


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
plot(EEGdata(alpha_electrode,1+second_begin*256:second_end*256)); //raw signal alpha

///////////////
// exporting //
///////////////

xs2pdf(1,'alpha_time');
//xs2pdf(gcf(),filename);
xs2pdf(11,'alpha_freq');
