# -*- coding: utf-8 -*-
"""
Created on Sun Sep 17 19:54:19 2023

@author: imade
"""

import numpy as np
import csv
from tkinter import ttk
import tkinter as tk
from tkinter.messagebox import showinfo


with open('typechart.csv', 'r') as f:
    reader = csv.reader(f)
    data = list(reader)
    
TC = np.array(data)
with open('Poke_Ref.csv', 'r') as g:
    reader1 = csv.reader(g)
    data = list(reader1)
    
PR = np.array(data)
indices1=np.where(PR[:,9]=='GRASS')
indices2=np.where(PR[:,10]=='')
indices=np.intersect1d(indices1, indices2)
types=TC[1,2:]
def getpivots(pkmn):
    def checkabilities(index):
        abil=PR[index][11:14]
        immn=[]
        rest=[]
        wkns=[]
        if 'Levitate' in abil:
            immn+=[6]
        if 'Earth Eater' in abil:
            immn+=[6]
        if 'Volt Absorb' in abil:
            immn+=[14]
        if 'LightningRod' in abil:
            immn+=[14]
        if 'Motor Drive' in abil:
            immn+=[14]
        if 'Water Absorb' in abil:
            immn+=[12]
        if 'Storm Drain' in abil:
            immn+=[12]
        if 'Dry Skin' in abil:
            immn+=[12] 
            wkns+=[11]
        if 'Fluffy' in abil:
            wkns+=[11]
        if 'Heatproof' in abil:
            rest+=[11]
        if 'Flash Fire' in abil:
            immn+=[11]
        if 'Sap Sipper' in abil:
            immn+=[13]
        if 'Thick Fat' in abil:
            rest+=[11]
            rest+=[16]
        if 'Water Bubble' in abil:
            rest+=[11]
        return [wkns,rest,immn]
    def lowerdef(index):
        if PR[index][4]<PR[index][6]:
            ldf=PR[index][4]
            i=4
        else:
            ldf=PR[index][6]
            i=6
        return [ldf,i]
    def returnmatchups(pokemon):
        index=int(np.where(PR==pokemon)[0])
        type1=PR[index,9]
        type2=PR[index,10]
        t1=np.where(TC==type1)[0][1]
        t2=np.where(TC==type2)[0][1]
        #types=[TC[:,t1],TC[:,t2]]
        wk=[]
        qx=[]
        rs=[]
        qr=[]
        im=[]
        sg=[]
        t=TC[:,t1]
        ty=TC[t1,:]
        wkns=checkabilities(index)[0]
        rst=checkabilities(index)[1]
        imm=checkabilities(index)[2]
        qxwk=[]
        qrst=[]
        strg=[*np.where(ty=='2')[0]]
        for i in [*np.where(t=='2')[0]]:
            if i in wkns:
                qxwk+=[i]
            elif i not in rst and i not in imm:
                wkns+=[i]
            elif i in rst:
                rst.remove(i)
        for i in [*np.where(t=='0.5')[0]]:
            if i in rst:
                qrst+=[i]
            elif i not in wkns:
                rst+=[i]
            elif i in wkns:
                wkns.remove(i)
        for i in [*np.where(t=='0')[0]]:
            if i in wkns:
                wkns.remove(i)
            if i in rst:
                rst.remove(i)
            imm+=[i]
        if t2!=0:
            t=TC[:,t2]
            for i in [*np.where(t=='2')[0]]:
                if i in wkns:
                    qxwk+=[i]
                elif i not in rst and i not in imm:
                    wkns+=[i]
                elif i in rst:
                    rst.remove(i)
            for i in [*np.where(t=='0.5')[0]]:
                if i in rst:
                    qrst+=[i]
                elif i not in wkns:
                    rst+=[i]
                elif i in wkns:
                    wkns.remove(i)
            for i in [*np.where(t=='0')[0]]:
                if i in wkns:
                    wkns.remove(i)
                if i in rst:
                    rst.remove(i)
                imm+=[i]
        
        matchup = [wkns,rst,imm,qxwk,qrst,strg]
        name=str(pokemon)
        ldf=lowerdef(index)
        match = [wk,rs,im,qx,qr,sg,name,ldf]
        for i in range(0,6):
            for k in matchup[i]:
                t=str(TC[1,k])
                match[i]+=[t]
        return match
    mat=returnmatchups(pkmn)
    pivots=[]
    dtypes=PR[2:,1]
    dtypes=np.unique(dtypes, axis = 0)
    #delete = [*np.where(dtypes.T[0] == '')[0]]
    #for d in delete:
     #   np.delete(dtypes, d)
    tera=[]
    trs=[]
    for p in dtypes:
        value=0
        ovalue=0
        index=int(np.where(PR==str(mat[6]))[0])
        ldf1=lowerdef(index)
        bulk1=int(PR[index][4])+int(PR[index][6])+int(PR[index][2])
        index=int(np.where(PR==p)[0])
        tmat=returnmatchups(p)
        bulk2=int(PR[index][4])+int(PR[index][6])+int(PR[index][2])
        bst=bulk2+int(PR[index][3])+int(PR[index][5])+int(PR[index][7])
        abil = PR[index][11:14]
        if 'Intimidate' in abil:
            value+=2
        if bulk2 > 300:
            value+=2
        if PR[index][ldf1[1]]>ldf1[0]:
            value+=1
        if bulk2 > bulk1:
            value+=0.5
        if bulk2<bulk1*0.7:
            value-=5
        if bst<350:
            value-=10
        if bst<450:
            value-=3
        for t in tmat[0]:
            if t in mat[0]:
                value-=2
            elif t in mat[1] or t in mat[4]:
                value+=1
            elif t in mat[2]:
                value += 1.5
            elif t in mat[3]:
                value-=2.5
        for t in tmat[1]:
            if t in mat[0]:
                value+=2.5
            if t in mat[3]:
                value+=3
        for t in tmat[2]:
            if t in mat[0]:
                value+=5
            if t in mat[3]:
                value+=6
        
        for t in tmat[4]:
            if t in mat[0]:
                value+=4
        for t in tmat[5]:
            if t in mat[0]:
                ovalue+=1.5
        value+=ovalue
        
        
        if value>5:
            pivots+=[[str(p),value-ovalue,ovalue]]
 #           if PR[index][10]=='' and str(PR[index][9]) not in tera[:][0]:
  #              tera+=[[str(PR[index][9]), value]]
    
    for k in TC[1,2:]:
        
        value=0
        indices1=np.where(PR[:,9]==str(k))
        indices2=np.where(PR[:,10]=='')
        indices=np.intersect1d(indices1, indices2)
        index=int(indices[0])
        if k == 'ELECTRIC' or k=='GHOST':
            index=int(indices[2])
        p=PR[index][1]
        tmat=returnmatchups(p)
        
        for t in tmat[0]:
            if t in mat[0]:
                value-=2
            elif t in mat[1] or t in mat[4]:
                value+=1
            elif t in mat[2]:
                value += 1.5
            elif t in mat[3]:
                value-=2.5
        for t in tmat[1]:
            if t in mat[0]:
                value+=2.5
            if t in mat[3]:
                value+=3
        for t in tmat[2]:
            if t in mat[0]:
                value+=5
            if t in mat[3]:
                value+=6
                
        for t in tmat[5]:
            if t in mat[0]:
                value+=3.5
        
        
        if value>0 and k not in trs:
            tera+=[[str(k),value]]
            trs+=[k]
 #           if PR[index][10]=='' and str(PR[index][9]) not in tera[:][0]:
  #              tera+=[[str(PR[index][9]), value]]
    def takeSecond(elem):
        return elem[1]
    pivots.sort(key=takeSecond,reverse=True)
    tera.sort(key=takeSecond,reverse=True)
    results=[pivots[:10], tera[:5]]
    return results
    
