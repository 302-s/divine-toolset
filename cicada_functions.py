from collections import Counter
import math
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import numpy as np
from collections import Counter

rune_to_decimal = {
    'ᚠ': 0, 'ᚢ': 1, 'ᚦ': 2, 'ᚩ': 3, 'ᚱ': 4, 'ᚳ': 5, 'ᚷ': 6, 'ᚹ': 7, 
    'ᚻ': 8, 'ᚾ': 9, 'ᛁ': 10, 'ᛄ': 11, 'ᛇ': 12, 'ᛈ': 13, 'ᛉ': 14, 'ᛋ': 15, 
    'ᛏ': 16, 'ᛒ': 17, 'ᛖ': 18, 'ᛗ': 19, 'ᛚ': 20, 'ᛝ': 21, 'ᛟ': 22, 'ᛞ': 23, 
    'ᚪ': 24, 'ᚫ': 25, 'ᚣ': 26, 'ᛡ': 27, 'ᛠ': 28
}

# Mapping of runes to phonetic or symbolic representations
rune_to_phonetic = {
    'ᚠ': 'F', 'ᚢ': 'V(U)', 'ᚦ': 'TH', 'ᚩ': 'O', 'ᚱ': 'R', 'ᚳ': 'C(K)', 
    'ᚷ': 'G', 'ᚹ': 'W', 'ᚻ': 'H', 'ᚾ': 'N', 'ᛁ': 'I', 'ᛄ': 'J', 'ᛇ': 'EO', 
    'ᛈ': 'P', 'ᛉ': 'X', 'ᛋ': 'S(Z)', 'ᛏ': 'T', 'ᛒ': 'B', 'ᛖ': 'E', 'ᛗ': 'M', 
    'ᛚ': 'L', 'ᛝ': 'NG(ING)', 'ᛟ': 'OE', 'ᛞ': 'D', 'ᚪ': 'A', 'ᚫ': 'AE', 
    'ᚣ': 'Y', 'ᛡ': 'IA(IO)', 'ᛠ': 'EA'
}

decimal_to_rune = {v: k for k, v in rune_to_decimal.items()}

primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199, 211, 223, 227, 229, 233, 239, 241, 251, 257, 263, 269, 271, 277, 281, 283, 293, 307, 311, 313, 317, 331, 337, 347, 349, 353, 359, 367, 373, 379, 383, 389, 397, 401, 409, 419, 421, 431, 433, 439, 443, 449, 457, 461, 463, 467, 479, 487, 491, 499, 503, 509, 521, 523, 541, 547, 557, 563, 569, 571, 577, 587, 593, 599, 601, 607, 613, 617, 619, 631, 641, 643, 647, 653, 659, 661, 673, 677, 683, 691, 701, 709, 719, 727, 733, 739, 743, 751, 757, 761, 769, 773, 787, 797, 809, 811, 821, 823, 827, 829, 839, 853, 857, 859, 863, 877, 881, 883, 887, 907, 911, 919, 929, 937, 941, 947, 953, 967, 971, 977, 983, 991, 997, 1009, 1013, 1019, 1021, 1031, 1033, 1039, 1049, 1051, 1061, 1063, 1069, 1087, 1091, 1093, 1097, 1103, 1109, 1117, 1123, 1129, 1151, 1153, 1163, 1171, 1181, 1187, 1193, 1201, 1213, 1217, 1223, 1229, 1231, 1237, 1249, 1259, 1277, 1279, 1283, 1289, 1291, 1297, 1301, 1303, 1307, 1319, 1321, 1327, 1361, 1367, 1373, 1381, 1399, 1409, 1423, 1427, 1429, 1433, 1439, 1447, 1451, 1453, 1459, 1471, 1481, 1483, 1487, 1489, 1493, 1499, 1511, 1523, 1531, 1543, 1549, 1553, 1559, 1567, 1571, 1579, 1583, 1597, 1601, 1607, 1609, 1613, 1619, 1621, 1627, 1637, 1657, 1663, 1667, 1669, 1693, 1697, 1699, 1709, 1721, 1723, 1733, 1741, 1747, 1753, 1759, 1777, 1783, 1787, 1789, 1801, 1811, 1823, 1831, 1847, 1861, 1867, 1871, 1873, 1877, 1879, 1889, 1901, 1907, 1913, 1931, 1933, 1949, 1951, 1973, 1979, 1987, 1993, 1997, 1999, 2003, 2011, 2017, 2027, 2029, 2039, 2053, 2063, 2069, 2081, 2083, 2087, 2089, 2099, 2111, 2113, 2129, 2131, 2137, 2141, 2143, 2153, 2161, 2179, 2203, 2207, 2213, 2221, 2237, 2239, 2243, 2251, 2267, 2269, 2273, 2281, 2287, 2293, 2297, 2309, 2311, 2333, 2339, 2341, 2347, 2351, 2357, 2371, 2377, 2381, 2383, 2389, 2393, 2399, 2411, 2417, 2423, 2437, 2441, 2447, 2459, 2467, 2473, 2477, 2503, 2521, 2531, 2539, 2543, 2549, 2551, 2557, 2579, 2591, 2593, 2609, 2617, 2621, 2633, 2647, 2657, 2659, 2663, 2671, 2677, 2683, 2687, 2689, 2693, 2699, 2707, 2711, 2713, 2719, 2729, 2731, 2741, 2749, 2753, 2767, 2777, 2789, 2791, 2797, 2801, 2803, 2819, 2833, 2837, 2843, 2851, 2857, 2861, 2879, 2887, 2897, 2903, 2909, 2917, 2927, 2939, 2953, 2957, 2963, 2969, 2971, 2999, 3001, 3011, 3019, 3023, 3037, 3041, 3049, 3061, 3067, 3079, 3083, 3089, 3109, 3119, 3121, 3137, 3163, 3167, 3169, 3181, 3187, 3191, 3203, 3209, 3217, 3221, 3229, 3251, 3253, 3257, 3259, 3271, 3299, 3301, 3307, 3313, 3319, 3323, 3329, 3331, 3343, 3347, 3359, 3361, 3371, 3373, 3389, 3391, 3407, 3413, 3433, 3449, 3457, 3461, 3463, 3467, 3469, 3491, 3499, 3511, 3517, 3527, 3529, 3533, 3539, 3541, 3547, 3557, 3559, 3571, 3581, 3583, 3593, 3607, 3613, 3617, 3623, 3631, 3637, 3643, 3659, 3671, 3673, 3677, 3691, 3697, 3701, 3709, 3719, 3727, 3733, 3739, 3761, 3767, 3769, 3779, 3793, 3797, 3803, 3821, 3823, 3833, 3847, 3851, 3853, 3863, 3877, 3881, 3889, 3907, 3911, 3917, 3919, 3923, 3929, 3931, 3943, 3947, 3967, 3989, 4001, 4003, 4007, 4013, 4019, 4021, 4027, 4049, 4051, 4057, 4073, 4079, 4091, 4093, 4099, 4111, 4127, 4129, 4133, 4139, 4153, 4157, 4159, 4177, 4201, 4211, 4217, 4219, 4229, 4231, 4241, 4243, 4253, 4259, 4261, 4271, 4273, 4283, 4289, 4297, 4327, 4337, 4339, 4349, 4357, 4363, 4373, 4391, 4397, 4409, 4421, 4423, 4441, 4447, 4451, 4457, 4463, 4481, 4483, 4493, 4507, 4513, 4517, 4519, 4523, 4547, 4549, 4561, 4567, 4583, 4591, 4597, 4603, 4621, 4637, 4639, 4643, 4649, 4651, 4657, 4663, 4673, 4679, 4691, 4703, 4721, 4723, 4729, 4733, 4751, 4759, 4783, 4787, 4789, 4793, 4799, 4801, 4813, 4817, 4831, 4861, 4871, 4877, 4889, 4903, 4909, 4919, 4931, 4933, 4937, 4943, 4951, 4957, 4967, 4969, 4973, 4987, 4993, 4999, 5003, 5009, 5011, 5021, 5023, 5039, 5051, 5059, 5077, 5081, 5087, 5099, 5101, 5107, 5113, 5119, 5147, 5153, 5167, 5171, 5179, 5189, 5197, 5209, 5227, 5231, 5233, 5237, 5261, 5273, 5279, 5281, 5297, 5303, 5309, 5323, 5333, 5347, 5351, 5381, 5387, 5393, 5399, 5407, 5413, 5417, 5419, 5431, 5437, 5441, 5443, 5449, 5471, 5477, 5479, 5483, 5501, 5503, 5507, 5519, 5521, 5527, 5531, 5557, 5563, 5569, 5573, 5581, 5591, 5623, 5639, 5641, 5647, 5651, 5653, 5657, 5659, 5669, 5683, 5689, 5693, 5701, 5711, 5717, 5737, 5741, 5743, 5749, 5779, 5783, 5791, 5801, 5807, 5813, 5821, 5827, 5839, 5843, 5849, 5851, 5857, 5861, 5867, 5869, 5879, 5881, 5897, 5903, 5923, 5927, 5939, 5953, 5981, 5987, 6007, 6011, 6029, 6037, 6043, 6047, 6053, 6067, 6073, 6079, 6089, 6091, 6101, 6113, 6121, 6131, 6133, 6143, 6151, 6163, 6173, 6197, 6199, 6203, 6211, 6217, 6221, 6229, 6247, 6257, 6263, 6269, 6271, 6277, 6287, 6299, 6301, 6311, 6317, 6323, 6329, 6337, 6343, 6353, 6359, 6361, 6367, 6373, 6379, 6389, 6397, 6421, 6427, 6449, 6451, 6469, 6473, 6481, 6491, 6521, 6529, 6547, 6551, 6553, 6563, 6569, 6571, 6577, 6581, 6599, 6607, 6619, 6637, 6653, 6659, 6661, 6673, 6679, 6689, 6691, 6701, 6703, 6709, 6719, 6733, 6737, 6761, 6763, 6779, 6781, 6791, 6793, 6803, 6823, 6827, 6829, 6833, 6841, 6857, 6863, 6869, 6871, 6883, 6899, 6907, 6911, 6917, 6947, 6949, 6959, 6961, 6967, 6971, 6977, 6983, 6991, 6997, 7001, 7013, 7019, 7027, 7039, 7043, 7057, 7069, 7079, 7103, 7109, 7121, 7127, 7129, 7151, 7159, 7177, 7187, 7193, 7207, 7211, 7213, 7219, 7229, 7237, 7243, 7247, 7253, 7283, 7297, 7307, 7309, 7321, 7331, 7333, 7349, 7351, 7369, 7393, 7411, 7417, 7433, 7451, 7457, 7459, 7477, 7481, 7487, 7489, 7499, 7507, 7517, 7523, 7529, 7537, 7541, 7547, 7549, 7559, 7561, 7573, 7577, 7583, 7589, 7591, 7603, 7607, 7621, 7639, 7643, 7649, 7669, 7673, 7681, 7687, 7691, 7699, 7703, 7717, 7723, 7727, 7741, 7753, 7757, 7759, 7789, 7793, 7817, 7823, 7829, 7841, 7853, 7867, 7873, 7877, 7879, 7883, 7901, 7907, 7919, 7927, 7933, 7937, 7949, 7951, 7963, 7993, 8009, 8011, 8017, 8039, 8053, 8059, 8069, 8081, 8087, 8089, 8093, 8101, 8111, 8117, 8123, 8147, 8161, 8167, 8171, 8179, 8191, 8209, 8219, 8221, 8231, 8233, 8237, 8243, 8263, 8269, 8273, 8287, 8291, 8293, 8297, 8311, 8317, 8329, 8353, 8363, 8369, 8377, 8387, 8389, 8419, 8423, 8429, 8431, 8443, 8447, 8461, 8467, 8501, 8513, 8521, 8527, 8537, 8539, 8543, 8563, 8573, 8581, 8597, 8599, 8609, 8623, 8627, 8629, 8641, 8647, 8663, 8669, 8677, 8681, 8689, 8693, 8699, 8707, 8713, 8719, 8731, 8737, 8741, 8747, 8753, 8761, 8779, 8783, 8803, 8807, 8819, 8821, 8831, 8837, 8839, 8849, 8861, 8863, 8867, 8887, 8893, 8923, 8929, 8933, 8941, 8951, 8963, 8969, 8971, 8999, 9001, 9007, 9011, 9013, 9029, 9041, 9043, 9049, 9059, 9067, 9091, 9103, 9109, 9127, 9133, 9137, 9151, 9157, 9161, 9173, 9181, 9187, 9199, 9203, 9209, 9221, 9227, 9239, 9241, 9257, 9277, 9281, 9283, 9293, 9311, 9319, 9323, 9337, 9341, 9343, 9349, 9371, 9377, 9391, 9397, 9403, 9413, 9419, 9421, 9431, 9433, 9437, 9439, 9461, 9463, 9467, 9473, 9479, 9491, 9497, 9511, 9521, 9533, 9539, 9547, 9551, 9587, 9601, 9613, 9619, 9623, 9629, 9631, 9643, 9649, 9661, 9677, 9679, 9689, 9697, 9719, 9721, 9733, 9739, 9743, 9749, 9767, 9769, 9781, 9787, 9791, 9803, 9811, 9817, 9829, 9833, 9839, 9851, 9857, 9859, 9871, 9883, 9887, 9901, 9907, 9923, 9929, 9931, 9941, 9949, 9967, 9973, 10007, 10009, 10037, 10039, 10061, 10067, 10069, 10079, 10091, 10093, 10099, 10103, 10111, 10133, 10139, 10141, 10151, 10159, 10163, 10169, 10177, 10181, 10193, 10211, 10223, 10243, 10247, 10253, 10259, 10267, 10271, 10273, 10289, 10301, 10303, 10313, 10321, 10331, 10333, 10337, 10343, 10357, 10369, 10391, 10399, 10427, 10429, 10433, 10453, 10457, 10459, 10463, 10477, 10487, 10499, 10501, 10513, 10529, 10531, 10559, 10567, 10589, 10597, 10601, 10607, 10613, 10627, 10631, 10639, 10651, 10657, 10663, 10667, 10687, 10691, 10709, 10711, 10723, 10729, 10733, 10739, 10753, 10771, 10781, 10789, 10799, 10831, 10837, 10847, 10853, 10859, 10861, 10867, 10883, 10889, 10891, 10903, 10909, 10937, 10939, 10949, 10957, 10973, 10979, 10987, 10993, 11003, 11027, 11047, 11057, 11059, 11069, 11071, 11083, 11087, 11093, 11113, 11117, 11119, 11131, 11149, 11159, 11161, 11171, 11173, 11177, 11197, 11213, 11239, 11243, 11251, 11257, 11261, 11273, 11279, 11287, 11299, 11311, 11317, 11321, 11329, 11351, 11353, 11369, 11383, 11393, 11399, 11411, 11423, 11437, 11443, 11447, 11467, 11471, 11483, 11489, 11491, 11497, 11503, 11519, 11527, 11549, 11551, 11579, 11587, 11593, 11597, 11617, 11621, 11633, 11657, 11677, 11681, 11689, 11699, 11701, 11717, 11719, 11731, 11743, 11777, 11779, 11783, 11789, 11801, 11807, 11813, 11821, 11827, 11831, 11833, 11839, 11863, 11867, 11887, 11897, 11903, 11909, 11923, 11927, 11933, 11939, 11941, 11953, 11959, 11969, 11971, 11981, 11987, 12007, 12011, 12037, 12041, 12043, 12049, 12071, 12073, 12097, 12101, 12107, 12109, 12113, 12119, 12143, 12149, 12157, 12161, 12163, 12197, 12203, 12211, 12227, 12239, 12241, 12251, 12253, 12263, 12269, 12277, 12281, 12289, 12301, 12323, 12329, 12343, 12347, 12373, 12377, 12379, 12391, 12401, 12409, 12413, 12421, 12433, 12437, 12451, 12457, 12473, 12479, 12487, 12491, 12497, 12503, 12511, 12517, 12527, 12539, 12541, 12547, 12553, 12569, 12577, 12583, 12589, 12601, 12611, 12613, 12619, 12637, 12641, 12647, 12653, 12659, 12671, 12689, 12697, 12703, 12713, 12721, 12739, 12743, 12757, 12763, 12781, 12791, 12799, 12809, 12821, 12823, 12829, 12841, 12853, 12889, 12893, 12899, 12907, 12911, 12917, 12919, 12923, 12941, 12953, 12959, 12967, 12973, 12979, 12983, 13001, 13003, 13007, 13009, 13033, 13037, 13043, 13049, 13063, 13093, 13099, 13103, 13109, 13121, 13127, 13147, 13151, 13159, 13163, 13171, 13177, 13183, 13187, 13217, 13219, 13229, 13241, 13249, 13259, 13267, 13291, 13297, 13309, 13313, 13327, 13331, 13337, 13339, 13367, 13381, 13397, 13399, 13411, 13417, 13421, 13441, 13451, 13457, 13463, 13469, 13477, 13487, 13499, 13513, 13523, 13537, 13553, 13567, 13577, 13591, 13597, 13613, 13619, 13627, 13633, 13649, 13669, 13679, 13681, 13687, 13691, 13693, 13697, 13709, 13711, 13721, 13723, 13729, 13751, 13757, 13759, 13763, 13781, 13789, 13799, 13807, 13829, 13831, 13841, 13859, 13873, 13877, 13879, 13883, 13901, 13903, 13907, 13913, 13921, 13931, 13933, 13963, 13967, 13997, 13999, 14009, 14011, 14029, 14033, 14051, 14057, 14071, 14081, 14083, 14087, 14107, 14143, 14149, 14153, 14159, 14173, 14177, 14197, 14207, 14221, 14243, 14249, 14251, 14281, 14293, 14303, 14321, 14323, 14327, 14341, 14347, 14369, 14387, 14389, 14401, 14407, 14411, 14419, 14423, 14431, 14437, 14447, 14449, 14461, 14479, 14489, 14503, 14519, 14533, 14537, 14543, 14549, 14551, 14557, 14561, 14563, 14591, 14593, 14621, 14627, 14629, 14633, 14639, 14653, 14657, 14669, 14683, 14699, 14713, 14717, 14723, 14731, 14737, 14741, 14747, 14753, 14759, 14767, 14771, 14779, 14783, 14797, 14813, 14821, 14827, 14831, 14843, 14851, 14867, 14869, 14879, 14887, 14891, 14897, 14923, 14929, 14939, 14947, 14951, 14957, 14969, 14983, 15013, 15017, 15031, 15053, 15061, 15073, 15077, 15083, 15091, 15101, 15107, 15121, 15131, 15137, 15139, 15149, 15161, 15173, 15187, 15193, 15199, 15217, 15227, 15233, 15241, 15259, 15263, 15269, 15271, 15277, 15287, 15289, 15299, 15307, 15313, 15319, 15329, 15331, 15349, 15359, 15361, 15373, 15377, 15383, 15391, 15401, 15413, 15427, 15439, 15443, 15451, 15461, 15467, 15473, 15493, 15497, 15511, 15527, 15541, 15551, 15559, 15569, 15581, 15583, 15601, 15607, 15619, 15629, 15641, 15643, 15647, 15649, 15661, 15667, 15671, 15679, 15683, 15727, 15731, 15733, 15737, 15739, 15749, 15761, 15767, 15773, 15787, 15791, 15797, 15803, 15809, 15817, 15823, 15859, 15877, 15881, 15887, 15889, 15901, 15907, 15913, 15919, 15923, 15937, 15959, 15971, 15973, 15991, 16001, 16007, 16033, 16057, 16061, 16063, 16067, 16069, 16073, 16087, 16091, 16097, 16103, 16111, 16127, 16139, 16141, 16183, 16187, 16189, 16193, 16217, 16223, 16229, 16231, 16249, 16253, 16267, 16273, 16301, 16319, 16333, 16339, 16349, 16361, 16363, 16369, 16381, 16411, 16417, 16421, 16427, 16433, 16447, 16451, 16453, 16477, 16481, 16487, 16493, 16519, 16529, 16547, 16553, 16561, 16567, 16573, 16603, 16607, 16619, 16631, 16633, 16649, 16651, 16657, 16661, 16673, 16691, 16693, 16699, 16703, 16729, 16741, 16747, 16759, 16763, 16787, 16811, 16823, 16829, 16831, 16843, 16871, 16879, 16883, 16889, 16901, 16903, 16921, 16927, 16931, 16937, 16943, 16963, 16979, 16981, 16987, 16993, 17011, 17021, 17027, 17029, 17033, 17041, 17047, 17053, 17077, 17093, 17099, 17107, 17117, 17123, 17137, 17159, 17167, 17183, 17189, 17191, 17203, 17207, 17209, 17231, 17239, 17257, 17291, 17293, 17299, 17317, 17321, 17327, 17333, 17341, 17351, 17359, 17377, 17383, 17387, 17389]

