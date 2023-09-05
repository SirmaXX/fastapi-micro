
def pagecount(dataset,per_page):
 last= len(dataset)
 newlist=[]
 l = range(1,last)
 # chunks using list comprehension
 x = [l[i:i + per_page] for i in range(0, len(l),per_page)]
 return  len(x)



def paginate(dataset,per_page,pagenumber):
 last= len(dataset)
 newlist=[]
 l = range(1,last)
 # chunks using list comprehension
 x = [l[i:i + per_page] for i in range(0, len(l), per_page)]
 #two dimensional array
 for k in x[pagenumber]:
    newlist.append(dataset[k])

 return newlist