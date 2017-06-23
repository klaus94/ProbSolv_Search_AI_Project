% data

machine(1..2).
time(1..20).
subjob(1, 5, 1, 1).   % (index, length, machine, main_job)
subjob(2, 10, 2, 1).
subjob(3, 1, 1, 2).
subjob(4, 1, 2, 2).


% generator

{exec(M, T, J) : time(T), subjob(J, _, M, _)}.				% exec(machine, starttime, subjob-index)


% constraints

% each job will be executed
1{exec(M, T, 1):machine(M), time(T), subjob(1, _, M, _)}1.
1{exec(M, T, 2):machine(M), time(T), subjob(2, _, M, _)}1.
1{exec(M, T, 3):machine(M), time(T), subjob(3, _, M, _)}1.
1{exec(M, T, 4):machine(M), time(T), subjob(4, _, M, _)}1.

% one job at a time
:- exec(M, T1, I1), exec(M, T2, I2), subjob(I1, L, M, _), subjob(I2, _, M, _), I1 < I2, T1 + L > T2.

% one subjob can start after its predecessor finished
T1+L < T2 :- exec(_, T1, J1), exec(_, T2, J2), subjob(J1, L, _, Nr), subjob(J2, _, _, Nr), J1 < J2.


% todo: optimizer ...

#show exec/3.