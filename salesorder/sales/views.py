from django.shortcuts import render
from django.http import HttpResponse
import pandas as pd
import json
from django.views.decorators.csrf import csrf_exempt
from .models import Dealer,Product,Promotion
from django.http import JsonResponse

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

 

    
    if dealer_name is not None:
        df_1=df[df['sdp']==dealer_name]
        df_1=df_1.reset_index()        

        json_records_d = df_1.to_json(orient ='records')
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
    # print("----Product table----")
    # print(df_p)
    df_p_1= df_p.copy()

    df_p_1['bonus_qty'] = 0
    df_p_1['order_qty'] = 0
    df_p_1['balance'] = 0
    

    sum_balance = df_p_1['balance'].sum()

    pro_amount = df_p_1['tp'] * df_p_1['bonus_qty']
    pro_amount = pro_amount.sum()
    net_total = sum_balance + pro_amount
    
    
    json_records_p = df_p_1.reset_index().to_json(orient ='records')
    data_p = []
    data_p = json.loads(json_records_p)

        


    context = {
        'net_total' :net_total,
        'pro_amount': pro_amount,
        'sum_balance':sum_balance,
        'd': data_p, 
        'f':data_df,
        'g':data_dt,
        'code':code,
        'cr_limit':cr_limit,
        'balance':balance,
        'territory':territory
    }
    

    return render(request, 'sales/index.html', context=context)


def ordercal(request):
    #getting input from forms
    global df_p_1
    global data_df
    
    if request.method == 'POST':
        data = request.POST.dict()
        data.pop('csrfmiddlewaretoken', None)
        print('data:',data)


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
        df = pd.DataFrame(list(Promotion_table))
        
        # print("----Promotion table----")
        # print(df)
        

        
        if dealer_name is not None:
            df_1=df[df['sdp']==dealer_name]
            df_1=df_1.reset_index()
            

            json_records_d = df_1.reset_index().to_json(orient ='records')
            data_df = []
            data_df = json.loads(json_records_d)
        else:

            json_records_d = df.reset_index().to_json(orient ='records')
            data_df = []
            data_df = json.loads(json_records_d)

     ##################################################product info#######################################################
    

        data ={x:y for x,y in data.items() if y!='0'}

        id_lst =[]
        value_lst =[]

        for i in data.items():
            id = i[0].replace('item_', '')
            id_lst.append(id)
            value = i[1]
            value_lst.append(value)

        
        ##################################################product info#######################################################
        Product_table= Product.objects.all().values()
        #print('Product-db-table:',Product_table)
        df_p = pd.DataFrame(list(Product_table))
        print(df_p)

        df_p_1= df_p.copy()

        df_p_1['order_qty'] = 0
        df_p_1['bonus_qty'] = 0
        df_p_1['balance'] = 0


    
        
        ##################################################promotion info#####################################################
        Promotion_table= Promotion.objects.all().values()
        #print('Promotion-db-table:',Promotion_table)
        df = pd.DataFrame(list(Promotion_table))
        
        # print("----Promotion table----")
        # print(df)
        # dealer_name = dealer_name 
        df_1=df[df['sdp']==dealer_name]

        id_lst = [int(x) for x in id_lst]
        df_p_2 = df_p_1[df_p_1['id'].isin(id_lst)]


        product_code=list(df_p_2['product'])
        # product_code


        dff = df_1[df_1['p_code'].isin(product_code)]
        # dff

        order_qty = [int(x) for x in list(dff['order_qty'])]
        bonus_qty = [int(x) for x in list(dff['bonus_qty'])]
        pro_code =  [x for x in list(dff['p_code'])]
        

        value_lst = [int(x) for x in value_lst]
        df_p_2 = df_p_1[df_p_1['id'].isin(id_lst)]
        tp=df_p_2['tp']

        bnv = [int(num1*num2) for num1, num2 in zip(bonus_qty,value_lst)]
        divition = [int(n1/n2) for n1,n2 in zip(bnv, order_qty)]

        df_p_1.loc[df_p_1['id'].isin(id_lst), "order_qty"] =value_lst
        df_p_1.loc[df_p_1['product'].isin(pro_code), "bonus_qty"] = list(pd.Series(divition))
        df_p_1.loc[df_p_1['id'].isin(id_lst), "balance"] = tp*value_lst
        df_p_1 = df_p_1.fillna(0)
        print(df_p_1)

        sum_balance = df_p_1['balance'].sum()

        pro_amount = df_p_1['tp'] * df_p_1['bonus_qty']
        pro_amount = pro_amount.sum()
        net_total = sum_balance + pro_amount

        json_records_p = df_p_1.reset_index().to_json(orient ='records')
        data_p = []
        data_p = json.loads(json_records_p)
        # print(data_p)
    else:     
        Product_table= Product.objects.all().values()
        #print('Product-db-table:',Product_table)
        df_p = pd.DataFrame(list(Product_table))
        print(df_p)

        df_p_1= df_p.copy()

        df_p_1['order_qty'] = 0
        df_p_1['bonus_qty'] = 0
        df_p_1['balance'] = 0   

        sum_balance = df_p_1['balance'].sum()
        pro_amount = df_p_1['tp'] * df_p_1['bonus_qty']
        pro_amount = pro_amount.sum()
        net_total = sum_balance + pro_amount

        print("don't get any post value")
        json_records_p = df_p_1.reset_index().to_json(orient ='records')
        data_p = []
        data_p = json.loads(json_records_p)
    


    # context = {
    #     'd': data_p, 
        
    # }

    context = {
        'net_total': net_total,
        'pro_amount': pro_amount,
        'sum_balance':sum_balance,
        'd': data_p, 
        'f':data_df,
        'g':data_dt,
        'code':code,
        'cr_limit':cr_limit,
        'balance':balance,
        'territory':territory
    }
    

    return render(request, 'sales/index.html', context=context)

