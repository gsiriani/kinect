import numpy as np
import pandas as pd
import json
import sklearn
import sklearn.tree as tree
import sklearn.naive_bayes as naive_bayes
import sklearn.metrics as metrics
from sklearn.model_selection import train_test_split, cross_val_score
import pydotplus  


archivo_datos = '/home/fer/kinect/casos/casos.txt'

# PREPROCESAMIENTO DE LOS DATOS
# =============================

# Abro el archivo con los datos a estudiar
df = pd.read_json(archivo_datos, lines=True)

# Obtengo el vector con los valores objetivos
y = np.array(df.intencion)

# Elimino atributos que no aportan a la solucion
del df['intencion']
X = df


# PARTICION DE DATOS
# =============================

# Separo aleatoriamente un 25% de los datos para testeo.

X_train,X_test,y_train,y_test = train_test_split(X,y, test_size=0.25)



# ENTRENAMIENTO
# =============================


# Arbol de clasificacion
# ----------------------

dt = tree.DecisionTreeClassifier(criterion='entropy')
dt.fit(X_train,y_train)


# Clasificador Bayesiano sencillo
# -------------------------------

nb = naive_bayes.GaussianNB()
nb.fit(X_train, y_train)


# TESTING
# =============================

def imprimir_performance(X, y, clf):
	'''
	Funcion auxiliar que permite imprimir en pantalla las distintas medidas de performance
	de cada clasificador
	:param X: matriz con datos de prueba
	:param y: vector con resultados esperados de la prueba
	:param clf: clasificador previamente entrenado
	'''

    # predicciones = np.array([clf.predict(np.array(x).reshape(1,-1)) for x in X.values])
	predicciones = clf.predict(np.array(X))
        
	print("Accuracy: " + str(metrics.accuracy_score(y, predicciones)))
    
	for l in ['Colaborativa', 'Competitiva']:
		print("Label " + l)
		print("   Precision: " + str(metrics.precision_score(y, predicciones, pos_label=l)))
		print("   Recall: " + str(metrics.recall_score(y, predicciones, pos_label=l)))
		print("   Medida-f: " + str(metrics.f1_score(y, predicciones, pos_label=l)))
        
	print("Confussion matrix:\n" + str(metrics.confusion_matrix(y, predicciones)))


# Imprimo performance del arbol
print 'Performance del Arbol:'
imprimir_performance(X_test, y_test, dt)
# Resultados Validacion cruzada
scores_dt = cross_val_score(dt, X, y, cv=5, scoring='accuracy')
print("\nAccuracy validacion cruzada del Arbol: %0.2f (+/- %0.2f)" % (scores_dt.mean(), scores_dt.std() * 2))


# Imprimo performance del clasificador bayesiano sencillo
print '\nPerformance del Clasificador Bayesiano Sencillo:'
imprimir_performance(X_test, y_test, nb)
# Resultados Validacion cruzada
scores_nb = cross_val_score(nb, X, y, cv=5, scoring='accuracy')
print("\nAccuracy validacion cruzada de Bayes: %0.2f (+/- %0.2f)" % (scores_nb.mean(), scores_nb.std() * 2))

                      
dot_data = tree.export_graphviz(dt, out_file='arbol.dot', 
                         feature_names=df.columns,  
                         class_names=['Colaborativa', 'Competitiva'],  
                         filled=True, rounded=True,  
                         special_characters=True) 








