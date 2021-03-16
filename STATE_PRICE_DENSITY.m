function SPD = STATE_PRICE_DENSITY(C,STRIKE,St)
% CONSTRUCT A SPREAD POSITION
% LONG THE CALL AT K1 
% SHORT THE CALL AT K2
N = length(C);
P = zeros(N,1);
for n = 1 : N-1
    if n == 1 
        P(1) = 1-(St-C(1))/STRIKE(1);
    else
        P(n) = 1-(C(n)-C(n-1))/(STRIKE(n)-STRIKE(n-1));
    end
end
P(N) = 1 - sum(P(N-1));
P = sort(P);
SPD = (P(2:N)-P(1:N-1))./(STRIKE(2:N)-STRIKE(1:N-1));
SPD = SPD(isnan(SPD)==0);
SPD = SPD(3:end-1);
end