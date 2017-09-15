Search.setIndex({docnames:["api/api_index","api/api_reference","api/pygeoc.TauDEM","api/pygeoc.hydro","api/pygeoc.postTauDEM","api/pygeoc.raster","api/pygeoc.utils","api/pygeoc.vector","get_started","index"],envversion:52,filenames:["api/api_index.rst","api/api_reference.rst","api/pygeoc.TauDEM.rst","api/pygeoc.hydro.rst","api/pygeoc.postTauDEM.rst","api/pygeoc.raster.rst","api/pygeoc.utils.rst","api/pygeoc.vector.rst","get_started.rst","index.rst"],objects:{"pygeoc.TauDEM":{TauDEM:[2,1,1,""],TauDEMFilesUtils:[2,1,1,""],TauDEMWorkflow:[2,1,1,""],run_test:[2,3,1,""]},"pygeoc.TauDEM.TauDEM":{aread8:[2,2,1,""],areadinf:[2,2,1,""],connectdown:[2,2,1,""],convertdistmethod:[2,2,1,""],convertstatsmethod:[2,2,1,""],d8distdowntostream:[2,2,1,""],d8flowdir:[2,2,1,""],dinfdistdown:[2,2,1,""],dinfflowdir:[2,2,1,""],dropanalysis:[2,2,1,""],error:[2,2,1,""],fill:[2,2,1,""],fullpath:[2,2,1,""],gridnet:[2,2,1,""],log:[2,2,1,""],moveoutletstostrm:[2,2,1,""],peukerdouglas:[2,2,1,""],run:[2,2,1,""],streamnet:[2,2,1,""],threshold:[2,2,1,""]},"pygeoc.TauDEM.TauDEMWorkflow":{watershed_delineation:[2,2,1,""]},"pygeoc.hydro":{D8Util:[3,1,1,""],FlowModelConst:[3,1,1,""]},"pygeoc.hydro.D8Util":{convert_code:[3,2,1,""],downstream_index:[3,2,1,""]},"pygeoc.hydro.FlowModelConst":{ccw_dcol:[3,4,1,""],ccw_drow:[3,4,1,""],d8_deltas:[3,4,1,""],d8_dirs:[3,4,1,""],d8_inflow_ag:[3,4,1,""],d8_inflow_td:[3,4,1,""],d8_inflow_wb:[3,4,1,""],d8_inflows:[3,4,1,""],d8_lens:[3,4,1,""],d8anglelist:[3,4,1,""],d8delta_ag:[3,4,1,""],d8delta_td:[3,4,1,""],d8delta_wb:[3,4,1,""],d8dir_ag:[3,4,1,""],d8dir_td:[3,4,1,""],d8dir_wb:[3,4,1,""],d8len_ag:[3,4,1,""],d8len_td:[3,4,1,""],d8len_wb:[3,4,1,""],e:[3,4,1,""],get_cell_length:[3,2,1,""],get_cell_shift:[3,2,1,""],n:[3,4,1,""],ne:[3,4,1,""],nw:[3,4,1,""],s:[3,4,1,""],se:[3,4,1,""],sw:[3,4,1,""],w:[3,4,1,""]},"pygeoc.postTauDEM":{DinfUtil:[4,1,1,""],StreamnetUtil:[4,1,1,""]},"pygeoc.postTauDEM.DinfUtil":{check_orthogonal:[4,2,1,""],compress_dinf:[4,2,1,""],dinf_downslope_direction:[4,2,1,""],downstream_index_dinf:[4,2,1,""],output_compressed_dinf:[4,2,1,""]},"pygeoc.postTauDEM.StreamnetUtil":{assign_stream_id_raster:[4,2,1,""],serialize_streamnet:[4,2,1,""]},"pygeoc.raster":{GDALDataType:[1,5,1,""],Raster:[5,1,1,""],RasterUtilClass:[5,1,1,""]},"pygeoc.raster.Raster":{data:[5,4,1,""],dataType:[5,4,1,""],dx:[5,4,1,""],geotrans:[5,4,1,""],get_average:[5,6,1,""],get_central_coors:[5,6,1,""],get_max:[5,6,1,""],get_min:[5,6,1,""],get_std:[5,6,1,""],get_sum:[5,6,1,""],get_type:[5,6,1,""],get_value_by_row_col:[5,6,1,""],get_value_by_xy:[5,6,1,""],nCols:[5,4,1,""],nRows:[5,4,1,""],noDataValue:[5,4,1,""],srs:[5,4,1,""],validValues:[5,4,1,""],validZone:[5,4,1,""],xMax:[5,4,1,""],xMin:[5,4,1,""],yMax:[5,4,1,""],yMin:[5,4,1,""]},"pygeoc.raster.RasterUtilClass":{get_mask_from_raster:[5,2,1,""],get_negative_dem:[5,2,1,""],mask_raster:[5,2,1,""],raster_reclassify:[5,2,1,""],raster_statistics:[5,2,1,""],raster_to_asc:[5,2,1,""],raster_to_gtiff:[5,2,1,""],read_raster:[5,2,1,""],split_raster:[5,2,1,""],write_asc_file:[5,2,1,""],write_gtiff_file:[5,2,1,""]},"pygeoc.utils":{C:[6,1,1,""],DEFAULT_NODATA:[1,5,1,""],DELTA:[1,5,1,""],DateClass:[6,1,1,""],FileClass:[6,1,1,""],MathClass:[6,1,1,""],PI:[1,5,1,""],SQ2:[1,5,1,""],StringClass:[6,1,1,""],UtilClass:[6,1,1,""],ZERO:[1,5,1,""],get_config_file:[6,3,1,""],get_config_parser:[6,3,1,""]},"pygeoc.utils.DateClass":{day_of_month:[6,2,1,""],day_of_year:[6,2,1,""],is_leapyear:[6,2,1,""]},"pygeoc.utils.FileClass":{add_postfix:[6,2,1,""],check_file_exists:[6,2,1,""],copy_files:[6,2,1,""],get_core_name_without_suffix:[6,2,1,""],get_executable_fullpath:[6,2,1,""],get_filename_by_suffixes:[6,2,1,""],get_full_filename_by_suffixes:[6,2,1,""],is_dir_exists:[6,2,1,""],is_file_exists:[6,2,1,""],is_up_to_date:[6,2,1,""],remove_files:[6,2,1,""]},"pygeoc.utils.MathClass":{floatequal:[6,2,1,""],isnumerical:[6,2,1,""],nashcoef:[6,2,1,""],pbias:[6,2,1,""],rmse:[6,2,1,""],rsquare:[6,2,1,""],rsr:[6,2,1,""]},"pygeoc.utils.StringClass":{convert_unicode2str:[6,2,1,""],convert_unicode2str_num:[6,2,1,""],extract_numeric_values_from_string:[6,2,1,""],get_datetime:[6,2,1,""],is_substring:[6,2,1,""],is_valid_ip_addr:[6,2,1,""],split_string:[6,2,1,""],string_in_list:[6,2,1,""],string_match:[6,2,1,""],strip_string:[6,2,1,""]},"pygeoc.utils.UtilClass":{current_path:[6,2,1,""],decode_strs_in_dict:[6,2,1,""],error:[6,2,1,""],mkdir:[6,2,1,""],print_msg:[6,2,1,""],rmmkdir:[6,2,1,""],run_command:[6,2,1,""],writelog:[6,2,1,""]},"pygeoc.vector":{VectorUtilClass:[7,1,1,""]},"pygeoc.vector.VectorUtilClass":{convert2geojson:[7,2,1,""],raster2shp:[7,2,1,""],write_line_shp:[7,2,1,""]},pygeoc:{TauDEM:[2,0,0,"-"],hydro:[3,0,0,"-"],postTauDEM:[4,0,0,"-"],raster:[5,0,0,"-"],utils:[6,0,0,"-"],vector:[7,0,0,"-"]}},objnames:{"0":["py","module","Python \u6a21\u5757"],"1":["py","class","Python \u7c7b"],"2":["py","staticmethod","Python \u9759\u6001\u65b9\u6cd5"],"3":["py","function","Python \u51fd\u6570"],"4":["py","attribute","Python \u5c5e\u6027"],"5":["py","data","Python \u6570\u636e"],"6":["py","method","Python \u65b9\u6cd5"]},objtypes:{"0":"py:module","1":"py:class","2":"py:staticmethod","3":"py:function","4":"py:attribute","5":"py:data","6":"py:method"},terms:{"03e":6,"2e9":6,"4e2":6,"99db":6,"\u5168\u5c40\u53d8\u91cf":9,"\u53c2\u6570":[2,5,6],"\u53c2\u8003":9,"\u5982\u53e6\u5b58\u4e3aasc\u683c\u5f0f\u6805\u683c":5,"\u5b50\u6a21\u5757":9,"\u5b89\u88c5pygeoc":9,"\u5f00\u59cb\u4f7f\u7528pygeoc":9,"\u63cf\u8ff0":1,"\u641c\u7d22\u9875\u9762":0,"\u6570\u503c\u5e38\u91cf":1,"\u6805\u683c\u91cd\u5206\u7c7b\u7b49":5,"\u6839\u53f72":1,"\u6a21\u5757\u7d22\u5f15":0,"\u6ce8\u91ca\u98ce\u683c":1,"\u6d6e\u70b9\u6570\u76f8\u7b49\u5224\u65ad":1,"\u7528\u4e8e\u521b\u5efa\u6805\u683c\u6570\u636e\u5bf9\u8c61\u5e76\u8fdb\u884c\u7b80\u5355\u64cd\u4f5c":5,"\u7d22\u5f15":9,"\u8be5\u6587\u6863\u7531sphinx\u4ece\u6e90\u7801\u4e2d\u81ea\u52a8\u63d0\u53d6\u751f\u6210":1,"\u8bf7\u6839\u636e\u5982\u4e0b\u547d\u4ee4\u5b89\u88c5\u6700\u65b0\u5f00\u53d1\u7248\u672c":8,"\u8fd4\u56de":[2,4,5,6],"\u8fd4\u56de\u7c7b\u578b":[4,6],"\u96f6\u503c":1,"\u9ed8\u8ba4nodata\u503c":1,"boolean":5,"case":6,"class":[2,3,4,5,6,7],"default":[3,5,6],"export":7,"float":[1,5,6],"function":[2,3,4,5,6,7],"gdal\u6570\u636e\u7c7b\u578b":1,"import":5,"int":5,"pygeoc\u5904\u5728\u4e0d\u65ad\u5f00\u53d1\u5b8c\u5584\u4e2d":8,"pygeoc\u610f\u4e3a\u7528python\u8fdb\u884c\u5730\u5b66\u8ba1\u7b97":9,"pygeoc\u91c7\u7528":1,"return":[2,4,6],"static":[2,3,4,5,6,7],"throw":6,"true":[2,6],The:[2,4,5],acc:2,accord:[2,3,4],accumul:2,ad8:2,add:[5,6],add_postfix:6,address:6,after:2,age:6,alg:3,algorithm:3,all:[2,6],analysi:2,ang:2,angfil:2,angl:4,ani:2,anoth:3,api:9,approach:2,arcgi:[3,4],area8:6,area:2,aread8:2,areadinf:2,argv:6,arrai:[5,6],asc_f:5,ascii:5,assign:4,assign_stream_id_rast:4,author:[2,3,4,5,6,7],avail:[2,3],ave:2,averag:5,base:[2,3,4,5,6,7],basedatetim:6,basic:[5,6],begin:6,bin:2,bin_dir:2,bit:1,boundari:5,calcul:6,call:[2,6],cannot:6,capit:6,ccw_dcol:3,ccw_drow:3,cell:[3,5],central:5,chang:5,change_gdal_typ:5,change_nodata:5,changlog:[2,3,4,5,6,7],charact:6,chcoord:2,check:[2,3,4,5,6,7],check_file_exist:6,check_orthogon:4,chnetwork:2,chri:2,classifi:5,clone:8,cluster:2,code:[1,3,4,5],coeffici:6,col:[4,5],column:5,com:[6,8],command:[2,6],common:[2,5,6],compar:6,compdinffil:4,complex:1,compress:4,compress_dinf:4,concaten:6,config:6,configur:6,connectdown:2,constant:3,contain:6,contentlist:6,contribut:2,convert2geojson:7,convert:[2,3,5,6,7],convert_cod:3,convert_unicode2str:6,convert_unicode2str_num:6,convertdistmethod:2,convertstatsmethod:2,coordin:[3,4,5],copi:6,copy_fil:6,core:6,correspond:4,could:6,count:5,crash:6,current:[3,4,6],current_path:6,d8_delta:3,d8_dir:3,d8_down_method:2,d8_inflow:3,d8_inflow_ag:3,d8_inflow_td:3,d8_inflow_wb:3,d8_len:3,d8anglelist:3,d8delta_ag:3,d8delta_td:3,d8delta_wb:3,d8dir_ag:3,d8dir_td:3,d8dir_wb:3,d8distdowntostream:2,d8flowdir:2,d8len_ag:3,d8len_td:3,d8len_wb:3,d8util:3,dai:6,data:[5,7],datatyp:[3,5],dateclass:6,datetim:6,day_of_month:6,day_of_year:6,decod:6,decode_strs_in_dict:6,default_nodata:1,delet:6,delin:2,delta:1,dem:[2,5,6],dem_fil:6,destin:5,detect:2,deviat:5,dict:[2,3,5,6],dictionari:6,differ:[3,6],dinf:[2,4],dinf_downslope_direct:4,dinfdir_valu:4,dinfdistdown:2,dinfflowang:4,dinfflowdir:2,dinfutil:4,dir_path:6,dir_src:6,dir_valu:3,direct:[2,3,4],directori:[5,6],dirnam:2,dirpath:6,dist:2,distanc:2,distancemethod:2,distm:2,docstr:1,doe:2,dougla:2,down:2,downslop:[3,4],downstream:4,downstream_index:3,downstream_index_dinf:4,drop:2,dropanalysi:2,drp:2,dst_sr:7,dstfile:5,dstfilenam:6,dta:6,earlier:2,edgecontaimin:2,edgecontamin:2,eight:1,elim_empti:6,elimin:[4,6],els:6,empti:6,encod:4,end:6,equal:6,error:[2,6],esri:[4,5,6,7],etc:6,exampl:[5,6],except:6,exclud:5,execut:[2,6],exedir:2,exist:[2,6],extern:6,extract:[2,6],extract_numeric_values_from_str:6,f_name:5,fals:[2,5,6],featur:7,fel:2,field:5,field_nam:5,fieldnam:7,file:[2,3,4,5,6,7],file_path:6,fileclass:6,filenam:[5,6],fill:[2,6],filleddem:2,find:[3,4,6],first:4,flag:2,float32:1,float64:1,floatequ:6,flood:2,flow:[2,3,4],flow_model:3,flowangl:2,flowdir:2,flowdirectioncod:3,flowmodelconst:3,folder:6,format:[5,6],formatted_str:6,four:1,from:[3,5,6],full:[2,6],fullpath:2,function_nam:2,gat:[3,5],gdal:5,gdal_typ:5,gdaldatatyp:[1,5],gdaltyp:5,gdt_byte:1,gdt_cfloat32:1,gdt_cfloat64:1,gdt_cint16:1,gdt_cint32:1,gdt_float32:[1,5],gdt_float64:1,gdt_int16:1,gdt_int32:1,gdt_uint16:1,gdt_uint32:1,gdt_unknown:1,gener:5,geograph:5,geojson:7,georg:2,geotif:5,geotiff:5,geotran:5,geotransform:5,get:[3,4,5,6],get_averag:5,get_cell_length:3,get_cell_shift:3,get_central_coor:5,get_config_fil:6,get_config_pars:6,get_core_name_without_suffix:6,get_datetim:6,get_executable_fullpath:6,get_filename_by_suffix:6,get_full_filename_by_suffix:6,get_mask_from_rast:5,get_max:5,get_min:5,get_negative_dem:5,get_std:5,get_sum:5,get_typ:5,get_value_by_row_col:5,get_value_by_xi:5,git:8,github:8,given:[2,4,5,6],googl:[1,2,3,4,5,6,7],gordfil:2,grid:5,gridnet:2,gtiff:5,handl:[5,6,7],home:[2,6],hostfil:2,how:6,http:[6,8],hydro:1,hydrolog:3,identifi:[2,5],in_alg:3,in_fil:[2,3],in_param:2,in_rast:5,includ:2,indent:6,index:6,induc:3,inf:[2,4],input:[2,3,4,5,6],insensit:6,instal:8,instanc:5,int16:1,int32:1,integ:[1,6],invalid:5,is_dir_exist:6,is_file_exist:6,is_leapyear:6,is_substr:6,is_up_to_d:6,is_valid_ip_addr:6,isnumer:6,jamaica_dem:5,jsonfil:7,kei:6,largest:2,last:2,layernam:7,leap:6,left:5,length:[3,4],level:6,liangjun:[2,3,4,5,6,7],line:[2,6,7],line_list:7,link:4,list1:6,list2:6,list:[2,5,6],locat:2,log:[2,6],log_fil:2,log_param:2,logfil:[2,6],logspac:2,lower:5,lrei:6,lreis2415:8,mai:6,make:6,map:4,mask:5,mask_rast:5,math:6,mathclass:6,max:[2,5],maximum:5,maxthresh:2,mean:5,messag:[2,6],method:2,method_str:2,min:[2,5],minimum:5,minthresh:2,mkdir:6,mode:6,model:[3,6],modifi:2,modifiedoutlet:2,modul:1,month:6,move:2,moveoutletstostrm:2,mpi:2,mpi_bin:2,mpi_param:2,mpiexedir:2,mpipath:2,msg:[2,6],n_col:5,n_row:5,name:[2,5,6],namecfg:2,nash:6,nashcoef:6,ncol:5,neg:5,neg_dem:5,net:4,network:4,newli:4,nodata:[4,5],nodata_flow:5,nodata_valu:5,nodatavalu:5,node:2,none:[2,3,5,6,7],nrow:5,nse:6,number:[5,6],numer:6,numpi:5,numthresh:2,object:[2,3,4,5,6,7],observ:6,obsvalu:6,older:6,one:3,open:2,optim:2,option:2,origin:[2,4,5,6,7],osgeo:5,osr:5,other:6,otherwis:2,out_alg:3,out_fil:[2,3],out_rast:5,out_shp:7,out_stream_fil:4,outfil:6,outlet:2,outlet_fil:2,outmaskfil:5,output:[2,3,4,5,6],output_compressed_dinf:4,output_reach_fil:4,pair:[2,4],param:[3,4,6],paramet:2,parser:6,part:6,path:[2,3,5,6],pbia:6,percentag:6,peuker:2,peukerdougla:2,pfile:2,pit:2,plenfil:2,point:1,post:4,postfix:6,posttaudem:1,predefin:2,print:[2,5],print_msg:6,process:4,pygeoc:[1,8],pylint:[2,3,4,5,6,7],python:[6,8],qswat:2,question:6,rais:[2,5,6],raster2shp:7,raster:[1,2,3,4,7],raster_f:5,raster_fil:5,raster_reclassifi:5,raster_statist:5,raster_to_asc:5,raster_to_gtiff:5,rasterfil:[5,7],rasterutilclass:5,raw_dem:5,reach:4,read:[2,5],read_rast:5,reclassifi:5,recurs:6,refer:[5,6],reformat:[2,3,4,5,6,7],regardless:6,relat:[3,6,7],remov:[2,6],remove_fil:6,reorgan:[2,4,5,6,7],replac:6,requir:2,result:2,right:5,rmmkdir:6,rmse:6,root:6,row:[4,5],rsquar:6,rsr:6,rst_file:5,rst_obj:5,rubric:6,run:2,run_command:6,run_test:2,runtim:2,runtimeerror:[2,6],same:[3,6],sca:2,serial:4,serialize_streamnet:4,set:2,setup:8,shapefil:[4,5,6,7],shift:3,sign:1,simul:6,simvalu:6,singl:6,singlebasin:2,sixteen:1,sixti:1,size:5,slope:2,slp:2,soft:2,softwar:2,sourc:[2,5,6],space:6,spatial:5,spatialrefer:5,spilt:5,split:[5,6],split_rast:5,split_shp:5,split_str:6,spliter:6,sq2:1,squar:6,src:2,src_file:7,src_sr:7,srcfile:5,srs:5,ssa:2,stackoverflow:6,standard:5,statist:[2,5],statsm:2,std:5,store:5,str1:6,str2:6,str_contains_valu:6,str_src:6,stream:[2,4],stream_fil:4,stream_rast:2,streamnet:2,streamnet_fil:4,streamnetutil:4,streamord:2,streamrast:2,streamskeleton:2,string:[2,6],string_in_list:6,string_match:6,stringclass:6,strip_str:6,strlist:6,style:[2,3,4,5,6,7],sub:6,subbasin:[2,4],subbasin_fil:4,subprocess:6,substr:6,successfulli:2,suffix:6,sum:5,support:3,system:5,tau_dir:2,taudem:[1,3,4,6],taudemfilesutil:2,taudemworkflow:2,temp_dir:5,test:[2,5,6],than:[2,6],thank:2,thirti:1,thresh:2,threshold:2,tif:[5,6],tlenfil:2,tmp_str:6,transform:5,two:[1,6],txt:[2,6],type:[1,5],unicod:6,unicode_dict:6,unicode_str:6,unknown:1,unsign:1,unspecifi:1,upper:5,usag:5,use:3,used:[2,5,6],user:2,user_fmt:6,using:2,util:[1,2,3,4,5,7],utilclass:6,v_dict:5,valid:6,validvalu:5,validzon:5,valu:[2,4,5,6],valueerror:5,vector:1,vectorshp:7,vectorutilclass:7,version:[2,4,5,6,7],want:6,watersh:2,watershed_delin:2,weight:4,weightfil:4,were:2,which:6,whitebox:[3,5],window:6,without:[2,6],workflow:2,workingdir:2,write:6,write_asc_fil:5,write_gtiff_fil:5,write_line_shp:7,writelog:6,xmax:5,xmin:5,xsize:5,year:6,ymax:5,ymin:5,ysize:5,zero:[1,4],zhu:[2,3,4,5,6,7],zhulj:6,zhuljigsnrrlrei:6},titles:["API \u7d22\u5f15","API \u53c2\u8003","pygeoc.TauDEM module","pygeoc.hydro module","pygeoc.postTauDEM module","pygeoc.raster module","pygeoc.utils module","pygeoc.vector module","\u5f00\u59cb\u4f7f\u7528PyGeoC","\u7528\u6237\u624b\u518c"],titleterms:{"\u5168\u5c40\u53d8\u91cf":1,"\u53c2\u8003":1,"\u5b50\u6a21\u5757":1,"\u5b89\u88c5pygeoc":8,"\u5f00\u53d1\u6587\u6863":9,"\u5f00\u59cb\u4f7f\u7528pygeoc":8,"\u7528\u6237\u624b\u518c":9,"\u7d22\u5f15":0,api:[0,1],hydro:3,modul:[2,3,4,5,6,7],posttaudem:4,pygeoc:[2,3,4,5,6,7],raster:5,taudem:2,util:6,vector:7}})