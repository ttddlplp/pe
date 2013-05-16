CREATE TABLE pebedba.USERINFORMATION 
   (	UUID VARCHAR(28 ) NOT NULL, 
	ANONYMOUSFLAG INTEGER, 
	DISABLEDFLAG INTEGER, 
	CURRENCYID VARCHAR(6 ), 
	LOCALEID VARCHAR(6 ), 
	LOGIN VARCHAR(255 ) NOT NULL, 
	PASSWORD VARCHAR(255 ), 
	PASSWORDDISABLEDFLAG BOOLEAN DEFAULT FALSE, 
	PASSWORDREMINDER VARCHAR(255 ), 
	REMINDEREMAIL VARCHAR(128 ), 
	NAME VARCHAR(255 ), 
	DESCRIPTION VARCHAR(255 ), 
	LASTMODIFIED DATE, 
	LAST_MODIFIED_BY_USER VARCHAR(50 ), 
	LAST_MODIFIED_BY_PROCESS VARCHAR(50 ) NOT NULL, 
	ACCESSCONTROLGROUP VARCHAR(128 ), 
	ACCESSIPRANGE VARCHAR(255 ), 
	ACCESSINFORMATION BIGINT, 
	SINGLEUSEFLAG INTEGER, 
	PASSWORDMODIFIEDDATE DATE, 
	CREATIONDATE DATE, 
	TITLE VARCHAR(255 ), 
	FIRSTNAME VARCHAR(255 ), 
	LASTNAME VARCHAR(255 ), 
	REFERRER VARCHAR(255 ), 
	ORDERCOUNT INTEGER, 
	VIP BOOLEAN DEFAULT FALSE, 
	COMMENTS VARCHAR(4000 ), 
	ENABLED BOOLEAN DEFAULT TRUE NOT NULL, 
	ACCESSIBILITY_ENABLED VARCHAR(1 ) DEFAULT 'N', 
	LAST_LOGIN DATE, 
	LAST_CHECKOUT DATE, 
	PIN VARCHAR(255 ), 
	IS_TEST_USER BOOLEAN DEFAULT FALSE, 
	 PRIMARY KEY (UUID)
   ) ;
  CREATE UNIQUE INDEX pebedba_USERINFORMATION_IAK1 ON pebedba.USERINFORMATION (LOGIN);
  CREATE INDEX pebedba_USERINFORMATION_IX1 ON pebedba.USERINFORMATION (ACCESSCONTROLGROUP);
  CREATE INDEX pebedba_USERINFORMATION_IX2 ON pebedba.USERINFORMATION (IS_TEST_USER) ;
  CREATE INDEX pebedba_USERINFORMATION_IX3 ON pebedba.USERINFORMATION (LASTMODIFIED);
  