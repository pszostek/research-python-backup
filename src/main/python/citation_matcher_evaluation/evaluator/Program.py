from results import load_ujf_results, load_icm_results, EmptyInternalMapping, InternalMapping

#mapping = InternalMapping(r'C:\Users\matfed\Desktop\matcher-results\id_manager_id_store')
mapping = EmptyInternalMapping()
names = ['alpha', 'abbrv', 'ieeetr', 'plain', 'apalike', 'acm', 'jpc', 'pccp', 'ppcf', 'revcompchem']
for name in names:
    res = load_ujf_results(r'C:\Users\matfed\Desktop\test-sets\%s_map.txt' % name, 
                           r'C:\Users\matfed\Desktop\parsed\%s.xml_result' % name, 
                           mapping)
    print res.get_csv()

#internal_mapping1 = InternalMapping(r'C:\Users\matfed\Desktop\matcher-results\id_manager_id_store')
#internal_mapping2 = InternalMapping(r'C:\Users\matfed\Desktop\matcher-test-results\id_manager_id_store')
##results1 = load_ujf_results(r'C:\Users\matfed\Desktop\test-sets\pccp_map.txt', 
##                           r'C:\Users\matfed\Desktop\matcher-results\ujf_results\pccp.txt_result', 
##                           internal_mapping)
##results1.print_results()
##print results1.get_csv()

#results1 = load_icm_results(r'C:\Users\matfed\Desktop\test-sets\pccp_map.txt', 
#                            r'C:\Users\matfed\Desktop\matcher-results\rel_1_bibreferences',
#                            'urn:eudml:doc:10961', 
#                            internal_mapping1)
##results1.print_results()

#results2 = load_icm_results(r'C:\Users\matfed\Desktop\test-sets\pccp_map.txt', 
#                            r'C:\Users\matfed\Desktop\matcher-test-results\matching-icm',
#                            'urn:eudml:doc:11206', 
#                            internal_mapping2)
##results2.print_results()

#correct1 = set(map(lambda (x,y): x, results1.get_correct_nonempty()))
#correct2 = set(map(lambda (x,y): x, results2.get_correct_nonempty()))

#print len(correct1)
#print len(correct2)


#print len(correct2 & correct1)

#print "####"
#for n in correct2 - correct1:
#   print n