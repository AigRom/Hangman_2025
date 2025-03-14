import sys
from sys import exit
from tkinter import Tk, messagebox

from controllers.Controller import Controller
from models.Database import Database
from models.Model import Model
from views.View import View



if __name__ == '__main__':
    try:
        #db=Database() #võibolla pole vaja
        model = Model() #Loo mudel
        view = View(model) #Loo view andes kaasa model
        Controller(model, view)  #Loo Controller
        view.mainloop() #viimane rida koodis

    except FileNotFoundError as error:
        #print(f'Viga: {error}')
        View.show_message(error)
        sys.exit(1)

    except ValueError as error:
        View.show_message(error)
        sys.exit(1)

    except Exception as error:
        #print(f'Tekkis ootamatu viga: {error}')
        View.show_message(error)
        sys.exit(1)