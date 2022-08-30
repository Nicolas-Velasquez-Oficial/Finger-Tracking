function [] = plotResults(x,y,res,pars,subj,names,time)


%% Computing useful graphic parameters
xC2 = linspace(angleX(pars.d(1),pars.d(2)), angleX(pars.a(1),pars.a(2)),100);
xC1 = linspace(angleX(-pars.b(1),pars.b(2)), angleX(-pars.c(1),pars.c(2)),100);
rescaled_xC2 = xC2' + repmat(360-180,length(xC2),1);
rescaled_xC2(rescaled_xC2>=360) = rescaled_xC2(rescaled_xC2>=360) - 360;
rescaled_xC1 = xC1' + repmat(360-180,length(xC1),1);
rescaled_xC1(rescaled_xC1>=360) = rescaled_xC1(rescaled_xC1>=360) - 360;
pols_xC1_rad = degtorad(rescaled_xC1); pols_xC2_rad = degtorad(rescaled_xC2);
radians_lbls = [pols_xC1_rad(1) pols_xC2_rad(end)];
radians_lbls2 = [pols_xC1_rad pols_xC2_rad];
k = find(res.xHist==median(res.xHist));
xHist_zeta1 = res.xHist(1:k-1); xHist_zeta2 = res.xHist(k+1:end);



%% Create figure
close all
hFig = figure(1);
set(hFig, 'Position', [20 100 1200 600], 'Color',[0.8 0.8 0.8],'Name','EMOT analysis')

%% Empirical mouse-movements
subplot(3,7,[1 10]);hold on
rectangle('Position',[pars.c(1), pars.c(2), abs(pars.c(1)-pars.b(1)),abs(pars.d(2)-pars.c(2))],'LineWidth',1,'LineStyle','--','FaceColor',[1,1,1])
rectangle('Position',[-pars.b(1), pars.b(2), abs(pars.c(1)-pars.b(1)),abs(pars.d(2)-pars.c(2))],'LineWidth',1,'LineStyle','--','FaceColor',[1,1,1])
text(pars.b(1)-0.1,pars.d(2)+0.05,'C2','Color','black','FontSize',14,'FontName','Arial')
text(-pars.b(1),pars.d(2)+0.05,'C1','Color','black','FontSize',14,'FontName','Arial')
text(pars.c(1)+0.05,pars.d(2)/1.15,upper(names(1)),'Color','black','FontSize',17,'FontName','Arial')
text(-pars.b(1)+0.05,pars.d(2)/1.15,upper(names(2)),'Color','black','FontSize',17,'FontName','Arial')
text(x(1)-0.17,y(1)-0.17,upper(names(3)),'Color','black','FontSize',17,'FontName','Arial')
xlim([-pars.b(1)-0.3 pars.b(1)+0.3]);
ylim([0 pars.d(2)+0.2])
scatter(x,y,'b')
plot(linspace(-2,2,200),res.thr)
title(['\fontsize{18} Participant ID: '    num2str(subj)],'fontweight','bold','FontName','Arial')

%% Histogram H_theta and H_theta0
subplot(3,7,[4 13]);hold on
bar(res.xHist,(res.H_theta/sum(res.H_theta)),1,'facecolor',[0.6 0.6 0.6])
bar(res.xHist,(res.H_theta0/sum(res.H_theta0)+1e-19),1,'facecolor',[0.9 0.9 0.9])
xlim([min(res.xHist)-0.20 max(res.xHist)+0.20])
plot(radians_lbls2(:,2),0,'-ks','markers',2,'Color', [0.05 0.05 0.05]);plot(radians_lbls2(:,1),0,'-ks','markers',2,'Color', [0.05 0.05 0.05])
text(mean(radians_lbls2(:,1)),-0.028,'C1','Color','black','FontSize',14,'FontName','Arial')
text(mean(radians_lbls2(:,2)),-0.028,'C2','Color','black','FontSize',14,'FontName','Arial')
legend('\fontsize{15} H_\theta','\fontsize{15} H_{\theta0}','Location','northoutside','Orientation','horizontal')
legend('boxoff')

%% Histograms CSI
subplot(3,7,[17.5 18.5]);hold on
bar(res.xHist,res.tau,1,'facecolor',[0.9 0.9 0.9])
legend('\fontsize{15}\tau','Location','northoutside','Orientation','vertical')
legend('boxoff')
xlim([min(res.xHist)-0.20 max(res.xHist)+0.20])

%% Histograms ZETA1 e ZETA2
subplot(3,7,[19.5 20.5]);hold on
bar(xHist_zeta1,res.u1,1,'facecolor',[0.9 0.9 0.9])
bar(xHist_zeta2,res.u2,1,'facecolor',[0.6 0.6 0.6])
legend('\fontsize{14}\upsilon_{ 1}','\fontsize{14}\upsilon_{ 2}','Location','northoutside','Orientation','horizontal')
legend('boxoff')
xlim([min(xHist_zeta1)-0.20 max(xHist_zeta2)+0.20])

%% Text of results
fontText=16;
subplot(3,7,[15]);hold on; axis('off'); 
text(0,0.8,['\psi = ' num2str(res.psi)],'Color','black','FontSize',fontText,'FontName','Arial')
text(1.4,0.8,['\xi = ' num2str(res.csi)],'Color','black','FontSize',fontText,'FontName','Arial')
text(0,0.6,['\zeta = ' num2str(res.zeta)],'Color','black','FontSize',fontText,'FontName','Arial')
text(1.4,0.55,['\zeta_{ 1} = ' num2str(res.zeta1)],'Color','black','FontSize',fontText,'FontName','Arial')
text(0,0.35,['\zeta_{ 2} = ' num2str(res.zeta2)],'Color','black','FontSize',fontText,'FontName','Arial')
text(1.4,0.4,['t = ' num2str(time(1)) ' (' num2str(time(2)) ') ms'],'Color','black','FontSize',fontText,'FontName','Arial')




end