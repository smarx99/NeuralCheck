from App.Controller.NetworkController import NetworkController
from App.Service.DataHandler import DataHandler
from App.Service.NetworkService import NetworkService
from App.Model.Configuration import Configuration


# Create instances of the classes
data_handler = DataHandler()
network_service = NetworkService()
configurations = Configuration(3, [30, 14, 1], ['relu', 'relu', 'sigmoid'], 0)
network_controller = NetworkController(network_service)

# load dataset
data = data_handler.load_dataset()

# prepare dataset
prepared_data = data_handler.prepare_data(data)

# split data
xtrain, xtest, ytrain, ytest = data_handler.split_data(prepared_data)

# test if methods work
# print(data.head())
# print(data.info())
# print(prepared_data.head())
# print(prepared_data.info())
# print(xtrain, xtest, ytrain, ytest)


# create network
# network = network_service.create_network(configurations)
network = network_controller.process(configurations)

# train network
trained_network = network_service.train_network(network, xtrain, ytrain)

# evaluate network
testacc = network_service.evaluate_network(trained_network, xtest, ytest)

print(trained_network.summary())
print('test_acc:', testacc)




