import Oger
import mdp
import matplotlib.pyplot as plt

from rbn import rbn_node, complexity_measures
from tasks import temporal

gotta_remember = 3

training_dataset, test_dataset = temporal.create_datasets(
    10,
    task_size=150,
    delay=0,
    window_size=gotta_remember,
    dataset_type="temporal_parity")

#plt.matshow(test_dataset[0], cmap=plt.cm.gray)
#plt.title('Test input')
#plt.matshow(test_dataset[1], cmap=plt.cm.gray)
#plt.title('Test output')

n_nodes = 500
rbn_reservoir = rbn_node.RBNNode(connectivity=2,
                                 heterogenous=True,
                                 input_connectivity=50,
                                 output_dim=n_nodes,
                                 should_perturb=True)

print complexity_measures.measure_computational_capability(rbn_reservoir, 10, 0)




readout = Oger.nodes.RidgeRegressionNode(input_dim=n_nodes,
                                         output_dim=1,
                                         verbose=True)

flow = mdp.Flow([rbn_reservoir, readout], verbose=1)
flow.train([None, training_dataset])

reservoir_input = test_dataset[0]
expected_output = test_dataset[1]

actual_output = flow.execute(reservoir_input)
avg = 0.5  # np.average(actual_output)
for i in range(actual_output.shape[0]):
    actual_output[i][0] = 1 if actual_output[i][0] > avg else 0


errors = sum(actual_output != expected_output)
print "Errors: ", errors, " of ", len(actual_output)

plt.plot(actual_output, 'r')
plt.plot(expected_output, 'b')
plt.show()


#rbn_states = rbn_reservoir.execute(input_data)


#input_connections = np.zeros((1, rbn_reservoir.output_dim), dtype='int32')
#input_connections[0, rbn_reservoir.input_connections] = 1
##
#plt.matshow(input_connections, cmap=plt.cm.gray)
#plt.title('Input connections')
#plt.matshow(rbn_states, cmap=plt.cm.gray)
#plt.title('RBN states')
#plt.show()

#print "NRMSE: " + str(Oger.utils.nrmse(expected, actually))

#pylab.plot(expected, 'r')
#pylab.plot(actually, 'b')
#pylab.show()
