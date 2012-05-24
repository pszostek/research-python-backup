similarity_aggregator_l = avg #python version: should work on list


 
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! 
def ____load_simmatrix_routine____(sim_matrix_path):
    starttime = time.clock()
    if sim_matrix_path.endswith(".pickle"):
        (rows, cols, sim_matrix_p) = pickle.load(open(sim_matrix_path))        
    else:
        (rows, cols, sim_matrix_p) = matrix_io.fread_smatrix_L(sim_matrix_path) #, datareader=matrix_io.__read_ftabs__, maxrows=1000
        print " loaded in",time.clock()-starttime,"s"
        #if not os.path.isfile(sim_matrix_path+".pickle"):       
        #    print " pickling to=",(sim_matrix_path+".pickle")
        #    pickle.dump((rows, cols, sim_matrix_p), open(sim_matrix_path+".pickle", "wb"))    
    print "","matrix of size=",len(rows),"x",len(cols),"loaded:",str(sim_matrix_p[:10])[:100],"in",time.clock()-starttime,"s"
    #print "","validating..."
    #if len(sim_matrix.validate_similarity_matrix(sim_matrix_p))>0: print "ERROR. invalid elements in sim_matrix_p!"; sys.exit(-2)
    zblid2simix = dict( (label,ix) for ix,label in enumerate(rows) )
    print " zblid2simix=", str(list(zblid2simix.iteritems()))[:100] 
    return (rows, cols, sim_matrix_p, zblid2simix)
     
def ____calc_sim_matrix_l_primarymsc_routine____(sim_matrix_l, mscmodel, msc2ix, doc2doc_similarity_calculator):
    gen =  mscmsc2sampleids_generator(mscmodel.mscprim2count.keys(), mscmodel.mscprim2zblidlist, mscmsc_calculate_sample_size)
    for (msc1,msc2),zbl_ids_pairs in gen:
        #print "[____calc_sim_matrix_l_primarymsc_routine____] Considering:",(msc1,msc2)        
        mscix1, mscix2 = msc2ix[msc1], msc2ix[msc2]         
        zbl2zbl_sim_submatrix  = build_sparse_similiarity_matrix(zblid2zbl, zbl_ids_pairs, doc2doc_similarity_calculator)                        
        sim_matrix_l[mscix1][mscix2] = sim_matrix_l[mscix2][mscix1] = similarity_aggregator_l(zbl2zbl_sim_submatrix.values())
        #logging.info("[build_mscmsc_sim]"+str((msc1,msc2))+":"+str(list(zbl2zbl_sim_submatrix.iteritems()))[:100]+ " -> "+str(sim_matrix_l[mscix1][mscix2]) )
    return sim_matrix_l                     
    

def __python_sim_matrix_l_generation_routine__(sim_matrix_path, mscmodel, msc2ix):
    print "--------------------------------------------------------"
    print "Loading sim_matrix_p from sim_matrix_path=",sim_matrix_path
    (rows, cols, sim_matrix_p, zblid2simix) = ____load_simmatrix_routine____(sim_matrix_path)
    #metoda liczenia odleglosci miedzy dwoma dokumentami:
    def doc2doc_similarity_calculator(zbl1, zbl2):        
        zblid1, zblid2 = zbl1[zbl_io.ZBL_ID_FIELD], zbl2[zbl_io.ZBL_ID_FIELD]
        #logging.info("[doc2doc_similarity_calculator] comparing "+str(zblid1)+" vs. "+str(zblid2)) 
        ix1,ix2 = zblid2simix[zblid1],zblid2simix[zblid2]
        #print "[doc2doc_similarity_calculator] ix1,ix2=",ix1,ix2
        return sim_matrix_p[max(ix1,ix2)][min(ix1,ix2)]
    
    print "--------------------------------------------------------"
    print "Preparing similarity matrix on L-level ..."
    sim_matrix_l = matrix_io.create_matrix(mscmodel.N(), mscmodel.N(), value = 0.0)
    matrix_io.set_diagonal(sim_matrix_l, sim_matrix.MAX_SIMILARITY_VALUE)
        
    print "--------------------------------------------------------"
    starttime = time.clock()
    print "Building similarity matrix on L-level (aggregator:",similarity_aggregator_l,")..."
    sim_matrix_l = ____calc_sim_matrix_l_primarymsc_routine____(sim_matrix_l, mscmodel, msc2ix, doc2doc_similarity_calculator)    
    print " built in",time.clock()-starttime,"s"
        
    return sim_matrix_l
