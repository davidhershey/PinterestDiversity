import pandas
import graphistry
# graphistry.register(key='YOUR_API_KEY_HERE')


links = pandas.read_csv('../graphs/firstMillionGraph.csv')
plotter = graphistry.bind(source="source", destination="target")
plotter.plot(links)
