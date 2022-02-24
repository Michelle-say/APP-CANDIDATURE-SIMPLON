from os import listdir

def recup_routes_names():
    lst = listdir("App/routes")
    lst2= []
    for i in lst:
        x = i.replace('.py','')
        lst2.append(x)
    return (lst2)

