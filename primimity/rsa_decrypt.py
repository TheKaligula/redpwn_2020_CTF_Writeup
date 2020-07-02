#!/usr/bin/python3

from Crypto.Util.number import inverse, long_to_bytes

prime_factors = [
139926822890670655977195962770726941986198973494425759476822219188316377933161673759394901805855617939978281385708941597117531007973713846772205166659227214187622925135931456526921198848312215276630974951050306344412865900075089120689559331322162952820292429725303619113876104177529039691490258588465409397803,
139926822890670655977195962770726941986198973494425759476822219188316377933161673759394901805855617939978281385708941597117531007973713846772205166659227214187622925135931456526921198848312215276630974951050306344412865900075089120689559331322162952820292429725303619113876104177529039691490258588465409494847,
139926822890670655977195962770726941986198973494425759476822219188316377933161673759394901805855617939978281385708941597117531007973713846772205166659227214187622925135931456526921198848312215276630974951050306344412865900075089120689559331322162952820292429725303619113876104177529039691490258588465409208581
]

n = 1
phi = 1
e = 65537
C = 2082926013138674164997791605512226759362824531322433048281306983526001801581956788909408046338065370689701410862433705395338736589120086871506362760060657440410056869674907314204346790554619655855805666327905912762300412323371126871463045993946331927129882715778396764969311565407104426500284824495461252591576672989633930916837016411523983491364869137945678029616541477271287052575817523864089061675401543733151180624855361245733039022140321494471318934716652758163593956711915212195328671373739342124211743835858897895276513396783328942978903764790088495033176253777832808572717335076829539988337505582696026111326821783912902713222712310343791755341823415393931813610365987465739339849380173805882522026704474308541271732478035913770922189429089852921985416202844838873352090355685075965831663443962706473737852392107876993485163981653038588544562512597409585410384189546449890975409183661424334789750460016306977673969147

for number in prime_factors:
    n *= number
    phi *= (number-1)

d = inverse(e, phi)
m = pow(C, d, n)

print(long_to_bytes(m))