@csrf_exempt
def test(request):

    # if request.method == 'POST':
    #     data = request.POST.dict()
    #     data.pop('csrfmiddlewaretoken', None)
    #     print('data:',data)

    #     data ={x:y for x,y in data.items() if y!='0'}

    #     id_lst =[]
    #     value_lst =[]

    #     for i in data.items():
    #         id = i[0].replace('item_', '')
    #         id_lst.append(id)
    #         value = i[1]
    #         value_lst.append(value)
    ######################################################################################################################
      
    #getting input from forms
    if request.method == "POST":
        # id=request.POST.get('id','')
        # type=request.POST.get('type','')
        data=request.POST.dict()
        #product=Product.objects.get(id=id)
        # print(id)
        # print(type)
        print(data)
        id_lst =[]
        id =int(data['id'])
        id_lst.append(id)

        value_lst =[]
        val=int(data['value'])
        value_lst.append(val)
       
        
        # ##################################################product info#######################################################
        Product_table= Product.objects.all().values()
        #print('Product-db-table:',Product_table)
        df_p = pd.DataFrame(list(Product_table))
        print(df_p)

        df_p_1= df_p.copy()

        df_p_1['order_qty'] = 0
        df_p_1['bonus_qty'] = 0
        df_p_1['balance'] = 0


    
        
        ##################################################promotion info#####################################################
        Promotion_table= Promotion.objects.all().values()
        #print('Promotion-db-table:',Promotion_table)
        df = pd.DataFrame(list(Promotion_table))
        
        # print("----Promotion table----")
        # print(df)
        dealer_name = "db-001"
        df_1=df[df['sdp']==dealer_name]

        id_lst = [int(x) for x in id_lst]
        df_p_2 = df_p_1[df_p_1['id'].isin(id_lst)]


        product_code=list(df_p_2['product'])
        product_code


        dff = df_1[df_1['p_code'].isin(product_code)]
        dff

        order_qty = [int(x) for x in list(dff['order_qty'])]
        bonus_qty = [int(x) for x in list(dff['bonus_qty'])]
        pro_code =  [x for x in list(dff['p_code'])]
        

        value_lst = [int(x) for x in value_lst]
        df_p_2 = df_p_1[df_p_1['id'].isin(id_lst)]
        tp=df_p_2['tp']

        bnv = [int(num1*num2) for num1, num2 in zip(bonus_qty,value_lst)]
        divition = [int(n1/n2) for n1,n2 in zip(bnv, order_qty)]

        df_p_1.loc[df_p_1['id'].isin(id_lst), "order_qty"] =value_lst
        df_p_1.loc[df_p_1['product'].isin(pro_code), "bonus_qty"] = list(pd.Series(divition))
        df_p_1.loc[df_p_1['id'].isin(id_lst), "balance"] = tp*value_lst
        df_p_1 = df_p_1.fillna(0)
        print(df_p_1)
        print(df_p_1)
        json_records_p = df_p_1.reset_index().to_json(orient ='records')
        data_p = []
        data_p = json.loads(json_records_p)
        print(data_p)
        return JsonResponse({'data_p':data_p})
        
        
    # else:     
    Product_table= Product.objects.all().values()
    #print('Product-db-table:',Product_table)
    df_p = pd.DataFrame(list(Product_table))
    # print(df_p)

    df_p_1= df_p.copy()

    df_p_1['order_qty'] = 0
    df_p_1['bonus_qty'] = 0
    df_p_1['balance'] = 0   


    # print("don't get any post value")
    json_records_p = df_p_1.reset_index().to_json(orient ='records')
    data_p = []
    data_p = json.loads(json_records_p)
    


    context = {
        'd': data_p, 
        
    }
    
    # print(context)


    return render(request, 'sales/test.html', context=context)

