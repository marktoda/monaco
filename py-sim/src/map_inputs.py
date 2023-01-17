a = """
[ -5.92403588  -2.09961041   5.10842475  -1.63619372   1.56596772
   7.78648556   6.40638994  -5.27050725   2.17560712   7.27581374
   8.25661028  -2.16783937  -8.73338452   5.16775773   4.43439213
 -10.08702292   5.32502721   3.34068275  -5.05668094   7.88928641
   7.04855914  11.40503862 -11.43984397  -6.01798165  -3.45369803
  -2.78160501  -9.50527209   4.94794348   1.73115421  -9.54193203
   4.56848694  -0.71558589   0.54187438   0.42186172  -9.20439745
  10.98993319   2.30649675   3.5517238   -0.49325797   4.06714769
   3.02003793  -0.84090557  -0.12617656  -5.65721236   5.00857652
  -1.12037216  -6.19347304  -0.48863355  -7.74925219  -5.83081974
  -2.00634125   8.55342369   8.21501223  -8.38177936   1.81574693
  -8.98401283  -3.76465674   9.90335496  -1.77966085  -0.53180865
   0.76155512  -0.89041625   1.71439182   9.80713344  -7.3089626
  -7.91987448  -2.57249113  -1.35536498   5.80312594   8.59604725
   2.73929098   4.91979225  -3.5076045   10.25572653   3.03228358
   1.57429602  -0.78500228  -1.41988512  -9.93841763  -3.56723041
  -4.57755683  -2.24552936   4.54141533  -4.12109438  -4.13473527
  -2.31165602   6.78085508   6.33976054   4.87972523   3.33017899
   8.0524662    5.96580217   1.70054952   0.47353315   6.02424368]


 """

res = []
for x in a.split():
    try:
        res.append(float(x))
    except:
        pass

print("ACCEL:")
print(f"\tposition: {res[0]}")
print(f"\ty: {res[1]}")
print(f"\tspeed: {res[2]}")
print(f"\tbalance: {res[3]}")
print(f"\tshield: {res[4]}")
print(f"\tworst opponent y: {res[5]}")
print(f"\tworst opponent speed: {res[6]}")
print(f"\tworst opponent balance: {res[7]}")
print(f"\tworst opponent shield: {res[8]}")
print(f"\tbest opponent y: {res[9]}")
print(f"\tbest opponent speed: {res[10]}")
print(f"\tbest opponent balance: {res[11]}")
print(f"\tbest opponent shield: {res[12]}")
print(f"\tdistance to banana: {res[13]}")
print(f"\taccel cost: {res[14]}")
print(f"\tshell cost: {res[15]}")
print(f"\tsuper cost: {res[16]}")
print(f"\tshield cost: {res[16]}")
print(f"\tbanana cost: {res[18]}")

diff = 19
print("")
print("SHELL:")
print(f"\tposition: {res[diff + 0]}")
print(f"\ty: {res[diff + 1]}")
print(f"\tspeed: {res[diff + 2]}")
print(f"\tbalance: {res[diff + 3]}")
print(f"\tshield: {res[diff + 4]}")
print(f"\tworst opponent y: {res[diff + 5]}")
print(f"\tworst opponent speed: {res[diff + 6]}")
print(f"\tworst opponent balance: {res[diff + 7]}")
print(f"\tworst opponent shield: {res[diff + 8]}")
print(f"\tbest opponent y: {res[diff + 9]}")
print(f"\tbest opponent speed: {res[diff + 10]}")
print(f"\tbest opponent balance: {res[diff + 11]}")
print(f"\tbest opponent shield: {res[diff + 12]}")
print(f"\tdistance to banana: {res[diff + 13]}")
print(f"\taccel cost: {res[diff + 14]}")
print(f"\tshell cost: {res[diff + 15]}")
print(f"\tsuper cost: {res[diff + 16]}")
print(f"\tshield cost: {res[diff + 16]}")
print(f"\tbanana cost: {res[diff + 18]}")

diff = 19 * 2
print("")
print("SUPER:")
print(f"\tposition: {res[diff + 0]}")
print(f"\ty: {res[diff + 1]}")
print(f"\tspeed: {res[diff + 2]}")
print(f"\tbalance: {res[diff + 3]}")
print(f"\tshield: {res[diff + 4]}")
print(f"\tworst opponent y: {res[diff + 5]}")
print(f"\tworst opponent speed: {res[diff + 6]}")
print(f"\tworst opponent balance: {res[diff + 7]}")
print(f"\tworst opponent shield: {res[diff + 8]}")
print(f"\tbest opponent y: {res[diff + 9]}")
print(f"\tbest opponent speed: {res[diff + 10]}")
print(f"\tbest opponent balance: {res[diff + 11]}")
print(f"\tbest opponent shield: {res[diff + 12]}")
print(f"\tdistance to banana: {res[diff + 13]}")
print(f"\taccel cost: {res[diff + 14]}")
print(f"\tshell cost: {res[diff + 15]}")
print(f"\tsuper cost: {res[diff + 16]}")
print(f"\tshield cost: {res[diff + 16]}")
print(f"\tbanana cost: {res[diff + 18]}")

diff = 19 * 3
print("")
print("SHIELD:")
print(f"\tposition: {res[diff + 0]}")
print(f"\ty: {res[diff + 1]}")
print(f"\tspeed: {res[diff + 2]}")
print(f"\tbalance: {res[diff + 3]}")
print(f"\tshield: {res[diff + 4]}")
print(f"\tworst opponent y: {res[diff + 5]}")
print(f"\tworst opponent speed: {res[diff + 6]}")
print(f"\tworst opponent balance: {res[diff + 7]}")
print(f"\tworst opponent shield: {res[diff + 8]}")
print(f"\tbest opponent y: {res[diff + 9]}")
print(f"\tbest opponent speed: {res[diff + 10]}")
print(f"\tbest opponent balance: {res[diff + 11]}")
print(f"\tbest opponent shield: {res[diff + 12]}")
print(f"\tdistance to banana: {res[diff + 13]}")
print(f"\taccel cost: {res[diff + 14]}")
print(f"\tshell cost: {res[diff + 15]}")
print(f"\tsuper cost: {res[diff + 16]}")
print(f"\tshield cost: {res[diff + 16]}")
print(f"\tbanana cost: {res[diff + 18]}")

diff = 19 * 4
print("")
print("BANANA:")
print(f"\tposition: {res[diff + 0]}")
print(f"\ty: {res[diff + 1]}")
print(f"\tspeed: {res[diff + 2]}")
print(f"\tbalance: {res[diff + 3]}")
print(f"\tshield: {res[diff + 4]}")
print(f"\tworst opponent y: {res[diff + 5]}")
print(f"\tworst opponent speed: {res[diff + 6]}")
print(f"\tworst opponent balance: {res[diff + 7]}")
print(f"\tworst opponent shield: {res[diff + 8]}")
print(f"\tbest opponent y: {res[diff + 9]}")
print(f"\tbest opponent speed: {res[diff + 10]}")
print(f"\tbest opponent balance: {res[diff + 11]}")
print(f"\tbest opponent shield: {res[diff + 12]}")
print(f"\tdistance to banana: {res[diff + 13]}")
print(f"\taccel cost: {res[diff + 14]}")
print(f"\tshell cost: {res[diff + 15]}")
print(f"\tsuper cost: {res[diff + 16]}")
print(f"\tshield cost: {res[diff + 16]}")