def autokey(ciphertext,phonetic, reversed):

    if reversed == "True":
        ciphertext = ciphertext[::-1]

    #ciphertext = clean(ciphertext,[])

    transformed_runes = ""

    first_rune = True
    last_rune = ""
    phonetics = ""

    drop = {'.', '-', '–', '—', '−', "/", "%"}

    for rune in ciphertext:
        if rune in drop:
            transformed_runes = transformed_runes + rune
        else:
            if first_rune:
                transformed_runes = transformed_runes + rune
                last_rune = rune
                first_rune = False
            else:
                new_rune = (rune_to_decimal[rune] - rune_to_decimal[last_rune]) % 29
                new_rune = decimal_to_rune[new_rune]
                last_rune = rune
                transformed_runes = transformed_runes + new_rune

    if phonetic == True:
        for rune in transformed_runes:
            if rune in rune_to_phonetic:
                rune_phon = rune_to_phonetic[rune]
                phonetics = phonetics + rune_phon
            else:
                phonetics = phonetics + rune

        return phonetics
    else:
        return transformed_runes
    

def fibo(nums):
    for num in nums:
        #print(num)
        index = 3301 - num
        print(f"Index: {index}, prime: {nthprime(index)}, position: {prime_position(index)}")


def clean(text,positions):
    # Keep all visible (non-whitespace) characters
    s = set(positions)
    drop = {'.', '-', '–', '—', '−', "/", "%"}
    text2 = ''.join(ch for i, ch in enumerate(text) if i not in s)
    return ''.join(ch for ch in text2 if not ch.isspace() and ch not in drop)