@csrf_exempt
def test_1(request):

    if request.method == 'POST':
        data = request.POST.dict()
        data.pop('csrfmiddlewaretoken', None)
        print('data:',data)

    #     data ={x:y for x,y in data.items() if y!='0'}

    #     id_lst =[]
    #     value_lst =[]

    #     for i in data.items():
    #         id = i[0].replace('item_', '')
    #         id_lst.append(id)
    #         value = i[1]
    #         value_lst.append(value)
    ######################################################################################################################
      
    #getting input from forms
    # if request.method == "POST":
    #     # id=request.POST.get('id','')
    #     # type=request.POST.get('type','')
    #     data=request.POST.dict()
    #     #product=Product.objects.get(id=id)
    #     print(id)
    #     print(type)
    #     print(data)
       
        
    #     ##################################################product info#######################################################
    #     Product_table= Product.objects.all().values()
    #     #print('Product-db-table:',Product_table)
    #     df_p = pd.DataFrame(list(Product_table))
    #     print(df_p)

    #     df_p_1= df_p.copy()

    #     df_p_1['order_qty'] = 0
    #     df_p_1['bonus_qty'] = 1
    #     df_p_1['balance'] = 123


    
        
        # ##################################################promotion info#####################################################
        # Promotion_table= Promotion.objects.all().values()
        # #print('Promotion-db-table:',Promotion_table)
        # df = pd.DataFrame(list(Promotion_table))
        
        # # print("----Promotion table----")
        # # print(df)
        # dealer_name = "db-001"
        # df_1=df[df['sdp']==dealer_name]

        # id_lst = [int(x) for x in id_lst]
        # df_p_2 = df_p_1[df_p_1['id'].isin(id_lst)]


        # product_code=list(df_p_2['product'])
        # product_code


        # dff = df_1[df_1['p_code'].isin(product_code)]
        # dff

        # order_qty = [int(x) for x in list(dff['order_qty'])]
        # bonus_qty = [int(x) for x in list(dff['bonus_qty'])]
        # pro_code =  [x for x in list(dff['p_code'])]
        

        # value_lst = [int(x) for x in value_lst]
        # df_p_2 = df_p_1[df_p_1['id'].isin(id_lst)]
        # tp=df_p_2['tp']

        # bnv = [int(num1*num2) for num1, num2 in zip(bonus_qty,value_lst)]
        # divition = [int(n1/n2) for n1,n2 in zip(bnv, order_qty)]

        # df_p_1.loc[df_p_1['id'].isin(id_lst), "order_qty"] =value_lst
        # df_p_1.loc[df_p_1['product'].isin(pro_code), "bonus_qty"] = list(pd.Series(divition))
        # df_p_1.loc[df_p_1['id'].isin(id_lst), "balance"] = tp*value_lst
        # df_p_1 = df_p_1.fillna(0)
        # print(df_p_1)
        # print(df_p_1)
        # json_records_p = df_p_1.reset_index().to_json(orient ='records')
        # data_p = []
        # data_p = json.loads(json_records_p)
        # print(data_p)
        # return JsonResponse({'data_p':data_p})
        
        
    # else:     
    Product_table= Product.objects.all().values()
    #print('Product-db-table:',Product_table)
    df_p = pd.DataFrame(list(Product_table))
    # print(df_p)

    df_p_1= df_p.copy()

    df_p_1['order_qty'] = 0
    df_p_1['bonus_qty'] = 0
    df_p_1['balance'] = 0   


    print("don't get any post value")
    json_records_p = df_p_1.reset_index().to_json(orient ='records')
    data_p = []
    data_p = json.loads(json_records_p)
    


    context = {
        'd': data_p, 
        
    }
    
    return render(request, 'sales/test_1.html', context=context)

def savetoserver(request):

    print('save func:',df_p_1)

    df_p_1.to_sql('order_table_of'+dealer_name, index_label='id' , if_exists='replace')
    print('saved succecefull..!!')

    return render (request, 'sales/index.html')
