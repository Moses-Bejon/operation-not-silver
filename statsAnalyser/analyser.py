from sklearn.svm import LinearSVC
from sklearn import model_selection
from sklearn.ensemble import RandomForestClassifier
import pickle
import pandas as pd
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.getcwd(), '..')))
from computeStatistics import getStatistics
from extractData_clean import generateYearsCSV, generateAllCSV


rf = RandomForestClassifier()
svm = LinearSVC()


def get_X_y(csv_filename):
    cipher_stats = pd.read_csv(csv_filename)
    
    y = cipher_stats.pop('CipherType')
    X = cipher_stats.drop('Ciphertext', axis=1) # remove columns (axis 1)
    return X, y


def svc_train_predict(X, y):
        
    train_x, test_x, train_y, test_y = model_selection.train_test_split(
    X, y, train_size=0.9)
    svm.fit(train_x, train_y)
    print(svm.predict(train_x))

    print(f"Training accuracy: {svm.score(train_x,train_y)}")
    print(f"Test accuracy: {svm.score(test_x,test_y)}")

    # coefficient display
    feature_coefficients = svm.coef_
    classes = map(lambda name: name[:4],svm.classes_)
    feature_names = map(lambda name: name[:5],svm.feature_names_in_)
    print(feature_coefficients.shape)
    # for i, coeff in enumerate(feature_coefficients):
    #     print(classes[i])
    #     for j, feature in enumerate(feature_names):
    #         print(f" {feature} :", "%.6f" % coeff[j])

    df = pd.DataFrame(feature_coefficients,index = classes, columns = feature_names)
    print (df)

# svc_train_predict(X, y)




def train_test(model_object, X, y, print_pred=False, drop_diff=False, drop_logmono=False):

    # if drop_diff:
    #     X.drop(columns='differenceIOC')
    # else:
    #     X.drop(columns='IOC')
    # if drop_logmono:
    #     X.drop(columns='logMonogramFitness')

    train_x, test_x, train_y, test_y = model_selection.train_test_split(
    X, y, train_size=0.8)

    model_object.fit(X, y)
    if print_pred:
        for predicted, real in zip(model_object.predict(X), y):
            print("Actual:"+real, "Predicted:"+predicted)

    print(f"Training accuracy: {model_object.score(train_x,train_y)}")
    if print_pred:
        for real, predicted in zip(model_object.predict(test_x), test_y):
            print("Actual:"+real, "Predicted:"+predicted)
    print(f"Test accuracy: {model_object.score(test_x,test_y)}")


def csv_predict(filename):
    X, y = get_X_y(filename)
    # label = rf.predict(cipher_stats)
    for predicted, real in zip(rf.predict(X), y):
        print("Actual:"+real, "Predicted:"+predicted)
        print(predicted == real)
    print(rf.score(X, y))

# csv_predict("2019_ciphertext_data_stats.csv")

def predict_text(model, testfile): # no ciphertype provided.
    with open(testfile, 'r') as f:
        ciphertext = f.read()
        stats_dict = getStatistics(ciphertext)
        df = pd.DataFrame([stats_dict])
        
        return model.predict(df)

def saveModel(model, name):
    with open(name+'.pkl','wb') as f:
        pickle.dump(model,f)

def loadModel(name):
    with open(name+'.pkl', 'rb') as f:
        model = pickle.load(f)
        return model
    print("Something went wrong.")
# train the model
def main():
    filename = generateAllCSV()
    X, y = get_X_y(filename)
    model = RandomForestClassifier()
    train_test(model, X, y)
    testfile = 'test_ciphertext.txt'

