@ECHO OFF
FOR %%A IN (*.log) DO IF NOT EXIST %%A.txt ( Macssplit < %%A | MacsRead3510 > %%A.txt )

