DROP TABLE IF EXISTS hallgato;
DROP TABLE IF EXISTS tanulotars;
DROP TABLE IF EXISTS post;
DROP TABLE IF EXISTS csoport;
DROP TABLE IF EXISTS korrepetalas;
DROP TABLE IF EXISTS korrepetalas_resztvevo;
DROP TABLE IF EXISTS csoport_tag;
DROP TABLE IF EXISTS tantargy;

CREATE TABLE hallgato (
  neptun   varchar(6) NOT NULL, 
  firstname     varchar(255) NOT NULL, 
  lastname     varchar(255) NOT NULL,
  email    varchar(255) NOT NULL, 
  password varchar(255) NOT NULL, 
  PRIMARY KEY (neptun));

CREATE TABLE tanulotars (
  hallgatoneptun  varchar(6) NOT NULL, 
  hallgatoneptun2 varchar(6) NOT NULL, 
  PRIMARY KEY (hallgatoneptun, 
  hallgatoneptun2));

CREATE TABLE post (
  id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
  hallgatoneptun varchar(6) NOT NULL,
  tkod varchar(255) NOT NULL,
  body varchar(255) NOT NULL,
  created date NOT NULL,
  FOREIGN KEY(hallgatoneptun) REFERENCES hallgato(neptun),
  FOREIGN KEY(tkod) REFERENCES tantargy(tkod));

CREATE TABLE tantargy (
  tkod varchar(255) NOT NULL, 
  tnev varchar(255) NOT NULL, 
  PRIMARY KEY (tkod));

CREATE TABLE korrepetalas (
  id                INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, 
  korrepetaloneptun varchar(6) NOT NULL, 
  korrepetalasnev   varchar(255) NOT NULL, 
  tkod              varchar(255) NOT NULL, 
  tol               date NOT NULL, 
  ig                date NOT NULL);

CREATE TABLE korrepetalas_resztvevo (
  hallgatoneptun varchar(6) NOT NULL, 
  korrepetalasid integer(10) NOT NULL, 
  FOREIGN KEY(hallgatoneptun) REFERENCES hallgato(neptun),
  FOREIGN KEY(korrepetalasid) REFERENCES korrepetalas(id));

CREATE TABLE csoport (
  id   INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, 
  name varchar(255));

CREATE TABLE csoport_tag (
  hallgatoneptun varchar(6) NOT NULL, 
  csoportid      integer(10) NOT NULL, 
  admin          integer(1) NOT NULL,
  FOREIGN KEY(hallgatoneptun) REFERENCES hallgato(neptun), 
  FOREIGN KEY(csoportid) REFERENCES csoport(id));

