[DATA_0303, TXT_0303,~] = xlsread('OPTIONS.xlsx','0303','A1:L201');
[DATA_0305, TXT_0305,~] = xlsread('OPTIONS.xlsx','0305','A1:L265');
[DATA_0308, TXT_0308,~] = xlsread('OPTIONS.xlsx','0308','A1:L195');
[DATA_0329, TXT_0329,~] = xlsread('OPTIONS.xlsx','0329','A1:L79');
[DATA_0331, TXT_0331,~] = xlsread('OPTIONS.xlsx','0331','A1:L437');
[DATA_0401, TXT_0401,~] = xlsread('OPTIONS.xlsx','0401','A1:L201');

% PLOT VOLATILITY SURFACE
TYPE_0303 = TXT_0303(2:end,4);
STRIKE_0303 = DATA_0303(strcmp(TYPE_0303,'C')==1,1);
IMPLIED_VOL_0303 = DATA_0303(strcmp(TYPE_0303,'C')==1,10);

TYPE_0305 = TXT_0305(2:end,4);
STRIKE_0305 = DATA_0305(strcmp(TYPE_0305,'C')==1,1);
IMPLIED_VOL_0305 = DATA_0305(strcmp(TYPE_0305,'C')==1,10);

TYPE_0308 = TXT_0308(2:end,4);
STRIKE_1021 = DATA_0308(strcmp(TYPE_0308,'C')==1,1);
IMPLIED_VOL_1021 = DATA_0308(strcmp(TYPE_0308,'C')==1,10);

TYPE_0329 = TXT_0329(2:end,4);
STRIKE_0329 = DATA_0329(strcmp(TYPE_0329,'C')==1,1);
IMPLIED_VOL_0329 = DATA_0329(strcmp(TYPE_0329,'C')==1,10);

TYPE_0331 = TXT_0331(2:end,4);
STRIKE_0331 = DATA_0331(strcmp(TYPE_0331,'C')==1,1);
IMPLIED_VOL_0331 = DATA_0331(strcmp(TYPE_0331,'C')==1,10);

TYPE_0401 = TXT_0401(2:end,4);
STRIKE_0401 = DATA_0401(strcmp(TYPE_0401,'C')==1,1);
IMPLIED_VOL_0401 = DATA_0401(strcmp(TYPE_0401,'C')==1,10);

% IMPLIED VOL SMILE
figure(1)
subplot(2,3,1)
scatter(STRIKE_0303,IMPLIED_VOL_0303,'filled');
title('03/03/2021');
subplot(2,3,2)
scatter(STRIKE_0305,IMPLIED_VOL_0305,'filled');
title('03/05/2021');
subplot(2,3,3)
scatter(STRIKE_1021,IMPLIED_VOL_1021,'filled');
title('03/08/2021');
subplot(2,3,4)
scatter(STRIKE_0329,IMPLIED_VOL_0329,'filled');
title('03/29/2021');
subplot(2,3,5)
scatter(STRIKE_0331,IMPLIED_VOL_0331,'filled');
title('03/31/2021');
subplot(2,3,6)
scatter(STRIKE_0401,IMPLIED_VOL_0401,'filled');
title('04/01/2021');

% IMPLIED VOL SURFACE
STRIKE_vec =unique([STRIKE_0303; STRIKE_0305; STRIKE_1021; STRIKE_0329;...
    STRIKE_0331; STRIKE_0401]); % 160 x 1

% MODEL 1: STRIKE = STRIKE_vec;
% MODEL 2: STRIKE = Interpolate 1000 points within range of STRIKE_vec
STRIKE = linspace(min(STRIKE_vec),max(STRIKE_vec),1000);

VOL_SMILE_0303 = spline(STRIKE_0303,IMPLIED_VOL_0303,STRIKE);
[K_0305,ia_0305,~] = unique(STRIKE_0305); 
VOL_SMILE_0305 = spline(K_0305,IMPLIED_VOL_0305(ia_0305),STRIKE);
VOL_SMILE_0308 = spline(STRIKE_1021,IMPLIED_VOL_1021,STRIKE);
VOL_SMILE_0329 = spline(STRIKE_0329,IMPLIED_VOL_0329,STRIKE);
[K_0331,ia_0331,~] = unique(STRIKE_0331); 
VOL_SMILE_0331 = spline(STRIKE_0331,IMPLIED_VOL_0331,STRIKE);
VOL_SMILE_0401 = spline(STRIKE_0401,IMPLIED_VOL_0401,STRIKE);

vec = linspace(601,800,200);
VOL_SMILE = [VOL_SMILE_0303(vec)' VOL_SMILE_0305(vec)' ...
    VOL_SMILE_0308(vec)' VOL_SMILE_0329(vec)' ...
    VOL_SMILE_0331(vec)' VOL_SMILE_0401(vec)'];
figure(2)
surf(VOL_SMILE);
xticks(linspace(1,8,8));
xticklabels({'03/03','03/05','03/08','03/29','03/31','04/01'});
yticks([1 50 100 150 200]);
yticklabels(cellstr(num2str(STRIKE([601 650 700 750 800]))));






