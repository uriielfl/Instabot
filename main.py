import sqlite3 
con = sqlite3.connect('users.db')
c = con.cursor()
from numpy import setdiff1d

c.execute("CREATE TABLE IF NOT EXISTS user_data(users, status)") #Criar DB para armezenar os usuários

import selenium
from selenium import webdriver
from time import sleep
import os
from selenium.webdriver.support.ui import WebDriverWait


os.system('cls') #Limpar a tela

#options = webdriver.ChromeOptions() #Define a variável que irá ser responsável pelas opções do Google Chrome.
#options.add_argument(r"user-data-dir=./temp")
dv = webdriver.Chrome('./chromedriver.exe')
#dv = webdriver.Chrome('./chromedriver.exe', chrome_options=options)
dv.get('http://instagram.com/') 
sleep(10)


def login():
    usr = dv.find_element_by_xpath('//*[@id="loginForm"]/div/div[1]/div/label/input')
    pw =  dv.find_element_by_xpath('//*[@id="loginForm"]/div/div[2]/div/label/input')
    sleep(3)
    #usr_input = 'excellnapratica'
    #pw_input = 'ma96rc43'
    usr_input = str(input("Usuário: \n"))
    pw_input = str(input('Senha: \n'))
    os.system('cls')
    usr.send_keys(usr_input)
    sleep(3)
    pw.send_keys(pw_input)
    sleep(3)
    dv.find_element_by_xpath("//button[contains(.,'Entrar')]").click()
    sleep(3)
login()

