import psycopg2

# first run these commands before executing this script
# $ wget https://archive.ics.uci.edu/ml/machine-learning-databases/20newsgroups-mld/20_newsgroups.tar.gz
# $ tar xzvf 20_newsgroups.tar.gz


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

def loadContent(cursor, fname, g, f):
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
    sql = "INSERT INTO news VALUES('" + g + "'," + f + ",'" + cnt + "')"
    cursor.execute(sql)
 
def loadNewsGroup(cursor, grp):
    msgFiles = getMsgFileNames(g)
    counter = 0
    for f in msgFiles:
        counter += 1
        fname = "./20_newsgroups/" + g + "/" + f
        try:
            content = loadContent(cursor, fname, g, f)
        except:
            print("Skip: " + fname)
        if counter % 50 == 0:
            print("Group %s Loaded %d" % (grp, counter))

if __name__ == '__main__':
    try:
        connection = psycopg2.connect(database="pytest")
        cursor = connection.cursor()
        cursor.execute("DROP TABLE if exists news;")
        cursor.execute("CREATE TABLE news(newsgroup text, id int, msg text) distributed randomly;")

        # load data
        newsGroups = getNewsGroups()
        for g in newsGroups:
            print ("Loading group ", g)
            loadNewsGroup(cursor, g)

        connection.commit()

    except (Exception, psycopg2.Error) as error :
        print ("Error while connecting to PostgreSQL", error)

    finally:
        if(connection):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")

    
