%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% EMOT Package v.1.0 (2016/04/25)                                                    
% by Antonio Calcagnì
% Dep. of Psychology and Cognitive Science, University of Trento (Italy)
% email: ant.calcagni@gmail.com
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

function [res] = EMOT_main(X,Y,analysis,graphic,saveFileName,options)


%% Useful parameters
if~exist('NUM_MVS'), NUM_MVS = computeNUM_MVS(X); end
if~exist('RTS'), time = [0 0]; else time = [0 0]; end %de-activated for now
try outs = evalin('base','outs'); catch, outs=[]; end
g=str2num(num2str(analysis{2}));   
if isempty(saveFileName), fileName = 'EMOT.results'; else fileName = saveFileName; end

%% EMOT routine
fprintf('\n');disp('==================== EMOT v.1.0 ==================================');
switch analysis{1}
    
    case 'single', i=g(1); fprintf('\n');disp(['@ Single trial analysis: Data id. ' num2str(i)]);
        x=X(i,1:NUM_MVS(i)); y=Y(i,1:NUM_MVS(i));
        res = EMOT(x,y,options);
        if graphic && ~res.fail 
            X0=X;Y0=Y; X0(outs,:)=[];Y0(outs,:)=[]; pars=clickArea(X0,Y0,NUM_MVS); names = {'', '', ''}; 
            plotResults(X(i,1:NUM_MVS(i)),Y(i,1:NUM_MVS(i)),res,pars,i,names,time); 
        end
        

    case 'group',
        for i=g(1):g(2), fprintf('\n');disp(['@ Group analysis: Data id. ' num2str(i)]);
            res{i} = EMOT(X(i,1:NUM_MVS(i)),Y(i,1:NUM_MVS(i)),options); 
            tosave(i,:) = [i res{i}.psi res{i}.csi res{i}.zeta1 res{i}.zeta2]; end
        csvwrite([fileName '_' date '_' datestr(clock,13) '.csv'],tosave)
        save([fileName '_' date '_' datestr(clock,13) '.mat'],'res')
      
end
fprintf('\n');disp('==================================================================');
end
