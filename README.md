# Public NTP Servers

This repository lists public NTP (Network Time Protocol) servers.
The list is sourced from various public resources and aims to provide configuration files for common NTP clients.

**Please note:** Server availability and accuracy can vary. Always verify servers before relying on them for critical applications. Contributions and updates to the list are welcome via pull requests to the `ntp-sources.yml` file.

## The List
|Hostname|AS|Stratum|Location|Owner|Notes|
|---|---|:---:|---|---|---|
|time.google.com|AS15169|2|Google Public NTP|Google|Anycast|
|time1.google.com|AS15169|2|Google Public NTP|Google||
|time2.google.com|AS15169|2|Google Public NTP|Google||
|time3.google.com|AS15169|2|Google Public NTP|Google||
|time4.google.com|AS15169|2|Google Public NTP|Google||
|time.android.com|AS15169|2|Google Public NTP|Google|Anycast|
||
|time.aws.com|AS16509, AS14618, AS399991|2|public Amazon Time Sync Service|Amazon|Anycast|
|amazon.pool.ntp.org|AS16509, AS14618, AS399991|2|public Amazon Time Sync Service|Amazon||
|0.amazon.pool.ntp.org|AS16509, AS14618, AS399991|2|public Amazon Time Sync Service|Amazon||
|1.amazon.pool.ntp.org|AS16509, AS14618, AS399991|2|public Amazon Time Sync Service|Amazon||
|2.amazon.pool.ntp.org|AS16509, AS14618, AS399991|2|public Amazon Time Sync Service|Amazon||
|3.amazon.pool.ntp.org|AS16509, AS14618, AS399991|2|public Amazon Time Sync Service|Amazon||
||
|time.cloudflare.com|AS13335|2|Cloudflare NTP|Cloudflare|Anycast|
||
|time.facebook.com|AS32934|2|Facebook NTP|Facebook|Anycast|
|time1.facebook.com|AS32934|2|Facebook NTP|Facebook||
|time2.facebook.com|AS32934|2|Facebook NTP|Facebook||
|time3.facebook.com|AS32934|2|Facebook NTP|Facebook||
|time4.facebook.com|AS32934|2|Facebook NTP|Facebook||
|time5.facebook.com|AS32934|2|Facebook NTP|Facebook||
||
|time.windows.com|AS8075|2|Microsoft NTP server|Microsoft|Anycast|
||
|time.apple.com|AS714, AS6185|2|Apple NTP server|Apple|Anycast|
|time-macos.apple.com|AS714, AS6185|2|Apple NTP server|Apple||
|time-ios.apple.com|AS714, AS6185|2|Apple NTP server|Apple||
|time1.apple.com|AS714, AS6185|2|Apple NTP server|Apple||
|time2.apple.com|AS714, AS6185|2|Apple NTP server|Apple||
|time3.apple.com|AS714, AS6185|2|Apple NTP server|Apple||
|time4.apple.com|AS714, AS6185|2|Apple NTP server|Apple||
|time5.apple.com|AS714, AS6185|2|Apple NTP server|Apple||
|time6.apple.com|AS714, AS6185|2|Apple NTP server|Apple||
|time7.apple.com|AS714, AS6185|2|Apple NTP server|Apple||
|time.euro.apple.com|AS714, AS6185|2|Apple NTP server|Apple|Europe region|
|time.asia.apple.com|AS714, AS6185|2|Apple NTP server|Apple|Asia region, From comments|
||
|clepsydra.dec.com|Unknown|Unknown|DEC/Compaq/HP|HP||
|clepsydra.labs.hp.com|Unknown|Unknown|DEC/Compaq/HP|HP||
|clepsydra.hpl.hp.com|Unknown|Unknown|DEC/Compaq/HP|HP||
|usno.labs.hp.com|Unknown|Unknown|DEC/Compaq/HP|HP||
||
|time-a-g.nist.gov|AS49, AS104|1|NIST Internet Time Service (ITS)|NIST||
|time-b-g.nist.gov|AS49, AS104|1|NIST Internet Time Service (ITS)|NIST||
|time-c-g.nist.gov|AS49, AS104|1|NIST Internet Time Service (ITS)|NIST||
|time-d-g.nist.gov|AS49, AS104|1|NIST Internet Time Service (ITS)|NIST||
|time-a-wwv.nist.gov|AS49, AS104|1|NIST Internet Time Service (ITS)|NIST||
|time-b-wwv.nist.gov|AS49, AS104|1|NIST Internet Time Service (ITS)|NIST||
|time-c-wwv.nist.gov|AS49, AS104|1|NIST Internet Time Service (ITS)|NIST||
|time-d-wwv.nist.gov|AS49, AS104|1|NIST Internet Time Service (ITS)|NIST||
|time-a-b.nist.gov|AS49, AS104|1|NIST Internet Time Service (ITS)|NIST||
|time-b-b.nist.gov|AS49, AS104|1|NIST Internet Time Service (ITS)|NIST||
|time-c-b.nist.gov|AS49, AS104|1|NIST Internet Time Service (ITS)|NIST||
|time-d-b.nist.gov|AS49, AS104|1|NIST Internet Time Service (ITS)|NIST||
|time.nist.gov|AS49, AS104|1|NIST Internet Time Service (ITS)|NIST|Anycast|
|time-e-b.nist.gov|AS49, AS104|1|NIST Internet Time Service (ITS)|NIST||
|time-e-g.nist.gov|AS49, AS104|1|NIST Internet Time Service (ITS)|NIST||
|time-e-wwv.nist.gov|AS49, AS104|1|NIST Internet Time Service (ITS)|NIST||
|time-nw.nist.gov|AS49, AS104|1|NIST Internet Time Service (ITS)|NIST||
|time-a.nist.gov|AS49, AS104|1|NIST Internet Time Service (ITS)|NIST||
|time-b.nist.gov|AS49, AS104|1|NIST Internet Time Service (ITS)|NIST||
|utcnist.colorado.edu|AS49, AS104|1|NIST Internet Time Service (ITS)|NIST|Operated by University of Colorado for NIST|
|utcnist2.colorado.edu|AS49, AS104|1|NIST Internet Time Service (ITS)|NIST|Operated by University of Colorado for NIST|
||
|ntp1.vniiftri.ru|Unknown|1|VNIIFTRI|VNIIFTRI|Stratum 1|
|ntp2.vniiftri.ru|Unknown|1|VNIIFTRI|VNIIFTRI|Stratum 1|
|ntp3.vniiftri.ru|Unknown|1|VNIIFTRI|VNIIFTRI|Stratum 1|
|ntp4.vniiftri.ru|Unknown|1|VNIIFTRI|VNIIFTRI|Stratum 1|
|ntp.sstf.nsk.ru|Unknown|1|VNIIFTRI|VNIIFTRI|Stratum 1|
|ntp1.niiftri.irkutsk.ru|Unknown|1|VNIIFTRI|VNIIFTRI|Stratum 1|
|ntp2.niiftri.irkutsk.ru|Unknown|1|VNIIFTRI|VNIIFTRI|Stratum 1|
|vniiftri.khv.ru|Unknown|1|VNIIFTRI|VNIIFTRI|Stratum 1|
|vniiftri2.khv.ru|Unknown|1|VNIIFTRI|VNIIFTRI|Stratum 1|
|ntp21.vniiftri.ru|Unknown|2|VNIIFTRI|VNIIFTRI|Stratum 2|
||
|ntp.mobatime.ru|Unknown|1|Mobatime|Mobatime|Stratum 1|
||
|ntp0.ntp-servers.net|Unknown|Unknown|NTP SERVERS|ntp-servers.net||
|ntp1.ntp-servers.net|Unknown|Unknown|NTP SERVERS|ntp-servers.net||
|ntp2.ntp-servers.net|Unknown|Unknown|NTP SERVERS|ntp-servers.net||
|ntp3.ntp-servers.net|Unknown|Unknown|NTP SERVERS|ntp-servers.net||
|ntp4.ntp-servers.net|Unknown|Unknown|NTP SERVERS|ntp-servers.net||
|ntp5.ntp-servers.net|Unknown|Unknown|NTP SERVERS|ntp-servers.net||
|ntp6.ntp-servers.net|Unknown|Unknown|NTP SERVERS|ntp-servers.net||
|ntp7.ntp-servers.net|Unknown|Unknown|NTP SERVERS|ntp-servers.net||
||
|ntp1.stratum1.ru|Unknown|1|Stratum 1 Russia|stratum1.ru|Stratum 1|
|ntp2.stratum1.ru|Unknown|1|Stratum 1 Russia|stratum1.ru|Stratum 1|
|ntp3.stratum1.ru|Unknown|1|Stratum 1 Russia|stratum1.ru|Stratum 1|
|ntp4.stratum1.ru|Unknown|1|Stratum 1 Russia|stratum1.ru|Stratum 1|
|ntp5.stratum1.ru|Unknown|1|Stratum 1 Russia|stratum1.ru|Stratum 1|
||
|ntp1.stratum2.ru|Unknown|2|Stratum 2 Russia|stratum2.ru|Stratum 2, Москва|
|ntp2.stratum2.ru|Unknown|2|Stratum 2 Russia|stratum2.ru|Stratum 2|
|ntp3.stratum2.ru|Unknown|2|Stratum 2 Russia|stratum2.ru|Stratum 2|
|ntp4.stratum2.ru|Unknown|2|Stratum 2 Russia|stratum2.ru|Stratum 2|
|ntp5.stratum2.ru|Unknown|2|Stratum 2 Russia|stratum2.ru|Stratum 2|
||
|stratum1.net|Unknown|1|stratum1.net|stratum1.net|Stratum 1|
||
|ntp.time.in.ua|Unknown|1|time.in.ua|time.in.ua|Stratum 1|
|ntp2.time.in.ua|Unknown|1|time.in.ua|time.in.ua|Stratum 1|
|ntp3.time.in.ua|Unknown|2|time.in.ua|time.in.ua|Stratum 2|
||
|ntp.ru|AS8915|Unknown|Company Delfa Co. Ltd.|Company Delfa Co. Ltd.||
||
|ts1.aco.net|AS1853|Unknown|ACO.net|ACO.net||
|ts2.aco.net|AS1853|Unknown|ACO.net|ACO.net||
||
|ntp1.net.berkeley.edu|AS25|1|Berkeley|University of California, Berkeley|Stratum 1|
|ntp2.net.berkeley.edu|AS25|1|Berkeley|University of California, Berkeley|Stratum 1|
||
|ntp.gsu.edu|AS10631|Unknown|Georgia State University|Georgia State University||
||
|tick.usask.ca|AS22950|Unknown|University of Saskatchewan|University of Saskatchewan||
|tock.usask.ca|AS22950|Unknown|University of Saskatchewan|University of Saskatchewan||
||
|ntp.nsu.ru|AS3335|2|NSU|Novosibirsk State University|Stratum 2|
||
|ntp.psn.ru|AS41783|Unknown|ITAEC|ITAEC||
||
|ntp.rsu.edu.ru|AS47124|1|RSU|Rostov State University|Stratum 1|
||
|ntp.nict.jp|AS9355|1|National Institute of Information and Communications Technology|NICT||
||
|ntp1.jst.mfeed.ad.jp|AS7521|1|INTERNET MULTIFEED CO.|INTERNET MULTIFEED CO.||
|ntp2.jst.mfeed.ad.jp|AS7521|1|INTERNET MULTIFEED CO.|INTERNET MULTIFEED CO.||
|ntp3.jst.mfeed.ad.jp|AS7521|1|INTERNET MULTIFEED CO.|INTERNET MULTIFEED CO.||
||
|x.ns.gin.ntt.net|AS2914|Unknown|NTT|NTT||
|y.ns.gin.ntt.net|AS2914|Unknown|NTT|NTT||
||
|clock.sjc.he.net|AS6939|1|HE.net Public Stratum 1 NTP servers|HE.net|San Jose, CA|
|clock.fmt.he.net|AS6939|1|HE.net Public Stratum 1 NTP servers|HE.net|Fremont, CA|
|clock.nyc.he.net|AS6939|1|HE.net Public Stratum 1 NTP servers|HE.net|New York City, NY|
||
|ntp.fiord.ru|AS28917|Unknown|TRC Fiord|TRC Fiord||
||
|gbg1.ntp.se|AS57021|1|Netnod NTP service|Netnod|Stratum 1, Göteborg|
|gbg2.ntp.se|AS57021|1|Netnod NTP service|Netnod|Stratum 1, Göteborg|
|mmo1.ntp.se|AS57021|1|Netnod NTP service|Netnod|Stratum 1, Malmö|
|mmo2.ntp.se|AS57021|1|Netnod NTP service|Netnod|Stratum 1, Malmö|
|sth1.ntp.se|AS57021|1|Netnod NTP service|Netnod|Stratum 1, Stockholm|
|sth2.ntp.se|AS57021|1|Netnod NTP service|Netnod|Stratum 1, Stockholm|
|svl1.ntp.se|AS57021|1|Netnod NTP service|Netnod|Stratum 1, Sundsvall|
|svl2.ntp.se|AS57021|1|Netnod NTP service|Netnod|Stratum 1, Sundsvall|
|ntp.se|AS57021|1|Netnod NTP service|Netnod|Anycast address for nearest NTP server|
||
|ntp.qix.ca|AS14086|Unknown|QiX NTP|QiX||
|ntp1.qix.ca|AS14086|Unknown|QiX NTP|QiX||
|ntp2.qix.ca|AS14086|Unknown|QiX NTP|QiX||
||
|ntp.yycix.ca|AS396515|Unknown|YYCIX NTP|YYCIX||
||
|ntp.ix.ru|AS43832|1|MSK-IX NTP|MSK-IX|Stratum 1|
||
|ntp1.hetzner.de|AS24940|2|Hetzner Online|Hetzner Online||
|ntp2.hetzner.de|AS24940|2|Hetzner Online|Hetzner Online||
|ntp3.hetzner.de|AS24940|2|Hetzner Online|Hetzner Online||
||
|time-a.as43289.net|AS43289|Unknown|Trabia-Network|Trabia-Network||
|time-b.as43289.net|AS43289|Unknown|Trabia-Network|Trabia-Network||
|time-c.as43289.net|AS43289|Unknown|Trabia-Network|Trabia-Network||
||
|ntp.ripe.net|AS3333|2|RIPE|RIPE NCC||
||
|clock.isc.org|AS1280|1|Internet Systems Consortium|ISC|prev ntp.isc.org|
||
|ntp.time.nl|AS1140|1|TimeNL/SIDN Labs|SIDN Labs|ntp1.time.nl|
|ntppool1.time.nl|AS1140|1|TimeNL/SIDN Labs|SIDN Labs|Preferred, From comments|
|ntppool2.time.nl|AS1140|1|TimeNL/SIDN Labs|SIDN Labs|Preferred, From comments|
||
|ntp0.as34288.net|AS34288|Unknown|Kantonsschule Zug|Kantonsschule Zug||
|ntp1.as34288.net|AS34288|Unknown|Kantonsschule Zug|Kantonsschule Zug||
||
|ntp.ntsc.ac.cn|AS4808, AS9808, AS23724|1|Chinese Academy of Sciences Nation Time Service Center|Chinese Academy of Sciences||
||
|ntp.nat.ms|AS30746|1|Nat Morris|Nat Morris|Stratum 1|
||
|tick.usno.navy.mil|AS747|1|US Naval Observatory|US Navy||
|tock.usno.navy.mil|AS747|1|US Naval Observatory|US Navy||
|ntp2.usno.navy.mil|AS747|1|US Naval Observatory|US Navy||
||
|timekeeper.isi.edu|AS2702|Unknown|ISI|Information Sciences Institute||
||
|rackety.udel.edu|AS300|Unknown|University of Delaware|University of Delaware||
|mizbeaver.udel.edu|AS300|Unknown|University of Delaware|University of Delaware||
||
|otc1.psu.edu|AS38|Unknown|Pennsylvania State University|Pennsylvania State University||
||
|gnomon.cc.columbia.edu|AS117|Unknown|Columbia University|Columbia University||
||
|navobs1.gatech.edu|AS2637|Unknown|Georgia Institute of Technology|Georgia Institute of Technology||
||
|navobs1.wustl.edu|AS288|Unknown|Washington University in St. Louis|Washington University in St. Louis||
||
|now.okstate.edu|AS111|Unknown|Oklahoma State University|Oklahoma State University||
||
|ntp.colby.edu|AS10566|Unknown|Colby College|Colby College||
||
|ntp-s1.cise.ufl.edu|AS5730|Unknown|University of Florida|University of Florida||
||
|bonehed.lcs.mit.edu|AS3|Unknown|MIT LCS|MIT||
||
|level1e.cs.unc.edu|AS2807|Unknown|University of North Carolina at Chapel Hill|University of North Carolina at Chapel Hill||
||
|tick.ucla.edu|AS52|Unknown|University of California, Los Angeles|University of California, Los Angeles||
||
|tick.uh.edu|AS638|Unknown|University of Hawaii|University of Hawaii||
||
|ntpstm.netbone-digital.com|Unknown|Unknown|NetBone Digital|NetBone Digital||
||
|nist1.symmetricom.com|AS3608|1|Microsemi/Symmetricom|Microsemi||
||
|ntp.quintex.com|Unknown|Unknown|Quintex|Quintex||
||
|ntp1.conectiv.com|AS16069|Unknown|Conectiv|Conectiv||
||
|tock.usshc.com|Unknown|Unknown|USSHC|USSHC||
||
|t2.timegps.net|Unknown|Unknown|timegps.net|timegps.net||
||
|gps.layer42.net|AS11491|Unknown|Layer42|Layer42||
||
|ntp-ca.stygium.net|AS3978|Unknown|Stygium|Stygium||
||
|sesku.planeacion.net|Unknown|Unknown|planeacion.net|planeacion.net||
||
|ntp0.nl.uu.net|AS8283|Unknown|KPN International Carrier|KPN International Carrier||
|ntp1.nl.uu.net|AS8283|Unknown|KPN International Carrier|KPN International Carrier||
||
|navobs1.oar.net|Unknown|Unknown|oar.net|oar.net||
||
|ntp-galway.hea.net|AS1213|Unknown|HEAnet|HEAnet|Galway|
||
|ntp1.ona.org|Unknown|Unknown|ona.org|ona.org||
||
|ntp.your.org|Unknown|Unknown|your.org|your.org||
||
|ntp.mrow.org|Unknown|Unknown|mrow.org|mrow.org||
||
|time.fu-berlin.de|AS680|Unknown|Germany|Freie Universitaet Berlin||
|ntps1-0.cs.tu-berlin.de|AS680|Unknown|Germany|Technische Universitaet Berlin||
|ntps1-1.cs.tu-berlin.de|AS680|Unknown|Germany|Technische Universitaet Berlin||
|ntps1-0.uni-erlangen.de|AS680|Unknown|Germany|University of Erlangen-Nuremberg||
|ntps1-1.uni-erlangen.de|AS680|Unknown|Germany|University of Erlangen-Nuremberg||
|ntp1.fau.de|AS680|Unknown|Germany|University of Erlangen-Nuremberg (FAU)|From .de comments|
|ntp2.fau.de|AS680|Unknown|Germany|University of Erlangen-Nuremberg (FAU)|From .de comments|
|ntp.dianacht.de|Unknown|Unknown|Germany|dianacht.de||
|zeit.fu-berlin.de|AS680|Unknown|Germany|Freie Universitaet Berlin||
|ptbtime1.ptb.de|AS1896|1|Germany|PTB||
|ptbtime2.ptb.de|AS1896|1|Germany|PTB||
|rustime01.rus.uni-stuttgart.de|AS680|Unknown|Germany|University of Stuttgart||
|rustime02.rus.uni-stuttgart.de|AS680|Unknown|Germany|University of Stuttgart||
||
|chime1.surfnet.nl|AS1103|Unknown|Netherlands|SURFnet||
|ntp.vsl.nl|AS34929|1|Netherlands|VSL||
||
|asynchronos.iiss.at|AS8401|Unknown|Austria|ACOnet / University of Vienna||
||
|ntp.nic.cz|AS25204|2|Czech Republic|CZ.NIC||
|time.ufe.cz|AS25192|1|Czech Republic|UFE CAS||
||
|ntp.fizyka.umk.pl|AS8805|Unknown|Poland|Nicolaus Copernicus University||
|tempus1.gum.gov.pl|AS43900|1|Poland|GUM||
|tempus2.gum.gov.pl|AS43900|1|Poland|GUM||
||
|ntp1.usv.ro|AS8713|Unknown|Romania|University Stefan cel Mare Suceava||
|ntp3.usv.ro|AS8713|Unknown|Romania|University Stefan cel Mare Suceava||
||
|timehost.lysator.liu.se|AS1653|Unknown|Sweden|Academic Computer Club Lysator||
|time1.stupi.se|Unknown|Unknown|Sweden|stupi.se||
||
|time.nrc.ca|AS573|1|Canada|National Research Council Canada||
|clock.uregina.ca|AS641|Unknown|Canada|University of Regina||
||
|cronos.cenam.mx|AS8017|1|Mexico|CENAM||
|ntp.lcf.mx|Unknown|Unknown|Mexico|lcf.mx||
||
|hora.roa.es|AS31007|1|Spain|ROA||
|minuto.roa.es|AS31007|1|Spain|ROA||
||
|ntp1.inrim.it|AS29109|1|Italy|INRIM||
|ntp2.inrim.it|AS29109|1|Italy|INRIM||
||
|ntp1.oma.be|AS5400|1|Belgium|Royal Observatory of Belgium||
|ntp2.oma.be|AS5400|1|Belgium|Royal Observatory of Belgium||
||
|ntp.atomki.mta.hu|AS197038|2|Hungary|ATOMKI||
||
|ntp.i2t.ehu.eus|AS2110|Unknown|Basque Country|University of the Basque Country (EHU)||
||
|ntp.neel.ch|AS34569|Unknown|Switzerland|Neel Engineering||
||
|ntp.neu.edu.cn|AS4538|Unknown|China|Northeastern University||
||
|ntps1.pads.ufrj.br|AS1553|Unknown|Brazil|Federal University of Rio de Janeiro||
||
|ntp.shoa.cl|AS16299|1|Chile|Hydrographic and Oceanographic Service of the Chilean Navy||
||
|time.esa.int|AS15559|Unknown|International|European Space Agency||
|time1.esa.int|AS15559|Unknown|International|European Space Agency||
||
|ntp.day.ir|AS42337|Unknown|Iran|Day ICT|From comments|
||
|ntp.ubuntu.com|AS201815|2|Ubuntu|Canonical|From comments, Anycast|
||
|ntp.viarouge.net|AS207288|Unknown|France|Hubert Viarouge|From comments|
||
|ntp1.dmz.terryburton.co.uk|Unknown|Unknown|UK|Terry Burton|From comments|
|ntp2.dmz.terryburton.co.uk|Unknown|Unknown|UK|Terry Burton|From comments|
||
|time1.ntp.hr|AS49932|Unknown|Croatia|CARNET|From comments|
|time2.ntp.hr|AS49932|Unknown|Croatia|CARNET|From comments|
|os.ntp.carnet.hr|AS49932|2|Croatia|CARNET|From comments, Stratum 2|
|ri.ntp.carnet.hr|AS49932|2|Croatia|CARNET|From comments, Stratum 2|
|st.ntp.carnet.hr|AS49932|2|Croatia|CARNET|From comments, Stratum 2|
|zg1.ntp.carnet.hr|AS49932|2|Croatia|CARNET|From comments, Stratum 2|
|zg2.ntp.carnet.hr|AS49932|2|Croatia|CARNET|From comments, Stratum 2|
||
|stdtime.gov.hk|AS4780|1|Hong Kong|Hong Kong Observatory|From comments|
||
|ntp5.leontp.com|Unknown|Unknown|UK|Leo Bodnar|From comments|
|ntp6.leontp.com|Unknown|Unknown|UK|Leo Bodnar|From comments|
|ntp7.leontp.com|Unknown|Unknown|UK|Leo Bodnar|From comments|
|ntp8.leontp.com|Unknown|Unknown|UK|Leo Bodnar|From comments|
|ntp9.leontp.com|Unknown|Unknown|UK|Leo Bodnar|From comments|
|timekeeper.webwiz.net|AS44929|Unknown|UK|Web Wiz|From comments|
|ntp.theitman.uk|Unknown|Unknown|UK|TheITMan|From comments|
|eshail.batc.org.uk|Unknown|Unknown|UK|BATC|From comments|
||
|ntp.heppen.be|Unknown|Unknown|Belgium|ON5HB Ham-radio users|From comments|
||
|time.xtracloud.net|AS174|Unknown|Qualcomm|Qualcomm|From comments|

## Star History
<!-- Placeholder for potential future Star History graph or section -->
