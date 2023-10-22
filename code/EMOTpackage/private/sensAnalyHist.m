function [results] = sensAnalyHist(x,y,Tmin,Tmax,fig,verbose)

%% Set EMOT parameters for the sensitivity analysis
opts.thr=0.1;
opts.maxFunEvals = 25000;
opts.maxIter = 25000;
opts.verbose = false;
tOpt = 22;
opts.F0iidtol = 0.005;

%% Remove 10% of initial points from xy
y(y<=opts.thr) = NaN;x((isnan(y))) = NaN; x(isnan(x))=[];y(isnan(y))=[];

%% Run EMOT over different T
if verbose, fprintf('@@ Optimizing T'), end
c=0; countNaN=0; D=[];
for k=Tmin:2:Tmax
    if verbose, fprintf('.');end, c=c+1;
    opts.binHist=k; 
    res(c) = EMOT(x,y,opts);
    if isnan(res(c).fail), countNaN=countNaN+1;end
    if ~isnan(res(c).fail)
        countNaN=0; 
        D = [D; k 0 res(c).psi res(c).csi res(c).zeta1 res(c).zeta2];
    end
    if countNaN>3, break, end
end
clear res opts

%% Compute best T
C = [(roundN(D(:,5),2)>roundN(D(:,6),2)) (roundN(D(:,5),2)<roundN(D(:,6),2)) (roundN(D(:,5),2)==roundN(D(:,6),2))];
[~,f] = max(sum(C)); iid = C(:,f); Dd = D(iid,:); 
tBest = zeros(1,3);
if median(Dd(:,4))>0.1, tBest(1) = max(D(find(abs(Dd(:,4)-median(Dd(:,4)))==min(abs(Dd(:,4)-median(Dd(:,4))))),1)); end % with respect to: CSI
if median(Dd(:,5))>0.1, tBest(2) = max(D(find(abs(Dd(:,5)-median(Dd(:,5)))==min(abs(Dd(:,5)-median(Dd(:,5))))),1)); end % with respect to: ZETA1
if median(Dd(:,6))>0.1, tBest(3) = max(D(find(abs(Dd(:,6)-median(Dd(:,6)))==min(abs(Dd(:,6)-median(Dd(:,6))))),1)); end % with respect to: ZETA2
tBest = tBest(tBest>0); 
if ~isempty(tBest)
    tOpt = roundN(mean(tBest),2); if mod(tOpt,2), tOpt=tOpt-1;end
    accOpt = (sum(C(:,f))/length(C(:,f)))*100; %compute accuracy of the bestT
else
    try tOpt = max(D(find(abs(Dd(:,3)-median(Dd(:,3)))==min(abs(Dd(:,3)-median(Dd(:,3))))),1)); end % with respect to: PSI
    accOpt=NaN;
end
if verbose, fprintf('done: %d',tOpt);fprintf('(%3.1f%%)',accOpt);fprintf('\n'), end
%D Dd [tBest tOpt accOpt] [median(Dd(:,3)) median(Dd(:,4)) median(Dd(:,5)) median(Dd(:,6))]

%% Save results
results.data = D;
results.T = tOpt;
results.acc = accOpt;

%% Graphics
if fig
figure(1);scatter(x,y);axis([-1.2 1.2 0 1.05])
hold on;plot([1,1]*0,ylim,'k-.','LineWidth',1);plot(x(end),y(end),'r.');

hFig = figure(2);
set(hFig, 'Position', [20 100 1000 600], 'Color',[0.8 0.8 0.8])
subplot(2,2,4);scatter(Dd(:,1),Dd(:,6),'b.');title(['\fontsize{17} \bf \upsilon_2'])
hold on;plot(Dd(:,1),Dd(:,6),'b-')
hold on;plot(xlim,[1,1]*mean(Dd(:,6)),'r-.','LineWidth',2);
hold on;plot(xlim,[1,1]*median(Dd(:,6)),'g-.','LineWidth',2);
hold on;plot(xlim,[1,1]*quantile(Dd(:,6),0.95),'k-.','LineWidth',2);
hold on;plot(xlim,[1,1]*quantile(Dd(:,6),0.05),'k-.','LineWidth',2);
%hold on;plot(xlim,[1,1]*quantile(Dd(:,6),0.70),'y-.','LineWidth',2);
try xlabel(['median: ' num2str(roundN(median(Dd(:,6)),3)) ', best-T: ' num2str(tBest(3))]), catch xlabel(['median: NA, best-T: NA']), end

subplot(2,2,3);scatter(Dd(:,1),Dd(:,5),'b.');title(['\fontsize{17} \bf \upsilon_1'])
hold on;plot(Dd(:,1),Dd(:,5),'b-')
hold on;plot(xlim,[1,1]*mean(Dd(:,5)),'r-.','LineWidth',2);
hold on;plot(xlim,[1,1]*median(Dd(:,5)),'g-.','LineWidth',2);
hold on;plot(xlim,[1,1]*quantile(Dd(:,5),0.95),'k-.','LineWidth',2);
hold on;plot(xlim,[1,1]*quantile(Dd(:,5),0.05),'k-.','LineWidth',2);
%hold on;plot(xlim,[1,1]*quantile(Dd(:,5),0.70),'y-.','LineWidth',2);
try xlabel(['median: ' num2str(roundN(median(Dd(:,5)),3)) ', best-T: ' num2str(tBest(2))]), catch xlabel(['median: NA, best-T: NA']), end

subplot(2,2,2);scatter(Dd(:,1),Dd(:,4),'b.');title(['\fontsize{17} \bf \xi'])
hold on;plot(Dd(:,1),Dd(:,4),'b-')
hold on;plot(xlim,[1,1]*mean(Dd(:,4)),'r-.','LineWidth',2);
hold on;plot(xlim,[1,1]*median(Dd(:,4)),'g-.','LineWidth',2);
hold on;plot(xlim,[1,1]*quantile(Dd(:,4),0.95),'k-.','LineWidth',2);
hold on;plot(xlim,[1,1]*quantile(Dd(:,4),0.05),'k-.','LineWidth',2);
%hold on;plot(xlim,[1,1]*quantile(Dd(:,4),0.70),'y-.','LineWidth',2);
try xlabel(['median: ' num2str(roundN(median(Dd(:,4)),3)) ', best-T: ' num2str(tBest(1))]), catch xlabel(['median: NA, best-T: NA']), end

subplot(2,2,1);scatter(Dd(:,1),Dd(:,3),'b.');title(['\fontsize{17} \bf \psi'])
hold on;plot(Dd(:,1),Dd(:,3),'b-')
hold on;plot(xlim,[1,1]*mean(Dd(:,3)),'r-.','LineWidth',2);
hold on;plot(xlim,[1,1]*median(Dd(:,3)),'g-.','LineWidth',2);
hold on;plot(xlim,[1,1]*quantile(Dd(:,3),0.95),'k-.','LineWidth',2);
hold on;plot(xlim,[1,1]*quantile(Dd(:,3),0.05),'k-.','LineWidth',2);
%hold on;plot(xlim,[1,1]*quantile(Dd(:,3),0.70),'y-.','LineWidth',2);    
end

end