# Public NTP Servers

[![Ask DeepWiki](https://deepwiki.com/badge.svg)](https://deepwiki.com/jauderho/public-ntp-servers)
[![OpenSSF Scorecard](https://api.securityscorecards.dev/projects/github.com/jauderho/public-ntp-servers/badge)](https://securityscorecards.dev/viewer/?uri=github.com/jauderho/public-ntp-servers)

This repository lists public NTP (Network Time Protocol) servers.
The list is sourced from various public resources and aims to provide configuration files for common NTP clients. The initial input for the list comes from the [Gist](https://gist.github.com/mutin-sa/eea1c396b1e610a2da1e5550d94b0453) created by [mutin-sa](https://github.com/mutin-sa).

**WARNING:** Server availability and accuracy can vary. Always verify servers before relying on them for critical applications. Visit the companion repo of [NTP servers with NTS support](https://github.com/jauderho/nts-servers/).

## Contribute
- Pull requests are welcome to add new sources ([signed commits](https://docs.github.com/en/authentication/managing-commit-signature-verification/signing-commits) are preferred)
- PR will not be merged until connectivity to server can be verified
- Please specify if server is virtualized
- Contributions and updates to the list are welcome via pull requests to `ntp-sources.yml` to modify the `README.md`, `chrony.conf`, and `ntp.toml`
  - Run `./scripts/ntpServerConverter.py ntp-sources.yml`
  - Use `git diff origin README.md chrony.conf ntp.toml` to verify that you have a clean update before submitting a PR
- AI generated documentation: https://deepwiki.com/jauderho/public-ntp-servers

## Usage
- This repository provides NTP server lists in multiple formats:
  - For use with chrony - [chrony.conf](chrony.conf)
  - For use with ntpd-rs - [ntp.toml](ntp.toml)
- Before using anycast NTP servers, make sure that you understand the [limitations](https://www.rfc-editor.org/rfc/rfc8633.html#page-17)
- Use [at least 4 time sources](https://support.ntp.org/Support/SelectingOffsiteNTPServers#Upstream_Time_Server_Quantity) as a best practice. No more than 10 should be used
- Generally, virtualized systems do not make for good time sources as there is too much jitter. Submissions should strive to ensure that high quality time is available
- Verify NTP server connectivity using the following command before submitting a pull request
  - `./scripts/ntpCheck.sh <NTP_SERVER_NAME>` 

## The List
|Hostname|AS|Stratum|Location|Owner|Notes|
|---|---|:---:|---|---|---|
|time.google.com|AS15169|1|Google NTP|Google|Anycast|
|time1.google.com|AS15169|1|Google NTP|Google||
|time2.google.com|AS15169|1|Google NTP|Google||
|time3.google.com|AS15169|1|Google NTP|Google||
|time4.google.com|AS15169|1|Google NTP|Google||
|time.android.com|AS15169|1|Google NTP|Google|Anycast|
||
|time.aws.com|AS14618, AS16509, AS399991|4|Amazon NTP|Amazon|Anycast|
|0.time.aws.com|AS14618, AS16509, AS399991|4|Amazon NTP|Amazon|Anycast|
|1.time.aws.com|AS14618, AS16509, AS399991|4|Amazon NTP|Amazon|Anycast|
|2.time.aws.com|AS14618, AS16509, AS399991|4|Amazon NTP|Amazon|Anycast|
|3.time.aws.com|AS14618, AS16509, AS399991|4|Amazon NTP|Amazon|Anycast|
||
|pool.ntp.org|||NTP global public Pool|pool.ntp.org||
|0.pool.ntp.org|||NTP global public Pool|pool.ntp.org||
|1.pool.ntp.org|||NTP global public Pool|pool.ntp.org||
|2.pool.ntp.org|||NTP global public Pool|pool.ntp.org||
|3.pool.ntp.org|||NTP global public Pool|pool.ntp.org||
|amazon.pool.ntp.org|||NTP public Pool for Amazon|pool.ntp.org||
|0.amazon.pool.ntp.org|||NTP public Pool for Amazon|pool.ntp.org||
|1.amazon.pool.ntp.org|||NTP public Pool for Amazon|pool.ntp.org||
|2.amazon.pool.ntp.org|||NTP public Pool for Amazon|pool.ntp.org||
|3.amazon.pool.ntp.org|||NTP public Pool for Amazon|pool.ntp.org||
|ubnt.pool.ntp.org|||NTP public Pool for Ubiquiti Unifi|pool.ntp.org||
|0.ubnt.pool.ntp.org|||NTP public Pool for Ubiquiti Unifi|pool.ntp.org||
|1.ubnt.pool.ntp.org|||NTP public Pool for Ubiquiti Unifi|pool.ntp.org||
|2.ubnt.pool.ntp.org|||NTP public Pool for Ubiquiti Unifi|pool.ntp.org||
|3.ubnt.pool.ntp.org|||NTP public Pool for Ubiquiti Unifi|pool.ntp.org||
||
|time.cloudflare.com|AS13335|3|Cloudflare NTP|Cloudflare|Anycast|
||
|time.facebook.com|AS32934|1|Facebook NTP|Facebook|Anycast|
|time1.facebook.com|AS32934|1|Facebook NTP|Facebook||
|time2.facebook.com|AS32934|1|Facebook NTP|Facebook||
|time3.facebook.com|AS32934|1|Facebook NTP|Facebook||
|time4.facebook.com|AS32934|1|Facebook NTP|Facebook||
|time5.facebook.com|AS32934|1|Facebook NTP|Facebook||
||
|time.windows.com|AS8075|3|Microsoft NTP|Microsoft|Anycast|
||
|time.apple.com|AS714, AS6185|1|Apple NTP|Apple|Anycast|
|time-macos.apple.com|AS714, AS6185|1|Apple NTP|Apple||
|time-ios.apple.com|AS714, AS6185|1|Apple NTP|Apple||
|time1.apple.com|AS714, AS6185|2|Apple NTP|Apple||
|time2.apple.com|AS714, AS6185|2|Apple NTP|Apple||
|time3.apple.com|AS714, AS6185|2|Apple NTP|Apple||
|time4.apple.com|AS714, AS6185|2|Apple NTP|Apple||
|time5.apple.com|AS714, AS6185|2|Apple NTP|Apple||
|time6.apple.com|AS714, AS6185|2|Apple NTP|Apple||
|time7.apple.com|AS714, AS6185|2|Apple NTP|Apple||
|time.euro.apple.com|AS714, AS6185|1|Apple NTP|Apple|Europe|
|time.asia.apple.com|AS714, AS6185|1|Apple NTP|Apple|Asia|
||
|clepsydra.dec.com|Unknown|Unknown|DEC/Compaq/HP|HP||
|clepsydra.labs.hp.com|Unknown|Unknown|DEC/Compaq/HP|HP||
|clepsydra.hpl.hp.com|Unknown|Unknown|DEC/Compaq/HP|HP||
|usno.labs.hp.com|Unknown|Unknown|DEC/Compaq/HP|HP||
||
|ntp0.ntp-servers.net|Unknown|2|NTP SERVERS|ntp-servers.net||
|ntp1.ntp-servers.net|Unknown|2|NTP SERVERS|ntp-servers.net||
|ntp2.ntp-servers.net|Unknown|2|NTP SERVERS|ntp-servers.net||
|ntp3.ntp-servers.net|Unknown|1|NTP SERVERS|ntp-servers.net||
|ntp4.ntp-servers.net|Unknown|1|NTP SERVERS|ntp-servers.net||
|ntp5.ntp-servers.net|Unknown|2|NTP SERVERS|ntp-servers.net||
|ntp6.ntp-servers.net|Unknown|2|NTP SERVERS|ntp-servers.net||
|ntp7.ntp-servers.net|Unknown|2|NTP SERVERS|ntp-servers.net||
||
|stratum1.net|Unknown|1|stratum1.net|stratum1.net||
||
|ts1.aco.net|AS1853|1|ACO.net|ACO.net||
|ts2.aco.net|AS1853|1|ACO.net|ACO.net||
||
|time-a.as43289.net|AS43289|2|Trabia-Network|Trabia-Network||
|time-b.as43289.net|AS43289|2|Trabia-Network|Trabia-Network||
|time-c.as43289.net|AS43289|2|Trabia-Network|Trabia-Network||
||
|ntp.ripe.net|AS3333|1|RIPE|RIPE NCC||
||
|[clock.isc.org](https://clock.isc.org)|AS1280|3|ISC|ISC|prev ntp.isc.org|
||
|ntp0.as34288.net|AS34288|2|KSZ|Kantonsschule Zug||
|ntp1.as34288.net|AS34288|2|KSZ|Kantonsschule Zug||
||
|ntp.nat.ms|AS30746|1|Nat Morris|Nat Morris||
||
|timekeeper.isi.edu|AS2702|1|ISI|Information Sciences Institute||
||
|ntpstm.netbone-digital.com|Unknown|Unknown|NetBone Digital|NetBone Digital||
||
|nist1.symmetricom.com|AS3608|1|Microchip|Microchip||
||
|ntp.quintex.com|Unknown|Unknown|Quintex|Quintex||
||
|ntp1.conectiv.com|AS16069|Unknown|Conectiv|Conectiv||
||
|tock.usshc.com|Unknown|1|USSHC|USSHC||
||
|t2.timegps.net|Unknown|Unknown|timegps.net|timegps.net||
||
|gps.layer42.net|AS11491|Unknown|Layer42|Layer42||
||
|ntp-ca.stygium.net|AS3978|Unknown|Stygium|Stygium||
||
|sesku.planeacion.net|Unknown|Unknown|planeacion.net|planeacion.net||
||
|ntp0.nl.uu.net|AS8283|1|KPN|KPN International Carrier||
|ntp1.nl.uu.net|AS8283|1|KPN|KPN International Carrier||
||
|navobs1.oar.net|Unknown|2|oar.net|oar.net||
||
|ntp-galway.hea.net|AS1213|2|HEAnet|HEAnet|Galway|
||
|ntp1.ona.org|Unknown|Unknown|ona.org|ona.org||
||
|ntp.your.org|Unknown|1|your.org|your.org||
||
|ntp.mrow.org|Unknown|1|mrow.org|mrow.org||
||
|ntp.ubuntu.com|AS201815|2|Ubuntu|Canonical|Anycast|
||
|time.xtracloud.net|AS174|4|Qualcomm|Qualcomm||
||
|asynchronos.iiss.at|AS8401|Unknown|Austria|ACOnet / University of Vienna||
||
|ntp.i2t.ehu.eus|AS2110|1|Basque Country|University of the Basque Country (EHU)||
||
|ntp.heppen.be|Unknown|1|Belgium|ON5HB Ham-radio users||
|ntp1.oma.be|AS5400|1|Belgium|Royal Observatory of Belgium||
|ntp2.oma.be|AS5400|1|Belgium|Royal Observatory of Belgium||
|ntp.teambelgium.net|AS5432|1|Belgium|Team Belgium||
||
|ntps1.pads.ufrj.br|AS1553|1|Brazil|Federal University of Rio de Janeiro||
||
|[time1.mbix.ca](https://time1.mbix.ca)|AS395611|1|Canada|Manitoba Internet Exchange||
|[time2.mbix.ca](https://time2.mbix.ca)|AS395611|1|Canada|Manitoba Internet Exchange||
|[time3.mbix.ca](https://time3.mbix.ca)|AS395611|1|Canada|Manitoba Internet Exchange||
|time.nrc.ca|AS573|2|Canada|National Research Council Canada||
|ntp.qix.ca|AS14086|1|Canada|QiX||
|ntp1.qix.ca|AS14086|1|Canada|QiX||
|ntp2.qix.ca|AS14086|1|Canada|QiX||
|clock.uregina.ca|AS641|1|Canada|University of Regina||
|tick.usask.ca|AS22950|1|Canada|University of Saskatchewan||
|tock.usask.ca|AS22950|1|Canada|University of Saskatchewan||
|ntp.yycix.ca|AS396515|Unknown|Canada|YYCIX||
||
|ntp.shoa.cl|AS16299|1|Chile|Hydrographic and Oceanographic Service of the Chilean Navy||
||
|ntp.ntsc.ac.cn|AS4808, AS9808, AS23724|2|China|Chinese Academy of Sciences||
|ntp.neu.edu.cn|AS4538|Unknown|China|Northeastern University||
||
|time1.ntp.hr|AS49932|1|Croatia|CARNET||
|time2.ntp.hr|AS49932|1|Croatia|CARNET||
|os.ntp.carnet.hr|AS49932|2|Croatia|CARNET||
|ri.ntp.carnet.hr|AS49932|2|Croatia|CARNET||
|st.ntp.carnet.hr|AS49932|2|Croatia|CARNET||
|zg1.ntp.carnet.hr|AS49932|2|Croatia|CARNET||
|zg2.ntp.carnet.hr|AS49932|2|Croatia|CARNET||
||
|ntp.nic.cz|AS25204|1|Czech Republic|CZ.NIC||
|time.ufe.cz|AS25192|1|Czech Republic|UFE CAS||
||
|ntp.viarouge.net|AS207288|2|France|Hubert Viarouge||
||
|ntp.dianacht.de|Unknown|2|Germany|dianacht.de||
|time.fu-berlin.de|AS680|1|Germany|Freie Universitaet Berlin||
|zeit.fu-berlin.de|AS680|1|Germany|Freie Universitaet Berlin||
|ntp1.hetzner.de|AS24940|2|Germany|Hetzner Online||
|ntp2.hetzner.de|AS24940|2|Germany|Hetzner Online||
|ntp3.hetzner.de|AS24940|2|Germany|Hetzner Online||
|ptbtime1.ptb.de|AS1896|1|Germany|PTB||
|ptbtime2.ptb.de|AS1896|1|Germany|PTB||
|ntps1-0.cs.tu-berlin.de|AS680|1|Germany|Technische Universitaet Berlin||
|ntps1-1.cs.tu-berlin.de|AS680|1|Germany|Technische Universitaet Berlin||
|ntps1-0.uni-erlangen.de|AS680|1|Germany|University of Erlangen-Nuremberg||
|ntps1-1.uni-erlangen.de|AS680|1|Germany|University of Erlangen-Nuremberg||
|ntp1.fau.de|AS680|1|Germany|University of Erlangen-Nuremberg (FAU)||
|ntp2.fau.de|AS680|1|Germany|University of Erlangen-Nuremberg (FAU)||
|rustime01.rus.uni-stuttgart.de|AS680|1|Germany|University of Stuttgart||
|rustime02.rus.uni-stuttgart.de|AS680|1|Germany|University of Stuttgart||
||
|stdtime.gov.hk|AS4780|2|Hong Kong|Hong Kong Observatory||
||
|ntp.atomki.mta.hu|AS197038|2|Hungary|ATOMKI||
||
|time.nplindia.org|Unknown|1|India|NPL India||
|time.nplindia.in|Unknown|1|India|NPL India||
|samay1.nic.in|Unknown|2|India|NIC India||
|samay2.nic.in|Unknown|2|India|NIC India||
|ntp.iitb.ac.in|Unknown|2|India|IIT Bombay||
||
|time.esa.int|AS15559|1|International|European Space Agency||
|time1.esa.int|AS15559|1|International|European Space Agency||
||
|ntp.day.ir|AS42337|10|Iran|Day ICT||
||
|ntp1.inrim.it|AS29109|1|Italy|INRIM||
|ntp2.inrim.it|AS29109|1|Italy|INRIM||
||
|ntp1.jst.mfeed.ad.jp|AS7521|1|Japan|INTERNET MULTIFEED CO.||
|ntp2.jst.mfeed.ad.jp|AS7521|1|Japan|INTERNET MULTIFEED CO.||
|ntp3.jst.mfeed.ad.jp|AS7521|1|Japan|INTERNET MULTIFEED CO.||
|ntp.nict.jp|AS9355|1|Japan|National Institute of Information and Communications Technology||
|x.ns.gin.ntt.net|AS2914|2|Japan|NTT||
|y.ns.gin.ntt.net|AS2914|2|Japan|NTT||
||
|cronos.cenam.mx|AS8017|1|Mexico|CENAM||
|ntp.lcf.mx|Unknown|Unknown|Mexico|lcf.mx||
||
|ntp.time.nl|AS1140|1|Netherlands|SIDN Labs|ntp1.time.nl|
|ntppool1.time.nl|AS1140|1|Netherlands|SIDN Labs|Preferred|
|ntppool2.time.nl|AS1140|1|Netherlands|SIDN Labs|Preferred|
|chime1.surfnet.nl|AS1103|1|Netherlands|SURFnet||
|ntp.vsl.nl|AS34929|1|Netherlands|VSL||
||
|tempus1.gum.gov.pl|AS43900|1|Poland|GUM||
|tempus2.gum.gov.pl|AS43900|1|Poland|GUM||
|ntp.fizyka.umk.pl|AS8805|1|Poland|Nicolaus Copernicus University||
||
|ntp1.usv.ro|AS8713|Unknown|Romania|University Stefan cel Mare Suceava||
|ntp3.usv.ro|AS8713|Unknown|Romania|University Stefan cel Mare Suceava||
||
|ntp.ru|AS8915|Unknown|Russia|Company Delfa Co. Ltd.||
|ntp.psn.ru|AS41783|Unknown|Russia|ITAEC||
|ntp.mobatime.ru|Unknown|1|Russia|Mobatime||
|ntp.ix.ru|AS43832|1|Russia|MSK-IX||
|ntp.nsu.ru|AS3335|2|Russia|Novosibirsk State University||
|ntp.rsu.edu.ru|AS47124|1|Russia|Rostov State University||
|ntp1.stratum1.ru|Unknown|1|Russia|stratum1.ru||
|ntp2.stratum1.ru|Unknown|1|Russia|stratum1.ru||
|ntp3.stratum1.ru|Unknown|1|Russia|stratum1.ru||
|ntp4.stratum1.ru|Unknown|1|Russia|stratum1.ru||
|ntp5.stratum1.ru|Unknown|1|Russia|stratum1.ru||
|ntp1.stratum2.ru|Unknown|2|Russia|stratum2.ru|Москва|
|ntp2.stratum2.ru|Unknown|2|Russia|stratum2.ru||
|ntp3.stratum2.ru|Unknown|2|Russia|stratum2.ru||
|ntp4.stratum2.ru|Unknown|2|Russia|stratum2.ru||
|ntp5.stratum2.ru|Unknown|2|Russia|stratum2.ru||
|ntp.fiord.ru|AS28917|Unknown|Russia|TRC Fiord||
|ntp1.vniiftri.ru|Unknown|1|Russia|VNIIFTRI||
|ntp2.vniiftri.ru|Unknown|1|Russia|VNIIFTRI||
|ntp3.vniiftri.ru|Unknown|1|Russia|VNIIFTRI||
|ntp4.vniiftri.ru|Unknown|1|Russia|VNIIFTRI||
|ntp.sstf.nsk.ru|Unknown|1|Russia|VNIIFTRI||
|ntp1.niiftri.irkutsk.ru|Unknown|1|Russia|VNIIFTRI||
|ntp2.niiftri.irkutsk.ru|Unknown|1|Russia|VNIIFTRI||
|vniiftri.khv.ru|Unknown|1|Russia|VNIIFTRI||
|vniiftri2.khv.ru|Unknown|1|Russia|VNIIFTRI||
|ntp21.vniiftri.ru|Unknown|2|Russia|VNIIFTRI||
||
|hora.roa.es|AS31007|1|Spain|ROA||
|minuto.roa.es|AS31007|1|Spain|ROA||
|tick.espanix.net|Unknown|1|Spain|Espanix||
|tock.espanix.net|Unknown|1|Spain|Espanix||
||
|timehost.lysator.liu.se|AS1653|Unknown|Sweden|Academic Computer Club Lysator||
|gbg1.ntp.se|AS57021|1|Sweden|Netnod|Göteborg|
|gbg2.ntp.se|AS57021|1|Sweden|Netnod|Göteborg|
|mmo1.ntp.se|AS57021|1|Sweden|Netnod|Malmö|
|mmo2.ntp.se|AS57021|1|Sweden|Netnod|Malmö|
|sth1.ntp.se|AS57021|1|Sweden|Netnod|Stockholm|
|sth2.ntp.se|AS57021|1|Sweden|Netnod|Stockholm|
|svl1.ntp.se|AS57021|1|Sweden|Netnod|Sundsvall|
|svl2.ntp.se|AS57021|1|Sweden|Netnod|Sundsvall|
|ntp.se|AS57021|1|Sweden|Netnod|Anycast|
|time1.stupi.se|Unknown|Unknown|Sweden|stupi.se||
||
|[ntp.neel.ch](https://ntp.neel.ch)|AS34569|Unknown|Switzerland|Neel Engineering||
||
|[eshail.batc.org.uk](https://eshail.batc.org.uk)|Unknown|1|UK|BATC||
|ntp5.leontp.com|Unknown|1|UK|Leo Bodnar||
|ntp6.leontp.com|Unknown|1|UK|Leo Bodnar||
|ntp7.leontp.com|Unknown|1|UK|Leo Bodnar||
|ntp8.leontp.com|Unknown|1|UK|Leo Bodnar||
|ntp9.leontp.com|Unknown|1|UK|Leo Bodnar||
|ntp1.dmz.terryburton.co.uk|Unknown|1|UK|Terry Burton||
|ntp2.dmz.terryburton.co.uk|Unknown|1|UK|Terry Burton||
|[ntp.theitman.uk](https://ntp.theitman.uk)|Unknown|1|UK|TheITMan||
|timekeeper.webwiz.net|AS44929|1|UK|Web Wiz||
||
|ntp.time.in.ua|Unknown|1|Ukraine|time.in.ua||
|ntp2.time.in.ua|Unknown|1|Ukraine|time.in.ua||
|ntp3.time.in.ua|Unknown|2|Ukraine|time.in.ua||
||
|ntp.colby.edu|AS10566|Unknown|US|Colby College||
|gnomon.cc.columbia.edu|AS117|Unknown|US|Columbia University||
|navobs1.gatech.edu|AS2637|1|US|Georgia Institute of Technology||
|ntp.gsu.edu|AS10631|Unknown|US|Georgia State University||
|clock.sjc.he.net|AS6939|2|US|HE.net|San Jose, CA|
|clock.fmt.he.net|AS6939|1|US|HE.net|Fremont, CA|
|clock.nyc.he.net|AS6939|2|US|HE.net|New York City, NY|
|bonehed.lcs.mit.edu|AS3|1|US|MIT||
|time.nist.gov|AS49, AS104|1|US|NIST|Anycast|
|time-a-g.nist.gov|AS49, AS104|1|US|NIST||
|time-b-g.nist.gov|AS49, AS104|1|US|NIST||
|time-c-g.nist.gov|AS49, AS104|1|US|NIST||
|time-d-g.nist.gov|AS49, AS104|1|US|NIST||
|time-e-g.nist.gov|AS49, AS104|1|US|NIST||
|time-a-wwv.nist.gov|AS49, AS104|1|US|NIST||
|time-b-wwv.nist.gov|AS49, AS104|1|US|NIST||
|time-c-wwv.nist.gov|AS49, AS104|1|US|NIST||
|time-d-wwv.nist.gov|AS49, AS104|1|US|NIST||
|time-e-wwv.nist.gov|AS49, AS104|1|US|NIST||
|time-a-b.nist.gov|AS49, AS104|1|US|NIST||
|time-b-b.nist.gov|AS49, AS104|1|US|NIST||
|time-c-b.nist.gov|AS49, AS104|1|US|NIST||
|time-d-b.nist.gov|AS49, AS104|1|US|NIST||
|time-e-b.nist.gov|AS49, AS104|1|US|NIST||
|time-nw.nist.gov|AS49, AS104|1|US|NIST||
|time-a.nist.gov|AS49, AS104|1|US|NIST||
|time-b.nist.gov|AS49, AS104|1|US|NIST||
|utcnist.colorado.edu|AS49, AS104|1|US|NIST|Operated by University of Colorado|
|utcnist2.colorado.edu|AS49, AS104|1|US|NIST|Operated by University of Colorado|
|utcnist3.colorado.edu|AS49, AS104|1|US|NIST|Operated by University of Colorado|
|now.okstate.edu|AS111|1|US|Oklahoma State University||
|otc1.psu.edu|AS38|Unknown|US|Pennsylvania State University||
|ntp1.net.berkeley.edu|AS25|1|US|University of California, Berkeley||
|ntp2.net.berkeley.edu|AS25|1|US|University of California, Berkeley||
|tick.ucla.edu|AS52|Unknown|US|University of California, Los Angeles||
|rackety.udel.edu|AS300|Unknown|US|University of Delaware||
|mizbeaver.udel.edu|AS300|Unknown|US|University of Delaware||
|ntp-s1.cise.ufl.edu|AS5730|Unknown|US|University of Florida||
|tick.uh.edu|AS638|2|US|University of Hawaii||
|level1e.cs.unc.edu|AS2807|Unknown|US|University of North Carolina at Chapel Hill||
|tick.usno.navy.mil|AS747|1|US|US Navy||
|tock.usno.navy.mil|AS747|1|US|US Navy||
|ntp2.usno.navy.mil|AS747|1|US|US Navy||
|navobs1.wustl.edu|AS288|1|US|Washington University in St. Louis||
|[ntp1.wiktel.com](https://ntp1.wiktel.com)|AS33362|1|US|Wikstrom Telephone Company||
|[ntp2.wiktel.com](https://ntp2.wiktel.com)|AS33362|1|US|Wikstrom Telephone Company||

## Star History
<a href="https://star-history.com/#jauderho/public-ntp-servers&Timeline">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/svg?repos=jauderho/public-ntp-servers&type=Date&theme=dark" />
    <source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/svg?repos=jauderho/public-ntp-servers&type=Date" />
    <img alt="Star History Chart" src="https://api.star-history.com/svg?repos=jauderho/public-ntp-servers&type=Date" />
  </picture>
</a>
