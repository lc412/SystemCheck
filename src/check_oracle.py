#!/bin/env python
# -*- coding: utf-8 -*- 
import os, sys, string
import cx_Oracle as orcl
from check_conf import * 

#add by freeeyes

#��ѯ��ǰ������Ϣ
def L_Oracle_Online_Info(objOracleDBInfo):
	try:
		strOnlineText = ""
		strOnlineRote = ""
		strOnlineAll  = ""
		strOnline     = ""
		
		dsn = orcl.makedsn(objOracleDBInfo.m_strHostIP, objOracleDBInfo.m_strPort, objOracleDBInfo.m_strsid)
		con = orcl.connect(objOracleDBInfo.m_strUserName, objOracleDBInfo.m_strPassword, dsn)
		cursor = con.cursor()
		
		#��õ�ǰ������
		strSql = "select (aaa.onlinenum/bbb.allnum)*100 from \
				(select count(*) as onlinenum \
				from corp_info a,corp_car_info b,terminal_info c \
				where a.corp_no=b.corp_no and b.terminal_id=c.terminal_id \
				and a.status=0 and b.status=0 and c.status=0 \
				and c.onlineflag=1 and a.prov_code='991') aaa, \
				(select count(*) as allnum \
				from corp_info a,corp_car_info b,terminal_info c \
				where a.corp_no=b.corp_no and b.terminal_id=c.terminal_id \
				and a.status=0 and b.status=0 and c.status=0 \
				and a.prov_code='991' ) bbb"
		cursor.execute(strSql);
		
		result = cursor.fetchall()
		#print("Total: " + str(cursor.rowcount))

		for row in result:
			#print("data=%s" %(row))
			strOnlineRote = str(row[0])
			#print("strOnlineRote=%s" %(strOnlineRote))
			break
		
		#��õ�ǰ�ĳ�������
		strSql = "select count(*) as allnum \
				from corp_info a,corp_car_info b,terminal_info c \
				where a.corp_no=b.corp_no and b.terminal_id=c.terminal_id \
				and a.status=0 and b.status=0 and c.status=0 \
				and a.prov_code='991'"
		
		cursor.execute(strSql);
		result = cursor.fetchall()
		#print("Total: " + str(cursor.rowcount))

		for row in result:
			#print("data=%s" %(row))
			strOnlineAll = str(row[0])	
			break
			
		#��õ�ǰ���߳�������
		strSql = "select count(*) \
				from corp_info a,corp_car_info b,terminal_info c \
				where a.corp_no=b.corp_no and b.terminal_id=c.terminal_id \
				and a.status=0 and b.status=0 and c.status=0 \
				and c.onlineflag=1 and a.prov_code='991'"
		
		cursor.execute(strSql);
		result = cursor.fetchall()
		#print("Total: " + str(cursor.rowcount))

		for row in result:
			#print("data=%s" %(row))
			strOnline = str(row[0])
			break
		
		cursor.close()
		con.close()
		
		strOnlineText = "������:" + strOnlineRote + ",�ܹ�����:" + strOnlineAll + ",��ǰ���߳���:" + strOnline
		print strOnlineText
		return strOnlineText
	except Exception,e:
		return ""

#��ѯ����
def L_Oracle_DeadLock_Info(objOracleDBInfo):
	try:
		strDeadLockText = ""
		dsn = orcl.makedsn(objOracleDBInfo.m_strHostIP, objOracleDBInfo.m_strPort, objOracleDBInfo.m_strsid)
		con = orcl.connect(objOracleDBInfo.m_strUserName, objOracleDBInfo.m_strPassword, dsn)
		cursor = con.cursor()

		#�������״̬
		strSql = "select \
				p.spid,a.serial#, c.object_name,b.session_id, \
				b.oracle_username,b.os_user_name \
				from v$process p,v$session a, v$locked_object b,all_objects c \
				where p.addr=a.paddr and a.process=b.process and c.object_id=b.object_id"		
		
		cursor.execute(strSql);
		result = cursor.fetchall()
		#print("Total: " + str(cursor.rowcount))

		for row in result:
			strDeadLockText = strDeadLockText + "<p>" + str(row[0])	+ "</p>"	
		
		cursor.close()
		con.close()
		
		if(strDeadLockText == ""):
			strDeadLockText = "û������"
		print strDeadLockText
		return strDeadLockText		
	except Exception,e:
		return ""	
		
