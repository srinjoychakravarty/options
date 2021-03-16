
% ESTIMATE RISK-NEUTRAL DENSITY (STATE-PRICE DENSITY)
[DATA_0303, TXT_0303,~] = xlsread('OPTIONS.xlsx','0303','A1:L201');
[DATA_0305, TXT_0305,~] = xlsread('OPTIONS.xlsx','0305','A1:L265');
[DATA_0308, TXT_0308,~] = xlsread('OPTIONS.xlsx','0308','A1:L195');
[DATA_0329, TXT_0329,~] = xlsread('OPTIONS.xlsx','0329','A1:L79');
[DATA_0331, TXT_0331,~] = xlsread('OPTIONS.xlsx','0331','A1:L437');
[DATA_0401, TXT_0401,~] = xlsread('OPTIONS.xlsx','0401','A1:L201');

% SPX PRICE
St = 3819.72; % AS OF MARCH 03, 2021

TYPE_0303 = TXT_0303(2:end,4);
STRIKE_0303 = DATA_0303(strcmp(TYPE_0303,'C')==1,1);
IMPLIED_VOL_0303 = DATA_0303(strcmp(TYPE_0303,'C')==1,10);
BID_0303 = DATA_0303(strcmp(TYPE_0303,'C')==1,4);
ASK_0303 = DATA_0303(strcmp(TYPE_0303,'C')==1,5);
C_0303 = (BID_0303 + ASK_0303)/2;
SPD_0303 = STATE_PRICE_DENSITY(C_0303,STRIKE_0303,St);

TYPE_0305 = TXT_0305(2:end,4);
STRIKE_0305 = DATA_0305(strcmp(TYPE_0305,'C')==1,1);
IMPLIED_VOL_0305 = DATA_0305(strcmp(TYPE_0305,'C')==1,10);
BID_0305 = DATA_0305(strcmp(TYPE_0305,'C')==1,4);
ASK_0305 = DATA_0305(strcmp(TYPE_0305,'C')==1,5);
[K_0305,ia_0305,~] = unique(STRIKE_0305); 
C_0305 = (BID_0305 + ASK_0305)/2;
SPD_0305 = STATE_PRICE_DENSITY(C_0305(ia_0305),K_0305,St);

TYPE_0308 = TXT_0308(2:end,4);
STRIKE_0308 = DATA_0308(strcmp(TYPE_0308,'C')==1,1);
IMPLIED_VOL_0308 = DATA_0308(strcmp(TYPE_0308,'C')==1,10);
BID_0308 = DATA_0308(strcmp(TYPE_0308,'C')==1,4);
ASK_0308 = DATA_0308(strcmp(TYPE_0308,'C')==1,5);
C_0308 = (BID_0308 + ASK_0308)/2;
SPD_0308 = STATE_PRICE_DENSITY(C_0308,STRIKE_0308,St);

TYPE_0329 = TXT_0329(2:end,4);
STRIKE_0329 = DATA_0329(strcmp(TYPE_0329,'C')==1,1);
IMPLIED_VOL_0329 = DATA_0329(strcmp(TYPE_0329,'C')==1,10);
BID_0329 = DATA_0329(strcmp(TYPE_0329,'C')==1,4);
ASK_0329 = DATA_0329(strcmp(TYPE_0329,'C')==1,5);
C_0329 = (BID_0329 + ASK_0329)/2;
SPD_0329 = STATE_PRICE_DENSITY(C_0329,STRIKE_0329,St);

TYPE_0331 = TXT_0331(2:end,4);
STRIKE_0331 = DATA_0331(strcmp(TYPE_0331,'C')==1,1);
IMPLIED_VOL_0331 = DATA_0331(strcmp(TYPE_0331,'C')==1,10);
BID_0331 = DATA_0331(strcmp(TYPE_0331,'C')==1,4);
ASK_0331 = DATA_0331(strcmp(TYPE_0331,'C')==1,5);
[K_0331,ia_0331,~] = unique(STRIKE_0331); 
C_0331 = (BID_0331 + ASK_0331)/2;
SPD_0331 = STATE_PRICE_DENSITY(C_0331(ia_0331),K_0331,St);

TYPE_0401 = TXT_0401(2:end,4);
STRIKE_0401 = DATA_0401(strcmp(TYPE_0401,'C')==1,1);
IMPLIED_VOL_0401 = DATA_0401(strcmp(TYPE_0401,'C')==1,10);
BID_0401 = DATA_0401(strcmp(TYPE_0401,'C')==1,4);
ASK_0401 = DATA_0401(strcmp(TYPE_0401,'C')==1,5);
C_0401 = (BID_0401 + ASK_0401)/2;
SPD_0401 = STATE_PRICE_DENSITY(C_0401,STRIKE_0401,St);

figure(3)
subplot(2,2,1)
stem(SPD_0303,'filled');
xticks(floor(size(SPD_0303,1)/2));
xticklabels(cellstr(['$',num2str(median(STRIKE_0303))]));
title('03/03/2021');
subplot(2,2,2)
stem(SPD_0305,'filled');
xticks(floor(size(SPD_0305,1)/2));
xticklabels(cellstr(['$',num2str(median(STRIKE_0305))]));
title('03/05/2021');
subplot(2,2,3)
stem(SPD_0329,'filled');
xticks(floor(size(SPD_0329,1)/2));
xticklabels(cellstr(['$',num2str(median(STRIKE_0329))]));
title('03/29/2021');
subplot(2,2,4)
stem(SPD_0401,'filled');
xticks(floor(size(SPD_0401,1)/2));
xticklabels(cellstr(['$',num2str(median(STRIKE_0401))]));
title('04/01/2021');


