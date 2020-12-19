"""Check if a host is in the Google Chrome HSTS Preload list"""

import functools
import os
import typing

__version__ = "2020.11.21"
__checksum__ = "2e850de3620c034a8ecb4302a5a03d12b6d549355d108cc157d6f6cef9ac3611"
__all__ = ["in_hsts_preload"]

# fmt: off
_GTLD_INCLUDE_SUBDOMAINS = {b'android', b'app', b'bank', b'chrome', b'dev', b'foo', b'gle', b'gmail', b'google', b'hangout', b'insurance', b'meet', b'new', b'page', b'play', b'search', b'youtube'}  # noqa: E501
_JUMPTABLE = [[(0, 11), (11, 5), None, (16, 57), (73, 26), (99, 12), None, (111, 19), (130, 22), (152, 7), (159, 20), (179, 18), None, (197, 29), (226, 45), (271, 7), (278, 9), (287, 36), (323, 10), (333, 10), (343, 28), None, (371, 50), (421, 8), (429, 18), (447, 19), (466, 13), (479, 14), (493, 14), None, None, (507, 29), (536, 16), (552, 35), (587, 14), (601, 24), (625, 9), None, (634, 25), (659, 27), (686, 8), (694, 13), (707, 10), None, (717, 17), (734, 6), (740, 26), (766, 5), (771, 5), (776, 10), (786, 10), (796, 11), (807, 12), (819, 27), None, (846, 11), (857, 11), (868, 7), (875, 29), (904, 18), (922, 27), (949, 46), (995, 25), (1020, 16), (1036, 8), (1044, 5), (1049, 22), (1071, 18), None, (1089, 36), (1125, 15), (1140, 8), (1148, 11), None, (1159, 5), (1164, 16), (1180, 14), (1194, 18), None, (1212, 14), (1226, 26), (1252, 48), (1300, 19), (1319, 5), (1324, 46), (1370, 14), (1384, 14), (1398, 20), None, (1418, 10), (1428, 13), (1441, 15), (1456, 19), None, (1475, 13), (1488, 19), (1507, 11), (1518, 4), (1522, 22), (1544, 10), (1554, 7), (1561, 14), (1575, 21), (1596, 11), (1607, 10), (1617, 12), (1629, 32), None, (1661, 10), (1671, 14), (1685, 12), (1697, 45), (1742, 15), None, (1757, 11), (1768, 23), (1791, 21), (1812, 26), (1838, 6), (1844, 6), (1850, 7), (1857, 5), (1862, 20), (1882, 23), (1905, 24), (1929, 13), (1942, 15), (1957, 19), (1976, 6), (1982, 61), (2043, 44), (2087, 12), (2099, 23), (2122, 16), (2138, 38), (2176, 6), (2182, 12), (2194, 44), (2238, 6), (2244, 41), (2285, 13), (2298, 23), (2321, 30), (2351, 16), (2367, 8), (2375, 15), (2390, 12), (2402, 19), (2421, 21), (2442, 15), None, (2457, 35), (2492, 21), (2513, 17), (2530, 19), (2549, 26), (2575, 5), (2580, 37), (2617, 26), (2643, 16), (2659, 10), (2669, 17), (2686, 23), (2709, 14), (2723, 17), (2740, 8), (2748, 4), (2752, 7), (2759, 29), (2788, 6), (2794, 18), (2812, 27), (2839, 20), (2859, 17), (2876, 19), (2895, 12), (2907, 40), (2947, 40), (2987, 12), (2999, 48), (3047, 25), (3072, 12), None, (3084, 8), (3092, 20), (3112, 19), (3131, 6), (3137, 23), None, (3160, 30), (3190, 33), (3223, 14), (3237, 12), (3249, 27), None, (3276, 26), (3302, 41), (3343, 50), (3393, 15), (3408, 20), (3428, 15), (3443, 21), (3464, 32), (3496, 24), (3520, 20), (3540, 13), (3553, 60), (3613, 19), (3632, 9), (3641, 12), (3653, 12), (3665, 11), (3676, 10), (3686, 48), (3734, 32), None, (3766, 25), (3791, 12), None, (3803, 8), (3811, 8), (3819, 7), None, (3826, 25), (3851, 17), None, (3868, 21), (3889, 35), (3924, 12), (3936, 10), (3946, 36), (3982, 20), (4002, 22), (4024, 23), (4047, 19), (4066, 12), (4078, 5), (4083, 30), (4113, 24), (4137, 14), (4151, 14), (4165, 47), (4212, 46), None, None, (4258, 51), (4309, 42), None, (4351, 14), None, (4365, 15), (4380, 8), (4388, 21), (4409, 6), (4415, 16), (4431, 17)], [(4448, 6557), (11005, 7038), (18043, 7303), (25346, 6266), (31612, 6574), (38186, 6381), (44567, 7247), (51814, 6408), (58222, 7062), (65284, 6279), (71563, 7474), (79037, 6652), (85689, 6832), (92521, 7484), (100005, 6717), (106722, 7020), (113742, 7357), (121099, 6162), (127261, 6523), (133784, 6753), (140537, 7172), (147709, 6834), (154543, 7121), (161664, 6444), (168108, 6656), (174764, 6931), (181695, 7070), (188765, 7180), (195945, 6475), (202420, 6960), (209380, 7118), (216498, 6690), (223188, 6761), (229949, 7262), (237211, 6332), (243543, 6917), (250460, 6540), (257000, 7262), (264262, 7055), (271317, 7167), (278484, 7734), (286218, 6611), (292829, 6675), (299504, 6378), (305882, 6567), (312449, 6449), (318898, 6575), (325473, 7371), (332844, 6602), (339446, 6263), (345709, 6628), (352337, 6845), (359182, 6851), (366033, 7069), (373102, 7121), (380223, 7054), (387277, 7114), (394391, 6292), (400683, 7150), (407833, 6061), (413894, 6972), (420866, 6697), (427563, 6600), (434163, 7081), (441244, 6876), (448120, 6951), (455071, 6398), (461469, 7386), (468855, 7188), (476043, 6984), (483027, 6751), (489778, 6717), (496495, 5855), (502350, 7149), (509499, 7305), (516804, 7522), (524326, 6148), (530474, 7410), (537884, 7274), (545158, 6411), (551569, 7079), (558648, 5992), (564640, 6733), (571373, 6925), (578298, 6643), (584941, 6687), (591628, 7145), (598773, 6909), (605682, 7103), (612785, 6873), (619658, 7699), (627357, 6125), (633482, 6427), (639909, 6752), (646661, 6882), (653543, 7321), (660864, 7334), (668198, 6545), (674743, 6520), (681263, 6469), (687732, 6471), (694203, 6912), (701115, 6483), (707598, 6731), (714329, 6429), (720758, 7058), (727816, 7053), (734869, 7325), (742194, 8323), (750517, 7487), (758004, 7239), (765243, 6823), (772066, 6570), (778636, 6822), (785458, 7134), (792592, 6925), (799517, 6447), (805964, 6510), (812474, 6638), (819112, 7481), (826593, 7183), (833776, 7193), (840969, 7193), (848162, 7176), (855338, 8096), (863434, 6569), (870003, 6067), (876070, 7160), (883230, 6813), (890043, 8384), (898427, 7450), (905877, 6343), (912220, 7098), (919318, 7067), (926385, 6585), (932970, 7069), (940039, 6314), (946353, 6865), (953218, 6599), (959817, 6864), (966681, 6950), (973631, 7539), (981170, 6465), (987635, 6594), (994229, 6954), (1001183, 6826), (1008009, 6755), (1014764, 7097), (1021861, 6465), (1028326, 7535), (1035861, 6793), (1042654, 6986), (1049640, 7207), (1056847, 6613), (1063460, 6961), (1070421, 6875), (1077296, 6629), (1083925, 6730), (1090655, 6518), (1097173, 6252), (1103425, 6474), (1109899, 6947), (1116846, 7613), (1124459, 6345), (1130804, 6765), (1137569, 7285), (1144854, 6615), (1151469, 6580), (1158049, 7265), (1165314, 6784), (1172098, 6061), (1178159, 6800), (1184959, 7928), (1192887, 6367), (1199254, 6540), (1205794, 7181), (1212975, 6712), (1219687, 7020), (1226707, 6720), (1233427, 6296), (1239723, 7823), (1247546, 7032), (1254578, 6874), (1261452, 7254), (1268706, 7744), (1276450, 7508), (1283958, 6369), (1290327, 7266), (1297593, 6478), (1304071, 6823), (1310894, 7195), (1318089, 6555), (1324644, 7097), (1331741, 7345), (1339086, 6794), (1345880, 6835), (1352715, 6712), (1359427, 6727), (1366154, 6925), (1373079, 6621), (1379700, 6953), (1386653, 6279), (1392932, 7282), (1400214, 7180), (1407394, 6867), (1414261, 7313), (1421574, 5971), (1427545, 6960), (1434505, 6800), (1441305, 7164), (1448469, 7043), (1455512, 7400), (1462912, 6947), (1469859, 7156), (1477015, 7066), (1484081, 6752), (1490833, 6885), (1497718, 6848), (1504566, 6983), (1511549, 6758), (1518307, 6994), (1525301, 6322), (1531623, 7783), (1539406, 6980), (1546386, 6519), (1552905, 6847), (1559752, 6995), (1566747, 6352), (1573099, 7060), (1580159, 6776), (1586935, 7798), (1594733, 6802), (1601535, 6346), (1607881, 7208), (1615089, 6661), (1621750, 7564), (1629314, 6408), (1635722, 6549), (1642271, 5960), (1648231, 6977), (1655208, 6786), (1661994, 7072), (1669066, 6655), (1675721, 6868), (1682589, 6579), (1689168, 7300), (1696468, 6668), (1703136, 6111), (1709247, 6874), (1716121, 6463), (1722584, 7035), (1729619, 7199), (1736818, 7400), (1744218, 6499), (1750717, 6538), (1757255, 6861)], [(1764116, 763), (1764879, 669), (1765548, 688), (1766236, 768), (1767004, 564), (1767568, 693), (1768261, 698), (1768959, 893), (1769852, 671), (1770523, 667), (1771190, 551), (1771741, 642), (1772383, 792), (1773175, 885), (1774060, 1046), (1775106, 868), (1775974, 1242), (1777216, 684), (1777900, 938), (1778838, 740), (1779578, 757), (1780335, 765), (1781100, 896), (1781996, 719), (1782715, 779), (1783494, 715), (1784209, 1007), (1785216, 1172), (1786388, 807), (1787195, 769), (1787964, 964), (1788928, 818), (1789746, 611), (1790357, 722), (1791079, 778), (1791857, 814), (1792671, 708), (1793379, 764), (1794143, 742), (1794885, 1119), (1796004, 695), (1796699, 827), (1797526, 748), (1798274, 736), (1799010, 748), (1799758, 420), (1800178, 965), (1801143, 896), (1802039, 746), (1802785, 592), (1803377, 834), (1804211, 692), (1804903, 780), (1805683, 1012), (1806695, 960), (1807655, 558), (1808213, 702), (1808915, 569), (1809484, 649), (1810133, 796), (1810929, 792), (1811721, 796), (1812517, 1054), (1813571, 968), (1814539, 764), (1815303, 719), (1816022, 767), (1816789, 475), (1817264, 617), (1817881, 592), (1818473, 716), (1819189, 877), (1820066, 636), (1820702, 742), (1821444, 650), (1822094, 699), (1822793, 611), (1823404, 711), (1824115, 828), (1824943, 496), (1825439, 792), (1826231, 644), (1826875, 828), (1827703, 682), (1828385, 638), (1829023, 439), (1829462, 597), (1830059, 759), (1830818, 804), (1831622, 782), (1832404, 883), (1833287, 1111), (1834398, 859), (1835257, 856), (1836113, 740), (1836853, 457), (1837310, 955), (1838265, 852), (1839117, 606), (1839723, 692), (1840415, 728), (1841143, 885), (1842028, 917), (1842945, 571), (1843516, 632), (1844148, 772), (1844920, 492), (1845412, 483), (1845895, 953), (1846848, 996), (1847844, 863), (1848707, 793), (1849500, 652), (1850152, 792), (1850944, 672), (1851616, 715), (1852331, 709), (1853040, 549), (1853589, 702), (1854291, 710), (1855001, 977), (1855978, 729), (1856707, 804), (1857511, 459), (1857970, 691), (1858661, 810), (1859471, 871), (1860342, 926), (1861268, 806), (1862074, 1010), (1863084, 802), (1863886, 591), (1864477, 815), (1865292, 697), (1865989, 816), (1866805, 794), (1867599, 764), (1868363, 681), (1869044, 688), (1869732, 654), (1870386, 621), (1871007, 696), (1871703, 726), (1872429, 648), (1873077, 517), (1873594, 603), (1874197, 676), (1874873, 597), (1875470, 748), (1876218, 618), (1876836, 773), (1877609, 550), (1878159, 550), (1878709, 718), (1879427, 669), (1880096, 657), (1880753, 678), (1881431, 903), (1882334, 673), (1883007, 622), (1883629, 967), (1884596, 895), (1885491, 583), (1886074, 712), (1886786, 844), (1887630, 699), (1888329, 707), (1889036, 484), (1889520, 651), (1890171, 694), (1890865, 810), (1891675, 654), (1892329, 932), (1893261, 760), (1894021, 807), (1894828, 721), (1895549, 668), (1896217, 582), (1896799, 704), (1897503, 727), (1898230, 1444), (1899674, 547), (1900221, 662), (1900883, 669), (1901552, 1027), (1902579, 818), (1903397, 798), (1904195, 602), (1904797, 609), (1905406, 846), (1906252, 601), (1906853, 589), (1907442, 814), (1908256, 737), (1908993, 937), (1909930, 810), (1910740, 785), (1911525, 710), (1912235, 883), (1913118, 637), (1913755, 947), (1914702, 662), (1915364, 842), (1916206, 602), (1916808, 761), (1917569, 510), (1918079, 848), (1918927, 843), (1919770, 688), (1920458, 945), (1921403, 777), (1922180, 840), (1923020, 954), (1923974, 1077), (1925051, 887), (1925938, 669), (1926607, 933), (1927540, 731), (1928271, 568), (1928839, 443), (1929282, 822), (1930104, 806), (1930910, 455), (1931365, 1028), (1932393, 549), (1932942, 798), (1933740, 881), (1934621, 827), (1935448, 826), (1936274, 696), (1936970, 826), (1937796, 768), (1938564, 828), (1939392, 604), (1939996, 604), (1940600, 476), (1941076, 686), (1941762, 484), (1942246, 816), (1943062, 894), (1943956, 835), (1944791, 718), (1945509, 658), (1946167, 604), (1946771, 890), (1947661, 523), (1948184, 606), (1948790, 780), (1949570, 542), (1950112, 903), (1951015, 2112), (1953127, 581), (1953708, 705), (1954413, 941), (1955354, 971), (1956325, 539)], [(1956864, 48), None, (1956912, 35), (1956947, 42), None, None, None, None, None, None, None, None, None, None, None, None, None, (1956989, 42), None, (1957031, 25), (1957056, 44), (1957100, 22), (1957122, 18), None, None, None, None, (1957140, 26), None, None, None, None, (1957166, 21), (1957187, 25), None, None, (1957212, 26), None, None, None, None, (1957238, 44), (1957282, 21), (1957303, 23), None, None, None, None, (1957326, 48), None, None, None, None, None, (1957374, 31), None, None, None, None, (1957405, 42), None, (1957447, 22), None, (1957469, 21), None, (1957490, 26), (1957516, 42), None, None, (1957558, 77), None, None, None, None, None, (1957635, 21), (1957656, 21), None, None, (1957677, 34), (1957711, 42), None, None, None, (1957753, 25), None, None, (1957778, 21), None, None, None, None, None, (1957799, 24), (1957823, 21), None, None, (1957844, 26), None, (1957870, 18), None, (1957888, 54), None, None, None, None, None, None, (1957942, 26), None, (1957968, 19), None, (1957987, 20), None, None, (1958007, 42), (1958049, 42), (1958091, 17), (1958108, 17), (1958125, 26), None, (1958151, 26), None, None, None, (1958177, 26), (1958203, 20), (1958223, 26), None, (1958249, 42), (1958291, 63), None, None, None, (1958354, 40), (1958394, 48), None, None, None, (1958442, 47), None, None, None, None, None, None, None, (1958489, 42), None, (1958531, 55), None, (1958586, 9), None, (1958595, 21), (1958616, 42), None, None, (1958658, 65), (1958723, 82), None, None, (1958805, 42), None, None, None, None, None, None, None, None, None, (1958847, 42), (1958889, 21), (1958910, 21), None, (1958931, 42), (1958973, 25), None, (1958998, 16), (1959014, 21), (1959035, 56), None, None, (1959091, 21), (1959112, 19), (1959131, 26), None, (1959157, 16), None, (1959173, 39), None, None, (1959212, 38), None, (1959250, 22), (1959272, 21), (1959293, 21), None, None, (1959314, 63), None, (1959377, 21), (1959398, 42), None, (1959440, 17), None, None, None, None, (1959457, 21), (1959478, 21), None, None, (1959499, 21), None, None, (1959520, 21), None, (1959541, 26), None, (1959567, 50), None, None, None, (1959617, 50), (1959667, 26), (1959693, 21), (1959714, 21), (1959735, 19), None, (1959754, 35), (1959789, 26), (1959815, 23), (1959838, 21), (1959859, 42), None, None, None, None, None, None, (1959901, 21), None, None, None, (1959922, 21), None, None, (1959943, 90), None, (1960033, 239), (1960272, 38), None, None, None, None]]  # noqa: E501
_CRC8_TABLE = [
    0x00, 0x07, 0x0e, 0x09, 0x1c, 0x1b, 0x12, 0x15,
    0x38, 0x3f, 0x36, 0x31, 0x24, 0x23, 0x2a, 0x2d,
    0x70, 0x77, 0x7e, 0x79, 0x6c, 0x6b, 0x62, 0x65,
    0x48, 0x4f, 0x46, 0x41, 0x54, 0x53, 0x5a, 0x5d,
    0xe0, 0xe7, 0xee, 0xe9, 0xfc, 0xfb, 0xf2, 0xf5,
    0xd8, 0xdf, 0xd6, 0xd1, 0xc4, 0xc3, 0xca, 0xcd,
    0x90, 0x97, 0x9e, 0x99, 0x8c, 0x8b, 0x82, 0x85,
    0xa8, 0xaf, 0xa6, 0xa1, 0xb4, 0xb3, 0xba, 0xbd,
    0xc7, 0xc0, 0xc9, 0xce, 0xdb, 0xdc, 0xd5, 0xd2,
    0xff, 0xf8, 0xf1, 0xf6, 0xe3, 0xe4, 0xed, 0xea,
    0xb7, 0xb0, 0xb9, 0xbe, 0xab, 0xac, 0xa5, 0xa2,
    0x8f, 0x88, 0x81, 0x86, 0x93, 0x94, 0x9d, 0x9a,
    0x27, 0x20, 0x29, 0x2e, 0x3b, 0x3c, 0x35, 0x32,
    0x1f, 0x18, 0x11, 0x16, 0x03, 0x04, 0x0d, 0x0a,
    0x57, 0x50, 0x59, 0x5e, 0x4b, 0x4c, 0x45, 0x42,
    0x6f, 0x68, 0x61, 0x66, 0x73, 0x74, 0x7d, 0x7a,
    0x89, 0x8e, 0x87, 0x80, 0x95, 0x92, 0x9b, 0x9c,
    0xb1, 0xb6, 0xbf, 0xb8, 0xad, 0xaa, 0xa3, 0xa4,
    0xf9, 0xfe, 0xf7, 0xf0, 0xe5, 0xe2, 0xeb, 0xec,
    0xc1, 0xc6, 0xcf, 0xc8, 0xdd, 0xda, 0xd3, 0xd4,
    0x69, 0x6e, 0x67, 0x60, 0x75, 0x72, 0x7b, 0x7c,
    0x51, 0x56, 0x5f, 0x58, 0x4d, 0x4a, 0x43, 0x44,
    0x19, 0x1e, 0x17, 0x10, 0x05, 0x02, 0x0b, 0x0c,
    0x21, 0x26, 0x2f, 0x28, 0x3d, 0x3a, 0x33, 0x34,
    0x4e, 0x49, 0x40, 0x47, 0x52, 0x55, 0x5c, 0x5b,
    0x76, 0x71, 0x78, 0x7f, 0x6a, 0x6d, 0x64, 0x63,
    0x3e, 0x39, 0x30, 0x37, 0x22, 0x25, 0x2c, 0x2b,
    0x06, 0x01, 0x08, 0x0f, 0x1a, 0x1d, 0x14, 0x13,
    0xae, 0xa9, 0xa0, 0xa7, 0xb2, 0xb5, 0xbc, 0xbb,
    0x96, 0x91, 0x98, 0x9f, 0x8a, 0x8d, 0x84, 0x83,
    0xde, 0xd9, 0xd0, 0xd7, 0xc2, 0xc5, 0xcc, 0xcb,
    0xe6, 0xe1, 0xe8, 0xef, 0xfa, 0xfd, 0xf4, 0xf3
]
# fmt: on