def ioc_of_text(text):
    N = len(text)
    if N < 2:
        return 0.0
    counts = Counter(text)
    num = sum(n*(n-1) for n in counts.values())
    return num / (N*(N-1))

def avg_ioc_for_keylen(ctext, k):
    groups = ['' for _ in range(k)]
    for i, ch in enumerate(ctext):
        groups[i % k] += ch
    iocs = [ioc_of_text(g) for g in groups if len(g) > 1]
    return sum(iocs)/len(iocs) if iocs else 0.0, iocs

def bigram_ioc_of_text(text):
    # Only consider alphabetic characters
    text = ''.join([c for c in text.upper() if c.isalpha()])
    if len(text) < 3:  # need at least 2 bigrams
        return 0.0

    # Create bigrams
    bigrams = [text[i:i+2] for i in range(len(text) - 1)]
    N = len(bigrams)
    counts = Counter(bigrams)
    
    num = sum(n * (n - 1) for n in counts.values())
    return num / (N * (N - 1))

def avg_bigram_ioc_for_keylen(ctext, k):
    groups = ['' for _ in range(k)]
    for i, ch in enumerate(ctext):
        groups[i % k] += ch
    iocs = [bigram_ioc_of_text(g) for g in groups if len(g) > 2]
    return sum(iocs) / len(iocs) if iocs else 0.0, iocs

