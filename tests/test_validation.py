# validate tsv/csv and lpf uploads
from django.http import HttpResponseRedirect
from django.test import Client
from django.test import TestCase, SimpleTestCase
from django.urls import reverse
import os, codecs, json, mimetypes, re, sys
from chardet import detect
from datasets.static.hashes import mimetypes as mthash
from datasets.static.hashes import mimetypes_plus as mthash_plus
from datasets.utils import validate_tsv

# DatasetCreateView() -> 
# load file, get encoding, mimetype (file.content_type)
# validate_tsv(filepath,extension)
fields = ['id','title','title_source','start','title_uri','ccodes','matches','variants',
 'types','aat_types','parent_name','parent_id','lon','lat','geo_wkt','geo_source',
 'geo_id','end','description']

class ValidateTSV(SimpleTestCase):
  # test 
  def testValidateSpreadsheet(self):
    import pandas as pd
    os.chdir('/Users/karlg/Documents/repos/_whgazetteer/')
    dd = '/Users/karlg/Documents/repos/_whgazetteer/_testdata/'
    files_ok = ['bdda34_xlsx.xlsx','bdda34_ods.ods']
    files_err = ['bdda34_err_xlsx.xlsx','bdda34_err_ods.ods']
    
    def get_encoding_excel(file):
      fin = codecs.open(file, 'r')
      return fin.encoding
    
    errors = []
    #for f in files_err:
    for f in files_ok:
      fn = dd+f
      mimetype = mimetypes.guess_type(fn, strict=True)[0]
      valid_mime = mimetype in mthash_plus.mimetypes
      if not valid_mime:
        errors.append({"file":f, "msg": "incorrect mimetype: "+mimetype})
        pass
      else:
        if 'spreadsheet' in mimetype:
          encoding = get_encoding_excel(fn)

      if encoding and encoding.lower().startswith('utf-8'):
        ext = mthash_plus.mimetypes[mimetype]

        fnout = dd+'/_temp/'+f+'.tsv'
        fout=codecs.open(fnout, 'w', encoding='utf8')
        df = pd.read_excel(fn)
        header = list(df.columns.values)
        # TODO: auto pop data_types_dict keys missing in header
        schema = {'id': str, 'start':str, 'end':str, 'aat_types': str, 'lon': float, 'lat': float}
        types = dict(filter(lambda col: col[0] in header, schema.items()))
        
        df = df.astype(types)
        table=df.to_csv(sep='\t', index=False)
        fout.write(table)
        fout.close()
        #infile = codecs.open(fnout, 'r')
        result = validate_tsv(fnout, 'tsv')
        
        ccodesRegex = r"^([a-zA-Z]{2})$|([a-zA-Z]{2})(;\s*(([a-zA-Z]{2});?)*)"
        ccodes=df['ccodes'].str.contains(ccodesRegex, regex=True)
        df.index[ccodes == False].tolist()
        
        #result = validate_tsv(fn, ext)
        errors.append({"file":f, "msg":result['errors']})
        # validate_tsv() adds extension; strip it
        os.rename(fn+'.'+ext,fn)
      else:
        errors.append({"file":f, "msg": "incorrect encoding: "+str(encoding)})
      
      print(f, mimetype, encoding)
    print(errors)

    # tests
    self.assertIn('constraint "required" is "True"', errors[0]['msg'][0])
    self.assertIn('not conform to a constraint', errors[0]['msg'][1])
    self.assertEquals(errors[1]['msg'],[])
    self.assertIn('Required field(s) missing', errors[2]['msg'][0])
    self.assertIn('incorrect encoding', errors[3]['msg'])

  # ok, 4 Jan 2021
  def testValidateTSV(self):
    os.chdir('/Users/karlg/Documents/repos/_whgazetteer/')
    dd = '/Users/karlg/Documents/repos/_whgazetteer/_testdata/'
    #files_ok = ['diamonds135.tsv', 'croniken20.tsv', 'bdda34.csv']
    files_err = ['bdda34_errors.tsv','bdda34_extra-col.csv','bdda34_missing-col.csv', 'bdda34_utf16.tsv']
    
    def get_encoding_type(file):
      with open(file, 'rb') as f:
        rawdata = f.read()
      return detect(rawdata)['encoding']

    def get_encoding_excel(file):
      fin = codecs.open(file, 'r')
      return fin.encoding
    
    errors = []
    #for f in files:
    for f in files_err:
      fn = dd+f
      mimetype = mimetypes.guess_type(fn, strict=True)[0]
      valid_mime = mimetype in mthash_plus.mimetypes
      if not valid_mime:
        errors.append({"file":f, "msg": "incorrect mimetype: "+mimetype})
        pass
      else:
        if mimetype.startswith('text/'):
          encoding = get_encoding_type(fn)
        elif 'spreadsheet' in mimetype:
          encoding = get_encoding_excel(fn)
      
      if encoding and encoding.lower().startswith('utf-8'):
        ext = mthash_plus.mimetypes[mimetype]
        result = validate_tsv(fn, ext)
        errors.append({"file":f, "msg":result['errors']})
        # validate_tsv() adds extension; strip it
        os.rename(fn+'.'+ext,fn)
      else:
        errors.append({"file":f, "msg": "incorrect encoding: "+str(encoding)})
      
      print(f, mimetype, encoding)
    print(errors)

    # tests
    self.assertIn('constraint "required"', errors[0]['msg'][0]) # missing 'start'
    self.assertIn('constraint "pattern"', errors[0]['msg'][1]) # malformed ccodes (commas)
    self.assertEquals(errors[1]['msg'],[])
    self.assertIn('Required field(s) missing', errors[2]['msg'][0])
    self.assertIn('incorrect encoding', errors[3]['msg'])
  
  
# TODO: validate_lpf(filepath,'coll')

# DatasetCreateModelForm ->
class CallViews(SimpleTestCase):
  def testViews(self):
    responses = []
    urls = ['dashboard', 'datasets:dataset-create']
    param_urls = ['datasets:dataset-detail', 'datasets:dataset-delete']
    client = Client()
    for url in urls:
      responses.append( client.get(reverse(url)).status_code )
    
    for url in param_urls:
      responses.append( HttpResponseRedirect(reverse(url, args=(99999,))).status_code )
    
    self.assertEquals(list(set(responses)), [302])

# datasets/dataset_create.html -> SUBMIT
# DatasetCreateView() -> form_valid()


#for f in files_err:
  # fn = dd+f
  # print(get_encoding_type(fn))