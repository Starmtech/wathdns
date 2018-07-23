#!/usr/bin/python
#-*- coding: utf-8 -*-
import socket
import sys
import os
import dns.resolver
import sqlite3

def request(dnsr, domain, records):
   try:
      Resolver = dns.resolver.Resolver()
      Resolver.nameservers = [dnsr]
      Resolver = dns.resolver.query(domain, records)
      for rdata in Resolver:
         if records in "A":
#            print 'IPv4:',rdata.address
            data = rdata.address
         elif records in "AAAA":
#            print 'IPv4:',rdata.address
            data = rdata.address
         elif records in "MX":
#            print 'Mail :',rdata.exchange,'preference:',rdata.preference
            data = rdata.exchange
         elif records in "TXT":
#            print rdata.to_text()
            data = rdata.to_text()
         elif records in "CNAME":
#            print rdata.to_text()
            data = rdata.to_text()
         else:
            print 'records not recognized'
         return data
   except dns.resolver.NoAnswer:
      print 'no-records'
   except dns.resolver.NXDOMAIN:
      print 'no-dns'


def bdd(country,limit):
   try:
      iplist = []
      countrylist = []
      conn = sqlite3.connect('/opt/wathdns/wathdns.db')
      cursor = conn.cursor()

      if len(country) == 2:
         if limit == 0:
            cursor.execute(" SELECT * FROM dns WHERE country_id = ?;", (country,))
         else:
            cursor.execute(" SELECT * FROM dns WHERE country_id = ? LIMIT ?;", (country,limit))
      else:
         if limit == 0:
            cursor.execute(" SELECT * FROM dns ")
         else:
            cursor.execute(" SELECT * FROM dns LIMIT ?;", (limit,))
      rows = cursor.fetchall()
      for row in rows:
         ip = '{0}'.format(row[0])
         country = '{0}'.format(row[2])
         iplist.append(ip)
         countrylist.append(country)
   except Exception as e:
      conn.rollback()
   finally:
      conn.close()
   return iplist, countrylist


def coloriage(s, color, bold=False):
   colors = {'red': 31, 'green': 32, 'yellow': 33,
             'blue': 34, 'magenta' : 36}
   if os.getenv('ANSI_COLORS_DISABLED') is None and color in colors:
       if bold:
           return '\033[1m\033[%dm%s\033[0m' % (colors[color], s)
       else:
           return '\033[%dm%s\033[0m' % (colors[color], s)
   else:
       return s


def help():
   print("\n")
   print("                    Aide pour l'utilisation du script:             ")
   print("-------------------------------------------------------------------")
   print(" exemple: wathdns -d starmtech.fr -r A -c FR")
   print(" ")
   print("  -d --domain :  indiquer le domaine ")
   print(" ")
   print("  -r --record : indiquer un record exemple : wathdns -r MX")
   print(" ")
   print("  -c --country : indiquer l'accronyme de votre pays")
   print(" ")
   print("  -l --limit : permet de definir un nombre limite de dns a tester")
   print(" ")
   print("  -h --help : permet d'obtenir de l'aide")
   print("-------------------------------------------------------------------")
   print("\n")


def tableau(lines, separate_head=True):
    larg = []
    for line in lines:
       for i,size in enumerate([len(x) for x in line]):
          while i >= len(larg):
             larg.append(0)
          if size > larg[i]:
             larg[i] = size
    a = ""
    for i,largs in enumerate(larg):
        a += "{" + str(i) + ":" + str(largs) + "} | "
    if (len(a) == 0):
        return
    a = a[:-3]
    for i,line in enumerate(lines):
        print(a.format(*line))
        if (i == 0 and separate_head):
           print("-"*(sum(larg)+3*(len(larg)-1)))


def demrecord(record):
   ipsrv = 0
   cnsrv = 0
   rtxt = 0
   if record == "A":
       print("Indiquer l'adresse ip du serveur:")
       ipsrv = raw_input()
   elif record in ("AAAA","aaaa"):
      print("Indiquer l'adresse ip du serveur:")
      ipsrv = raw_input()
   elif record in ("MX","mx"):
       print("Indiquer l'adresse ip du serveur Mail:")
       ipsrv = raw_input()
   return (ipsrv, rtxt, cnsrv);

   if record in ("TXT","txt"):
      print("Indiquer l'enregistrement txt:")
      rtxt = raw_input()
      return (ipsrv, rtxt, cnsrv);
   if record in ("CNAME","cname"):
      print("Indiquer l'enregistrement CNAME:")
      cnsrv = raw_input()
      return (ipsrv, rtxt, cnsrv);
   else:
       print "error"


def pourcentage(nbr, total):
   nombre = nbr / total
   nombre = nombre * 100
   return nombre


if __name__ == '__main__':
   rows = []
   result = []
   country = "ALL"
   if 1 != len(sys.argv):
      i = 0
      while i < len(sys.argv):
         if sys.argv[i] in ("-r", "--r"):
            record = sys.argv[i+1]
            print 'Record :', record
         elif sys.argv[i] in ("-h", "--help"):
            help()
         elif sys.argv[i] in ("-c", "--country"):
            country = sys.argv[i+1]
            print 'Country :', country
         elif sys.argv[i] in ("-l", "--limit"):
            limit = sys.argv[i+1]
            print 'limite :', limit
         elif sys.argv[i] in ("-d", "--domain"):
            domain = sys.argv[i+1]
            print 'Domain :', domain
         i = i + 1
   else:
      help()
      sys.exit(0)
   try:
      ipsrv, rtxt, cnsrv = demrecord(record)
   except NameError:
      print("Indiquer un type d'enregistrement DNS 'exemple: A':")
      record = raw_input()
      ipsrv, rtxt, cnsrv = demrecord(record)
   try:
      iplist, countrylist, = bdd(country,limit)
   except NameError:
      limit = 0
      iplist, countrylist, = bdd(country, limit)
   error = reussi = cpt = cmpt = 0
   rows.append(("Nb","Pays","Dns Ip","Ip Serveur","Status"))
   for dnsr in iplist:
      req = request(dnsr, domain, record)
      result.append(req)
      cpt = cpt + 1
      print 'Dns Testé: ', cpt, 'sur ', len(iplist)

   for ipresult in result:
      if ipresult in ipsrv:
         status = coloriage('OK','blue', False)
         reussi = reussi + 1
      else:
         status = coloriage('KO','red', True)
         error = error + 1
      cmpt = cmpt + 1
      rows.append((str(cmpt),country,ipsrv,ipresult,status))
   resultatreussi = pourcentage(reussi, len(iplist))
   resultaterr = pourcentage(error, len(iplist))
   print '\n'
   tableau(rows)
   print 'Error:',  resultaterr, '%'
   print 'Reussi:', resultatreussi, '%'
   print 'Nombre de DNS testé: ', len(iplist)