def find_true_keylen(ioc_values, k_max, tolerance=0.9):
    max_val = ioc_values[k_max]
    for d in range(1, k_max):
        if k_max % d == 0 and ioc_values.get(d, 0) >= tolerance * max_val:
            return d
    return k_max

def undo_transposition(ciphertext, key_order):
    n_cols = len(key_order)
    n_rows = math.ceil(len(ciphertext) / n_cols)
    n_full_cols = len(ciphertext) % n_cols  # how many columns are longer

    # Split ciphertext into columns
    col_lengths = [n_rows if i < n_full_cols else n_rows - 1 for i in range(n_cols)]
    cols = []
    start = 0
    for length in col_lengths:
        cols.append(list(ciphertext[start:start + length]))
        start += length

    # Reorder columns back to original order
    ordered_cols = [None] * n_cols
    for idx, col_index in enumerate(key_order):
        ordered_cols[col_index] = cols[idx]

    # Reconstruct plaintext by reading row-wise
    plaintext = ''
    for i in range(n_rows):
        for col in ordered_cols:
            if i < len(col):
                plaintext += col[i]

    return plaintext

def rune_decimals(runes):

    decimals = []

    for rune in runes:
        decimals.append(rune_to_decimal[rune])

    return decimals

def decimal_runes(decimals):
    runes = []
    for decimal in decimals:
        runes.append(decimal_to_rune[decimal])
    return runes

