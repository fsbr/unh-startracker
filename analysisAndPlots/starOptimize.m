% this script tries to plot the error in the intercept by useing the actual
% data.  let's hope it works!
% tckf spring 2016
clear all; close all;
plotData = csvread('plotData.csv');
analysis = csvread('analysis.csv');
%conversion factor degrees to pixels
K = -3600/24.2;
% pulling out variables that we need
x = plotData(:, 1);
y = plotData(:, 2);
pitch = mean(plotData(:,3));
roll = mean(plotData(:,4));

% the roll and pitch offsets will go here 
% remember these are possible errors.
rollOff = linspace(-15, 15, 100); % these need to be in pixel units
pitchOff = linspace(-15*K, 15*K, 100);

% roll and pitch operations, but idk the order yet
[PO, RO] = meshgrid(pitchOff, rollOff);
%tht = roll;%+ RO;
% need to just do one computation but then repeat it a bunch of times.
newy = [];
newy1 = [];
newy2 = [];

for j = 1:length(pitchOff)
    
    for i = 1:length(rollOff)
        tht = roll + rollOff(i);
        %newx(i) = x(i).*cosd(tht) + y(i).*sind(tht);
        newy(j,i) = pitchOff(j) -x(1).*sind(tht) + y(1).*cosd(tht);  
        newy1(j,i) = pitchOff(j) -x(2).*sind(tht) + y(1).*cosd(tht);  
        newy2(j,i) = pitchOff(j) -x(3).*sind(tht) + y(1).*cosd(tht);  
    end
end


y1= y(1:3:end)
y2 = y(2:3:end)
y3 = y(3:3:end)


HC1 = analysis(:,4);
HC2 = analysis(:,5);
HC3 = analysis(:,6);
DC1 = HC1 - pitch;
DC2 = HC2 - pitch;
DC3 = HC3 - pitch;

%convert Desired Center angles into desired center pixels
DP1 = DC1*K;
DP2 = DC2*K;
DP3 = DC3*K;
%lets get some values of E
%Desired Pixel Total
DPT = [];
for i = 1:length(DP1)
    DPT(end+1) = DP1(i);
    DPT(end+1) = DP2(i);
    DPT(end+1) = DP3(i);
end

%the actual error is for each try of the pitch and roll ugh.
%for i =1:length(DPT)
 %   E(i,:) = newy(i,:) - DPT(i);
%end

% its gotta follow the below form more or less.
%DPTm = meshgrid(DPT);
E = (1/6)*((newy - DP1(1)).^2 + (newy1 - DP2(1)).^2 + (newy2 - DP3(1)).^2)
surf(PO,RO, E)
xlabel('pitch axis (pixels)')
ylabel('roll axis (degrees?)')
zlabel('cost function value')
%figure;plot(pitchOff,E)
%figure;plot(rollOff,E)
%E1 = analysis(:,1) - analysis(:,4);
%E2 = analysis(:,2) - analysis(:,5);
%E3 = analysis(:,3) - analysis(:,6);
%ET is the error total (in degrees) of my motherfucka
%ET = 0
%for i = 1:length(E1)
%   ET(end+1) = E1(i);
%   ET(end+1) = E2(i);
%   ET(end+1) = E3(i);
%end
%ET(1) =[];
