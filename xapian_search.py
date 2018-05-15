import json
import sys
import xapian

### Start of example code.
def search(dbpath, querystring, offset=0, pagesize=100, ident=0):
    # offset - defines starting point within result set
    # pagesize - defines number of records to retrieve

    # Open the database we're going to search.
    db = xapian.Database(dbpath)

    # Set up a QueryParser with a stemmer and suitable prefixes
    queryparser = xapian.QueryParser()
    queryparser.set_stemmer(xapian.Stem("pt"))
    queryparser.set_stemming_strategy(queryparser.STEM_SOME)
    # Start of prefix configuration.
    queryparser.add_prefix("text", "XD")
    # End of prefix configuration.

    # And parse the query
    query = queryparser.parse_query(querystring)

    # Use an Enquire object on the database to run the query
    enquire = xapian.Enquire(db)
    enquire.set_query(query)

    # And print out something about each match
    matches = []
    for match in enquire.get_mset(offset, pagesize):
        field = match.document.get_data()
        print(u"%(ident)s Q0 %(id)s %(rank)i %(weight)s danielatkinson_filipemoreira" % {
            'ident': ident,
            'rank': match.rank,
            'weight': match.weight,
            'id': field.split(":")[0]
            })
        matches.append(match.docid)

    # Finally, make sure we log the query and displayed results
    # log_matches(querystring, offset, pagesize, matches)
### End of example code.

def log_matches(querystring, offset, pagesize, matches):
    print(
        "'%s'[%i:%i] = %s" % (
            querystring,
            offset,
            offset + pagesize,
            ' '.join(str(docid) for docid in matches),
        )
    )


if len(sys.argv) < 3:
    if len(sys.argv) > 1:
        queries = [u"uso energia atomica fim pacifico favor pro contra argumento", u"nome top model supermodel internacional famosa", u"consequencia constitucional Reino Unido constituicao divorcio principe Carlos princesa Diana Gales", u"nome filme Keanu Reeves atua lancado exibido cartaz ator", u"pintura o grito roubada roubo edvard munch galeria nacional oslo", u"quatro casamentos e um funeral bom sucesso popular filme", u"brasil suecia semifinal campeonato mundo 1994 resultado equipe jogo", u"grand slam 1995 campeao vencedor nome pais nacionalidade", u"oscar melhor filme 1994 nome", u"morte richard nixon doenca causa"]
        for i in range(len(queries)):
            search(dbpath = sys.argv[1], querystring = queries[i], ident = (i+1))
        sys.exit(1)
    else:
        print("Usage: %s DBPATH QUERYTERM..." % sys.argv[0])
        sys.exit(1)

search(dbpath = sys.argv[1], querystring = " ".join(sys.argv[2:]))