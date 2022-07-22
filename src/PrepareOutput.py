import pandas as pd

import os

plflist1_ML=['PLF_561_00049890','PLF_561_00004782','PLF_561_00007970','PLF_561_00005659','PLF_561_00006091',
          'PLF_561_00013716','PLF_561_00019473','PLF_561_00009406','PLF_561_00015082','PLF_561_00003350',
          'PLF_561_00009585','PLF_561_00005191','PLF_561_00008661','PLF_561_00019538','PLF_561_00008369',
          'PLF_561_00000117','PLF_561_00071721','PLF_561_00006969','PLF_561_00005448','PLF_561_00028701',
          'PLF_561_00017967','PLF_561_00028114','PLF_561_00005992','PLF_561_00011189','PLF_561_00175318']
          #'PLF_561_00028965','PLF_561_00003914','PLF_561_00051514','PLF_561_00009167']


plflist1_IG=['PLF_561_00004782', 'PLF_561_00015082', 'PLF_561_00051514', 'PLF_561_00007970', 'PLF_561_00013716',
            'PLF_561_00003800', 'PLF_561_00194287', 'PLF_561_00005453', 'PLF_561_00032227', 'PLF_561_00008661',
            'PLF_561_00004767', 'PLF_561_00006645', 'PLF_561_00006369', 'PLF_561_00004266', 'PLF_561_00003934',
            'PLF_561_00005188', 'PLF_561_00006148', 'PLF_561_00005227', 'PLF_561_00050366', 'PLF_561_00004864', 
            'PLF_561_00009597', 'PLF_561_00012859', 'PLF_561_00004757', 'PLF_561_00105022', 'PLF_561_00057682']


plflist1_G=['PLF_561_00004782','PLF_561_00051514', 'PLF_561_00013577', 'PLF_561_00010277', 'PLF_561_00009538',
            'PLF_561_00015082', 'PLF_561_00008524', 'PLF_561_00023808', 'PLF_561_00171609', 'PLF_561_00193976',
            'PLF_561_00005188', 'PLF_561_00105022', 'PLF_561_00004266', 'PLF_561_00008154', 'PLF_561_00004767',
            'PLF_561_00004864', 'PLF_561_00003863', 'PLF_561_00049278', 'PLF_561_00014914', 'PLF_561_00058863',
            'PLF_561_00009909', 'PLF_561_00005477', 'PLF_561_00007819', 'PLF_561_00006645' 'PLF_561_00050366']
intersection = set(plflist1_ML).intersection(plflist1_IG)
print(list(intersection))

intersection = set(plflist1_ML).intersection(plflist1_G)
print(list(intersection))

intersection = set(plflist1_G).intersection(plflist1_IG)
print(list(intersection))



def CheckGenes(dir,plflist,finaldf):
    if (len(plflist) > 0):
        for filename in os.listdir(dir):
            df = pd.read_csv(dir + filename, sep="\t", index_col=5, low_memory=False)
            selectedf = df[['plfam_id', 'pgfam_id', 'feature_type', 'gene', 'product']]
            selectedf = selectedf.dropna(subset=['plfam_id'])
            if (len(plflist) <= 0):
                break
            for itm in plflist:
                pgfam = selectedf[selectedf['plfam_id'] == itm]
                if (len(pgfam.values) != 0):
                    print('found')
                    finaldf = finaldf.append({'plfam_id': itm, 'pgfam_id': pgfam['pgfam_id'].iloc[0],
                                              'feature_type': pgfam['feature_type'].iloc[0],
                                              'gene': pgfam['gene'].iloc[0], 'product': pgfam['product'].iloc[0]},
                                             ignore_index=True)
                    plflist.remove(itm)
    return plflist,finaldf


plflist=list(set(plflist1_IG))

finaldf = pd.DataFrame({'plfam_id':[''],'pgfam_id':[''],'feature_type':[''],'figfam_id':[''],'gene':[''], 'product':['']})

BaseDir='../../../../../../data/Escherichia/'
for subdir in os.listdir(BaseDir):
    if (subdir=='piperacillin'):
        subdir=subdir+'/tazobactam'
    dir=BaseDir+subdir+'/Resistant/features/'
    plflist,finaldf=CheckGenes(dir,plflist,finaldf)
    print(len(plflist))
    if(len(plflist) ==0):
        break
finaldf.to_csv('../outpt/plfam_id_description_dataset_IG_EColi.csv',sep=',')