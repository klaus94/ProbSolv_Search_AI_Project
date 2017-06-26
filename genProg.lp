machine(0..2).
time(0..200).
subjob(1, 5, 0, 1).
subjob(2, 1, 1, 1).
subjob(3, 1, 2, 1).
subjob(4, 3, 0, 2).
subjob(5, 1, 1, 2).
subjob(6, 2, 0, 2).
subjob(7, 1, 2, 3).
subjob(8, 2, 1, 3).
subjob(9, 2, 1, 3).
{exec(M, T, J) : time(T), subjob(J, _, M, _)}.
1{exec(M, T, 1):machine(M), time(T), subjob(1, _, M, _)}1.
1{exec(M, T, 2):machine(M), time(T), subjob(2, _, M, _)}1.
1{exec(M, T, 3):machine(M), time(T), subjob(3, _, M, _)}1.
1{exec(M, T, 4):machine(M), time(T), subjob(4, _, M, _)}1.
1{exec(M, T, 5):machine(M), time(T), subjob(5, _, M, _)}1.
1{exec(M, T, 6):machine(M), time(T), subjob(6, _, M, _)}1.
1{exec(M, T, 7):machine(M), time(T), subjob(7, _, M, _)}1.
1{exec(M, T, 8):machine(M), time(T), subjob(8, _, M, _)}1.
1{exec(M, T, 9):machine(M), time(T), subjob(9, _, M, _)}1.
:- exec(M, T1, I1), exec(M, T2, I2), subjob(I1, L, M, _), subjob(I2, _, M, _), I1 < I2, T1 + L > T2.
:- exec(_, T2, J2), exec(_, T1, J1), subjob(J1, L, _, N), subjob(J2, _, _, N), J1 < J2, T1+L > T2.
#minimize { T, L : exec(_, T, J), subjob(J, L, _, _), time(T)}.
#show exec/3.
