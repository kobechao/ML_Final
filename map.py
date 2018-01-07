import matplotlib.pyplot as plt
import geopandas as gp
import pandas as pd
import numpy as np
import sys
import chardet


villages_shp = gp.read_file("./TOWN_MOI_1061130.shp")
taipei_crime_shp = villages_shp.query('COUNTYNAME=="%s"' % ( u'臺北市' ))
# print( taipei_crime_shp, type(taipei_crime_shp) )

def main() :

	with open('./map.csv', 'rb') as f:
		result = chardet.detect(f.read())
	raw = pd.read_csv('./map.csv', encoding=result['encoding'])
	distCount_accom = raw.loc[ raw['Catagotry_Num'] == 1][['Catagotry_Num','District','Category_Count_In_Dist']].drop_duplicates()
	distCount_cycle = raw.loc[ raw['Catagotry_Num'] == 2][['Catagotry_Num','District','Category_Count_In_Dist']].drop_duplicates()
	distCount_car 	= raw.loc[ raw['Catagotry_Num'] == 3][['Catagotry_Num','District','Category_Count_In_Dist']].drop_duplicates()

	# print( np.array(distCount_accom['District']), type( distCount_accom['District'] ) )
	assert len( distCount_accom ) == len( distCount_car ) == len( distCount_cycle )
	total = np.zeros( len(distCount_accom) )
	lst = ['accommodation thief', 'cycle thief', 'car thief']
	datas = [ distCount_accom, distCount_cycle, distCount_car ]
	for i in range( len( datas )) :
		total += makeCrimeMap( datas[i], lst[i] )

	total /= total.sum( axis=0 )
	makeTotalMap( total )

	plt.show()



def makeTotalMap( total ) :
	taipei_crime_shp['total_crime_percentage'] = total
	rlt = taipei_crime_shp.plot( cmap = 'BuGn', column = 'total_crime_percentage', edgecolor='black' )
	rlt.set_title( 'Total Result' )


def makeCrimeMap( data, title ) :
	raw_count = np.array( data['Category_Count_In_Dist'] ); raw_count = raw_count / raw_count.sum( axis=0 )
	taipei_crime_shp['crime_percentage'] = raw_count
	# print( raw_count )
	# print( taipei_crime_shp )
	# print( data )
	print( np.array( data['Catagotry_Num'] )[0], type(data['Catagotry_Num']), "NUMMMMM" )

	color = ''
	if np.array( data['Catagotry_Num'] )[0] == 1 :
		color = 'OrRd'
	elif np.array( data['Catagotry_Num'] )[0] == 2 :
		color = 'PuRd'
	elif np.array( data['Catagotry_Num'] )[0] == 3 :
		color = 'BuPu'
	
	rlt = taipei_crime_shp.plot( cmap = color, column = 'crime_percentage', edgecolor='black'  )
	rlt.set_title( title )
	return raw_count


if __name__ == '__main__':
	# testMap()
	main()