_IS_LEAF = 0x80
_INCLUDE_SUBDOMAINS = 0x40


try:
    from importlib.resources import open_binary

    def open_pkg_binary(path: str) -> typing.BinaryIO:
        return open_binary("hstspreload", path)


except ImportError:

    def open_pkg_binary(path: str) -> typing.BinaryIO:
        return open(
            os.path.join(os.path.dirname(os.path.abspath(__file__)), path),
            "rb",
        )


@functools.lru_cache(maxsize=1024)
def in_hsts_preload(host: typing.AnyStr) -> bool:
    """Determines if an IDNA-encoded host is on the HSTS preload list"""

    if isinstance(host, str):
        host = host.encode("ascii")
    labels = host.lower().split(b".")

    # Fast-branch for gTLDs that are registered to preload all sub-domains.
    if labels[-1] in _GTLD_INCLUDE_SUBDOMAINS:
        return True

    with open_pkg_binary("hstspreload.bin") as f:
        for layer, label in enumerate(labels[::-1]):
            # None of our layers are greater than 4 deep.
            if layer > 3:
                return False

            # Read the jump table for the layer and label
            jump_info = _JUMPTABLE[layer][_crc8(label)]
            if jump_info is None:
                # No entry: host is not preloaded
                return False

            # Read the set of entries for that layer and label
            f.seek(jump_info[0])
            data = bytearray(jump_info[1])
            f.readinto(data)

            for is_leaf, include_subdomains, ent_label in _iter_entries(data):
                # We found a potential leaf
                if is_leaf:
                    if ent_label == host:
                        return True
                    if include_subdomains and host.endswith(b"." + ent_label):
                        return True

                # Continue traversing as we're not at a leaf.
                elif label == ent_label:
                    break
            else:
                return False
    return False


def _iter_entries(data: bytes) -> typing.Iterable[typing.Tuple[int, int, bytes]]:
    while data:
        flags = data[0]
        size = data[1]
        label = bytes(data[2 : 2 + size])
        yield (flags & _IS_LEAF, flags & _INCLUDE_SUBDOMAINS, label)
        data = data[2 + size :]


def _crc8(value: bytes) -> int:
    # CRC8 reference implementation: https://github.com/niccokunzmann/crc8
    checksum = 0x00
    for byte in value:
        checksum = _CRC8_TABLE[checksum ^ byte]
    return checksum
