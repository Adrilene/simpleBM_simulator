from solution import observer
from controller.smart_tv_controller import block_tv

# observer_controller.observer_connect()
agn_observer = observer.Observer()
agn_observer.messages_types = ("status", "notification", "confirmation")
agn_observer.steps_to_adapt = [(block_tv, (False,))]
agn_observer.steps_for_normal_behave = [(block_tv, (True,))]
agn_observer.start()