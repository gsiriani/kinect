import numpy as np
import pandas as pd
import sklearn
import sklearn.cross_validation
import sklearn.tree as tree
import sklearn.naive_bayes as naive_bayes
import sklearn.metrics as metrics

# PREPROCESAMIENTO DE LOS DATOS
# =============================

# Abro el archivo con los datos a estudiar
# TODO: nombre correcto del archivo con los casos de estudio 
df = pd.read_csv('adult_data.csv',skipinitialspace=True)

# Obtengo el vector con los valores objetivos
# TODO: sutituir intencion por el nombre del atributo objetivo a aprender
y = np.array(df.intencion)

# Elimino atributos que no aportan a la solucion
# TODO: sutituir intencion por el nombre del atributo objetivo a aprender
del df['intencion']



# PARTICION DE DATOS
# =============================

# Separo aleatoriamente un 25% de los datos para testeo.

X_train,X_test,y_train,y_test = sklearn.cross_validation.train_test_split(X,y, test_size=0.25)



# ENTRENAMIENTO
# =============================


# Arbol de clasificacion
# ----------------------

dt = tree.DecisionTreeClassifier()
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
    
    # TODO: verificar que los nombres de las categorias coincidan
    for l in ['Competitivo', 'Colaborativo']:
        print("Label " + l)
        print("   Precision: " + str(metrics.precision_score(y, predicciones, pos_label=l)))
        print("   Recall: " + str(metrics.recall_score(y, predicciones, pos_label=l)))
        print("   Medida-f: " + str(metrics.f1_score(y, predicciones, pos_label=l)))
        
    print("Confussion matrix:\n" + str(metrics.confusion_matrix(y, predicciones)))


# Imprimo performance del arbol
print 'Performance del Arbol:'
imprimir_performance(X_test, y_test, dt)


# Imprimo performance del clasificador bayesiano sencillo
print '\nPerformance del Clasificador Bayesiano Sencillo:'
imprimir_performance(X_test, y_test, nb)
