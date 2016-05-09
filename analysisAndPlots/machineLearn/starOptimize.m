% this script tries to plot the error in the intercept by useing the actual
% data.  let's hope it works!
% tckf spring 2016
clear all; close all;
plotData = csvread('plotData.csv', 1, 0);
analysis = csvread('analysis.csv');
%conversion factor degrees to pixels
K = 3600/24.2; % the signs are basically opposite due to the weird origin
% pulling out variables that we need
x = plotData(:, 6);
y = plotData(:, 7);

%degrees originall. we mult by K to convert to pixels
pitch = mean(plotData(:,8))*K;
roll = mean(plotData(:,9));

% the roll and pitch offsets will go here 
% remember these are possible errors.
rollOff = linspace(-25, 25, 500); % these need to be in pixel units
pitchOff = linspace(-30*K, 30*K, 500);

% roll and pitch operations, but idk the order yet
[PO, RO] = meshgrid(pitchOff, rollOff);

% the normalization happen here if desired.
PO = PO;
RO = RO;
%tht = roll;%+ RO;
% need to just do one computation but then repeat it a bunch of times.
newy = [];
newy1 = [];
newy2 = [];


y1= y(1:3:end);
y2 = y(2:3:end);
y3 = y(3:3:end);


HC1 = analysis(:,4);
HC2 = analysis(:,5);
HC3 = analysis(:,6);
HCT = [HC1;HC2;HC3];
DC1 = HC1 - pitch;
DC2 = HC2 - pitch;
DC3 = HC3 - pitch;

%convert Desired Center angles into desired center pixels
DP1 = DC1*K;
DP2 = DC2*K;
DP3 = DC3*K;
G1 = newy-DP1(1);
G2 = newy1-DP2(1);
G3 = newy2-DP3(1);

E = cell(length(x),1);

% might have to FIRST do pitch, THEN do roll. but idk.
for n = 1:1:length(x)
for j = 1:length(pitchOff)
    for i = 1:length(rollOff)
        tht = roll + rollOff(i);
        %newx(i) = x(i).*cosd(tht) + y(i).*sind(tht);
        %newytest(j,i) = -x(1)*sind(tht) + (y(1)+(pitch+pitchOff(j)))*cosd(tht);
        newy(j,i) = (-x(n)*sind(tht) + (y(n) +(pitch+pitchOff(j)))*cosd(tht));%+;  
      %  newy1(j,i) = (-x(2)*sind(tht) + (y(2) +(pitch+pitchOff(j)))*cosd(tht));%%+;  
       % newy2(j,i) = (-x(3)*sind(tht) + (y(3) +(pitch+pitchOff(j)))*cosd(tht));%%+;  
    end
end

E{n} = (1/6)*((newy - HCT(n)*K).^2); %+ (newy1 - HC2(1)).^2 + (newy2 - HC3(1)).^2);
end

%to save all error plots for later plotting witout having to recalculate

% directory = '/home/newmy/research/exp/unh-startracker/dataSets/';
% save(strcat(directory,'Error_plots.mat', 'E'));
% 
% load('E.mat')

%E = 0.5*G'*G;;
%E = abs(newy-HC1(1) +newy1-HC2(1) + newy2-HC3(1))
%the error is in units of sum of pixels squared.
% now that I have this plot, I need to do GD on it.
mesh(RO,PO, E{1})
xlabel('pitch axis (pix normalized)')
ylabel('roll axis (degrees normalized)')
zlabel('cost function value')

%plot the derivative figure
%figure;
%surf(PO,RO, gradient(E))
%figure;
%surf(PO,RO, abs(newy-DP1(1)))
%xlabel('pitch axis domain')
%ylabel('roll axis domain')
%zlabel('new y location (pixels')

thresh = 0.001; %threshold for stopping GD
learningRate = 0.0001; %how "fast" our algorithm "learns"
xR_old = 0;
xR_new = 1; %degree
xP_old = 0;
xP_new = 1000; %pixels

% while abs((xR_new-xR_old) + (xP_new-xP_old))> thresh
%    xR_old = xR_new;
%    xP_old = xP_new;
%    % need to be getting a CERTAIN value of the gradient i think? im not too
%    % sure.  
%    [DX, DY] = gradient(E);
%    temp1 = xR_old -learningRate*DY;
%    temp2 = xP_new - learningRate*DX;
%    xR_new = temp1;
%    xP_new = temp2;
% end




