import collections
import re

#під'єднаємо наші файли до програми
with open("1task.txt", 'r', encoding='utf-8') as task1:
    opentext = re.sub(r'[^а-яё]', '', task1.read().replace("\n","").replace(" ","").lower().replace("ё", "е"))

with open("3task.txt", 'r', encoding='utf-8') as task3:
	opentext2 = task3.read()
	opentext2 = opentext2.replace('\n',"")
	
#виведемо обраний  фрагмент тексту 
print(opentext)

#Оголосимо нашу абетку, яку програма використовуватиме як зразок
abetka = ['а', 'б', 'в', 'г', 'д', 'е', 'ж', 'з', 'и', 'й', 'к', 'л', 'м', 'н', 'о', 'п', 'р', 'с', 'т', 'у', 'ф', 'х', 'ц', 'ч', 'ш', 'щ', 'ъ', 'ы', 'ь', 'э', 'ю', 'я']
    
#обчислюємо потрібний  індекс відповідності за допомогою функції Index
def Index(txt): 
    y = dict(collections.Counter(txt))
    j = []
    for key in list(y.keys()):
        j.append(y[key]*(y[key]-1))
    J = 1/(len(txt)*(len(txt)-1))*sum(j)
    return(J)
   

#здійснюємо розшифрування шифротексту chipertxt за допомогою функції DecodeTxt
def DecodeTxt(chipertxt, keys): 
    h=0
    txt = ''
    for i in chipertxt:
        txt += abetka[(abetka.index(i) - abetka.index(keys[h]))%32]
        h+=1
        if (h >= len(keys)):
            h = 0
    return(txt)  
    
    
#здійснюємо зашифрування відкритого тексту txt за допомогою функції EncodeTxt
def EncodeTxt(txt, keys): 
    chipertxt = ''
    h=0
    for j in txt:
        chipertxt += abetka[(abetka.index(j) + abetka.index(keys[h]))%32]
        h+=1
        if (h >= len(keys)):
            h = 0
    return(chipertxt)   


#Розіб'ємо відкритий текст на блоки функцією BlockPart
def BlockPart(txt, l): 
	block=list()
	for j in range(l):
		block.append('')
		q=j
		while(q<len(txt)):
			block[j] = block[j]+txt[q]
			q+=l
	return block


#шукаємо індекс відповідності для кожного блоку окремо, аби потім порівняти із значенням, отрианим раніше. Використовуємо перший із двох алгоритмів, описаних у теоретичних відомостях до виконання комп'ютерного практикуму
def IndexEach(txt, l): 
    parts = BlockPart(txt, l) 
    index = 0
    for j in range(len(parts)):
        index = index + Index(parts[j])
    index = index/l
    return index

#команда KeyFind здійснює пошук ключів для декодування, спираючись на проведений криптоаналіз (отримані значення індексу відповідності)
def KeyFind(txt, l, letter): 
    parts = BlockPart(txt, l)
    bukva = ''
    i = 0
    while i < len(parts):
        lba = collections.Counter(parts[i]).most_common(1)[0]
        bukva += abetka[(abetka.index(lba[0]) - abetka.index(letter))%32]
        i += 1
    print(bukva)

def Part1(txt): 
    keywords = ['да','жук','муха','пчела','луггихауст','еммороженко','здесьстобукв','ведьмынегорят','параллелограмм','всегдаделаюлабы','петухидеткиндюку','напитокмаргаритта','хочускушатьконфету','дайтежратьпокаживой','спасибонадопкунехочу']
    print('---------------Задачка #1---------------')
    print("Iндекс відповідності для відкритого тексту:", Index(txt), "\n")
    for j in keywords:
    	print("Довжина ключа ",len(j),":",Index(EncodeTxt(txt, j)), "\n")

#викликаємо до виконання першу частину
print("\n", '-----------------------------------', "\n")
Part1(opentext)
print("\n", '-----------------------------------', "\n")
print(EncodeTxt(opentext, 'луггихауст'))
print("\n", '-----------------------------------', "\n")


def Part2(txt):
	print('---------------Задача #2---------------') 
	for j in range(2, len(abetka)):   
		print("Довжина ключа ", j,':', IndexEach(txt, j))
	print('-----------------------------------')
	for bukva in 'оеа':
    		KeyFind(opentext2, 13, bukva)  #згідно з діаграмою, на вхід можна подати або 13, або 26; 13 обрано, бо ключем найімовірніше є слово, а не фраза
	print("\n", '-----------------------------------', "\n")
	print('---------------Задача #3---------------')
	print(DecodeTxt(txt, 'громыковедьма'))

#викликаємо до виконання другу частину
print("\n", '-----------------------------------', "\n")
Part2(opentext2)	



