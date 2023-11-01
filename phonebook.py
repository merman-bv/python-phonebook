'''
Задача 38: 
Дополнить телефонный справочник 
возможностью изменения и удаления данных.
Пользователь также может ввести имя или фамилию, 
и Вы должны реализовать функционал
для изменения и удаления данных.


Дополнить справочник возможностью копирования данных 
из одного файла в другой. Пользователь вводит номер строки, 
которую необходимо перенести из одного файла в другой.

'''
import os

fields = ['Фамилия','Имя','Телефон','Описание']
filename_phonebook = 'phonebook.csv'
#openPhoneBook('phonebook.csv')

def workPhoneBook(actionChoice=''):
    if actionChoice=='':
        choice = showMenu()
    else:
        choice =  int(actionChoice)
    phbook = openPhoneBook(filename_phonebook)
    chosen = list()
    while (choice != 0 ):
        #print(f'Основной набор главного меню получен - код действия: {choice}')
        if choice == 1: # Покажем телефонную книгу полностью
            choice = showPhoneBook(phbook) # Показываем тел. книгу
        elif choice == 2: # 2. Найти по Фамилии(Номеру)'
            numField = showExtraMenuFind()
            # print(f'Поиск в поле: {fields[numField-1]}')
            newSearch = showRequestFind(fields[numField-1])
            #newSearch = input('Поиск (цифры для номеров, буквы для фамилий): ')
            chosen = findRecord(phbook, newSearch, fields[numField-1]) # Отбор записей в тел. книгу
            choice = 10 + showPhoneBook(chosen) # Показываем тел. книгу
            choice = 10 + showExtraMenu() # Показываем доп. меню
        elif choice == 3: #  3. Добавить запись
            chosen =list()
            chosen = actionRecords(chosen, phbook)
            writePhoneBook(filename_phonebook, phbook)
            choice = showPhoneBook(chosen) # Показываем тел. книгу
        # Выбор для доп. меню
        #print(f'Второй набор главноого меню - код действия: {choice}')
        if choice == 11: # Изменить(Удалить) запись
            chosen = actionRecords(chosen, phbook, False) # Правка
            writePhoneBook(filename_phonebook, phbook)
            choice = showPhoneBook(chosen) # Показываем тел. книгу
        elif choice == 12: # Удалить запись
            actionRecords(chosen, phbook, True) # Удаление
            writePhoneBook(filename_phonebook, phbook)
            choice = showPhoneBook(phbook) # Показываем тел. книгу 

        
        choice = showMenu()

''' --- Показать основное меню --- '''
def showMenu():
    print('--- Доступные действия ---')
    print(
        '[1: Показать справочник]',
        '[2: Найти запись]',
        '[3: Добавить запись]',
        '[0: Завершить работу]', sep=' ')
    choice = int(input('Ожидание кода действия: '))
    if not choice in [1,2,3]:
        choice = 0
    #print(f'--- Выбран код: {choice} ---')
    return choice

''' --- Показать дополнительное меню --- '''
def showExtraMenu():
    print (f'--- Для выбранных записей можно применить --- ')
    print ('[1: Изменить]','[2: Удалить]','[0:Вернуться]',sep=' ')
    choice = int(input('Ожидание номера действия: '))
    if not choice in [1,2]:
        choice = 0
    # print(f'Выбран доп. код: {choice}')
    return choice

'''--- Показать дополнительное меню поиска ---
Возвращает код поля для поиска
'''
def showExtraMenuFind():
    print (f'--- Указать поля для поиска --- ')
    print ('[1: Фамилия]','[2: Имя]','[3: Телефон[]','[4: Описание]','[0:Вернуться]',sep=' ')
    choice = int(input('Ожидание кода выбранного поля: '))
    if not choice in [1,2,3,4]:
        choice = 0
    # print(f'Выбран доп. код: {choice}')
    return choice

'''--- Показать запрос строки поиска ---'''
def showRequestFind(inform=''):
    #print('--- Request Search  ---')
    inform = 'Ожидание значения для поиска в поле '+ inform +': '
    search = input(inform)
    return search

'''--- Показать телефонную книгу ---'''
def showPhoneBook(records):
    print (f"--- Show phonebook ---")
    choice = 0
    #header
    for field in fields:
        print(field, end='     \t')
    print()
    for field in fields:
        for bkv in field:
            print('-', end='')
        print('     \t', end='')
    print()
    # body
    for dict in records:
        stroka = ''
        for item in fields:
            stroka = stroka + dict[item] + '     \t'
        stroka = stroka[:len(stroka)-1] # Удаляем табуляцию
        print(stroka)
    # footer
    for field in fields:
        for bkv in field:
            print('-', end='')
        print('     \t', end='')
    print()
    # choice = showExtraMenu(extramenu)
    return choice
    
''' --- Фильтр к телефонной книге ---
Возвращает список записей отобранных по значению search
Первый аргумент список абонентов
Второй строка для поиска
Третий поле для поиска, по умолчанию fields[0]
если цифры - ищем среди номеров и модифицируем список
если буквы - ищем среди фамилий и модифицируем список
Возвращает модифицированный набор
'''
def findRecord(records, search='', key=fields[0]):
    print(f'--- Search Records {key}:{search} ---')
    search = search.upper()
    res = list(filter(lambda dict: str(dict[key]).upper().startswith(search),records))
    # print(res)
    return res
