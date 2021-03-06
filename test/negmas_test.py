#%%
from negmas.apps.scml import SCMLWorld
from matplotlib import pyplot as plt
from my_factory_managers import MyFactoryManager
from negmas.apps.scml.utils import anac2019_tournament 
from negmas.apps.scml import GreedyFactoryManager
from negmas.tournaments import WorldRunResults, TournamentResults, tournament
import datetime
from negmas.utilities import LinearUtilityAggregationFunction
from EventEngine import Public_NegmasAccount, ListenerTypeOne, EventEngine
import glovar
from test_drawing import *
from multiprocessing import Process

def tournament_progress_callback(results:WorldRunResults):
    pass

def world_progress_callback(world:SCMLWorld):
    global Event_Porcess_New_Step
    print('current_step {}'.format(world.current_step))
    publicAcc.processNewStep(Event_Porcess_New_Step, world)
    if not glovar.event.is_set():
        if not glovar.world_recall_reuslt_naodongbanana_manager_dict['current_step'] == -1:
            glovar.event.set()
    # print('factories {}'.format(world.factories))

def run_negmas():
    starttime = datetime.datetime.now()
    results = anac2019_tournament(competitors=(MyFactoryManager, GreedyFactoryManager)
                        , agent_names_reveal_type=True,n_configs=1,
                        n_agents_per_competitor=10
                        , max_worlds_per_config=1        # we are allowing only 10 worlds to run
                        ,n_runs_per_world=1
                        , n_steps=100              # we are running each world for 20 steps only
                        , negotiator_type =  'negmas.sao.AspirationNegotiator'
                        # ,name= 'test_tournament2'
                        ,verbose= True
                        , parallelism = 'serial'
                        ,world_progress_callback=world_progress_callback
                        # ,configs_only= True
                        # ,randomize= False
                        )
# results.scores.head() 
    print(results.total_scores)
    endtime = datetime.datetime.now()
    print (endtime - starttime)
    buyer_utility = LinearUtilityAggregationFunction({'price': lambda x: - x
                        , 'number of items': lambda x: 0.5 * x
                        , 'delivery': {'delivered': 1.0, 'not delivered': 0.0}})


# TODO test for anac2019 tournament
if __name__ == "__main__":
    fig, ax = plt.subplots(1,1) 
    a = ShowProcess(ax=ax, fig=fig,world_recall_reuslt_dict=glovar.world_recall_reuslt_naodongbanana_manager_dict)
    Event_Porcess_New_Step = "Porcess_New_Step"
    listener1 = ListenerTypeOne('naodongbanana',
                                world_recall_reuslt_dict=glovar.world_recall_reuslt_naodongbanana_manager_dict)
    ee = EventEngine()
    ee.register(Event_Porcess_New_Step, listener1.showNewStep)
    ee.start()
    publicAcc = Public_NegmasAccount(ee)
    negmas = Process(target=run_negmas)
    negmas.start()
    # glovar.world_recall_reuslt_naodongbanana_manager_dict['init'].wait()
    a.show()
    