def vigenere(runes, key, phonetic, skips, reverse):


    if reverse == True:
        runes = runes[::-1]
    transformed_runes = ""
    phonetics = ""
    i = 0
    rune_indx = 0
    skip = skips
    for rune in runes:
        rune_indx = rune_indx + 1
        if rune_indx in skip:
            transformed_runes = transformed_runes + rune
            continue
        else:
            if rune in rune_to_decimal:
                rune_num = rune_to_decimal[rune]

                if i < len(key):
                    key_num = rune_to_decimal[key[i]]
                    rune_num = (rune_num - key_num) % 29
                    new_rune = decimal_to_rune[rune_num]
                    transformed_runes = transformed_runes + new_rune
                    i = i + 1
                else:
                    i = 0
                    key_num = rune_to_decimal[key[i]]
                    rune_num = (rune_num - key_num) % 29
                    new_rune = decimal_to_rune[rune_num]
                    transformed_runes = transformed_runes + new_rune
                    i = i + 1
            else:
                transformed_runes = transformed_runes + rune


    if phonetic == True:
        for rune in transformed_runes:
            if rune in rune_to_phonetic:
                rune_phon = rune_to_phonetic[rune]
                phonetics = phonetics + rune_phon
            else:
                phonetics = phonetics + rune

        return phonetics
    else:
        return transformed_runes

