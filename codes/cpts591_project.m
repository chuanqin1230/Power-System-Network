%% cpts 591 element of networkm science research
clc
clear all
load IEEE123.txt
load IEEE13.txt
G13=graph(IEEE13(:,1),IEEE13(:,2),IEEE13(:,4)); % creating the weighted graph
plot(G13,'EdgeLabel',G13.Edges.Weight)
%% Analysis on IEEE 13 topological analysis
[Wt Dt]=compute_WD(IEEE13(:,[1 2]),IEEE13(:,3));

% computing Laplacain
Lt=Dt-Wt; % unnormalized admittance matrix
Lnt=Dt^-0.5*Lt*Dt^-0.5; % nomralized
[Rvt,lambdat,~]=eig(Lnt,'vector');
[lambdats,It]=sort(lambdat);

% now computing the eigen gap
indx=find(lambdats>0.001);% finding the index of first nonzero eigenvalue
eigengap=(lambdats(indx(2):end)-lambdats(indx(1):end-1))./lambdats(indx(1):end-1);
Xt=Rvt(:,indx(1:ceil(max(eigengap))));
k=ceil(max(eigengap));% number of cluster
idxt=spectralcluster(Xt,k);
gscatter(Xt(:,1),Xt(:,2),idxt);

%% Analysis on IEEE 13 node system with admittance matrix as a weight 
[W D]=compute_WD(IEEE13(:,[1 2]),IEEE13(:,4));

% computing Laplacain
L=D-W; % unnormalized admittance matrix
Ln=D^-0.5*L*D^-0.5; % nomralized
[Rv,lambda,~]=eig(Ln,'vector');
[lambdas,I]=sort(lambda);

% now computing the eigen gap
indx=find(lambdas>0.001);% finding the index of first nonzero eigenvalue
eigengap=(lambdas(indx(2):end)-lambdas(indx(1):end-1))./lambdas(indx(1):end-1);
X=Rv(:,indx(1:ceil(max(eigengap))));
k=ceil(max(eigengap));% number of cluster
idx=spectralcluster(X,k);
figure
gscatter(X(:,1),X(:,2),idx);

%% Analysis on IEEE 123 node system 
% topological analysis

[Wt Dt]=compute_WD(IEEE123(:,[1 2]),IEEE123(:,3));

% computing Laplacain
L123t=Dt-Wt; % unnormalized admittance matrix
%Lnt=Dt^-0.5*Lt*Dt^-0.5; % nomralized
[Rv123t,lambda123t,~]=eig(L123t,'vector');
[lambdat123s,I123t]=sort(lambda123t);

% now computing the eigen gap
indx=find(lambdat123s>0.001);% finding the index of first nonzero eigenvalue
eigengap=(lambdat123s(indx(2):end)-lambdat123s(indx(1):end-1))./lambdat123s(indx(1):end-1);

k=ceil(max(eigengap));% number of cluster
if k<2
    k=2;
end
X123t=Rv123t(:,indx(1:k));
idx123t=spectralcluster(X123t,k);
gscatter(X123t(:,1),X123t(:,2),idx123t);

%% Analysis in IEEE9 bus system
load IEEE9.txt
wA=1./IEEE9(:,3); % Admittance as a weight
[W9 D9]=compute_WD(IEEE9(:,[1 2]),wA);
L9=D9-W9; % unnormalized admittance matrix
L9n=D9^-0.5*L9*D9^-0.5; % nomralized
[Rv9,lambda9,~]=eig(L9n,'vector');
[lambda9s,I9]=sort(lambda9);
indx=find(lambda9s>0.001);% finding the index of first nonzero eigenvalue
eigengap9=(lambda9s(indx(2):end)-lambda9s(indx(1):end-1))./lambda9s(indx(1):end-1);

k=ceil(max(eigengap9));% number of cluster
if k<2
    k=2;
end
X9=Rv9(:,indx(1:k));
X9=X9./norm(X9); % normalizing the eigen vetors
idx9=spectralcluster(X9,k);
%gscatter(X9(:,1),X9(:,2),idx9);
%% Analysis based on the powerflow on IEEE9 bus system
wP=1./IEEE9(:,4); % Power as a weight
[Wp9 Dp9]=compute_WD(IEEE9(:,[1 2]),wP);
Lp9=Dp9-Wp9; % unnormalized admittance matrix
L9pn=Dp9^-0.5*Lp9*Dp9^-0.5; % nomralized
[Rvp9,lambdap9,~]=eig(L9pn,'vector');
[lambdap9s,Ip9]=sort(lambdap9);
indx=find(lambdap9s>0.001);% finding the index of first nonzero eigenvalue
eigengapp9=(lambdap9s(indx(2):end)-lambdap9s(indx(1):end-1))./lambdap9s(indx(1):end-1);

k=floor(max(eigengapp9));% number of cluster
if k<2
    k=2;
end
Xp9=Rvp9(:,indx(1:k));
Xp9=Xp9./norm(Xp9); % normalizing the eigen vetors
idxp9=spectralcluster(Xp9,k);
gscatter(Xp9(:,1),Xp9(:,2),idxp9);
%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
function [Wt Dt]=compute_WD(Graph,w)
Wt=zeros(size(Graph,1),size(Graph,1)); % weight matrix 
Dt=zeros(size(Wt));
for ii= 1: length(Wt)
    for jj=1:length(Wt)
        if ii~=jj
            indx=find(ii==Graph(:,1) &jj==Graph(:,2));
            if ~isempty(indx)
            Wt(ii,jj)=w(indx);
            Wt(jj,ii)=Wt(ii,jj);
            end
        end
       Dt(ii,ii)=sum(Wt(ii,:));
    end
end
end