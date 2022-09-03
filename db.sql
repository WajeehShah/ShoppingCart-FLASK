BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "cart" (
	"image"	text,
	"team"	text,
	"qty"	integer,
	"price"	integer,
	"subtotal"	integer,
	"id"	INTEGER,
	"uid"	text
);
CREATE TABLE IF NOT EXISTS "users" (
	"id"	SERIAL NOT NULL,
	"username"	text NOT NULL,
	"password"	text NOT NULL,
	"fname"	text,
	"lname"	text,
	"email"	text,
	PRIMARY KEY("id")
);
CREATE TABLE IF NOT EXISTS "shirts" (
	"id"	SERIAL NOT NULL,
	"team"	text,
	"image"	text,
	"price"	integer,
	"onsale"	integer,
	"onsaleprice"  integer,
	"kind"	text,
	"continent"	text,
	PRIMARY KEY("id")
);
CREATE TABLE IF NOT EXISTS "purchases" (
	"uid"	text,
	"team"	text,
	"image"	text,
	"quantity"	integer,
	"id"	INTEGER,
	"date"	date NOT NULL DEFAULT CURRENT_DATE
);
INSERT INTO "shirts" VALUES (1,'Argentina','argentina.png',1789.0,0,1789.0,'national','americas'),
 (2,'Brazil','brasil.jpg',1889.0,0,1889.0,'national','americas'),
 (3,'Peru','peru.jpg',1779.0,1,1669.0,'national','americas'),
 (4,'France','france.jpg',1589.0,0,1589.0,'national','europe'),
 (5,'Mexico','mexico.jpg',1279.0,0,1279.0,'national','americas'),
 (6,'Spain','spain.jpg',1999.0,0,1999.0,'national','europe'),
 (7,'Senegal','senegal.jpg',1679.0,0,1679.0,'national','africa'),
 (8,'Belgium','belgium.png',1889.0,1,1579.0,'national','europe');
COMMIT;
