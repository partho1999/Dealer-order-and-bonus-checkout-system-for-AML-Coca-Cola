from django.shortcuts import render
from django.http import HttpResponse
import pandas as pd
import json
from .models import Dealer,Product,Promotion

# Create your views here.
def index(request):
    global dealer_name
    #getting input from forms
    
    request.method == "POST"
    
    order_input = (request.POST.get("q"))
    print("Order Qty:",order_input)

    #getting input from dropdown
    dealer_name = request.POST.get('p')
    print("dealer_name:",dealer_name)

    Dealer_table= Dealer.objects.all().values()
    #print('Dealer_table-db-table:',Dealer_table)
    df_d = pd.DataFrame(list(Dealer_table))
    # print("----Dealer table----")
    # print(df_d)


    json_records_d = df_d.reset_index().to_json(orient ='records')
    data_dt = []
    data_dt = json.loads(json_records_d)
    #print('data_dt:',data_dt)


    code = 'None'
    cr_limit = 0
    balance = 0
    territory = 'None'

    if dealer_name is not None:
        df_d=df_d[df_d['code']==dealer_name]
        df_d = df_d.reset_index()

        code= df_d['code'][0]
        cr_limit = df_d['cr_limit'][0]
        balance = df_d['balance'][0]
        territory = df_d['territory'][0]

    ##################################################promotion info#####################################################
    Promotion_table= Promotion.objects.all().values()
    #print('Promotion-db-table:',Promotion_table)
    df= pd.DataFrame(list(Promotion_table))

    # print("----Promotion table----")
    # print(df['bonus_qty'])

    df_1 = df.copy()

   

    territories= df_1["territory"].values.tolist()
    regions= df_1["region"].values.tolist()
    sdp= df_1["sdp"].values.tolist()

    # print('territories',territories)
    # print('regions',regions)
    # print('sdp',sdp)
        
    if "jessore" in territories and "cumilla" in regions and"db-001"in sdp :
        #print("step-1")
        df_1.loc[df_1["territory"] == "jessore", "order_qty"] = '15'
        df_1.loc[df_1["territory"] == "jessore", "bonus_qty"] = '1'  
        
        #print("step-2")
        df_1.loc[df_1["region"] == "cumilla", "order_qty"] = '10' 
        df_1.loc[df_1["region"] == "cumilla", "bonus_qty"] = '1'

        #print("step-3")
        df_1.loc[df_1["sdp"] == "db-001", "order_qty"] = '12'
        df_1.loc[df_1["sdp"] == "db-001", "bonus_qty"] = '2'

    df_2 = pd.concat([df, df_1], axis=0)
    df_2 = df_2.reset_index()

    # print("----Promotion table----")
    # print(df)
    
    if dealer_name is not None:
        df_2=df_2[df_2['sdp']==dealer_name]
        df_2=df_2.reset_index()

        if df_2['order_qty'][0]==df_2['order_qty'][1] and df_2['bonus_qty'][0]==df_2['bonus_qty'][1]:
            df_2=df_2[df_2['sdp']==dealer_name]
            df_2=df_2.head(1)
        else:
            df_2=df_2[df_2['sdp']==dealer_name]
            #df_2=df_2.reset_index()
        

        json_records_d = df_2.to_json(orient ='records')
        data_df = []
        data_df = json.loads(json_records_d)
    else:
        print(df['bonus_qty'])
        json_records_d = df.reset_index().to_json(orient ='records')
        data_df = []
        data_df = json.loads(json_records_d)

    ##################################################product info#######################################################
    Product_table= Product.objects.all().values()
    #print('Product-db-table:',Product_table)
    df_p = pd.DataFrame(list(Product_table))
    # print("----Product table----")
    # print(df_p)
    
    
    json_records_p = df_p.reset_index().to_json(orient ='records')
    data_p = []
    data_p = json.loads(json_records_p)

    disc= 0
    bonus =0
    net_total=0
        


    context = {
        'd': data_p, 
        'f':data_df,
        'g':data_dt,
        'disc':disc,
        'bonus':bonus,
        'net_total':net_total,
        'code':code,
        'cr_limit':cr_limit,
        'balance':balance,
        'territory':territory
    }
    

    return render(request, 'sales/index.html', context=context)


