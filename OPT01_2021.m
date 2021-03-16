% OPTION PRICING
mu = 0.15;
sigma = 0.30;
Delta_t = 0.192; % 1/52 years = 1 week
T = 100;
S = zeros(T,1); 
Delta_S = zeros(T,1);
for s = 2 : T
    var_eps = randn;
    Delta_S(s) = mu*Delta_t*S(s)+sigma*sqrt(Delta_t)*var_eps;
    S(s)= S(s-1)+Delta_S(s);
end
figure(1)
subplot(2,1,1)
plot(S)
subplot(2,1,2)
plot(Delta_S)

M = 10;
S = zeros(T,M); 
Delta_S = zeros(T,M);
for m = 1 : M
    for s = 2 : T
        var_eps = randn;
        Delta_S(s,m) = mu*Delta_t*S(s,m)+sigma*sqrt(Delta_t)*var_eps;
        S(s,m)= S(s-1,m)+Delta_S(s,m);
    end
end
figure(2)
subplot(2,1,1)
plot(S)
subplot(2,1,2)
plot(Delta_S)