from multiprocessing import Process, Manager, Value

# multiprocess share paramters
world_recall_reuslt_naodongbanana = Value('d', 0.0)
world_recall_reuslt_schorsch = Value('d', 0.0)

world_recall_reuslt_naodongbanana_manager_dict = Manager().dict()
# multithread global parameters
step= 0
scmlworld = None