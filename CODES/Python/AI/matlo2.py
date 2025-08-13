import matplotlib.pyplot as plt
sizes = [30, 20, 50]
labels = ['Python', 'Java', 'C++']
colors = ['#ff9999','#66b3ff','#99ff99']

plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%')
plt.title("Programming Language Popularity")
plt.show()
