import psycopg2

# first run these commands before executing this script
# $ wget https://archive.ics.uci.edu/ml/machine-learning-databases/20newsgroups-mld/20_newsgroups.tar.gz
# $ tar xzvf 20_newsgroups.tar.gz

connection = None
cursor = None

def getNewsGroups():
    ngroups = []
    try:
        import os
        for root, dirs, files in os.walk('20_newsgroups'):
            if root == "20_newsgroups":
                # skip the localdir and move on to subdirs
                continue
            ngroups.append(root.split("/")[1])
    except (Exception) as error :
        print ("Error while directories", error)

    return ngroups

def getMsgFileNames(grp):
    fnames = []
    try:
        import os
        dirname = "./20_newsgroups/" + grp
        for root, dirs, files in os.walk(dirname):
            for f in files:
                fnames.append(f)
    except (Exception) as error :
        print ("Error while reading filenames", error)

    return fnames

def loadContent(fname, g, f):
    cnt = ""
    linesSection = False
    cStarted = False
    with open (fname, "r") as myfile:
        data=myfile.readlines()
        for ln in data:
            if cStarted:
                # HACK should be properly escaped to not lose single quote
                cnt += ln.replace("'", "")
                continue
            if linesSection:
                cStarted = True
                continue
            if ln.startswith("Lines: "):
                linesSection = True
    sql = "INSERT INTO messages VALUES('" + g + "'," + f + ",'" + cnt + "')"
    try:
        cursor.execute(sql)
    except (Exception) as error :
        print(sql)
        print("Failed INSERT: ", error)


 
def loadNewsGroup(grp):
    msgFiles = getMsgFileNames(g)
    for f in msgFiles:
        fname = "./20_newsgroups/" + g + "/" + f
        content = loadContent(fname, g, f)
        break

if __name__ == '__main__':
    connection = psycopg2.connect(database="pytest")
    cursor = connection.cursor()
    try:
        cursor.execute("DROP TABLE if exists messages")
        cursor.execute("CREATE TABLE messages(newsgroup text, id int, msg text) distributed randomly")
    except (Exception) as error :
        print("Failed CREATE TABLE: ", error)

    # load data
    newsGroups = getNewsGroups()
    for g in newsGroups:
        print ("Loading group ", g)
        loadNewsGroup(g)
        break