def ordercal(request):
    #getting input from forms
    
    request.method == "POST"
    
    order_input = (request.POST.get("q"))
    print("Order Qty:",order_input)

    #getting input from dropdown
    # dealer_name = request.POST.get('p')
    # print("dealer_name:",dealer_name)
    # dealer_name = 'db-001'

    Dealer_table= Dealer.objects.all().values()
    #print('Dealer_table-db-table:',Dealer_table)
    df_d = pd.DataFrame(list(Dealer_table))
    # print("----Dealer table----")
    # print(df_d)

    # # initialize data of lists.
    # data = {'code': ['db-001', 'db-002', 'db-003', 'db-004','db-005'],
    #         'name': ['partho_enterprise', "shafie_traders", 'pranto_enterprise', "sofi_traders","khan_enterprise"],
    #         'cr_limit': [800000, 1000000, 800000, 1000000,500000],
    #         'balance': [550000, 6000000, 550000, 6000000,500000],
    #         'territory': ['khulna base-1', 'gournodi', 'nohakhali', 'ctg base-1','jessore']
    #         }
  
    # # Create DataFrame
    # df_d = pd.DataFrame(data)
    
    # # Print the output.
    # #print("----Dealer table----")
    # #df.head(5)
    # #print(df_d)

    json_records_d = df_d.reset_index().to_json(orient ='records')
    data_dt = []
    data_dt = json.loads(json_records_d)
    #print('data_dt:',data_dt)


    code = 'None'
    cr_limit = 0
    balance = 0
    territory = 'None'

    if dealer_name is not None:
        df_d=df_d[df_d['code']==dealer_name]
        df_d = df_d.reset_index()

        code= df_d['code'][0]
        cr_limit = df_d['cr_limit'][0]
        balance = df_d['balance'][0]
        territory = df_d['territory'][0]

    ##################################################promotion info#####################################################
    Promotion_table= Promotion.objects.all().values()
    #print('Promotion-db-table:',Promotion_table)
    df = pd.DataFrame(list(Promotion_table))
    df_1 = df.copy()
    # print("----Promotion table----")
    # print(df)
    

    territories= df_1["territory"].values.tolist()
    regions= df_1["region"].values.tolist()
    sdp= df_1["sdp"].values.tolist()
        
    if "jessore" in territories and "cumilla" in regions and"db-001"in sdp :
        #print("step-1")
        df_1.loc[df_1["territory"] == "jessore", "order_qty"] = '15'
        df_1.loc[df_1["territory"] == "jessore", "bonus_qty"] = '1'  
        
        #print("step-2")
        df_1.loc[df_1["region"] == "cumilla", "order_qty"] = '10' 
        df_1.loc[df_1["region"] == "cumilla", "bonus_qty"] = '1'

        #print("step-3")
        df_1.loc[df_1["sdp"] == "db-001", "order_qty"] = '12'
        df_1.loc[df_1["sdp"] == "db-001", "bonus_qty"] = '2'

       

    # print("----Promotion table----")
    # print(df)
    df_2 = pd.concat([df, df_1], axis=0)
    df_2 = df_2.reset_index()

    
    if dealer_name is not None:
        df_2=df_2[df_2['sdp']==dealer_name]
        df_2=df_2.reset_index()
        
        if df_2['order_qty'][0]==df_2['order_qty'][1] and df_2['bonus_qty'][0]==df_2['bonus_qty'][1]:
            df_2=df_2[df_2['sdp']==dealer_name]
            df_2=df_2.head(1)
        else:
            df_2=df_2[df_2['sdp']==dealer_name]
            #df_2=df_2.reset_index()

        json_records_d = df_2.reset_index().to_json(orient ='records')
        data_df = []
        data_df = json.loads(json_records_d)
    else:

        json_records_d = df.reset_index().to_json(orient ='records')
        data_df = []
        data_df = json.loads(json_records_d)

    ##################################################product info#######################################################
    Product_table= Product.objects.all().values()
    #print('Product-db-table:',Product_table)
    df_p = pd.DataFrame(list(Product_table))

    Promotion_table= Promotion.objects.all().values()
    #print('Promotion-db-table:',Promotion_table)
    df = pd.DataFrame(list(Promotion_table))
    
 
    bonus_lst =[]
    order_qty_lst=[]

    b=df['bonus_qty']
    for a in range(df['bonus_qty'],1000,12):
        b +=1
        bonus_lst.append(b)
        order_qty_lst.append(a)

    df_o = pd.DataFrame(list(zip(order_qty_lst, bonus_lst)),
               columns =['order_qty', 'bonus_qty'])

    print(df_o)
    
    if order_input is None:
        json_records_p = df_p.reset_index().to_json(orient ='records')
        data_p = []
        data_p = json.loads(json_records_p)

        disc= 0
        bonus =0
        net_total=0
    
    # elif int(order_input) in df['order_qty']:
    #     json_records_p = df_p.reset_index().to_json(orient ='records')
    #     data_p = []
    #     data_p = json.loads(json_records_p)

    #     df=df[df['order_qty']==int(order_input)]
    #     df = df.reset_index()
    #     #print(df)
    #     bonus= int(df['bonus_qty'])
    #     disc= 0
    #     net_total=24000
    elif int(order_input) in list(df_o['order_qty']):
        print('in condition')
        json_records_p = df_p.reset_index().to_json(orient ='records')
        data_p = []
        data_p = json.loads(json_records_p)
        
        #print(int(order_input))
        df_o=df_o[df_o['order_qty']==int(order_input)]
        df_o = df_o.reset_index()
        #print(df)
        bonus= int(df_o['bonus_qty'])
        #print(bonus)
        disc= 0
        price=df_p['tp']
        # print(price)
        net_total= list(price*int(order_input))
        # df_net_total = pd.DataFrame(net_total_lst, columns =['balance'])



        # net_total = df_net_total['balance']
        # net_total = str(net_total.values)
        # print(net_total)

        # for item in net_total_lst:
        #     net_total = item
        #print(net_total)
        #net_total=24000

    else:
        json_records_p = df_p.reset_index().to_json(orient ='records')
        data_p = []
        data_p = json.loads(json_records_p)
        
        

         

        disc= 0
        bonus =2
        net_total=24000

        


    


    context = {
        'd': data_p, 
        'f':data_df,
        'g':data_dt,
        'disc':disc,
        'bonus':bonus,
        'net_total':net_total,
        'code':code,
        'cr_limit':cr_limit,
        'balance':balance,
        'territory':territory
    }
    

    return render(request, 'sales/index.html', context=context)


