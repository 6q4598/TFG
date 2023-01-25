PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
CREATE TABLE esp32_table (
ID integer primary key autoincrement,
date default current_timestamp,
OK string, TempsOK string,
NOK string, TempsNOK string,
Auto string, Error string,
TempsError string,
DI1 string, TempsDI1 string, DI2 string, TempsDI2 string, DI3 string, TempsDI3 string, DI4 string, TempsDI4 string, DI5 string, TempsDI5 string, DI6 string, TempsDI6 string, DI7 string, TempsDI7 string, DI8 string, TempsDI8 string, DI9 string, TempsDI9 string, DI10 string, TempsDI10 string);
INSERT INTO esp32_table VALUES(1,'2023-01-18 17:08:18',NULL,NULL,NULL,NULL,NULL,NULL,NULL,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0);
INSERT INTO esp32_table VALUES(2,'2023-01-18 17:23:26',NULL,NULL,NULL,NULL,NULL,NULL,NULL,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0);
INSERT INTO esp32_table VALUES(3,'2023-01-18 17:36:27',NULL,NULL,NULL,NULL,NULL,NULL,NULL,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0);
DELETE FROM sqlite_sequence;
INSERT INTO sqlite_sequence VALUES('esp32_table',3);
COMMIT;
