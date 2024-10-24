import sys
import pandas as pd
import multiprocessing
vuoti=[]
inputfile = sys.argv[1]
Loci = sys.argv[2]
out=sys.argv[3]
df = pd.read_csv(str(inputfile), sep='\t')
#df.index = df['#PopUID'].str.split('_').str[0]
da_controllare=[]
data1=df.transpose()

def your_task_function(arg1):
    grouped = df.groupby(df['#PopUID'].str.split('_').str[0])
    b=[]
    a=999
    c=[]
    try:
        var = grouped.get_group("L" + str(arg1))
    except:
        vuoti.append(arg1)
        return arg1+1
    data=var.transpose()
    data.columns=range(data.columns.size)
    for y in range(1,len(data)):
        lista1=[]
        for x in range(0,len(var)):
            lista1.append(var.iloc[x][y])
        zeri = lista1.count(0)
        nAlleli = (len(lista1)-zeri)
        b.append(nAlleli)
    if max(b)<3 and max(b)>0:
        for j in range (1,len(data)):
            base=[]
            d=[]
            if data[0][j] > 0:
                base.append(str(a))

            else:
                d.append(0)    
            for i in range(1,len(lista1)):
                if data[i][j] > 0:
                    if i <10:
                        base.append(str('00')+str(i))
                    else:
                        base.append(str('0')+str(i))
                else: 
                    d.append(0)     

            if len(d)==(len(var)):
                c.append(['000'])
            else:
                c.append(base)
        fi = open(out + "/L"+str(arg1)+'.genepop', 'w')
        orig_stdout = sys.stdout
        sys.stdout = fi
        for k in range(0,len(data)-1):
            if len(c[k])== 1:
                c[k].append(c[k][0])
            print(str(c[k][0])+str(c[k][1]))
        sys.stdout = orig_stdout
        fi.close()    

    else:
        da_controllare.append(arg1)

    return da_controllare

if __name__ == "__main__":
    num_processes = 8  # Adjust the number of processes as needed
    pool = multiprocessing.Pool(processes=num_processes)

    num = int(Loci) + 1

    results = [pool.apply_async(your_task_function, (i,)) for i in range(1, num)]
    
    pool.close()
    pool.join()

beta=1	
while beta<num+1:
  try:
    hr=["codice"]
    df = pd.read_csv(out + "L"+str(beta)+".genepop", dtype=str, names=hr, sep='\t')
    fi = open(out + "/L"+str(beta)+'.genepop', 'w')
    orig_stdout = sys.stdout
    sys.stdout = fi
    df.insert(loc=0, column='species', value=data1.index[1:])
    df.insert(loc=1, column='sp', value=",")
    print(df.to_string(index=False, header=False))
    sys.stdout = orig_stdout
    fi.close()
    break

  except:
    beta=beta+1

path= out + "/Log_genepop.txt"
with open(path, 'a') as file:
    file.write("genepop ok" + '\n')