def vigenere_bruteforce(runes, key_len, phonetic,skips):

    i = 0
    key = ""

    runes_mod = runes[:key_len]

    while i<key_len:
        if key == "":
            # print out every option and corresponding vigenere.
            for rune in rune_to_decimal:
                results = vigenere(runes_mod, rune, True, [])
                print("{0}[{1}]: {2}".format(rune,rune_to_decimal.get(rune),results))
            key_letter = input("Select decimal [0-28]: ")
            new_key_rune = list(rune_to_decimal.keys())[list(rune_to_decimal.values()).index(int(key_letter))]
            key = key + new_key_rune
            i = i +1
            print("\n")
        else:
            # print out every option and corresponding vigenere.
            for rune in rune_to_decimal:
                trial_key = key + rune
                results = vigenere(runes_mod, trial_key, True, [])
                print("{0}[{1}]: {2}".format(rune,rune_to_decimal.get(rune),results))
            key_letter = input("Select decimal [0-28]: ")
            new_key_rune = list(rune_to_decimal.keys())[list(rune_to_decimal.values()).index(int(key_letter))]
            key = key + new_key_rune
            i = i +1
            print("\n")

    print(vigenere(runes, key, phonetic, skips))


def analysis_functions(analysis, ciphertext):
    if analysis.get("IoC"):

        ioc_values = {}  # store IoC per key length
        max_k = 29

        for k in range(1, max_k+1):
            avg_ioc, per = avg_ioc_for_keylen(ciphertext, k)
            ioc_values[k] = avg_ioc
            #print(f"{k:2d}\tavg IoC={avg_ioc:.5f}\tper-group={['%.5f' % x for x in per]}")

        # Plot
        print("\nIoC graph (higher bar = higher IoC):\n")
        scale = 200  # adjust scaling factor
        for k, v in ioc_values.items():
            bar = "█" * int(v * scale)
            print(f"{k:2d} | {bar} ({v:.4f})")

        # Find the key length with the highest IoC
        k_max = max(ioc_values, key=ioc_values.get)
        max_val = ioc_values[k_max]

        true_k = find_true_keylen(ioc_values, k_max)

        print(f"\nHighest IoC: {max_val:.5f} at k={k_max}")
        if true_k != k_max:
            print(f"Adjusted (fundamental) theorised key length: {true_k} (harmonic correction applied)")
        else:
            print(f"Theorised key length: {true_k}")

    if analysis.get("IC2"):
        print("IC2 functionality doesn't exist yet")

    if analysis.get("Frequency"):
        print(letter_frequency2(ciphertext))

def direct_translation(runes):
    phonetics = ""
    for rune in runes:
        if rune in rune_to_phonetic:
            rune_phon = rune_to_phonetic[rune]
            phonetics = phonetics + rune_phon
        else:
            phonetics = phonetics + rune

    return phonetics

def direct_translation_with_space(runes):
    phonetics = ""
    for rune in runes:
        if rune in rune_to_phonetic:
            rune_phon = rune_to_phonetic[rune]
            phonetics = phonetics + rune_phon + " "
        else:
            phonetics = phonetics + rune

    return phonetics