def Menu():
    os.system('cls')
    print("Bem vindo ao instabot!\nSelecione uma das opções abaixo:")
    menu_options_1 = str(input("1 - Aumentar a lista\n2 - Seguir\n3 - Apagar Dados da Lista\n4 - Ver lista\n5 - Pesquisar por um nome\n6 - Parar de seguir quem não lhe segue\n0 - Sair\n"))
  
    if menu_options_1 == "1":
        dv.get('http://instagram.com/explore/people/suggested/')
        sleep(2)
        try:
            for x in range(0,5):
                dv.execute_script("window.scrollBy(0,3000)")
                sleep(2)
        except KeyboardInterrupt:
            pass
        sleep(3)
        names = dv.find_elements_by_class_name('FPmhX')

        num_pessoas = 0
        pessoas = []
        for name in names:                
            pessoas.append(name.text)     
            num_pessoas = num_pessoas + 1  
            c.execute("INSERT INTO user_data(users,status) VALUES (?,'pendente')",(name.text,))  
            con.commit()
            print("Salvando na lista")
            os.system('cls')
            print("Salvando na lista.")
            os.system('cls')
            print("Salvando na lista..")
            os.system('cls')
            print("Salvando na lista...")
            os.system('cls')
        print("Lista cheia!")
        menu_show_opt = str(input("\n\n\n1 - Voltar para o Menu Principal\n2 - Sair\n"))
        if menu_show_opt == "1":
            Menu()
        elif menu_show_opt == "2":
            exit()
    elif menu_options_1 == "2":       

        follow_it = c.execute("SELECT users FROM user_data")
        con.commit()
        listoutput=[i[0] for i in follow_it]
        qnt = int(input("Até quantas pessoas você quer seguir?(PS: SE VOCÊ SEGUIR MUITAS DE UMA VEZ, PODERÁ RESULTAR EM BANIMENTO DE SUA CONTA NO INSTAGRAM)"))
        j = 0
        for e in listoutput:          
            try:
                dv.get("https://instagram.com/"+str(e)+"/")
           
                sleep(2)
           
                dv.find_element_by_xpath("//button[contains(.,'Seguir')]").click()
                sleep(1)
                c.execute("UPDATE user_data SET status = 'aprovado' WHERE users = '"+str(e)+"'")
                con.commit()
                print("SEGUINDO.")
                os.system('cls')
                print("SEGUINDO..")
                os.system('cls')
                print("SEGUINDO...")
                os.system('cls') 
                c.execute('DELETE FROM user_data WHERE status = "aprovado"')
                con.commit()
                if j == qnt:
                    break
                j = j + 1
            except:
                pass
        print("Você terminou!")
        menu_show_opt = str(input("\n\n\n1 - Voltar para o Menu Principal\n2 - Sair\n"))
        if menu_show_opt == "1":
            Menu()
        elif menu_show_opt == "2":           
            exit()
    elif menu_options_1 == "3":
        menu_del_opt = str(input("Deseja mesmo deletar sua lista?\n1 - Sim\n2 - Não\n0 - Sair"))
        if menu_del_opt == "1":
            c.execute("DELETE FROM user_data")
            con.commit()
            print("Lista de Usuários Limpa!")
        if menu_del_opt == "2":
            Menu()
        if menu_del_opt == "0":
            exit()
        menu_show_opt = str(input("\n\n\n1 - Voltar para o Menu Principal\n2 - Sair\n"))
        if menu_show_opt == "1":
            Menu()
        elif menu_show_opt == "2":
            exit()
        

    elif menu_options_1 == "4":
        full_list = c.execute("SELECT users FROM user_data")
        con.commit()
        listoutput=[i[0] for i in full_list]
        for b in listoutput:
            print(str(b))
        menu_show_opt = str(input("\n\n\n1 - Voltar para o Menu Principal\n2 - Sair\n"))
        if menu_show_opt == "1":
            Menu()
        elif menu_show_opt == "2":
            exit()
    elif menu_options_1 == "5":
        search_var = str(input("Digite o nome ou parte do nome do usuário que você deseja procurar\n"))
        full_list = c.execute("SELECT * FROM user_data WHERE users LIKE '%"+str(search_var)+"%';")
        
        con.commit()
        listoutput=[i[0] for i in full_list]
        for b in listoutput:
            print(str(b))
        menu_show_opt = str(input("\n\n\n1 - Voltar para o Menu Principal\n2 - Sair\n"))
        if menu_show_opt == "1":
            Menu()
        elif menu_show_opt == "2":
            exit()
    elif menu_options_1 == "6":        
        following_me = "https://www.instagram.com/accounts/access_tool/accounts_following_you"
        fm_list = []
        iamfollowing = "https://www.instagram.com/accounts/access_tool/accounts_you_follow"
        iamf_list = []

        dv.get(following_me)
        sleep(3)
        try:
            while True:
                dv.find_element_by_xpath("//button[contains(.,'Ver mais')]").click()
                sleep(1)
                break
        except:
            pass 
        listfollowing_me = dv.find_elements_by_class_name('-utLf')
        sleep(1)
        for lfollowing_me in listfollowing_me:
            fm_list.append(lfollowing_me.text)
        print(fm_list)
        for x in range(0, 3):
            print('\n')

        dv.get(iamfollowing)
        sleep(3)
        try:
            while True:
                dv.find_element_by_xpath("//button[contains(.,'Ver mais')]").click()
                sleep(1)
                break
            sleep(2)
        except:
            pass 
        listiamfollowing = dv.find_elements_by_class_name('-utLf')
        sleep(1)
        for liam_following in listiamfollowing:
            iamf_list.append(liam_following.text)
        print(iamf_list)
     

        for x in range(0, 3):
            print('\n')
      
        
        for i in setdiff1d(iamf_list,fm_list):           
            sleep(1)
            dv.get('http://instagram.com/'+str(i))
            sleep(2)
            dv.find_element_by_css_selector("[aria-label=Seguindo]").click()
            break
        sleep(2)
        menu_show_opt = str(input("\n\n\n1 - Voltar para o Menu Principal\n2 - Sair\n"))
        if menu_show_opt == "1":
            Menu()
        elif menu_show_opt == "2":
            exit()
        
    elif menu_options_1 == "0":
        exit()
            
      
Menu()
