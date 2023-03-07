import load_json as lj

def print_menu():
    print("|======================================|")
    print("|               Main Menu              |")
    print("|======================================|")
    print("|   option  |        description       |")
    print("|======================================|")
    print("|     1     |    Search for articles   |")
    print("|     2     |    Search for authors    |")
    print("|     3     |    List top n venues     |")
    print("|     4     |      Add an article      |")
    print("|     5     |            Exit          |")
    print("|======================================|")


def search_article():
    '''
        The user should be able to provide one or more keywords, and the 
        system should retrieve all articles that match all those keywords (AND semantics).
        A keyword matches if it appears in any of title, authors, abstract, venue and year 
        fields (the matches should be case-insensitive). For each matching article, display the id, 
        the title, the year and the venue fields. The user should be able to select an article to see all fields 
        including the abstract and the authors in addition to the fields shown before. If the article is 
        referenced by other articles, the id, the title, and the year of those references should be also listed.
    '''

    keywords = [f"\"{word}\"" for word in input("Please enter one(more) keyword(s): ").split()] 


    match = set()
    cursor = lj.collection.find(
                    { "$text":{
                       "$search": f"{' '.join(keywords)}"
                    }},{"id":1,"title":1,"venue":1,"year":1})

    
    print("Searching ...")
    print("================================================")
    match = list(match)
    print("Finding matching result:")
    # using cursor ( show 5 at a time)
    # index = 1
    # limit = 5
    # match = {}
    # for i in cursor:
    #     match[str(index)] = i['id']
    #     print("article "+str(index))
    #     print("   Id: ",i["id"]) 
    #     print("   Title: "+i["title"]) 
    #     print("   Year: "+str(i['year']))
    #     print("   Venue: "+i["venue"])
    #     print("")
    #     if index >= limit:
    #         see_next = input("Please enter 'y' if you want to see more results, or 'n' to selete article: ").strip()
    #         while len(see_next) ==0 or see_next not in ['y','n']:
    #             see_next = input("Please enter 'y' if you want to see more results: ").strip()
    #         if see_next == 'y':
    #             limit+=5
    #             continue
    #         else:
    #             break
    #     index +=1

    # show all at a time 
    index = 1
    match = {}
    for i in cursor:
        match[str(index)] = i['id']
        print("article "+str(index))
        print("   Id: ",i["id"]) 
        print("   Title: "+i["title"]) 
        print("   Year: "+str(i['year']))
        print("   Venue: "+i["venue"])
        print("")
        index+=1

    print("=========================================================")
    if index>1: 
        print("*** Note: If you want to select article 3, then type 3 !")
        select_article = input("Please select an article to see the full information: ")
        print("=========================================================")

        while len(select_article)==0 or select_article.isdigit() == False or int(select_article)<=0 or int(select_article)>=index: # before: int(select_article)>len(match)
            select_article = input("Please select a valid article: ")
        
        print("Full information of article "+select_article+ " :\n")
        #id = match[int(select_article)-1][0]
        id = match[select_article.strip()]
        cursor = lj.collection.find({"id": id},{"_id":0,"references":0}) # search by id (index)
        print("id: "+ cursor[0]["id"] +"\n") # id
        print("title: "+cursor[0]["title"]+"\n") # title
        print("venue: "+cursor[0]["venue"]+"\n") #venue
        print("year: "+str(cursor[0]["year"])+"\n") #year
        if (cursor[0].get("abstract") != None): # abstract
            print("abstract: ")
            print("          "+cursor[0]["abstract"]+"\n")
        print("authors: ") # author
        for i in cursor[0]["authors"]:
            print("        "+i)
        print("n_citation: "+str(cursor[0]["n_citation"])+"\n")  # n_citation

        # referenced_by
        
        #cursor1 = lj.collection.find({"results": {"$elemMatch": {"references":id}}},{"id":1})
        cursor1 = lj.collection.find({"references": id},{"id":1})
        ref_ids = []
        for c in cursor1:
            #the id, the title, and the year of those references should also be shown
            ref_ids.append(c["id"])
        index = 1
        if len(ref_ids)!= 0:
            print("Referenced by: ")
            print("    Index Id                                      Year    Title")
            for i in ref_ids:
                cursor = lj.collection.find({"id":i},{"id":1,"title":1,"year":1})
                print("      "+str(index)+"   "+cursor[0]["id"]+"    "+str(cursor[0]["year"])+"    "+cursor[0]["title"] +'\n')
                index+=1
        else:
            print("There is no article reference this! ")

    
    else:
        print("There is no matching article\n")
        # start a new search or return to the main menu
    
    print("|======================================|")
    print("|                 Menu                 |")
    print("|======================================|")
    print("|   option  |        description       |")
    print("|======================================|")
    print("|     1     |   Search article again   |")
    print("|     2     |     Back to main menu    |")
    print("|======================================|")
    again = input("Enter an option:").strip()
    while again not in ["1","2"]:
        again = input("Please enter a valid option :").strip()

    if again=="1":
        search_article()
    else:
        return

