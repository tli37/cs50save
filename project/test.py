import plotly.express as px
import datetime as dt



#date = ['2020-09-20', '2020-09-20', '2020-09-20', '2020-09-20', '2020-09-20', '2020-09-26', '2020-09-26', '2020-09-26']
#svolume= [1050, 1050, 1050, 1050, 0, 1050, 70, 0]

#dates = [dt.datetime.strptime(d,'%Y-%m-%d').date() for d in date]

#fig = px.line(x= dates, y= svolume, title="testing")
#print(fig)
#fig.show()


x=["a","b","c"]
y=[1,3,2]

fig = px.line(x=x, y=y, title="sample figure")
print(fig)
fig.show()