'''
    if search.isdigit():
        # print('Телефон',' ',search.isdigit())
        # print(type(search))
        res = list(filter(lambda dict: str(dict['Телефон']).startswith(search),records))
        # print(res)
        return res
    else: # search.isalpha(search):
        search = search.upper()
        #print('str')
        res = list(filter(lambda dict: str(dict['Фамилия']).upper().startswith(search),records))
        return res
'''
        
''' --- Действие над нобором записей --- 
Получает три параметра:
список записей(словарей), тел. книку, признак удаления
Если список записей пустой, то добавляем запись
Если в списке есть записи и признак ИСТИНА, удаляем записи
Если в списке есть записи и признак ЛОЖЬ, редактируем записи
Возвращает список записей
'''
def actionRecords(records, phbook, delrec=False):
    print ('--- Transform PhoneBok ---')
    if len(records)!=0: # Взможно или Удаление или Правка т.к. records!=0
        print('--- Possible to Edit or Delete ---')
        if delrec: # Удаление т.к. records!=0 delrec=True
            print('--- Transfer to Delete ---')
            records = delRecord(records, phbook) # Возвращаем результат удаления
            return records
        else: # Редактирование т.к records!=0 delrec=False
            print('--- Transfer to Edit ---')
            for record in records:
                NewRecord = addRecord(record) # addRecord(records[0])
                OldRecord = record # records[0]
                records = trasformRecord(NewRecord, phbook, OldRecord)
                return records      
    else: # Добавление т.к. records==0
        print('--- Transfer to Add ---')
        NewRecord = addRecord()
        records = trasformRecord(NewRecord, phbook)
        return records

''' --- Добавление/Исправление записи --- 
Передаем запись(словарь)
Возвращает словарь с ключами из списка fields
'''
def addRecord(record={}):
    print('--- Add record ---')
    newDict = {}
    for itemField in fields:
        stroka = str(itemField)
        if len(record)!= 0:
            stroka = itemField + ' ('+ record[itemField] +')'
        stroka = stroka + ": "
        parcel = input(stroka)
        if len(record)!= 0 and parcel == '':
            parcel = record[itemField]
        newDict[itemField] = parcel.capitalize()
    # print(newDict)
    return newDict        

''' --- Удаление записи из тел. книги--- 
Получаем спискок записей и тел. книгу
Возвращаем тел. книгу
'''
def delRecord(records, phbook):
    print('--- Delete Record from PhoneBook---')
    if len(records)!=0:
        for record in records:
            phbook.remove(record)
    # phbook.remove(phb[len(phb)-1])
    return phbook

''' --- Преобразование записи в тел. книге --- 
Передаем  новую запись, тел. книгу и старую запись
Если найдем новую, возвратим позицию первой найденной
Если нет новой, но есть старая заменим найденную запись
Если нет новой, а так же старой добавим запись в конец
Возвращаем тел. книгу
'''
def trasformRecord(newrec, phbook, oldrec={}):
    print('--- Transform Record in PhoneBook ---')
    # print(f'New Record:{newrec}')
    # print(f'Old Record:{oldrec}')
    # print(f'Результат поиска: New-{newrec in phbook} Old-{oldrec in phbook}')
    if not newrec in phbook:
        if oldrec in phbook:
            # print(f'--- index(oldrec): {phbook.index(oldrec)} ---')
            pos = phbook.index(oldrec)
            phbook[pos] = newrec
            return phbook
        else:            
            # print(f'--- Append(newrec) ---')
            phbook.append(newrec)
            return phbook
    else:
        # print(f'--- index(newrec): {phbook.index(newrec)} ---')
        pos = phbook.index(newrec)
        return phbook  

''' --- Запись файла ---'''    
def writePhoneBook(filename, phbook):
    # print(filename)
    # print(phbook)
    with open(filename, 'r') as f:
        data = f.read()
 
    with open('phbook-temp.txt', 'w') as f:
        f.write(data)

    with open(filename, 'w', encoding='utf-8') as fileOut:
        for i in range(len(phbook)):
            s=''
            for v in phbook[i].values():
                s=s + v +','
            fileOut.write(f'{s[:-1]}\n')

'''--- Читаем файл ---'''
def openPhoneBook(filename):
    print ("--- Open phonebook ---")
    curdir = os.path.dirname(__file__)
    os.chdir(curdir)
    print(curdir)
    fullfilename = os.path.join(curdir,filename)
    print(fullfilename)
    #f = open(curdir+'/'+filename)
    f = open(fullfilename)
    data = list()
    for line in f:
        line = line [:len(line)-1] # Удаляем перенос строки
        record = dict(zip(fields, line.split(',')))
        data.append(record)
    f.close()
    return data

workPhoneBook()
# addRecord({'Фамилия': 'pentov', 'Имя': 'petr', 'Телефон': '999', 'Описание': 'novic'})
# workPhoneBook(1) # Показать тел. книгу
# workPhoneBook(2) # Поиск в тел. книге
# workPhoneBook(3) # Добавить запись в тел. книгу