def search_authors():
    matched={}
    keywords = str(input("enter one keyword that you wannt to search: "))
    while(1):
        if ' ' in keywords:
            keywords = str(input("No space allowed, one word only, please try again: "))
        else:
            break
    count =0
    cursor = lj.collection.find({"$text":{'$search' : keywords} },{"id":1 , "authors": 1, "title": 1 , "year" : 1, "venue": 1}).sort("year" , -1)
    for i in cursor:
        split=[item.split() for item in i['authors']]
        for x in split:
            if keywords.upper() in map(str.upper, x):
                string = ' '.join(x)
                if string in matched.keys():
                    matched[string]+=([[i["id"],i["title"],i["year"],i["venue"]]])
                else:
                    matched[string]=([[i["id"],i["title"],i["year"],i["venue"]]])
    if len(matched) == 0 :
        print("No info mathched your input keyword ! ")
        return
    limit=0
    count=0
    select_author=''
    for i in matched.keys():
        print("Author name: "+i.ljust(20)+ "        Number of published: "+ str(len(matched[i])))
        limit+=1

        while(limit==len(matched.keys())):
            select = input("All info has been displayed, please select one: ")
            if select.lstrip().rstrip() in matched.keys():
                select_author=select.lstrip().rstrip()
                break
            else:
                print("Invalid input ! ")
        if limit%5 == 0 :
            select = input("Please enter the author name that you interested or by enter anything to show more matched info : ")
            if select.lstrip().rstrip() in matched.keys():
                select_author=select.lstrip().rstrip()
                break
            else:
                pass
        for j in matched[i]:
            count +=1
        if select_author!='':
            break
        count =0
    print("--------------------")
    print("--------------------")
    for i in matched[select_author]:
        print("author: ".ljust(15)+select_author)
        print("Id: ".ljust(15),str(i[0]))
        print("Title: ".ljust(15)+i[1])
        print("Year: ".ljust(15)+str(i[2]))
        print("Venue: ".ljust(15)+i[3])
        print("")

        print("|======================================|")
    print("|                 Menu                 |")
    print("|======================================|")
    print("|   option  |        description       |")
    print("|======================================|")
    print("|     1     |    Search author again   |")
    print("|     2     |     Back to main menu    |")
    print("|======================================|")
    again = input("Enter an option:").strip()
    while again not in ["1","2"]:
        again = input("Please enter a valid option :").strip()

    if again=="1":
        search_authors()
    else:
        return


