import subprocess, re, math, shutil, time

dossier = "input"
prefix = "out"
extention  = ".png"

gpu_1 = 0 # gpu 1 use cuda  le  plus  rapide
gpu_2 = 3 # gpu 2 use openCL le  plus lent
commande = ".\waifu2x\waifu2x-converter-cpp.exe --scale-ratio 6 -v 1 -i sample.jpg -o NUL -p " #commande pour effectuer un benchmark 
re_nombre_fichier = re.compile('([0-9]+) fichier')#regex du resultat du  bench
regex_result = re.compile('GFLOPS: ([0-9]+\.[0-9]+),')

#trouver a  lancer  la  paralelisation
print("benchmark du  gpu 1")
result_gpu_1 = subprocess.check_output(commande+str(gpu_1), shell=True)#on lance la commande dans  un shell est on atribut la valeur du message de retour dans la variable de retour
print("benchmark du  gpu 2")
result_gpu_2 = subprocess.check_output(commande+str(gpu_2), shell=True)#on lance la commande dans  un shell est on atribut la valeur du message de retour dans la variable de retour

resultat_gpu_1 = float(regex_result.findall(str(result_gpu_1))[0])
resultat_gpu_2 = float(regex_result.findall(str(result_gpu_2))[0])
print(result_gpu_1)
print(result_gpu_2)
ratio =  resultat_gpu_1/resultat_gpu_2
print("raport des  2 ", ratio)
ratio = ratio * 10 # comme ca  on  grate les vigule  au  lieux  de  5.8  / 1 on a    58 / 10  car  sinon on coupe la  varest  on   serait a 5  /  1

nombre_fichier_tmp = subprocess.check_output("dir "+dossier, shell=True)
nombre_fichier = int(re_nombre_fichier.findall(str(nombre_fichier_tmp))[0])
print("il  y  a  "+str(nombre_fichier)+" image")

subprocess.Popen("mkdir final", shell=True)
subprocess.Popen("mkdir gpu_1", shell=True)
subprocess.Popen("mkdir gpu_2", shell=True)
time.sleep(1)  #la  comande  est longue a la   detante

#nombre_fichier=352
#ratio=16.27
var_ratio =  0
varbis_ratio =  0
for i in range(1,nombre_fichier+1):

	nb_zero = int(math.log10(nombre_fichier))-int(math.log10(i))#on calcule  le  nombre  de  0  fait en  fonction  du nombre  d'image

	if nb_zero!=0:
		zero =  "0" #variable  qui  va representer les zero
		for z in range(nb_zero-1):#pour  le  le  nombre  de    0
			zero=zero+"0"#on  ajjoute
	else:
		zero  = ""

	fichier=prefix+zero+str(i)+extention#noms final  du  fichier
	
	if var_ratio+1 > ratio: #choix  si  gpu  1 ou 2
		
		varbis_ratio+=1
		if  varbis_ratio > 10:#on  regarde si  le asser image dans  gpu2
			var_ratio  =  0 
			varbis_ratio =  0

		print("gpu_2",fichier)
		shutil.move(dossier+"/"+fichier, "gpu_2/"+fichier)
	else:
		var_ratio+=1
		print("gpu_1",fichier)
		shutil.move(dossier+"/"+fichier, "gpu_1/"+fichier)

#subprocess.Popen(".\waifu2x\waifu2x-converter-cpp.exe  -i gpu_2/ -o final/ --scale-ratio 1.7778 --noise-level 2 -z -a 0 -v 1", shell=True)
subprocess.Popen("reprise.bat", shell=True)