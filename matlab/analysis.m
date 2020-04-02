%% clear memory.
clear;
close all;

%% global path.
addpath(genpath('./'));
load('matlab/features.mat');

%% PCA2
visual2PCA(features(1:8000,:), label);

%% PCA3
visual3PCA(features(1:8000,:), label);