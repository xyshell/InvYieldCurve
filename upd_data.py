import pandas as pd
import pandas_datareader.data as web
import datetime

# inverted yield curve: 1989, 2000, 2006
# 1990 unemployment; 2001: internet bubble; 2008 subprime mortage
start = datetime.datetime(1980, 1, 1)
end = datetime.datetime.now()
securities = [
    'DGS30', 'DGS20', 'DGS10', 'DGS7', 'DGS5', 'DGS3', 'DGS2', 'DGS1',
    'DGS6MO', 'DGS3MO', 'DGS1MO',
]
securities.reverse()
df = web.DataReader(securities[0], 'fred', start, end)
i = 1
while i < len(securities):
    temp_df = web.DataReader(securities[i], 'fred', start, end)
    df = pd.concat([df, temp_df], axis=1, sort=False)
    i += 1
df = df.dropna(how='all', axis=0)
df.to_csv("YieldCurve.csv")