def atbash(runes, phonetic):

    transformed_runes = ""
    phonetics = ""

    for rune in runes:
        if rune in rune_to_decimal:
            rune_num = rune_to_decimal[rune]
            rune_num = 28 - rune_num
            new_rune = decimal_to_rune[rune_num]
            transformed_runes = transformed_runes + new_rune
        else:
            transformed_runes = transformed_runes + rune

    if phonetic == True:

        for rune in transformed_runes:
            if rune in rune_to_phonetic:
                rune_phon = rune_to_phonetic[rune]
                phonetics = phonetics + rune_phon
            else:
                phonetics = phonetics + rune

        return phonetics
    else:
        return transformed_runes
    
def shift(runes, shifts, phonetic):
    transformed_runes =  ""
    phonetics = ""

    for rune in runes:
        if rune in rune_to_decimal:
            rune_num = rune_to_decimal[rune]
            rune_num = (rune_num + shifts) % 29
            new_rune = decimal_to_rune[rune_num]
            transformed_runes = transformed_runes + new_rune
        else:
            transformed_runes = transformed_runes + rune
    
    if phonetic == True:

        for rune in transformed_runes:
            if rune in rune_to_phonetic:
                rune_phon = rune_to_phonetic[rune]
                phonetics = phonetics + rune_phon
            else:
                phonetics = phonetics + rune

        return phonetics
    else:
        return transformed_runes
    
def nthprime(n):
    import math
    start = 2
    count = 0
    while True:
        if all([start % i for i in range(2, int(math.sqrt(start)) + 1)]) != 0:
            count += 1
            if count == n:
                return start
        start += 1 

def prime_position(n):
    index = primes.index(n)
    return index

def eulers(runes, phonetic):
    transformed_runes = ""
    phonetics = ""
    rune_index = 0
    for rune in runes:
        if rune in rune_to_decimal:
            rune_num = rune_to_decimal[rune]
            prime = primes[rune_index]
            rune_num = (rune_num - (prime - 1)) % 29
            new_rune = decimal_to_rune[rune_num]
            transformed_runes = transformed_runes + new_rune
            rune_index = rune_index + 1
        else:
            transformed_runes = transformed_runes + rune

    if phonetic == True:

        for rune in transformed_runes:
            if rune in rune_to_phonetic:
                rune_phon = rune_to_phonetic[rune]
                phonetics = phonetics + rune_phon
            else:
                phonetics = phonetics + rune

        return phonetics
    else:
        return transformed_runes
    
def letter_frequency(text: str) -> list:
    text = text.replace(" ", "").lower()  # Remove spaces and convert to lowercase

    text2 = ""
    for rune in text:
        if rune in rune_to_decimal:
            text2 += rune

    letter_count = Counter(text2)
    total = sum(letter_count.values())

    # Compute percentage (with % sign, rounded to 2 decimal places)
    freq_list = sorted(
        [(r, f"{(count / total) * 100:.2f}%") for r, count in letter_count.items()],
        key=lambda x: float(x[1].strip('%')),
        reverse=True
    )

    return freq_list

def letter_frequency2(text: str) -> list:
    text = clean(text,[])
    text2 = "".join(r for r in text if r in rune_to_decimal)
    
    if not text2:
        print("No valid runes found in text. Nothing to graph.")
        return []

    letter_count = Counter(text2)
    total = sum(letter_count.values())

    freq_list = sorted(
        [(r, (count / total) * 100) for r, count in letter_count.items()],
        key=lambda x: x[1],
        reverse=True
    )

    if not freq_list:
        print("No frequency data available.")
        return []

    # Graph
    print("\nLetter Frequency Chart:\n")
    max_val = max(freq for _, freq in freq_list)
    scale = 40 / max_val  # 40 chars = max width

    for r, freq in freq_list:
        bar = "█" * int(freq * scale)
        print(f"{r} | {bar} {freq:5.2f}%")

    return "See frequencies above"

def letter_frequency_latin(text: str) -> list:

    letter_count = Counter(text)
    total = sum(letter_count.values())

    # Compute percentage (with % sign, rounded to 2 decimal places)
    freq_list = sorted(
        [(r, f"{(count / total) * 100:.2f}%") for r, count in letter_count.items()],
        key=lambda x: float(x[1].strip('%')),
        reverse=True
    )

    return freq_list

