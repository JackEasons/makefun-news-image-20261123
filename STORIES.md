# Stories on the front page — Monday 23 November 2026

THE WORLD TODAY, 33 stories, 7 regions. Every story below happened or was
first reported on Monday 23 November 2026, except the three items flagged
in the DATE CHECK footer (Cyclone Akvan landfall 20 Nov, BepiColombo
Mercury arrival 21 Nov, Riemann proof claim 20 Nov).

## Drawn stories (1–13)

1. BANTEN, INDONESIA — 24 killed in a candy factory fire; about 30
   missing. Fire broke out Sat 21 Nov at the PT Fonusa Agung Mulia plant
   in Cikande; the toll of 24 was confirmed Mon 23 Nov. — Reuters
2. STRAIT OF HORMUZ — Mines set three oil tankers ablaze; Iran's
   Revolutionary Guard claims the strikes, as the US naval blockade of
   Iranian oil enters its 130th day. — Al Jazeera
3. ANTALYA, TURKIYE — COP31 climate talks end with no deal after
   record-long talks; 190+ nations split over fossil fuels and adaptation
   finance. — Reuters
4. SANTA CLARA — Nvidia's board brings back Jensen Huang as chief
   executive, weeks after he quit in a spy row. — AP
5. BENGHAZI, LIBYA — Ukraine says its naval drones sank a Russian
   warship in port; Zelensky confirms, Moscow warns of escalation. —
   Reuters
6. BEIJING — Trump, Xi and Putin meet in a three-way summit in China;
   little yielded as Xi presses on Taiwan. — Standard Topic
7. NEW DELHI — India pledges a $1.62bn economic package to flood-hit
   Nepal after Modi talks with Nepal's PM. — Reuters
8. BRUSSELS — Flights grounded across Belgium in a nationwide strike
   against austerity measures. — BBC
9. MERCURY — BepiColombo enters orbit around Mercury after an 8-year
   cruise; a software glitch cut its arrival burn short (arrival 21 Nov,
   glitch reported 22 Nov, updates 23 Nov). — Gizmodo / ESA
10. MATHS — Anthropic mathematician claims an AI-assisted proof of the
    Riemann hypothesis (announced 20 Nov); verification debate continues.
    — Nature
11. MARKETS — Bitcoin rebounds to $61K from a two-year low as Wall
    Street futures recover. — CoinDesk
12. NEW YORK — The Mets agree a record deal for Detroit ace Tarik Skubal.
    — Standard Topic
13. HOLLYWOOD — "Sunrise on the Reaping" opens with $120M at the box
    office; Miley Cyrus weds. — Standard Topic

## Briefs (14–33)

14. SEOUL — Education minister quits over exam-cheating chaos. — Reuters
15. LONDON — Burnham's EU summit deal reopens the Brexit debate. —
    The Guardian
16. ISLAMABAD — Pakistan PM cancels Russia trip amid border clashes. —
    The Hindu
17. WASHINGTON — Trump orders federal contractors to check with the
    White House before answering Congress. — AP
18. WASHINGTON — Appeals court lets Trump try again to move his
    hush-money case to federal court. — AP
19. SEATTLE — Masked ICE agents pull a father and daughter off a jet
    bridge; protests follow. — CBS
20. GAZA — Oxfam: Israeli attacks turned Gaza into a "toxic wasteland".
    — Oxfam
21. PARIS — Global wealth-tax campaign gathers momentum. — 10 Things
22. WARSAW — Poland accuses Russia of provocation over missiles. —
    10 Things
23. JERUSALEM — Israeli coalition talks stall over leadership. —
    10 Things
24. JAKARTA — EU and Indonesia sign a trade deal scrapping most tariffs.
    — AP
25. BEIJING — China, South Korea and Taiwan step in to prop up stock
    markets. — Standard Topic
26. NEW DELHI — World Bank: India's extreme poverty fell to 2.6%. —
    Standard Topic
27. LONDON — NHS starts an AI trial in breast-cancer screening. —
    Principia
28. NEW YORK — Anthropic shares slide 3% after IPO as the AI sell-off
    deepens. — Standard Topic
29. WASHINGTON — FBI probes a possible hack of its crime database. —
    Principia
30. LONDON — Signal limits mobile screenshots, citing AI surveillance.
    — Morning Brief
31. ABUJA — Nigeria's presidential villa hit by water and power cuts. —
    BBC
32. MEXICO CITY — Mexico and China agree a trade working group. —
    Standard Topic
33. CANBERRA — Georgie Prespakis wins the AFLW best and fairest. — ABC

## Region counts

ASIA 8 · EUROPE 6 · MIDDLE EAST 3 · AMERICAS 9 · AFRICA 2 · OCEANIA 1 ·
GLOBAL 4 = 33 stories.

## How it is built

`draw23.py` draws the whole front page with PIL (masthead, big-number
strip, 3 large + 10 small illustrated stories, 20 briefs, a numbered world
map, DATE CHECK footer) and saves `entry.png` (1024×1024, ~197 KB).
`main.py` only copies that pre-rendered image to
`$MAKEFUN_OUTPUT_DIR/entry.png`; it never renders and never writes to the
repository directory. Re-running `draw23.py` produces byte-identical PNGs.
