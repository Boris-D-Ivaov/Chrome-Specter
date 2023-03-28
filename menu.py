import os

def menuSystem():
    global root_dir
    menu1=True
    menu2=True
    while menu1:
        menu2=True
        print ("""
    [1] Detect folder
    [2] Specify folder location
    [3] Exit
        """)
        ans1 = input("[+] Make a selection! ")
        if ans1 == "1":
          root_dir = os.path.join(os.environ["USERPROFILE"], "AppData", "Local",
                                      "Google", "Chrome", "User Data", "default")
          os.system("cls||clear")
          print("\n[+] Chrome folder located at: " + root_dir)
          while menu2:
              print ("""
    [1] Run
    [2] Go back
    [3] Exit
              """)
              ans2 = input("[+] Make a selection! ")
              if ans2 == "1":
                root_dir = os.path.join(os.environ["USERPROFILE"], "AppData", "Local",
                                            "Google", "Chrome", "User Data", "default")
                menu1=False
                break
              if ans2 == "2":
                 os.system("cls||clear")
                 menu2=False
                 break
              if ans2 == "3":
                os.system("cls||clear")
                print("[-] Exiting ChromeSpecter!")
                exit()
              else:
                  os.system("cls||clear")
                  print("\n[-] Invalid selection!")
        elif ans1 == "2":
          os.system("cls||clear")
          print("[?]Hint! Usually(C:\\Users\\username\AppData\Local\Google\Chrome\\User Data\Default)")
          root_dir = input("\n[+] Please enter Chrome's default folder: ")
          if os.path.isdir(root_dir):
              os.system("cls||clear")#clear terminal
              print("\n[+] Chrome folder located at: " + root_dir)
              break
          else:
              os.system("cls||clear")#clear terminal
              print("[-] Path does not exist, please try again.")
        elif ans1 == "3":
            os.system("cls||clear")
            print("[-] Exiting ChromeSpecter!")
            exit()
        elif ans1 != "":
          os.system("cls||clear")
          print("\n[-] Invalid selection!")
