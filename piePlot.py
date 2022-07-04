from matplotlib import pyplot as plt
from topUsers import sort_users
def create_graph():
  plt.figure(figsize=(14,14))
  plt.style.use("fivethirtyeight")
  table = sort_users()
  slices = [int(table[0][1]),int(table[1][1]),int(table[2][1]),int(table[3][1]),int(table[4][1])]
  labels = [table[0][0],table[1][0],table[2][0],table[3][0],table[4][0]]
  colors = ['#64C2A6', '#FDBB2F', '#377B2B','#7AC142','#007CC3']
  text = {'size': 35, 'color': 'black'}
  wedgeprops = {'linewidth': 1.5, 'edgecolor': 'white'}
  
  plt.pie(slices, labels=labels, colors=colors, autopct=lambda p: '{:.0f}'.format(p * sum(slices) / 100), startangle=90, explode=[0.1, 0, 0, 0,0], shadow=True, wedgeprops=wedgeprops, textprops=text)
  
  plt.title("Top 5 Uploader Que Mais Enviaram Memes pelo MemedroidBot",fontsize=40,fontweight='bold')
  plt.tight_layout()
  plt.savefig("topUsersPieChart.png", transparent=False, dpi=299)

create_graph()