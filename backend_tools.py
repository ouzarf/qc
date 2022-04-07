import os, sys
from qiskit import IBMQ, Aer
from qiskit.providers.ibmq import least_busy, ibmqbackend
from qiskit.result import postprocess

def print_backend(backend, output_gate_props=False, output_qubit_props=False, output_job_info=False):
   """
      Function outputs info about the given backend
    
      Inputs:
         output_gate_props  (bool): indicates if information about gates is to be output
         output_qubit_props (bool): indicates if information about qubits is to be output
         output_job_info    (bool): indicates if information about jobs run on the backend is to be output
   """

   print("Provider: {}".format(backend.provider()))
   print("Name: {}".format(backend.name()))
   if backend.name() == 'qasm_simulator':
       print("Hub: {}".format(backend.hub))   # The simulator does not have hub, group or project attributes
       print("Group: {}".format(backend.group))
       print("Project: {}".format(backend.project))
   print("Status info:")
   status = backend.status().to_dict()
   for i,k in status.items():
       print("   {:30s}: {}".format(i, k))
   print("Configuration info:")
   config = backend.configuration().to_dict()
   for i,k in config.items():
       if i == "gates":
           print("   gates:")
           for d in k:
               print("      gate:")
               for ig,kg in d.items():
                   print("         {:10s}: {}".format(ig, kg))
       elif i == "basis_gates":
           print("   basic gates:")
           gate_list = ", ".join([str(x) for x in k])  
           print("     {}".format(gate_list))
       else:
           print("   {:30s}: {}".format(i, k))
   props = backend.properties()
   if props is not None:
      print("Property info:")
      props_dict = props.to_dict()
      for i,k in props_dict.items():
          if i == 'gates':
             if output_gate_props:
                print("   gates:")
                for d in k:
                    print("      gate:")
                    for ig,kg in d.items():
                        print("         {:10s}: {}".format(ig, kg))
          elif i == 'qubits':
             if output_qubit_props:
                print("   qubits:")
                for l in k:
                    for d in l:
                        print("      qubit:")
                        for ig,kg in d.items():
                            print("         {:10s}: {}".format(ig, kg))
          else:
             print("   {:30s}: {}".format(i, k))
   if output_job_info:
      joblist = backend.jobs()
      if joblist is not None and len(joblist) > 0:
         print("Jobs:")
         for job in joblist:
             print_job(job)


def print_job(job=None, job_id=None, backend=None, output_job_details=False):
   """
      Function outputs info about the given job
      - user can supply either the job, or the job ID and backend
   """

   if job is None:
      # Retrieve the job
      job = backend.retrieve_job(job_id())
   else:
      job_id = job.job_id()

   print("Job: {}".format(job))
   print("   id: {}".format(job_id))
   print("   status: {}".format(job.status()))
   print("   run on backend: {}".format(job.backend()))
   print("   creation date: {}".format(job.creation_date()))

   if output_job_details:
       result = job.result()
       job_info = result.to_dict()
       print("   Job details:")
       # To output the counts, we need the job status to be COMPLETED and the success flag to be True
       output_flag = -1
       for key,value in job_info.items():
           if key != 'results':
               print("      {}: {}".format(key, value))
               if key == 'status' and value == 'COMPLETED':
                   output_flag += 1
               if key == 'success' and value is True:
                   output_flag += 1
       # Output the results
       for circuit in job_info['results']:
           if output_flag == 1:
               print("         Circuit: {}".format(circuit['header']['name']))
               counts = postprocess.format_counts(circuit['data']['counts'])
               for k,v in counts.items():
                   print("            state: {:10s}: counts: {:10d}".format(k, v))


def list_backends(hub=None, group=None, project=None, output_gate_props=False, output_qubit_props=False, output_job_info=False):
   """
      Function lists all available backends
    
      Inputs:
         hub, group, project (string): info will only be output for backends matching these constraints
         output_gate_props  (bool): indicates if information about gates is to be output
         output_qubit_props (bool): indicates if information about qubits is to be output
         output_job_info    (bool): indicates if information about jobs run on the backend is to be output
   """
   # There should be a local simulator
   print("\n---------------- Local simulators: ----------------")
   for sim_name in ['statevector_simulator', 'unitary_simulator', 'qasm_simulator']:
       sim = Aer.get_backend(sim_name) 
       print("\t----------- Backend: {} ----------------".format(sim))

   # List the IBM-Q backends, including the cloud simulator
   for provider in IBMQ.providers(hub=hub, group=group, project=project):
            
       if isinstance(provider, ibmqbackend.IBMQSimulator):
           print("\n---------------- Provider: {} ----------------".format(provider))
       else:
           for backend in provider.backends():
               print("\n---------------- Provider: {} ----------------".format(provider))
               print("\t----------- Backend: {} ----------------".format(backend))
               print_backend(backend)


def get_list_of_jobs(backend):
   """
      Function returns a list of all jobs on the given backend
   """
   print("backend is ", backend)

   joblist = backend.jobs()
   if joblist is not None and len(joblist) > 0:
      return joblist
   else:
      return None


def get_backend(hub=None, group=None, project=None, backend_name=None, use_sim=False, use_cloud_sim=False, min_qubits=1):
    """
       Function returns a backend matching the given criteria
      
       Inputs:
         hub, group, project (string): only select a backend from the subset matching these constraints
    """

    if use_sim or use_cloud_sim:
       # Return the simulator
       if use_cloud_sim == True:
           provider = IBMQ.get_provider(hub=hub, group=group, project=project)
           be = provider.get_backend('ibmq_qasm_simulator')
       else:
           # Use the local simulator
           be = Aer.get_backend('qasm_simulator')
    else:
       # Get the provider
       provider = IBMQ.get_provider(hub=hub, group=group, project=project)

       if backend_name is not None:
          be = provider.get_backend(backend_name)
          if be.status().operational is False:
              raise AttributeError("Requested device is not operational")
       else:
          # Get all backends that match the criteria
          backends = provider.backends(filters=lambda x:
                                    x.configuration().n_qubits >= min_qubits and 
                                    not x.configuration().simulator and
                                    x.status().operational==True)
   
          if backends is None:
              raise AttributeError("Could not get a suitable backend")
          else:
              be = least_busy(backends)

    # Should only be one matching backend, but it is in a list so return the first one
    if isinstance(be, list):
        return be[0]
    else:
        return be


if __name__== "__main__":
   IBMQ.load_account()
   #list_backends()

   #backend = get_backend(use_sim=True)
   #backend = get_backend(use_sim=True, use_cloud_sim=True)
   #backend = get_backend(backend_name='ibmqx2')
   backend = get_backend(min_qubits=4, hub='ibm-q')
   print("Got backend: ", backend)

   #job_list = get_list_of_jobs(backend)
   #for job in job_list:
   #   print_job(job)


#show filtering of jobs and job results


# This deletes the local account info in ~/.qiskit/qiskitrc
# IBMQ.delete_accounts()
