from flask import Flask, request
import plotly.graph_objects as go
import pandas as pd
import datetime
import investpy
import requests
import json
from model_storage import Storage

s = Storage()

def getStock(stock, country, year):
  stock = investpy.get_stock_historical_data(stock = stock,
                                        country = country,
                                        from_date=str('01/01/{}'.format(year)),
                                        to_date=str('30/12/{}'.format(year)))
  df = pd.DataFrame(stock)  
  return df
  
def createGraphic(df):
  fig = go.Figure()

  fig.add_trace(go.Scatter(x = df.index, y = df.Close, 
                      mode='lines',
                      name='Fechamento',
                      marker_color = '#D62728',))
  
  fig.update_layout(
      title='Histórico de Preço', 
      titlefont_size = 28,           
      xaxis = dict( 
          title='Período Histórico', 
          titlefont_size=16, 
          tickfont_size=14), 
      height = 500, 
      yaxis=dict(
          title='Preço em {}'.format(df['Currency'].iloc[0]), 
          titlefont_size=16, 
          tickfont_size=14),       
      legend=dict(
          y=1, x=1,
          bgcolor='rgba(255, 255, 255, 0)',
          bordercolor='rgba(255, 255, 255, 0)')) 
  
  return fig.to_image(format="png", width=600, height=350, scale=2)

def convertCash(close, date, br_to_usd = True):
  mes = str(date).split('-')[1]  
  #caso mes já pesquisado
  if s.mounth == mes:   
      if br_to_usd:
        value = float(close)/float(s.valueCambio)
      else:
        value = float(close)*float(s.valueCambio)
      return value

  response = requests.get('https://economia.awesomeapi.com.br/json/daily/USD-BRL/?start_date=2018{}01&end_date=2018{}27'.format(mes, mes))
  r = response.json()
  
  value = r[0]['bid']   
  s.valueCambio = value
  s.mounth = mes
  if br_to_usd:
    value = float(close)/float(value)
  else:
    value = float(close)*float(value)
  return value

app = Flask(__name__)

@app.route('/', methods=['GET'])
def get():
  return 'API investimento funcionando {}'.format(datetime.datetime.date())

@app.route("/getStock", methods=['POST'])
def consulta():
  try:  
    params = request.get_json()        
    if not (params['pais']  == 'United States' or 'BRAZIL'):
      raise Exception('Pais não permitido para consulta')

    df = getStock(params['acao'], params['pais'], params['ano'])  

    image = None
    if params['moeda'] == 'USD' and params['pais'] == 'BRAZIL':  
      df['Close'] = df.apply(lambda x: convertCash(x.Close, x.Date), axis = 1)
      image = createGraphic(df)
    elif params['moeda'] == 'BR' and params['pais'] == 'BRAZIL':              
      image = createGraphic(df)
    elif params['moeda'] == 'BR' and params['pais'] == 'EUA':
      df['Close'] = df.apply(lambda x: convertCash(x.Close, x.Date, False), axis = 1)
      image = createGraphic(df)
    elif params['moeda'] == 'USD' and params['pais'] == 'EUA':
      image = createGraphic(df)
    else:
      raise Exception('Parametros incorretos para consulta')

    result = {}
    result['processo'] = True
    result['msg'] = 'Gráfico ação ({}) do {} em moeda () buscada com sucesso!'.format(params['acao'], params['pais'], params['moeda'])
    result['grafico_base64'] = image
    
    return json.dumps(result, indent=1, ensure_ascii=False).encode('utf8'), 200
  except Exception as e:
    return 'Error: ' + str(e), 400

if __name__ == '__main__':
  app.run(host='127.0.0.1', port=3030)
  print('Rodando...')