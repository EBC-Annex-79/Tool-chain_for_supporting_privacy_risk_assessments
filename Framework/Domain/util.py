def find_domain_data_in_data_list(data_list):
    return  [d.domain_data_type  for d in data_list]

def find_domain_data_in_data_list_dict(data_list):
    key_list = find_domain_data_in_data_list(data_list)
    out_put = {}
    for index in range(len(key_list)):
        out_put[key_list[index]] = data_list[index]
    return  out_put
