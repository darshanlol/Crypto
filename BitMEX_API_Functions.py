
def cancel_bit(ordid):
    verb="DELETE"
    nonce= str(generate_nonce())

    path='/api/v1/order'
    data='orderID=' + ordid
    c= generate_signature(bit_api_secret,verb,path,nonce,data)

    a=requests.delete('https://www.bitmex.com/api/v1/order',headers={'api-nonce':nonce,'api-key':bit_api_key,'api-signature':c},data={'orderID':ordid})
    vv=json.loads(a.content)[0]
    pprint(vv)
    cumqty = vv['simpleCumQty']
    leaveqty = vv['leavesQty']
    kleaveqty = vv['simpleLeavesQty']
    busdqty = vv['cumQty']
    return cumqty, leaveqty, busdqty, kleaveqty



def see_bit(count, symbol):
    verb="GET"
    nonce= str(generate_nonce())

    path='/api/v1/order'
    data='symbol='+symbol+'&reverse=true&count='+str(count)
    c= generate_signature(bit_api_secret,verb,path,nonce,data)

    a=requests.get('https://www.bitmex.com/api/v1/order',headers={'api-nonce':nonce,'api-key':bit_api_key,'api-signature':c},data={'symbol':symbol,'reverse':'true','count':str(count)})
    vvv=json.loads(a.content)
    pprint(vvv)
    
    return vvv[0]['simpleCumQty']

def get_balance():
 

    verb="GET"
    nonce= str(generate_nonce())

    path='/api/v1/user/margin'
    data=''
    c= generate_signature(bit_api_secret,verb,path,nonce,data)
    with concurrent.futures.ThreadPoolExecutor(2) as poolbal:
        bitMEX = poolbal.submit(requests.get, 'https://www.bitmex.com/api/v1/user/margin' ,headers={'api-nonce':nonce,'api-key':bit_api_key,'api-signature':c})
        
        
    bitmex_balance_btc= float((json.loads(bitMEX.result().content)['availableMargin'])) / 100000000
    print (bitmex_balance_btc)
    
    return  bitmex_balance_btc  


def trade_bit(quantity,price,symbol):
    
    verb="POST"
    price = round(price * 2) / 2
    nonce= str(generate_nonce())

    path = '/api/v1/order'
    data = "symbol="+symbol+"&simpleOrderQty="+str(quantity)+"&ordType=Limit&price=" + str(price)+"&execInst=ParticipateDoNotInitiate"
    

    print (data)
    c = generate_signature(bit_api_secret,verb,path,nonce,data)

    page=requests.post('https://www.bitmex.com/api/v1/order',headers={'api-nonce':nonce,'api-key':bit_api_key,'api-signature':c}, data = {'symbol':symbol,'simpleOrderQty':str(quantity),'ordType':'Limit','price':str(price),'execInst':'ParticipateDoNotInitiate'})
    
    
    qtyqty=json.loads(page.content)
    pprint(qtyqty)
    return qtyqty['simpleCumQty'], qtyqty['orderID']



def trade_bit_usd(quantity,price,symbol):
    
    verb="POST"
    nonce= str(generate_nonce())
    price = round(price * 2) / 2


    path = '/api/v1/order'
    data = "symbol="+symbol+"&orderQty="+str(quantity)+"&ordType=Limit&price=" + str(price)+"&execInst=ParticipateDoNotInitiate"
    

    print (data)
    c = generate_signature(bit_api_secret,verb,path,nonce,data)
    

    page=requests.post('https://www.bitmex.com/api/v1/order',headers={'api-nonce':nonce,'api-key':bit_api_key,'api-signature':c}, data = {'symbol':symbol,'orderQty':str(quantity),'ordType':'Limit','price':str(price),'execInst':'ParticipateDoNotInitiate'})
    
    qtyqty=json.loads(page.content)
    
    pprint(qtyqty)
    return qtyqty['simpleCumQty'], qtyqty['orderID']



def close_bit(symbol):
    verb="POST"
    nonce= str(generate_nonce())

    path='/api/v1/order/closePosition'
    data='symbol=' + symbol
    c= generate_signature(bit_api_secret,verb,path,nonce,data)

    a=requests.post('https://www.bitmex.com/api/v1/order/closePosition',headers={'api-nonce':nonce,'api-key':bit_api_key,'api-signature':c},data={'symbol':symbol})
    s= json.loads(a.content)
    pprint(s)
    
    
    return s['simpleCumQty'], s['simpleCumQty'] 