#��ѯ���ռ�ʹ��
def L_Oracle_TableUsed_Info(objOracleDBInfo):
	try:
		strTableText = []
		dsn = orcl.makedsn(objOracleDBInfo.m_strHostIP, objOracleDBInfo.m_strPort, objOracleDBInfo.m_strsid)
		con = orcl.connect(objOracleDBInfo.m_strUserName, objOracleDBInfo.m_strPassword, dsn)
		cursor = con.cursor()

		#�������״̬
		strSql = "SELECT A.TABLESPACE_NAME, A.BYTES/1024/1024/1024 \"TOTAL(G)\", B.BYTES/1024/1024/1024 \"USED(G)\", \
				C.BYTES/1024/1024/1024 \"FREE(G)\", (B.BYTES*100)/A.BYTES \"% USED\",(C.BYTES*100)/A.BYTES \"% FREE\" \
				FROM SYS.SM$TS_AVAIL A,SYS.SM$TS_USED B,SYS.SM$TS_FREE C \
				WHERE A.TABLESPACE_NAME=B.TABLESPACE_NAME AND A.TABLESPACE_NAME=C.TABLESPACE_NAME"		
		
		cursor.execute(strSql);
		result = cursor.fetchall()
		#print("Total: " + str(cursor.rowcount))

		for row in result:
			strTableText.append(str(row))
		
		cursor.close()
		con.close()
		
		#print "len(strTableText)=" + str(len(strTableText))
		for i in range(0, len(strTableText)):
			print strTableText[i]
		return strTableText		
	except Exception,e:
		return ""		
		
#��ѯ�û��˺�ʹ��
def L_Oracle_User_Info(objOracleDBInfo):
	try:
		strUserText = []
		dsn = orcl.makedsn(objOracleDBInfo.m_strHostIP, objOracleDBInfo.m_strPort, objOracleDBInfo.m_strsid)
		con = orcl.connect(objOracleDBInfo.m_strUserName, objOracleDBInfo.m_strPassword, dsn)
		cursor = con.cursor()

		#�������״̬
		strSql = "select username, account_status from dba_users"		
		
		cursor.execute(strSql);
		result = cursor.fetchall()
		#print("Total: " + str(cursor.rowcount))

		for row in result:
			if("CAR" in str(row)):
				strUserText.append(str(row))
		
		cursor.close()
		con.close()
		
		for i in range(0, len(strUserText)):
			print strUserText[i]
		return strUserText		
	except Exception,e:
		return ""	

#��ѯ�û��˺�ʹ��
def L_Oracle_ClientConnect_Info(objOracleDBInfo):
	try:
		strConnectText = []
		dsn = orcl.makedsn(objOracleDBInfo.m_strHostIP, objOracleDBInfo.m_strPort, objOracleDBInfo.m_strsid)
		con = orcl.connect(objOracleDBInfo.m_strUserName, objOracleDBInfo.m_strPassword, dsn)
		cursor = con.cursor()

		#�������״̬
		strSql = "SELECT count(*) FROM v$session"		
		
		cursor.execute(strSql);
		result = cursor.fetchall()
		#print("Total: " + str(cursor.rowcount))

		for row in result:
			strConnectText = "��ǰ����������:" + str(row[0])
		
		cursor.close()
		con.close()
		
		print strConnectText
		return strConnectText		
	except Exception,e:
		return ""

'''		
#���Դ���
if __name__ == "__main__": 
	objOracleDBInfo = COracleDBInfo()
	
	objOracleDBInfo.m_strUserName = "car_admin"
	objOracleDBInfo.m_strPassword = "bdoLts_LwdjM7zh"
	objOracleDBInfo.m_strHostIP   = "10.238.73.52"
	objOracleDBInfo.m_strPort     = "1521"
	objOracleDBInfo.m_strsid      = "m2mdb"

	L_Oracle_Online_Info(objOracleDBInfo)
	L_Oracle_DeadLock_Info(objOracleDBInfo)
	L_Oracle_TableUsed_Info(objOracleDBInfo)
	L_Oracle_User_Info(objOracleDBInfo)
	L_Oracle_ClientConnect_Info(objOracleDBInfo)
'''	