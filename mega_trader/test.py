import quickfix as fix

recv = "8=FIXT.1.19=35835=AAM49=BM56=MT34=1924=1115=29022=148=13631883=25311884=61891=01892=01893=01894=01847=11711895=239.951896=3001897=01899=01900=01901=01861=01890=01909=01835=239.951843=3001844=12/9/2018 2:30:01 PM1845=239.95387=31823=5368709.121828=51911=240.11912=3001911=2421912=3001911=248.951912=711911=2491912=3001911=2501912=10010=180"
# received = "8=FIXT.1.19=108135=IB49=NSECM56=MTBM34=1924=1115=21828=61826=Nifty CPSE1815=2294.51816=2310.151817=2286.551818=2276.751819=2294.21820=1967852601488651821=262231822=257851823=0.771824=2799.551825=2139.51827=-1826=Nifty GrowSect 151815=7037.751816=7070.351817=7023.651818=6990.61819=7042.91820=7768216282514231821=782041822=750561823=0.751824=7354.551825=5942.151827= 1826=Nifty50 Value 201815=5444.71816=5465.61817=5417.41818=5413.61819=5425.91820=1.90667550936387E+151821=1348851822=1341791823=0.231824=5563.81825=4171.651827=-1826=Nifty Mid Liq 151815=4133.551816=4206.551817=4133.551818=4107.21819=4205.41820=1573956262705091821=428041822=442911823=2.391824=4677.051825=3770.551827=-1826=Nifty Pvt Bank1815=15385.21816=15415.51817=15339.751818=15248.81819=15377.71820=9015155094048031821=589741822=592681823=0.851824=16152.151825=13298.31827=+1826=NIFTY MIDCAP 1001815=19184.851816=19326.31817=19184.851818=19046.551819=19314.251820=7127426889917151821=1858871822=1884631823=1.411824=21840.851825=17700.91827=-10=174"
# # received = "8=FIXT.1.19=57835=W49=NSECM56=MTBM34=1924=1115=248=1333207=NSECM268=10269=4844=1991.45271=5346=1269=4844=1991.4271=444346=2269=4844=1991.35271=2346=1269=4844=1991.3271=12346=1269=4844=1991.25271=132346=3269=4944=1991.55271=3346=1269=4944=1991.65271=51346=3269=4944=1991.7271=51346=3269=4944=1992271=20346=1269=4944=1992.15271=75346=1779=17/9/2018 2:34:14 PM1835=1991.551843=91844=17/9/2018 2:34:14 PM1845=1998.181824=2022.951825=928.001840=35763.74534881846=1877761847=989038387=17898161861=2021.31809=2029.61802=2022.951801=199010=027"

# data_parser.read_msg(recv)
# f = open("test-log.log", "r")
# lines = f.readlines()
# for line in lines:
#     line = line.replace("\n", "")
