from pyspark.sql import SQLContext
from pyspark.sql.types import *
import pyspark
from pyspark.sql.functions import *
from pyspark.ml.classification import LogisticRegression

from pyspark.mllib.util import MLUtils
from pyspark.mllib.linalg import Vectors
from pyspark.mllib.feature import StandardScaler

from pyspark.mllib.regression import LabeledPoint
from pyspark.sql.functions import *
from pyspark.mllib.regression import LinearRegressionWithSGD
from pyspark.mllib.evaluation import RegressionMetrics
from pyspark.mllib.classification import LogisticRegressionWithSGD

sc = pyspark.SparkContext()
sqlcontext = SQLContext(sc)
df = sqlcontext.read.load('rank.csv',format='com.databricks.spark.csv',header='true',inferSchema='true')
print df.count()
print df.dtypes
#df.describe().dtypes
#df.filter(df.Rank < 10).show()
#df.select(max("Rank")).show() -- pyspark.sql.functions REQUIRED

##https://www.nodalpoint.com/spark-dataframes-from-csv-files/
#http://www.techpoweredmath.com/spark-dataframes-mllib-tutorial/#.WkcDHnWWanw  
# spark-mllib uses RDDs.
#spark-mll uses DataFrames.     

# df.registerTempTable("rank")
# sqlcontext.sql("SELECT * FROM rank").show()

df = df.select('Rank','Mark','Gender')
df.describe(['Rank','Mark','Gender']).show()

features = df.rdd.map(lambda row: row[1:])
print "FEATURES"
print features.take(25)


standardizer = StandardScaler()
model = standardizer.fit(features)
features_transform = model.transform(features)
print features_transform.take(25)

lab = df.rdd.map(lambda row: row[0])
lab.take(5)

transformedData = lab.zip(features_transform)
transformedData.take(5)

transformedData = transformedData.map(lambda row: LabeledPoint(row[0],[row[1]]))
print transformedData.take(5)

#WORKING
trainingData, testingData = transformedData.randomSplit([.8,.2],seed=1234)
#linearModel = LinearRegressionWithSGD.train(trainingData,1000,.2)

lr = LogisticRegressionWithSGD.train((trainingData), iterations=10)
#lr = LogisticRegression(maxIter=10, regParam=0.3, elasticNetParam=0.8)
#model = lr.fit((trainingData))    




# prediObserRDDin = trainingData.map(lambda row: (float(linearModel.predict(row.features[0])),row.label))
# metrics = RegressionMetrics(prediObserRDDin)

# print metrics.r2
prediObserRDDout = testingData.map(lambda row: (float(linearModel.predict(row.features[0])),row.label))
metrics = RegressionMetrics(prediObserRDDout)

print metrics.rootMeanSquaredError
print metrics.r2