def list_venue():
    '''
    The user should be able to enter a number n and see a listing of top n venues. 
    For each venue, list the venue, the number of articles in that venue, and the 
    number of articles that reference a paper in that venue. Sort the result based 
    on the number of papers that reference the venue with the top most cited venues shown first. 
    '''
    n = input("Please enter a number: ").strip()
    while n.isdigit() ==False:
        n = input("Please enter a number: ")
    n = int(n)

    cursor = lj.collection.aggregate([
                                      {"$match":{"venue":{"$ne":""}}},
                                      {"$lookup":{
                                            "from": "dblp",
                                            "localField": "id",              # a2.id
                                            "foreignField": "references",    # a1.references 
                                            "as":"ref_list"
                                        }},
                                      {"$unwind":{"path": "$ref_list","preserveNullAndEmptyArrays":True }},
                                      {"$addFields": {"ref": "$ref_list.id"}},
                                      {"$project":{"_id":0,"id":1,"venue":1,"ref":1}},
                                      {"$group": {     
                                            "_id":"$venue",  # GROUP BY  a2.venue
                                            "unique_refs":{"$addToSet":"$ref"}
                                        }},
                                     {"$addFields": {"number_of_refs": {"$size": "$unique_refs"}}},
                                     {"$project": {"_id":1,"number_article_in_venue":1,"number_of_refs":1}},
                                    {"$sort":{"number_of_refs":-1} },
                                    {"$limit":n}
                                    ], allowDiskUse = True)
    venue_ref = {}
    venue = []
    for i in cursor:
        venue.append(i["_id"])
        venue_ref[i["_id"]] = i["number_of_refs"]
        
    cursor = lj.collection.aggregate([{"$match":{"venue":{"$in":venue}}},
                                      {"$group":{
                                        "_id":"$venue",
                                        "number_article_in_venue":{"$sum":1}
                                      }},
                                      {"$project":{"_id":1,"number_article_in_venue":1}}])
    venue_num= {}
    for i in cursor:
        venue_num[i["_id"]] = i["number_article_in_venue"]

    print("=========================================================================================================================")
    print("venue".rjust(30)+ "          number of article in this venue".rjust(70)+"          number of paper that references this venue".rjust(10))
    for i in venue:
        print(i.ljust(70)+str(venue_num[i]).rjust(20)+str(venue_ref[i]).rjust(40))

    print("=========================================================================================================================")

    print("|======================================|")
    print("|                 Menu                 |")
    print("|======================================|")
    print("|   option  |        description       |")
    print("|======================================|")
    print("|     1     |    List top n venues     |")
    print("|     2     |     Back to main menu    |")
    print("|======================================|")
    again = input("Please select an option:").strip()
    while again not in ["1","2"]:
        again = input("Please enter a valid option :").strip()

    if again=="1":
        list_venue()
    else:   
        return

def add_article():
    '''
    The user should be able to add an article to the collection by providing 
    a unique id, a title, a list of authors, and a year. The fields abstract and 
    venue should be set to null, references should be set to an empty array and
    n_citations should be set to zero. 
    '''
    # id
    n_id = input("Please enter the id of the article: ")
    cursor = lj.collection.count_documents({"id": n_id})
    while (1):
        if int(cursor) > 0:
            n_id = input("The id is not unique please enter it again: ")
            cursor = lj.collection.count_documents({"id": n_id})

        else:
            break
    # title
    n_title = input("Please enter a title of the article: ").strip()
    while len(n_title)==0:
        n_title = input("Please enter a valid title of the article: ").strip()

    # author
    author_list= []
    ask1 = input("if you want add authors for the article enter 2: ").strip()    
    while(1): # change 
        while ask1 not in ["1","2"]:
            print("\nPlease enter a valid option")
            ask1 = input("if you want add more authors for the article enter 2, if you not enter 1: ").strip()            
        if ask1 == "1": # no author create together
            break
        elif ask1 == "2": # other authors create together
            ask2=input("Enter the author title: ").strip()
            while (1):
                if ask2 not in author_list:
                    author_list.append(ask2)
                    ask1 = input("if you want add more authors for the article enter 2, if not enter 1: ").strip()
                    break
                else:
                    ask2=input("The author does not exist or the authors already has inserted,please enter cooporate author title again: ").strip()    
    # year    
    n_year =input("Please enter a year of the article: ")
    while(1):
        if n_year.isdigit() :
            n_year=int(n_year)
            break
        else:
            n_year= input("Invalid input! Please enter the year of the article again: ")
    lj.collection.insert_one({"id":n_id,"title":n_title,"authors":author_list,"venue": " ","year":n_year,"n_citation":0,"references":[],"absract":" "})
    print("Successfully insert!")

    print("|======================================|")
    print("|                 Menu                 |")
    print("|======================================|")
    print("|   option  |        description       |")
    print("|======================================|")
    print("|     1     |    Add another article   |")
    print("|     2     |     Back to main menu    |")
    print("|======================================|")
    again = input("Enter an option:").strip()
    while again not in ["1","2"]:
        again = input("Please enter a valid option :").strip()

    if again=="1":
        add_article()
    else:
        return

def check_exist_id(id):
    cursor = lj.collection.count_documents({"id":id})
    if cursor>0:
        return -1
    return 0

 
def main():
    print_menu()
    opt= input("Please select an option from the menu: ").strip()
    if len(opt)==0 or opt.isdigit() == False :
        opt= input("Please enter a valid option: ").strip()
    
    while opt!= "5":
        if opt=="1":
            search_article()
        if opt=="2":
            search_authors()
        if opt=="3":
            list_venue()
        if opt=="4": # exit
            add_article()

        print_menu()
        opt= input("Please select an option from the menu: ").strip()
        while len(opt)==0 or opt.isdigit() == False :
            opt= input("Please enter a valid option: ").strip()

main()