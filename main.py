from funciones import clean_cache, clean_temp, clean_history, clean_cookies, clean_all, return_menu

print("\n")

print("███████╗███╗   ██╗██╗██████╗ ███████╗██████╗  ██████╗ ██╗   ██╗ █████╗ ██████╗ ██████╗   ")
print("██╔════╝████╗  ██║██║██╔══██╗██╔════╝██╔══██╗██╔════╝ ██║   ██║██╔══██╗██╔══██╗██╔══██╗  ")
print("███████╗██╔██╗ ██║██║██████╔╝█████╗  ██████╔╝██║  ███╗██║   ██║███████║██████╔╝██║  ██║  ")
print("╚════██║██║╚██╗██║██║██╔═══╝ ██╔══╝  ██╔══██╗██║   ██║██║   ██║██╔══██║██╔══██╗██║  ██║  ")
print("███████║██║ ╚████║██║██║     ███████╗██║  ██║╚██████╔╝╚██████╔╝██║  ██║██║  ██║██████╔╝  ")
print("╚══════╝╚═╝  ╚═══╝╚═╝╚═╝     ╚══════╝╚═╝  ╚═╝ ╚═════╝  ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═════╝   ") 


print("\n")


print("Initializing SniperGuard...")

print("\n")

print("Options:")

print("\n")

print("1. Hardening (Not yet implemented)")
print("2. Cleaning")


option = input(">")

if option == "1":
    print("Hardening module is not yet implemented.")
    exit()

else:
    print("\n")
    print("***Cleaning Options:***")


    options = {
        "1": ("Clean cache", clean_cache),
        "2": ("Clean temp", clean_temp),
        "3": ("Clean history", clean_history),
        "4": ("Clean cookies", clean_cookies),
        "5": ("Clean all", clean_all),
        "6": ("Return to menu", return_menu)
    }

    for key, (label, func) in options.items():
        print(f"{key}. {label}")
       

    print("\n")

    cleaning_option = input("> ")

    action = options.get(cleaning_option)

    if action:
        action[1]()    
    else:
        print("Invalid cleaning option selected.")

