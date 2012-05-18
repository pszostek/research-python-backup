from results import InternalMapping, load_ujf_results, load_icm_results

internal_mapping = InternalMapping(r'C:\Users\matfed\Desktop\matcher-results\id_manager_id_store')
results1 = load_ujf_results(r'C:\Users\matfed\Desktop\test-sets\pccp_map.txt', 
                           r'C:\Users\matfed\Desktop\matcher-results\ujf_results\pccp.txt_result', 
                           internal_mapping)
results1.print_results()
print results1.get_csv()

results2 = load_icm_results(r'C:\Users\matfed\Desktop\test-sets\pccp_map.txt', 
                            r'C:\Users\matfed\Desktop\matcher-results\rel_1_bibreferences',
                            'urn:eudml:doc:10961', 
                            internal_mapping)
results2.print_results()
print results2.get_csv()
