import os
import pandas as pd
import scipy.integrate as integrate
import numpy as np

class PostProcess:
    def __init__(self):
        self.name_files = ''
        self.data = {}
        self.rebuild_data = {}
        self.newData = {}

    def load_csv_file(self, name_file, dir=os.getcwd(), key='1'):
        filePath = os.path.join(dir, name_file)
        self.data[key] = pd.read_csv(filePath)
        return self.data[key]

    def rebuildDataRun(self, key, data=None, values=['U:0'], columns=['Points:2'], index=['Points:0', 'Points:1'],
                       methodFill='bfill'):

        if data == None:
            self.rebuild_data[key] = pd.pivot_table(self.data[key], values=values, columns=columns,
                           index=index).fillna(method=methodFill)
        else:
            self.rebuild_data[key] = pd.pivot_table(data[key], values=values, columns=columns,
                           index=index).fillna(method=methodFill)
        dataNew = {}
        for value in values:
            dataNew[value] = dict()
            dataNew[value]['value'] = dict()
            dataNew[value]['xnew'] = self.rebuild_data[key].index.levels[0].values
            dataNew[value]['ynew'] = dict()
            dataNew[value]['znew'] = dict()

            for xi in dataNew[value]['xnew']:
                dataNew[value]['value'][xi] = self.rebuild_data[key][value].xs(xi, level='Points:0').values
                dataNew[value]['ynew'][xi] = self.rebuild_data[key][value].xs(xi, level='Points:0').axes[0].values
                dataNew[value]['znew'][xi] = self.rebuild_data[key][value].xs(xi, level='Points:0').axes[1].values

        self.newData[key] = dataNew

    def rebuildDataRun2(self, key, data=None, values=['U:0'], generalAxis='Points:0',
                        surfaceAxis=['Points:1', 'Points:2'], methodFill='bfill'):
        """

        :param key: to take data
        :param data: external data
        :param values: which values you need
        :param generalAxis:
        :param surfaceAxis:
        :param methodFill: 'bfill', 'interpolate'
        :return:
        """
        index = [generalAxis, surfaceAxis[0]]
        columns = [surfaceAxis[1]]

        if data is None:
            if methodFill == 'interpolate':
                self.rebuild_data[key] = pd.pivot_table(self.data[key], values=values, columns=columns,
                                                        index=index).interpolate()
            else:
                self.rebuild_data[key] = pd.pivot_table(self.data[key], values=values, columns=columns,
                                                    index=index).fillna(method=methodFill)


        else:
            self.rebuild_data[key] = pd.pivot_table(data, values=values, columns=columns,
                                                    index=index).fillna(method=methodFill)
        dataNew = {}
        for value in values:
            dataNew[value] = dict()
            dataNew['gAxis'] = self.rebuild_data[key].index.levels[0].values
            dataNew['sAxis1'] = dict()
            dataNew['sAxis2'] = dict()
            for xi in dataNew['gAxis']:
                # y for graph
                dataNew[value][xi] = self.rebuild_data[key][value].xs(xi, level=generalAxis).values
                dataNew['sAxis2'][xi] = self.rebuild_data[key][value].xs(xi, level=generalAxis).axes[0].values
                # x for graph
                dataNew['sAxis1'][xi] = self.rebuild_data[key][value].xs(xi, level=generalAxis).axes[1].values

        self.newData[key] = dataNew


    def getGaxis(self, key, number='all'):
        if number == 'all':
            gAxis = self.newData[key][:]
        else:
            gAxis = self.newData[key][number]
        return gAxis

    def surfaceIntegral(self, key, variable='U:0', generalNumber=0):
        gAxis = self.newData[key]['gAxis'][generalNumber]
        s1 = self.newData[key]['sAxis1'][gAxis]
        s2 = self.newData[key]['sAxis2'][gAxis]
        data = self.newData[key][variable][gAxis]
        return integrate.simps(integrate.simps(data, s1), s2)

    def lineIntegral(self, key, variable='U:0', integAxis='sAxis1', valueAxis=0.1, gVal=0):
        gNum = self.gFindIndexByNearestValue(key, gVal)
        gAxis = self.newData[key]['gAxis'][gNum]
        s1 = self.newData[key]['sAxis1'][gAxis]
        s2 = self.newData[key]['sAxis2'][gAxis]
        if integAxis == 'sAxis1':
            data = self.newData[key][variable][gAxis]
            if valueAxis == 'all':
                integratedData = integrate.simps(data, s1)[:]
            else:
                index = self.findIndexByNearestValue(key, valueAxis, where='sAxis2')
                integratedData = integrate.simps(data, s1)[index]
        elif integAxis == 'sAxis2':
            data = self.newData[key][variable][gAxis].T
            if valueAxis == 'all':
                integratedData = integrate.simps(data, s2)[:]
            else:
                index = self.findIndexByNearestValue(key, valueAxis, where='sAxis2')
                integratedData = integrate.simps(data, s2)[index]

        return integratedData

    def gFindIndexByNearestValue(self, keyData, target):
        gIndex = np.argmin(np.abs(self.newData[keyData]['gAxis'] - target))
        return gIndex

    def findIndexByNearestValue(self, keyData, target, where='sAxis1', gTarget=0):
        gIndex = np.argmin(np.abs(self.newData[keyData]['gAxis'] - gTarget))
        gAxis = self.newData[keyData]['gAxis'][gIndex]
        index = np.argmin(np.abs(self.newData[keyData][where][gAxis] - target))
        return index



