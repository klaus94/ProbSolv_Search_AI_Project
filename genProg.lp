machine(0..1).
time(0..100).
subjob(1, 8, 0, 1).
subjob(2, 8, 1, 1).
subjob(3, 2, 1, 2).
subjob(4, 1, 0, 2).
{exec(M, T, J) : time(T), subjob(J, _, M, _)}.
1{exec(M, T, 1):machine(M), time(T), subjob(1, _, M, _)}1.
1{exec(M, T, 2):machine(M), time(T), subjob(2, _, M, _)}1.
1{exec(M, T, 3):machine(M), time(T), subjob(3, _, M, _)}1.
1{exec(M, T, 4):machine(M), time(T), subjob(4, _, M, _)}1.
:- exec(M, T1, I1), exec(M, T2, I2), subjob(I1, L, M, _), subjob(I2, _, M, _), I1 < I2, T1 + L > T2.
:- exec(_, T2, J2), exec(_, T1, J1), subjob(J1, L, _, N), subjob(J2, _, _, N), J1 < J2, T1+L > T2.
#minimize { T, L : exec(_, T, J), subjob(J, L, _, _), time(T)}.
#show exec/3.