choices=[*PR[1:,1]]
win= tk.Tk()

# Set the size of the window
win.geometry("400x300")

# Set the title of the window
win.title("Pivots")

# Update the Entry widget with the selected item in list
def ShowPivots():
    # get all selected indices
    i = menu.curselection()
    output.delete(0, tk.END)
    tera.delete(0, tk.END)
    # get selected items
    pkmn = str(menu.get(i))
    pivots=getpivots(pkmn)[0]
    teras=getpivots(pkmn)[1]
    for k in pivots:
        output.insert(tk.END, k)
    for k in teras:
        tera.insert(tk.END,k)

def check(e):
   v= entry.get()
   if v=='':
      data= choices
   else:
      data=[]
      for item in choices:
         if v.lower() in item.lower():
            data.append(item)
   update(data)
def update(data):
   # Clear the Combobox
   menu.delete(0, tk.END)
   # Add values to the combobox
   for value in data:
      menu.insert(tk.END,value)
# Add a Label widget
#label= tk.Label(win, text= "Pivots")
#label.pack(padx= 5, pady= 5, side=tk.RIGHT)
# Add a Bottom Label
#teras=tk.Label(win, text = "Potential Teras:")
#teras.pack(padx= 5,pady= 5, side=tk.RIGHT)


#button


# Create an Entry widget
entry= tk.Entry(win, width= 35)
entry.pack()
entry.bind('<KeyRelease>',check)
# Create a Listbox widget to display the list of items
showpivots = tk.Button(win, 
                      text="Get Pivots",
                      command=ShowPivots
                      )
showpivots.pack()

text= tk.Label(win, text="Select a Pokemon:                   Potential Teras:                         Pivots:")
text.pack()


output= tk.Listbox(win)
output.pack(padx=5, pady=5, side=tk.RIGHT)

tera= tk.Listbox(win)
tera.pack(padx=5, pady=5, side=tk.RIGHT)

menu= tk.Listbox(win)
menu.pack(padx=5, pady=5, side=tk.RIGHT)
# Add values to our combobox
update(choices)
#def upd_entry():
 #   entry = menu.curselection
#menu.bind('<Double-Button>',upd_entry())
def items_selected(event):
    # get all selected indices
    i = menu.curselection()
    # get selected items
    pkmn = str(menu.get(i))
    msg = pkmn
    entry.delete(0,tk.END)
    entry.insert(0, msg)


menu.bind('<<ListboxSelect>>', items_selected)

# Binding the combobox onclick
win.mainloop()

