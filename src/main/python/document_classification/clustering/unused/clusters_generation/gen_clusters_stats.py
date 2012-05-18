"""Reads information about clusters and generates statistics."""

#Skrypt bierze informacje o podziale na klastry 
#i na tej podstawie generuje plik zawierajacy statystyki poszczegolnych klastrow.


import Image, ImageDraw, ImageFont, ImageOps
import operator, math
import data.io, calc.processing, calc.maths
import sys, os

if __name__ == "__main__":

    args = sys.argv
    if len(sys.argv) != 3:
        print "[ERROR] Exactly two arguments are expected: input-matrix-path labels'-prefix-length"
        exit(-1)
    simMatrixPath   = args[1] 
    prefix_len      = int(args[2])                                                              #length of prefix used for clusters' etiquettes generating

    name            = os.path.basename(simMatrixPath).split('.')[0]                             #file path base name
    labelsPath      = '/tmp/tr_' + name + '_labels_' + str(prefix_len) + '.svector'             #etiguettes of elements
    inClustPath     = '/tmp/tr_' + name + '_clustdesc_' + str(prefix_len) + '.txt'              #file with aggregated information about clusters (etiquette + list of indexes)
    outStatsPath    = '/tmp/tr_' + name + '_stats_' + str(prefix_len) + '.txt'                  #file to put output statistics



    clustdesc       = data.io.fread_clusters(inClustPath)        # clustering
    labels          = data.io.fread_svector(labelsPath)
    print "Read assignment of", len(labels), "elements to", len(clustdesc),"clusters..."


    #statistisc:
    wrongs_count        = []
    wrongs_fractions    = []
    gini_ixs            = []
    entropies           = []

    #calculates etiquettes and statistics:
    fout = open(outStatsPath, 'w')
    for cluster in clustdesc:
        etiquette   = cluster[0]
        ixs         = cluster[1]
        lbls        = [labels[ix] for ix in ixs] #labels of selected indexes
        n           = float(len(ixs)) #number of elements in cluster
        count       = calc.processing.count_unique_prefixes(lbls, prefix_len) #count prefixes in labels
        #impurity factors:
        if count.has_key(etiquette):
            selected_count  = count[etiquette]
        else:
            selected_count  = 0
        wrong_count = calc.maths.wrongly_classified(count.values(), selected_count)
        wrong_frac  = calc.maths.wrongly_classified_fraction(count.values(), selected_count)
        gini_ix     = calc.maths.gini_index(count.values())
        entropy     = calc.maths.entropy(count.values())
        #saving results:
        wrongs_count.append( wrong_count )
        wrongs_fractions.append( wrong_frac )
        gini_ixs.append( gini_ix )
        entropies.append( entropy )
        #writing to file:
        fout.write(etiquette+"\t"+str(len(ixs))+"\t"+str(max(count.values()))+"\t")
        fout.write(str(wrong_count)+"\t"+str(wrong_frac)+"\t"+str(gini_ix)+"\t"+str(entropy)+"\t")
        lbls_str = str(lbls).replace("[","").replace("]","").replace("'","").replace(",","\t").replace(" ","")
        fout.write(lbls_str+"\n")
    fout.close()


    #printing overall statistics:
    etiquettes = [element[0] for element in clustdesc] 
    uq_etiquettes = set(etiquettes)
    etiq_count = dict([(etiq, sum(1 for e in etiquettes if e == etiq) ) for etiq in etiquettes]) #dictionary: (etiquette -> number of occurrences)
    print "Unique etiquettes =", len(uq_etiquettes), " out of", len(etiquettes)

    print "[wrongs_count]\t"," min=", min(wrongs_count), "\t max=", max(wrongs_count), "\t avg=", calc.maths.avg(wrongs_count), "\t std=", calc.maths.std(wrongs_count), "\t sum=", sum(wrongs_count)
    print "[wrongs_frac]\t"," min=", min(wrongs_fractions), "\t max=", max(wrongs_fractions), "\t avg=", calc.maths.avg(wrongs_fractions), "\t std=", calc.maths.std(wrongs_fractions)
    print "[entropies]\t"," min=", min(entropies), "\t max=", max(entropies), "\t avg=", calc.maths.avg(entropies), "\t std=", calc.maths.std(entropies)
    print "[gini_ixs]\t"," min=", min(gini_ixs), "\t max=", max(gini_ixs), "\t avg=", calc.maths.avg(gini_ixs), "\t std=", calc.maths.std(gini_ixs)




