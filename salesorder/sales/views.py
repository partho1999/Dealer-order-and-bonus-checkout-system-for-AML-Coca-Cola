from django.shortcuts import render
from django.http import HttpResponse
import pandas as pd
import json
from django.views.decorators.csrf import csrf_exempt
from .models import Dealer,Product,Promotion,order,dealer_code
from django.http import JsonResponse
from django.template import loader
from sqlalchemy import create_engine


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
    print("dealer_type:",type(dealer_name))
    data = {
    "dealer_name": [dealer_name],
    
    }

    #load data into a DataFrame object:
    df_dealer_name = pd.DataFrame(data)

    print(df_dealer_name)
    df_dealer_name.to_csv("dealar_name.csv")

    #engine = create_engine('sqlite:///db.sqlite3')

    #df_dealer_name.to_sql(dealer_code._meta.db_table, if_exists='replace', con =engine, index= False)

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
    
    if request.method == 'POST':
        print("i'm if") 
        data = request.POST.dict()
        data.pop('csrfmiddlewaretoken', None)
        print('data:',data)

        data ={x:y for x,y in data.items() if y!='0'}

        id_lst =[]
        value_lst =[]

        for i in data.items():
            id = int(i[0])
            id_lst.append(id)
            value = i[1]
            value_lst.append(value)
        #####################################################################################################################
        
       
        
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
        df_dealer_name = pd.read_csv('../salesorder/dealar_name.csv')
        dealer_name = list(df_dealer_name ['dealer_name'])[0]
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
        engine = create_engine('sqlite:///db.sqlite3')

        df_p_1.to_sql(order._meta.db_table, if_exists='replace', con =engine, index= False)

        sum_balance = df_p_1['balance'].sum()

        pro_amount = df_p_1['tp'] * df_p_1['bonus_qty']
        pro_amount = pro_amount.sum()
        net_total = sum_balance + pro_amount

        data = {
        "sum_balance": [sum_balance],
        "pro_amount": [pro_amount],
        "net_total": [net_total]
        }

        #load data into a DataFrame object:
        df_total_amount = pd.DataFrame(data)

        print(df_total_amount)

        d_order = order.objects.all().values()
        print("save value:",d_order)

        json_records_p = df_total_amount.reset_index().to_json(orient ='records')
        data_Q = []
        data_Q = json.loads(json_records_p)
        data_p = list(d_order)
        # df_total_amount = list(df_total_amount)
        
        
        context = {
        'd': data_p, 
        
        }
        #template = loader.get_template('sales/test_1.html')
        return JsonResponse({'data_p': data_p,'data_Q':data_Q})


# @csrf_exempt
# def test(request):

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
        id=request.POST.get('id','')
        #type=request.POST.get('type','')
        data=request.POST.get('value','')
        #product=Product.objects.get(id=id)
        print(id)
        #print(type)
        print(data)
    #     id_lst =[]
    #     # id =int(id)
    #     id_lst.append(id)
    #     print(id_lst)

    #     value_lst =[]
    #     val=int(data)
    #     value_lst.append(val)
    #     print(value_lst)

        # id_lst =[1]
        # value_lst=[12]

        # valu={
        #         'id':[0],
        #         'value':[0],
        #         }
            
        # new_df = pd.DataFrame(valu)

        # # print(int(new_df['id']))


        # if int(new_df['id']) == 0 and int(new_df['value']) == 0:
        #     print("yea!!")
        #     new_df.loc[new_df['id']== 0, "id"] =id_lst
        #     new_df.loc[new_df['value']== 0, "value"] =value_lst

        # else:
        #     print('no')
        #     valu={
        #         'id':id_lst,
        #         'value':value_lst,
        #         }
            
        #     new_df = pd.DataFrame(valu)


                
        # print(new_df)



        #################################################product info#######################################################
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
        
        
    else:     
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
def test(request):
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
    # json_records_p = df_p_1.reset_index().to_json(orient ='records')
    # data_p = []
    # data_p = json.loads(json_records_p)
    engine = create_engine('sqlite:///db.sqlite3')

    df_p_1.to_sql(order._meta.db_table, if_exists='replace', con =engine, index= False)

    d_order = order.objects.all().values()
    print(d_order)
    


    context = {
        'd': d_order, 
        
    }
    
    return render(request, 'sales/test_1.html', context=context)
    


@csrf_exempt
def test_1(request):

    if request.method == 'POST':
        print("i'm if") 
        data = request.POST.dict()
        data.pop('csrfmiddlewaretoken', None)
        print('data:',data)

        data ={x:y for x,y in data.items() if y!='0'}

        id_lst =[]
        value_lst =[]

        for i in data.items():
            id = int(i[0])
            id_lst.append(id)
            value = i[1]
            value_lst.append(value)
        #####################################################################################################################
        
        #getting input from forms
        # if request.method == "POST":
        #     i=request.POST.get('id','')
        #     type=request.POST.get('type','')
        #     da=request.POST.get('value','')
        #     #product=Product.objects.get(id=id)
        #     print(i)
        #     print(type)
        #     print(da)
       
        
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
        engine = create_engine('sqlite:///db.sqlite3')

        df_p_1.to_sql(order._meta.db_table, if_exists='replace', con =engine, index= False)

        d_order = order.objects.all().values()
        print("save value:",d_order)

        # json_records_p = df_p_1.reset_index().to_json(orient ='records')
        # data_p = []
        # data_p = json.loads(json_records_p)
        data_p = list(d_order)
        
        
        context = {
        'd': data_p, 
        
        }
        #template = loader.get_template('sales/test_1.html')
        return JsonResponse({'data_p': data_p})
        #render(request, 'sales/test_1.html', {'data_p':data_p})
        #return HttpResponse(template,render(context, request))
        #return None
        
    else:    
        print("i'm else") 
        Product_table= Product.objects.all().values()
        #print('Product-db-table:',Product_table)
        df_p = pd.DataFrame(list(Product_table))
        # print(df_p)

        df_p_1= df_p.copy()

        df_p_1['order_qty'] = 0
        df_p_1['bonus_qty'] = 0
        df_p_1['balance'] = 0   


        # print("don't get any post value")
        # json_records_p = df_p_1.reset_index().to_json(orient ='records')
        # data_p = []
        # data_p = json.loads(json_records_p)
        engine = create_engine('sqlite:///db.sqlite3')

        df_p_1.to_sql(order._meta.db_table, if_exists='replace', con =engine, index= False)

        d_order = order.objects.all().values()
        print(d_order)
        


        context = {
            'd': d_order, 
            
        }
        
        return render(request, 'sales/test_1.html', context=context)
        
    

def savetoserver(request):

    print('save func:',df_p_1)

    df_p_1.to_sql('order_table_of'+dealer_name, index_label='id' , if_exists='replace')
    print('saved succecefull..!!')

    return render (request, 'sales/index.html')
